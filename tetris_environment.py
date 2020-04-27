import gym
from tetris import Tetromino, Tetris
from gym import spaces
import numpy as np
import pygame
from game import draw_board


class TetrisEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(TetrisEnv, self).__init__()
        self.game = Tetris()
        self.action_list = [self.game.left, self.game.right, self.game.up, self.game.down, self.rotatel, self.rotater, self.game.hold]
        # up down left right hold rotateleft rotateright
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.MultiDiscrete([2]*Tetris.width*Tetris.height + [8]*7 + [8] + [2] + [8] + [4] + [10]+ [20])
        self.reset()

    def get_state_size(self):
        return 243

    def rotatel(self, tetromino):
        self.game.rotate(tetromino, -1)
    def rotater(self, tetromino):
        self.game.rotate(tetromino, 1)
    

    def step(self, action):
        score1 = self.game.score
        self.action_list[action](self.game.current_piece)
        score2 = self.game.score

        reward = score2-score1

        current_board = self.game.get_board()
        flag = False
        for board in self.game.board_list:
            if np.array_equal(np.array(current_board),np.array(board)):
                flag = True
                break
        if(flag):
            reward -= 10
        else:
            self.game.board_list.append(self.game.get_board())
        
        done = self.game.game_over or score2 > 5000
        if(not hasattr(self.game, 'held_piece')):
            held_piece = 8
        else:
            held_piece = self.game.held_piece.t
        observation = np.concatenate((np.reshape((self.game.board>0).astype(int),(Tetris.width*Tetris.height,)),np.array(self.game.queue),np.array([held_piece, self.game.has_switched, self.game.current_piece.t,self.game.current_piece.r,self.game.current_piece.x,self.game.current_piece.y]))
        ,axis = 0)
        self.render()

        return observation, reward, done, {}
    def reset(self):
        self.game.reset()
        if(not hasattr(self.game, 'held_piece')):
            held_piece = 8
        else:
            held_piece = self.game.held_piece.t
        observation = np.concatenate((np.reshape((self.game.board > 0).astype(int),(Tetris.width*Tetris.height,)),np.array(self.game.queue),np.array([held_piece, self.game.has_switched, self.game.current_piece.t,self.game.current_piece.r,self.game.current_piece.x,self.game.current_piece.y]))
        ,axis = 0)
        return observation
    def render(self, mode='human'):
        if not hasattr(self, 'window'):
            pygame.init()
            pygame.font.init()
            self.window = pygame.display.set_mode((24*30,24*30))
        pygame.event.pump()
        draw_board(self.window,self.game)
    def close (self):
        pygame.quit()