import random as random
import numpy as np
from bridson import poisson_disc_samples

import draw
from physics_system import PhysicsSystem
from rendering_system import RenderingSystem

num = 50
env_size = 30
rad  = .5

positions = None
goal_velocities = None
velocities = None

def add_crowd(num, region=None, angle=None, velocity_k=1.):
    ''' sample positions either randomly or within specified region
    '''
    if region == None:
        # positions = env_size * np.random.rand(num, 2)
        positions = np.array(random.sample(poisson_disc_samples(width=env_size, height=env_size, r=2*rad), k=num)).reshape(num, 2)
        
    else:
        # positions_x = np.random.uniform(low=region[0][0], high=region[1][0], size=[num])
        # positions_y = np.random.uniform(low=region[0][1], high=region[1][1], size=[num])
        positions = np.array(random.sample(poisson_disc_samples(width=region[1][0]-region[0][0],
                                                                height=region[1][1]-region[0][1], r=2*rad), k=num)).reshape(num, 2)

        # positions = np.column_stack((positions_x, positions_y))
        positions[:, 0] += region[0][0]
        positions[:, 1] += region[0][1]

    ''' sample velocities either randomly or with a specified angle and magnitude
    '''
    if angle == None:
        angles_local = 2 * 3.14 * np.random.rand(num, 1)
    else:
        angles_local = np.full(num, angle)
    
    velocities = np.empty(shape=(num, 2))

    velocities[:, 0] = np.cos(angles_local).reshape(num)
    velocities[:, 1] = np.sin(angles_local).reshape(num)

    velocities *= velocity_k

    goal_velocities = 1.5 * np.copy(velocities)

    return positions, goal_velocities, velocities

def colliding():
    global positions, goal_velocities, velocities

    positions1, goal_velocities1, velocities1 = add_crowd(int(num / 2), ((0, env_size / 3.), (env_size / 3., 2. * env_size / 3.)), 0.)
    positions2, goal_velocities2, velocities2 = add_crowd(int(num / 2), ((2. * env_size / 3., env_size / 3.), (env_size, 2. * env_size / 3.)), 3.14)

    positions = np.concatenate((positions1, positions2))
    goal_velocities = np.concatenate((goal_velocities1, goal_velocities2))
    velocities = np.concatenate((velocities1, velocities2))

def intersecting():
    global positions, goal_velocities, velocities

    positions1, goal_velocities1, velocities1 = add_crowd(int(num / 2), ((0, env_size / 3.), (env_size / 3., 2. * env_size / 3.)), 0.)
    positions2, goal_velocities2, velocities2 = add_crowd(int(num / 2), ((env_size / 3., 0), (2. * env_size / 3., env_size/3.)), 3.14 / 2.)

    positions = np.concatenate((positions1, positions2))
    goal_velocities = np.concatenate((goal_velocities1, goal_velocities2))
    velocities = np.concatenate((velocities1, velocities2))

def init_sim():
    global positions, goal_velocities, velocities
    global rad

    positions1, goal_velocities1, velocities1 = add_crowd(num)
    positions = positions1
    goal_velocities = goal_velocities1
    velocities = velocities1
    # for i in range(5):
    #     add_walker()

    # colliding()
    # print('positions')
    # print(positions)
    # intersecting()

    # add_crowd(int(num), ((0, s / 3.), (s / 3., 2. * s / 3.)), 0)
    # add_walker(((2. * s / 3, s / 3.), (s, 2. * s / 3.)), 0, (-1.5, 0))

    # add_crowd(int(num), ((0, s / 3.), (s / 3., 2. * s / 3.)), 0)
    # add_walker(((s / 3., 0), (2. * s / 3., s / 5.)), 3.14 / 2., (0, 1.5))

    # add_walker(((0, s / 2.), (0, s / 2.)), None, (1, 0))
    # add_walker(((s, s / 2.), (s, s / 2.)), None, (-1, 0))

    draw.init()

    draw.set_x_scale(0, env_size)
    draw.set_y_scale(0, env_size)

def draw_frame(rendering, physics):
    global positions, goal_velocities, velocities 

    positions, goal_velocities, velocities = physics.update(positions, goal_velocities, velocities, 0.005)
    rendering.draw_agents(positions, goal_velocities, velocities)

def _draw_neighbors(rendering, physics):
    global positions, goal_velocities, velocities

    positions, agent_neighbors_indicies = physics._check_neighbors(positions, goal_velocities, velocities, 0.005)
    rendering._draw_neighbors(positions, agent_neighbors_indicies)

def main():
    init_sim()

    physics = PhysicsSystem(env_size)
    rendering = RenderingSystem(rad)

    while True:
        draw_frame(rendering, physics)
        draw.show(0.0)
        draw.clear()

if __name__ == '__main__':
    start_time = time.time()
    main()