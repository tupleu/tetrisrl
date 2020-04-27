import pygame
from tetris import Tetris, Tetromino

#Global Variables
block_size = 30
screen_size = 24
screen_width = screen_size*block_size
screen_height = screen_size*block_size

game_width = block_size * Tetris.width
game_height = block_size * 20
border_width = block_size //5

def draw_board(surface, game):
    board = game.get_just_board()
    piece = game.get_current_piece()
    ghost = game.get_ghost_piece()
    held_piece = game.get_held_piece()

    rot = 0

    surface.fill((255,255,255))

    x_start = screen_width//2 - game_width//2
    y_start = screen_height//2 - game_height//2
    
    
    font = pygame.font.SysFont("avenir",block_size)
    score = font.render("score: " + str(game.score), 1, (0,0,0))
    level = font.render("level: " + str(game.level),1,(0,0,0))
    lines = font.render("lines: " + str(game.lines),1,(0,0,0))
    award = font.render(game.award, 1, (0,0,0))

    surface.blit(score, (x_start + game_width + block_size, y_start + game_height-block_size))
    surface.blit(level, (x_start -4*block_size, y_start + game_height-3*block_size))
    surface.blit(lines, (x_start -4*block_size, y_start + game_height-block_size))
    if(game.award != ""):
        surface.blit(award, (x_start + game_width + block_size, y_start + game_height-3*block_size))

    #draw board
    for i in range(len(board)):
        for j in range(3,len(board[i])):
            pygame.draw.rect(surface, Tetromino.tetromino_colors[board[i][j]], (x_start + i*block_size, y_start + (j-3)*block_size,block_size,block_size), 0)
    
    #draw queue
    for i in range(len(game.queue)):
        for j in range(4):
            pygame.draw.rect(surface, Tetromino.tetromino_colors[game.queue[i]], (x_start + block_size/2 + 10*block_size + (block_size/2)*(Tetromino.tetrominos[game.queue[i]][rot][j][0]),y_start + block_size/2 + (len(game.queue)-1-i)*block_size*2 + (block_size/2)*(Tetromino.tetrominos[game.queue[i]][rot][j][1]), block_size/2, block_size/2), 0)
    pygame.draw.rect(surface, (0,0,0), (x_start + block_size/2 + 10*block_size, y_start,2*block_size,14*block_size),border_width)

    #draw ghost
    for i in range(4):
        pygame.draw.rect(surface, (100,100,100), (x_start + block_size*(ghost.x+Tetromino.tetrominos[ghost.t][ghost.r][i][0]), y_start + block_size*(ghost.y-3+Tetromino.tetrominos[ghost.t][ghost.r][i][1]), block_size, block_size), 0)
    #draw current piece
    for i in range(4):
        pygame.draw.rect(surface, Tetromino.tetromino_colors[piece.t], (x_start + block_size*(piece.x+Tetromino.tetrominos[piece.t][piece.r][i][0]), y_start + block_size*(piece.y-3+Tetromino.tetrominos[piece.t][piece.r][i][1]), block_size, block_size), 0)

    #draw held piece
    if(held_piece):
        for i in range(4):
            pygame.draw.rect(surface, Tetromino.tetromino_colors[held_piece.t], (x_start - 4*block_size + block_size*(Tetromino.tetrominos[held_piece.t][rot][i][0]), y_start + block_size + block_size*(Tetromino.tetrominos[held_piece.t][rot][i][1]), block_size, block_size), 0)

    pygame.draw.rect(surface, (0,0,0), (x_start - 4*block_size - border_width//2,y_start + border_width//2,4*block_size,4*block_size),border_width)
    pygame.display.update()
    
    

def main():
    game = Tetris()
   
    clock = pygame.time.Clock()
    fall = 0
    fall_rate = 1

    while not game.game_over:
        current_piece = game.get_current_piece()
        fall += clock.get_rawtime()
        clock.tick()
        if fall/1000 > fall_rate:
            fall = 0
            # game.down(current_piece) #uncomment to add fall

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game.left(current_piece)
                if event.key == pygame.K_d:
                    fall = 0
                    game.right(current_piece)
                if event.key == pygame.K_s:
                    game.down(current_piece)
                if event.key == pygame.K_w:
                    game.up(current_piece)
                if event.key == pygame.K_LEFT:
                    game.rotate(current_piece,-1)
                if event.key == pygame.K_RIGHT:
                    game.rotate(current_piece,1)
                if event.key == pygame.K_ESCAPE:
                    game.game_over = True
                if event.key == pygame.K_UP:
                    game.hold(current_piece)
        draw_board(window,game)
    
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((screen_width,screen_height))
    main()