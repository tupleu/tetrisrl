import gym

from tetris import Tetris, Tetromino
from tetris_environment import TetrisEnv

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
import pygame

from stable_baselines.deepq.policies import FeedForwardPolicy


class TetrisPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(TetrisPolicy, self).__init__(*args, **kwargs,
                                           layers=[512, 1024, 512],
                                           layer_norm=False,
                                           feature_extraction="mlp")

def main():
    env = TetrisEnv()
    model = DQN(TetrisPolicy, env, verbose=1)
    model.learn(total_timesteps=1000000)
    model.save("tetris_model")


if __name__ == '__main__':
    main()