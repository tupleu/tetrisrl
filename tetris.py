import pygame
import random
import numpy as np
from time import sleep


def out_of_bounds(tet, x, y):
    return(x >= Tetris.width or y >= Tetris.height or x < 0 or y < 0)

class Tetromino:
    tetrominos = {
        1: { # I
            0: [(0,1), (1,1), (2,1), (3,1)],
            1: [(2,0), (2,1), (2,2), (2,3)],
            2: [(3,2), (2,2), (1,2), (0,2)],
            3: [(1,3), (1,2), (1,1), (1,0)],
        },
        2: { # J
            0: [(0,0), (0,1), (1,1), (2,1)],
            1: [(2,0), (1,0), (1,1), (1,2)],
            2: [(2,2), (2,1), (1,1), (0,1)],
            3: [(0,2), (1,2), (1,1), (1,0)],
        },
        3: { # L
            0: [(0,1), (1,1), (2,1), (2,0)],
            1: [(1,0), (1,1), (1,2), (2,2)],
            2: [(2,1), (1,1), (0,1), (0,2)],
            3: [(1,2), (1,1), (1,0), (0,0)],
        },
        4: { # O
            0: [(1,0), (2,0), (1,1), (2,1)],
            1: [(1,0), (2,0), (1,1), (2,1)],
            2: [(1,0), (2,0), (1,1), (2,1)],
            3: [(1,0), (2,0), (1,1), (2,1)],
        },
        5: { # S
            0: [(0,1), (1,1), (1,0), (2,0)],
            1: [(1,0), (1,1), (2,1), (2,2)],
            2: [(2,1), (1,1), (1,2), (0,2)],
            3: [(1,2), (1,1), (0,1), (0,0)],
        },
        6: { # T
            0: [(0,1), (1,1), (1,0), (2,1)],
            1: [(1,0), (1,1), (2,1), (1,2)],
            2: [(2,1), (1,1), (1,2), (0,1)],
            3: [(1,2), (1,1), (0,1), (1,0)],
        },
        7: { # Z
            0: [(0,0), (1,0), (1,1), (2,1)],
            1: [(2,0), (2,1), (1,1), (1,2)],
            2: [(2,2), (1,2), (1,1), (0,1)],
            3: [(0,2), (0,1), (1,1), (1,0)],
        }
    }
    tetromino_colors = {
        0: (0, 0, 0),
        1: (61, 203, 255),
        2: (40, 80, 255),
        3: (255, 164, 25),
        4: (255, 240, 74),
        5: (100, 255, 69),
        6: (183, 74, 255),
        7: (255, 25, 25),
    }
    tetromino_rotation = {
        1: [(-1,0),(-1,1),(0,-2),(-1,-2)],
        2: [(1,0),(1,-1),(0,2),(1,2)],
        4: [(1,0),(1,-1),(0,2),(1,2)],
        5: [(-1,0),(-1,1),(0,-2),(-1,-2)],
        7: [(1,0),(1,1),(0,-2),(1,-2)],
        8: [(-1,0),(-1,-1),(0,2),(-1,2)],
        6: [(-1,0),(-1,-1),(0,2),(-1,2)],
        3: [(1,0),(1,1),(0,-2),(1,-2)]
    }
    i_rotation = {
        1: [(-2,0),(1,0),(-2,-1),(1,2)],
        2: [(2,0),(-1,0),(2,1),(-1,-2)],
        4: [(-1,0),(2,0),(-1,2),(2,-1)],
        5: [(1,0),(-2,0),(1,-2),(-2,1)],
        7: [(2,0),(-1,0),(2,1),(-1,-2)],
        8: [(-2,0),(1,0),(-2,-1),(1,2)],
        6: [(1,0),(-2,0),(1,-2),(-2,1)],
        3: [(-1,0),(2,0),(-1,2),(2,-1)]
    }

    def __init__(self, x = 0, y = 0, r = 0, t = 1):
        self.x = x
        self.y = y
        self.r = r
        self.t = t
    def __copy__(self):
        return Tetromino(self.x,self.y,self.r,self.t)

class Tetris:
    width = 10
    height = 23

    difficult_clears = ["BACK-TO-BACK","TETRIS","tspin triple","tspin double","mini tspin double","tspin single","mini tspin single","tspin no lines", "mini tspin no lines"]


    def __init__(self):
        self.reset()

    
    def reset(self):
        self.board = np.zeros((Tetris.width,Tetris.height))
        self.game_over = False
        self.new_round(True)
        self.score = 0
        self.combo = 0
        self.award = ""
        self.previous_award = ""
        self.level = 1
        self.lines = 0
        self.has_switched = False
        self.previous_rotate = False
        self.previous_triple_kick = False
    

    def collide(self, tetromino):
        for tet in Tetromino.tetrominos[tetromino.t][tetromino.r]:
            if(out_of_bounds(tet,tet[0]+tetromino.x,tet[1]+tetromino.y) or self.board[tet[0]+tetromino.x][tet[1]+tetromino.y] > 0):
                return True
        return False
    
    
    def add(self, tetromino):
        self.has_switched = False
        out_count = 0
        for tet in Tetromino.tetrominos[tetromino.t][tetromino.r]:
            if(tet[1]+tetromino.y<3):
                out_count+=1
            self.board[tet[0]+tetromino.x][tet[1]+tetromino.y] = tetromino.t
        if(out_count == 4):
            self.game_over = True
            return
        #scoring
        points = 0
        if(self.previous_award in Tetris.difficult_clears):
            difficult = True
        else:
            difficult = False
        #check for tspins
        full = False
        mini = False
        if(tetromino.t == 6 and self.previous_rotate):
            count = 0
            x = tetromino.x
            y = tetromino.y
            r = tetromino.r
            #check for mini tspin
            if(self.board[x][y] != 0):
                count+=1
            elif(r == 0 or r == 3):
                mini = True
            if(x+2 >= Tetris.width or self.board[x+2][y] != 0):
                count+=1
            elif(r == 0 or r == 1):
                mini = True
            if(y+2 >= Tetris.width or self.board[x][y+2] != 0):
                count+=1
            elif(r == 2 or r == 3):
                mini = True
            if(x+2 >= Tetris.width or y+2 >= Tetris.width  or self.board[x+2][y+2] != 0):
                count+=1
            elif(r == 1 or r == 2):
                mini = True
            full = count >= 3
        if(full):
            lines_cleared = self.clear_lines()
            if(mini and not self.previous_triple_kick): #mini tspin
                if(lines_cleared == 0):
                    points = self.level * 100
                    self.award = "mini tspin no lines"
                    self.previous_award = self.award
                elif(lines_cleared == 1):
                    points = self.level * 200
                    self.award = "mini tspin single"
                    self.previous_award = self.award
                elif(lines_cleared == 2):
                    points = self.level * 400
                    self.award = "mini tspin double"
                    self.previous_award = self.award
            else:                                       #full tspin
                if(lines_cleared == 0):
                    points = self.level * 400
                    self.award = "tspin no lines"
                    self.previous_award = self.award
                elif(lines_cleared == 1):
                    points = self.level * 800
                    self.award = "tspin single"
                    self.previous_award = self.award
                elif(lines_cleared == 2):
                    points = self.level * 1200
                    self.award = "tspin double"
                    self.previous_award = self.award
                elif(lines_cleared == 3):
                    points = self.level * 1600
                    self.award = "tspin triple"
                    self.previous_award = self.award
        else:
            lines_cleared = self.clear_lines()
            if(lines_cleared == 1):
                points = self.level * 100
                self.award = "single"
                self.previous_award = self.award
            elif(lines_cleared == 2):
                points = self.level * 300
                self.award = "double"
                self.previous_award = self.award
            elif(lines_cleared == 3):
                points = self.level * 500
                self.award = "triple"
                self.previous_award = self.award
            elif(lines_cleared == 4):
                self.score += self.level * 800
                if(self.previous_award == "TETRIS" or self.previous_award == "BACK-TO-BACK"):
                    self.award = "BACK-TO-BACK"
                else:
                    self.award = "TETRIS"
                self.previous_award = self.award
            else:
                self.award = ""

        if(lines_cleared >= 1):
            self.score += self.level * self.combo * 50
            self.combo+=1
        else:
            self.combo = 0
        if(difficult and self.award in Tetris.difficult_clears and self.award != "tspin no lines" and self.award != "mini tspin no lines"):
            self.score += 3*points//2
        else:
            self.score += points
        
        self.lines+=lines_cleared
        self.level = self.lines//10 + 1

        self.new_round()

        
    def left(self, tetromino):
        temp = tetromino.__copy__()
        temp.x -= 1
        if(not self.collide(temp)):
            tetromino.x -= 1
            self.previous_rotate = False
            return True
        return False
    def right(self, tetromino):
        temp = tetromino.__copy__()
        temp.x += 1
        if(not self.collide(temp)):
            tetromino.x += 1
            self.previous_rotate = False
            return True
        return False  
    def down(self, tetromino):
        temp = tetromino.__copy__()
        temp.y += 1
        if(not self.collide(temp)):
            tetromino.y += 1
            self.score+=1
            self.previous_rotate = False
            return True
        else:
            self.add(tetromino)
            return False
    def up(self, tetromino):
        while(self.down(tetromino)):
            self.score+=1
        return True
    def hold(self, tetromino):
        if(self.has_switched):
            return
        self.previous_rotate = False
        self.has_switched = True
        if not hasattr(self, 'held_piece'):
            self.held_piece = tetromino.__copy__()
            self.new_round()
        else:
            self.current_piece = Tetromino(3,2,0,self.held_piece.t)
            self.held_piece = tetromino.__copy__()
            if self.collide(self.current_piece):
                self.current_piece.y-=1
                if self.collide(self.current_piece):
                    self.game_over = True
        
    def rotate(self, tetromino, r):
        temp = tetromino.__copy__()
        temp.r = (temp.r + r) % 4
        if(not self.collide(temp)):
            tetromino.r = (tetromino.r + r) % 4
            self.previous_rotate = True
            self.previous_triple_kick = False
            return True
        else:
            if(tetromino.t == 1):
                test = tetromino.i_rotation[2*tetromino.r+(tetromino.r+r)%4]
                for i in range(len(test)):
                    temp = tetromino.__copy__()
                    temp.x += test[i][0]
                    temp.y -= test[i][1]
                    temp.r = (temp.r + r) % 4
                    if(not self.collide(temp)):
                        tetromino.r = (tetromino.r + r) % 4
                        tetromino.x += test[i][0]
                        tetromino.y -= test[i][1]
                        self.previous_rotate = True
                        self.previous_triple_kick = (i == 3)
                        return True
            else:
                test = tetromino.tetromino_rotation[2*tetromino.r+(tetromino.r+r)%4]
                for i in range(len(test)):
                    temp = tetromino.__copy__()
                    temp.x += test[i][0]
                    temp.y -= test[i][1]
                    temp.r = (temp.r + r) % 4
                    if(not self.collide(temp)):
                        tetromino.r = (tetromino.r + r) % 4
                        tetromino.x += test[i][0]
                        tetromino.y -= test[i][1]
                        self.previous_rotate = True
                        self.previous_triple_kick = (i == 3)
                        return True
        return False
    

    def get_board(self):
        tetromino = self.current_piece
        board = self.board.__copy__()
        for tet in Tetromino.tetrominos[tetromino.t][tetromino.r]:
            board[tet[0]+tetromino.x][tet[1]+tetromino.y] = tetromino.t
        return board
    def get_just_board(self):
        return self.board

    def get_current_piece(self):
        return self.current_piece
    
    def get_held_piece(self):
        if hasattr(self, 'held_piece'):
            return self.held_piece
        else:
            return False

    def get_ghost_piece(self):
        self.ghost_piece = self.current_piece.__copy__()
        while(not self.collide(self.ghost_piece)):
            self.ghost_piece.y += 1
        self.ghost_piece.y -= 1
        return self.ghost_piece
    

    def new_round(self, new = False):
        #get next piece
        if not hasattr(self, 'queue'):
            self.queue = list(range(1,len(Tetromino.tetrominos)+1))
            random.shuffle(self.queue)
        
        if not hasattr(self, 'bag') or len(self.bag) == 0:
            self.bag = list(range(1,len(Tetromino.tetrominos)+1))
            random.shuffle(self.bag)

        self.current_piece = Tetromino(3,2,0,self.queue.pop())
        self.queue.insert(0,self.bag.pop())

        self.previous_rotate = False
        self.previous_triple_kick = False

        self.board_list = [self.get_board]
        if self.collide(self.current_piece):
            self.current_piece.y-=1
            if self.collide(self.current_piece):
                self.game_over = True

    def clear_line(self,line,num):
        self.board[:,num:line+num]=self.board[:,0:line]
        self.board[:,0:num] = np.zeros_like(self.board[:,0:num])

    def clear_lines(self):
        lines_to_clear = [i for i in range(Tetris.height) if np.all(self.board[:,i])]
        if lines_to_clear:
            count = 0
            for i,j in enumerate(lines_to_clear):
                if(i < len(lines_to_clear)-1 and j == lines_to_clear[i+1] - 1):
                    count+=1
                else:
                    self.clear_line(lines_to_clear[i-(count)], count+1)
                    count = 0
        return len(lines_to_clear)