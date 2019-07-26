import abc
import numpy as np
from gym.spaces import Box, Dict

from multiworld.core.serializable import Serializable
from multiworld.envs.mujoco.classic_mujoco.ant import AntEnv
from multiworld.envs.mujoco.mujoco_env import MujocoEnv
from multiworld.core.multitask_env import MultitaskEnv
from multiworld.envs.env_util import get_asset_full_path

from collections import OrderedDict
from multiworld.envs.env_util import (
    get_stat_in_paths,
    create_stats_ordered_dict,
)


class AntMazeEnv(AntEnv):
    def __init__(self, *args, **kwargs):
        self.quick_init(locals())
        super().__init__(
            *args,
            model_path='classic_mujoco/ant_maze.xml',
            **kwargs
        )
    def sample_goals(self, batch_size):
        assert self.goal_is_xy
        goals = np.random.uniform(
            self.goal_space.low,
            self.goal_space.high,
            size=(batch_size, self.goal_space.low.size),
        )
        if self.two_frames:
            goals = goals[:,:int(self.goal_space.low.size/2)]

        if self.goal_is_xy:
            goals[(0 <= goals) * (goals < 0.5)] += 2
            goals[(0 <= goals) * (goals < 1.5)] += 1.5
            goals[(0 >= goals) * (goals > -0.5)] -= 2
            goals[(0 >= goals) * (goals > -1.5)] -= 1.5
            goals_dict = {
                'xy_desired_goal': goals,
            }
        else:
            if self.two_frames:
                goals_dict = {
                    'desired_goal': np.concatenate((goals, goals), axis=1),
                    'state_desired_goal': np.concatenate((goals, goals), axis=1),
                }
            else:
                goals_dict = {
                    'desired_goal': goals,
                    'state_desired_goal': goals,
                }

        return goals_dict

if __name__ == '__main__':
    env = AntMazeEnv(
        goal_low=[-4, -4],
        goal_high=[4, 4],
        goal_is_xy=True,
        init_qpos=[
            -3, -3, 0.5, 1,
            0, 0, 0,
            0,
            1.,
            0.,
            -1.,
            0.,
            -1.,
            0.,
            1.,
        ],
        reward_type='xy_dense',
    )
    env.reset()
    i = 0
    while True:
        i += 1
        env.render()
        action = env.action_space.sample()
        # action = np.zeros_like(action)
        env.step(action)
        if i % 10 == 0:
            env.reset()
