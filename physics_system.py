import numpy as np
import scipy.spatial as spatial

k = 1.5
m = 2.0
t0 = 2.5

rad  = .5  
sight = 5
max_f = 20  

class PhysicsSystem:
    def __init__(self, env_size):
        self._env_size = env_size

    def find_neighbors(self, agent_positions):
        ''' build agents tree (as if they were positioned on torus)
        '''
        # neighbors_tree = spatial.cKDTree(agent_positions)
        neighbors_tree = spatial.cKDTree(agent_positions, boxsize=(self._env_size + 0.01, self._env_size + 0.01))

        ''' query agents closer than sight
        '''
        self._neighbors_indicies = neighbors_tree.query_ball_point(agent_positions, sight)
    
    ''' returns agent and his neighbors
    '''
    def _check_neighbors(self, agent_positions, agent_goal_velocities, agent_velocities, dt):
        ''' wrap positions as if our environment was a torus
        '''
        agent_positions [:, 0][agent_positions[:, 0] > self._env_size] = 0
        agent_positions [:, 0][agent_positions[:, 0] < 0] = self._env_size
        agent_positions [:, 1][agent_positions[:, 1] > self._env_size] = 0
        agent_positions [:, 1][agent_positions[:, 1] < 0] = self._env_size

        self.find_neighbors(agent_positions)

        ''' get all agent neighbors indicies
        '''
        agent_neighbors_indicies = np.array(self._neighbors_indicies[0])

        ''' filter current agent from indecies of his neighbors
            we don't want to calculate force exerted by agent on himself
        '''
        agent_neighbors_indicies = agent_neighbors_indicies[agent_neighbors_indicies != 0]
        agent_positions += agent_velocities * dt

        return agent_positions, agent_neighbors_indicies


    def f_agent_neighbors(self, r_agent, r_neighbors, v_agent, v_neighbors):
        global k, m, t0

        r_ij =  r_agent - r_neighbors
        v_ij = v_agent - v_neighbors

        ''' wrap r_ij around torus
        '''
        r_ij[:, 0][r_ij[:, 0] >  self._env_size / 2] -= self._env_size
        r_ij[:, 0][r_ij[:, 0] < -self._env_size / 2] += self._env_size
        r_ij[:, 1][r_ij[:, 1] >  self._env_size / 2] -= self._env_size
        r_ij[:, 1][r_ij[:, 1] < -self._env_size / 2] += self._env_size

        ''' shrink diameter if agents already collided
        '''
        r_ij_squared = np.einsum('ij,ij->i', r_ij, r_ij)
        diameter_squared = np.full(r_ij_squared.shape, 4*rad**2)

        diameter_squared[diameter_squared > r_ij_squared] = r_ij_squared[diameter_squared > r_ij_squared]

        ''' find t by solving system of two vector equations
            r1 = r1 + v1*t
            r2 = r2 + v2*t
            ||r1-r2|| = 2R
            using quadratic formulae
        '''
        a =  np.einsum('ij,ij->i', v_ij, v_ij)
        b = -np.einsum('ij,ij->i', r_ij, v_ij)
        # c =  np.einsum('ij,ij->i', r_ij, r_ij) - 4*rad**2
        c = r_ij_squared - diameter_squared

        det = b**2 - a*c

        ''' time-to-collision doesnt exist for every neighbor,
            so we fill t martix with NaN
        '''
        neighbors_num = r_neighbors.shape[0]
        t = np.full(neighbors_num, np.nan)

        ''' compute t only for det > 0, otherwise it doesnt exist
        '''
        t_exists = (det >= 0) 
        # & np.bitwise_or(a > 0.001, a < - 0.001)
        det[t_exists] = np.sqrt(det[t_exists])

        t[t_exists] = (b[t_exists] - det[t_exists]) / a[t_exists]

        ''' if t <= 0 (collision in the past), invalidate t
        '''
        t[t < 0] = np.nan
        t[t == 0] = 0.001

        ''' find f_ij using f_ij = - d/dx e(t)
        '''
        f_ij = np.zeros(shape=(neighbors_num, 2))
        
        ''' proceed computing force only for existing t
            but before align dimension
        '''
        f_exists = np.array(~np.isnan(t))
        v_ij = v_ij[f_exists]
        r_ij = r_ij[f_exists]

        t = t[f_exists][:, np.newaxis]
        a = a[f_exists][:, np.newaxis]
        b = b[f_exists][:, np.newaxis]
        c = c[f_exists][:, np.newaxis]

        det = det[f_exists][:, np.newaxis]

        # f_ij = -( (k * np.exp(- t / t0)) * (m / t + 1 / t0) / (a * t**m) )[:, np.newaxis] * (v_ij - (a[:, np.newaxis] * r_ij + b[:, np.newaxis] * v_ij) / np.sqrt(det[:, np.newaxis]))
        if f_exists.size != 0:
            f_ij[f_exists] =                       \
            -k * np.exp(-t / t0)                   \
            * (v_ij - (a * r_ij - b * v_ij) / det) \
            / (a * t**m)                           \
            * (m / t + 1 / t0)                     

            # -( ( (k * np.exp(- t[f_exists] / t0)) * (m / t[f_exists] + 1 / t0) / (a[f_exists] * t[f_exists]**2) )[:, np.newaxis] \
            # * (v_ij[f_exists] - (a[f_exists][:, np.newaxis] * r_ij[f_exists, :] - b[f_exists][:, np.newaxis] * v_ij[f_exists]) / det[f_exists][:, np.newaxis]) )

        ''' resulting force is a sum of all forces experienced from all neighbors
        '''
        f_resulting = f_ij.sum(axis=0)

        ''' clamp resulting force
        '''
        f_norm = np.linalg.norm(f_resulting)
        if f_norm > max_f:
            f_resulting = max_f * f_resulting / f_norm

        return f_resulting

    def update(self, agent_positions, agent_goal_velocities, agent_velocities, dt):
        self.find_neighbors(agent_positions)

        ''' initizalize matrix of resulting forces experienced by agents
        '''
        f = np.zeros_like(agent_velocities)
        ''' driving force exerted on agent
        '''
        
        f += (agent_goal_velocities - agent_velocities) / .5
        f += np.random.uniform(low=-1., high=1., size=(agent_velocities.shape))

        ''' get number of agents
        '''
        num = agent_positions.shape[0]
        for i in range(num):
            ''' get all agent neighbors indicies
            '''
            agent_neighbors_indicies = np.array(self._neighbors_indicies[i])

            if len(agent_neighbors_indicies) == 1: 
                continue

            ''' filter current agent from indecies of his neighbors
                we don't want to calculate force exerted by agent on himself
            '''
            agent_neighbors_indicies = agent_neighbors_indicies[agent_neighbors_indicies != i]

            f[i] += self.f_agent_neighbors(agent_positions[i],  agent_positions[agent_neighbors_indicies],
                                           agent_velocities[i], agent_velocities[agent_neighbors_indicies])

        agent_velocities += f * dt
        agent_positions += agent_velocities * dt

        ''' wrap positions as if our environment was a torus
        '''
        agent_positions [:, 0][agent_positions[:, 0] > self._env_size] = 0
        agent_positions [:, 0][agent_positions[:, 0] < 0] = self._env_size
        agent_positions [:, 1][agent_positions[:, 1] > self._env_size] = 0
        agent_positions [:, 1][agent_positions[:, 1] < 0] = self._env_size

        return agent_positions, agent_goal_velocities, agent_velocities