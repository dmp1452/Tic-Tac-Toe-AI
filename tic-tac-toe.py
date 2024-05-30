import sys
import pygame
import numpy as np
import random
import copy
import time
from values import *

pygame.init()
screen = pygame.display.set_mode((W,H+100))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BACKGROUND_COLOR)
font = pygame.font.Font(None,30)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.marked_squares=0

    #Searches if there is a win and returns 1 or -1, otherwise returns 0
    def final_state(self):
        for row in range(ROWS):
            if abs(np.sum(self.squares[row,:]))==3:
                return self.squares[row,0]
            
        for col in range(COLS):
            if abs(np.sum(self.squares[:,col]))==3:
                return self.squares[0,col]
            
        if abs(np.sum(np.diag(self.squares)))==3:
            return self.squares[1,1]
        
        if abs(np.sum(np.diag(np.fliplr(self.squares))))==3:
            return self.squares[1,1]
        return 0

    
    def place(self,row,col,player):
        self.squares[row][col]=player
        self.marked_squares+=1

    def check_empty(self,row,col):
        return self.squares[row][col]==0
    
    def is_full(self):
        return self.marked_squares==9

    def is_empty(self):
        return self.marked_squares ==0
    
    def get_empty(self):#simplify

        empty = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.check_empty(row,col):
                    empty.append((row,col))

        return empty

class AI:
    def __init__(self, player=-1):
        self.player =player

    #Used for initial pick, otherwise takes a while
    def random_choice(self,board):
        empty_squares = board.get_empty()
        index = random.randrange(0,len(empty_squares))
        return empty_squares[index]

    def minimax(self,board,maximizing,alpha,beta):
        case = board.final_state()
        if case !=0:
           return case, None
        elif board.is_full():
            return 0, None
        
        empty_squares = board.get_empty()
        if maximizing:
            max_eval =-2
            best_move = None
            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.place(row,col,1)
                eval =self.minimax(temp_board,False,alpha,beta)[0]
                if eval > max_eval:
                    max_eval=eval
                    best_move = (row,col)
                alpha = max(alpha,max_eval)
                if beta<= alpha:
                    break
            return max_eval, best_move
        elif not maximizing:
            min_eval =2
            best_move = None
            for (row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.place(row,col,self.player)
                eval =self.minimax(temp_board,True,alpha,beta)[0]
                if eval < min_eval:
                    min_eval=eval
                    best_move = (row,col)
                beta = min(beta,min_eval)
                if beta<= alpha:
                    break
                
            return min_eval, best_move


    def eval(self,main_board):
        """
        if main_board.is_empty():
            eval = 'random, all choices equal'
            move=self.random_choice(main_board)
        else:"""
        start_time = time.time()
        eval , move =self.minimax(main_board,False,-10,10)
        end_time = time.time()
        elapsed = end_time-start_time
        print(str(elapsed))
        message("AI has chosen "+ str(move)+" with eval "+ str(eval))
        return move



class Game:
    def __init__(self, player, gamemode):
        self.board =Board()
        self.ai =AI()
        self.player =player
        self.gamemode = gamemode
        self.running = True
        self.lines()
        self.buttons()
    def make_move(self,row,col,player):
        self.board.place(row,col,player)
        self.draw_fig(row,col)
        self.next_turn()


    def next_turn(self):
        self.player=self.player*-1
         
    def buttons(self):
        pygame.draw.rect(screen,(255,255,255),(0,0,200,50))
        pygame.draw.rect(screen,BLACK,(0,0,200,50),1)
        text1_surface = font.render("PvP",True,BLACK)
        text1_rect = text1_surface.get_rect()
        text1_rect.center=(100,25)
        screen.blit(text1_surface,text1_rect)

        pygame.draw.rect(screen,(255,255,255),(200,0,400,50))
        pygame.draw.rect(screen,BLACK,(200,0,400,50),1)
        text2_surface = font.render("AI Starts", True, BLACK)
        text2_rect = text2_surface.get_rect()
        text2_rect.center=(300,25)
        screen.blit(text2_surface,text2_rect)

        pygame.draw.rect(screen,(255,255,255),(400,0,600,50))
        pygame.draw.rect(screen,BLACK,(400,0,600,50),1)
        text3_surface = font.render("AI you start", True, BLACK)
        text3_rect = text1_surface.get_rect()
        text3_rect.center=(465,25)
        screen.blit(text3_surface,text3_rect)

        message("New Game vs AI, you go first")

    def lines(self):
        pygame.draw.line(screen,LINE_COLOR,(SQUARE_SIZE,50),(SQUARE_SIZE,H+50),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(W-SQUARE_SIZE,50),(W-SQUARE_SIZE,H+50),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,SQUARE_SIZE+50),(W,SQUARE_SIZE+50),LINE_WIDTH) 
        pygame.draw.line(screen,LINE_COLOR,(0,H-SQUARE_SIZE+50),(W,H-SQUARE_SIZE+50),LINE_WIDTH)
    
    def draw_fig(self,row,col):
        if self.player ==1:
            start_desc=(col*SQUARE_SIZE+OFFSET,row*SQUARE_SIZE+OFFSET+50)
            end_desc= (col*SQUARE_SIZE+SQUARE_SIZE-OFFSET, row*SQUARE_SIZE+SQUARE_SIZE-OFFSET+50)
            pygame.draw.line(screen,BLACK,start_desc,end_desc,CROSS_WIDTH)

            start_asc=(col*SQUARE_SIZE+OFFSET,row*SQUARE_SIZE+SQUARE_SIZE-OFFSET+50)
            end_asc= (col*SQUARE_SIZE+SQUARE_SIZE-OFFSET, row*SQUARE_SIZE+OFFSET+50)
            pygame.draw.line(screen,BLACK,start_asc,end_asc,CROSS_WIDTH)
        else:
            center=(col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE+SQUARE_SIZE//2+50)
            pygame.draw.circle(screen,BLACK,center,RADIUS,CIRC_WIDTH)

def message( message):
        pygame.draw.rect(screen,(255,255,255),(0,650,600,700))
        pygame.draw.rect(screen,BLACK,(0,650,600,700),3)
        message_surface = font.render(message, True, BLACK)
        message_rect = message_surface.get_rect()
        message_rect.center=(300,675)
        screen.blit(message_surface,message_rect)

def main():
    game = Game(1,'ai')
    board = game.board
    ai =game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1]<50:
                    mode = event.pos[0]//200
                    screen.fill(BACKGROUND_COLOR)
                    if mode ==0:
                        game = Game(1,'pvp')
                        message("New Game, PvP")
                    elif mode ==1:
                        game = Game(-1, 'ai')
                        message("New Game vs AI, AI goes first")
                    else:
                        game = Game(1, 'ai')
                        message("New Game vs AI, you go first")
                    board = game.board
                    ai = game.ai


                elif board.final_state() ==0:
                    row =int ((event.pos[1]-50)//SQUARE_SIZE)
                    col = int(event.pos[0]//SQUARE_SIZE)
                    if board.check_empty(row,col):
                        game.make_move(row,col,game.player)
                    if board.final_state() !=0:
                        message("Game won!")
                    elif board.is_full():
                        message("Game Tied!")
                pygame.display.update()

        if game.gamemode=='ai' and game.player == ai.player and board.final_state()==0 and not board.is_full():
            row,col = ai.eval(board)
            game.make_move(row,col,ai.player)
            if board.final_state() !=0:
                message("Game won by AI!")
            elif board.is_full():
                message("Game Tied!")

        pygame.display.update()
            

main()