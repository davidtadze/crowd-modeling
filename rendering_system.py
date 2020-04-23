import draw
from util.color import Color

from math import floor, sqrt
import numpy as np

class RenderingSystem:
    def __init__(self, rad):
        self._rad = rad

    def get_heatmap_color(self, value):
            heatmap = [[47, 72, 88], [0, 109, 137], [0, 148, 163], [0, 187, 157], [0,223,117], [0,255,0]]
            
            idx1 = 0        
            idx2 = 0        
            fract_between = 0  
            
            if value <= 0:
                idx1 = idx2 = 0
            elif value >= 1:
                idx1 = idx2 = len(heatmap) - 1
            else:
                value = value * (len(heatmap) - 1)
                idx1  = floor(value)                 
                idx2  = idx1 + 1                  
                fract_between = value - float(idx1)
                
            r = (heatmap[idx2][0] - heatmap[idx1][0]) * fract_between + heatmap[idx1][0]
            g = (heatmap[idx2][1] - heatmap[idx1][1]) * fract_between + heatmap[idx1][1]
            b = (heatmap[idx2][2] - heatmap[idx1][2]) * fract_between + heatmap[idx1][2]
            
            return Color(int(r), int(g), int(b))

    def draw_agents(self, agent_positions, agent_goal_velocities, agent_velocities):
        for i in range(len(agent_positions)):
            # print(agent_positions[i])
            agent_x = agent_positions[i][0]
            agent_y = agent_positions[i][1]

            v_i =  agent_velocities[i]
            norm_v_i = np.linalg.norm(v_i)

            goal_v_i = agent_goal_velocities[i]
            norm_goal_v_i = np.linalg.norm(goal_v_i)

            normalized_v = norm_v_i / 2
            draw.filled_circle(agent_x, agent_y, self._rad, self.get_heatmap_color(normalized_v))

            draw.line(agent_positions[i], agent_positions[i] + 1.5 * self._rad * v_i / norm_v_i, self.get_heatmap_color(normalized_v))
            draw.line(agent_positions[i], agent_positions[i] + self._rad * goal_v_i / norm_goal_v_i, Color(255, 255, 255))

    def _draw_neighbors(self, agent_positions, agent_neighbors_indicies):
        for i in range(len(agent_positions)):
            agent_x = agent_positions[i][0]
            agent_y = agent_positions[i][1]

            color = Color(47, 72, 88)

            if i in agent_neighbors_indicies:
                color = Color(0,255,0)
            elif i == 0:
                color = Color(0, 0 ,0)

            draw.filled_circle(agent_x, agent_y, self._rad, color)


        