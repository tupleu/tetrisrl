import sys
import gym
import numpy as np

from tetris import Tetris, Tetromino
from tetris_environment import TetrisEnv

from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
import pygame

from stable_baselines.deepq.policies import FeedForwardPolicy

def main():
    num = len(sys.argv)
    if(num == 2):
        games = int(sys.argv[1])
    else:
        print("python ",sys.argv[0]," (number of games)")
        sys.exit(1)
    env = TetrisEnv()
    model = DQN.load("tetris_model")
    total_model_score = 0
    total_random_score = 0
    for _ in range(games):
        obs = env.reset()
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            current_board = env.game.get_board()
            for board in env.game.board_list:
                if np.array_equal(np.array(current_board),np.array(board)):
                    obs, rewards, dones, info = env.step(3) #move down if repeated
                    break
            if(dones):
                total_model_score += env.game.score
                break
        #using random actions
        obs = env.reset()
        while True:
            action= env.action_space.sample()
            obs, rewards, dones, info = env.step(action)
            if(dones):
                total_random_score += env.game.score
                break
    print("Final avg score using model: ", total_model_score/games)
    print("Final avg score using random actions: ", total_random_score/games)

if __name__ == '__main__':
    main()
