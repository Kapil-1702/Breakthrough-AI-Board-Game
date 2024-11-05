import numpy as np
import pygame
import sys, os, math
import time
import random

startingBoardRepresentation = [[1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [2, 2, 2, 2, 2, 2, 2, 2],
                      [2, 2, 2, 2, 2, 2, 2, 2]]

MAXNUM = float("inf")
MINNUM = -float("inf")
MAXTUPLE = (MAXNUM, MAXNUM)
MINTUPLE = (MINNUM, MINNUM)

def single_move(initial_pos, direction, turn):
    if turn == 1:
        if direction == 1:
            return initial_pos[0] + 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] + 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] + 1, initial_pos[1] + 1
    elif turn == 2:
        if direction == 1:
            return initial_pos[0] - 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] - 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] - 1, initial_pos[1] + 1


def alterturn(turn):
    if turn == 1:
        return 2
    if turn == 2:
        return 1


class Action:
    def __init__(self, coordinate, direction, turn):
        self.coordinate = coordinate
        self.direction = direction
        self.turn = turn
    def getString(self):
        return self.coordinate, self.direction, self.turn
    def getCoordinate_x(self):
        return self.coordinate[0]


class State:
    def __init__(self,
                 BoardRepresentation=None,
                 BlackPawnPosition=None,
                 WhitePawnPosition=None,
                 black_num=0,
                 white_num=0,
                 turn=1,
                 function=0,
                 width=8,
                 height=8):
        self.width = width
        self.height = height
        if BlackPawnPosition is None:
            self.BlackPawnPositions = []
        else:
            self.BlackPawnPositions = BlackPawnPosition
        if WhitePawnPosition is None:
            self.WhitePawnPositions = []
        else:
            self.WhitePawnPositions = WhitePawnPosition
        self.black_num = black_num
        self.white_num = white_num
        self.turn = turn
        self.function = function
        if BoardRepresentation is not None:
            for i in range(self.height):
                for j in range(self.width):
                    if BoardRepresentation[i][j] == 1:
                        self.BlackPawnPositions.append((i, j))
                        self.black_num += 1
                    if BoardRepresentation[i][j] == 2:
                        self.WhitePawnPositions.append((i, j))
                        self.white_num += 1


    def transfer(self, action):
        black_pos = list(self.BlackPawnPositions)
        white_pos = list(self.WhitePawnPositions)

        if action.turn == 1:
            if action.coordinate in self.BlackPawnPositions:
                index = black_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                black_pos[index] = new_pos
                if new_pos in self.WhitePawnPositions:
                    white_pos.remove(new_pos)
            else:
                print("Invalid action!")

        elif action.turn == 2:
            if action.coordinate in self.WhitePawnPositions:
                index = white_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                white_pos[index] = new_pos
                if new_pos in self.BlackPawnPositions:
                    black_pos.remove(new_pos)
            else:
                print("Invalid action!")

        state = State(BlackPawnPosition=black_pos, WhitePawnPosition=white_pos, black_num=self.black_num, white_num=self.white_num, turn=alterturn(action.turn), function=self.function, height=self.height, width=self.width)
        return state


    def available_actions(self):
        available_actions = []

        if self.turn == 1:
            for pos in sorted(self.BlackPawnPositions, key=lambda p: (p[0], -p[1]), reverse=True):
                if pos[0] != self.height - 1 and pos[1] != 0 and (pos[0] + 1, pos[1] - 1) not in self.BlackPawnPositions:
                    available_actions.append(Action(pos, 1, 1))
                if pos[0] != self.height - 1 and (pos[0] + 1, pos[1]) not in self.BlackPawnPositions and (pos[0] + 1, pos[1]) not in self.WhitePawnPositions:
                    available_actions.append(Action(pos, 2, 1))
                if pos[0] != self.height - 1 and pos[1] != self.width - 1 and (pos[0] + 1, pos[1] + 1) not in self.BlackPawnPositions:
                    available_actions.append(Action(pos, 3, 1))

        elif self.turn == 2:
            for pos in sorted(self.WhitePawnPositions, key=lambda p: (p[0], p[1])):
                if pos[0] != 0 and pos[1] != 0 and (pos[0] - 1, pos[1] - 1) not in self.WhitePawnPositions:
                    available_actions.append(Action(pos, 1, 2))
                if pos[0] != 0 and (pos[0] - 1, pos[1]) not in self.BlackPawnPositions and (pos[0] - 1, pos[1]) not in self.WhitePawnPositions:
                    available_actions.append(Action(pos, 2, 2))
                if pos[0] != 0 and pos[1] != self.width - 1 and (pos[0] - 1, pos[1] + 1) not in self.WhitePawnPositions:
                    available_actions.append(Action(pos, 3, 2))

        return available_actions

    
    def getMatrix(self):
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for item in self.BlackPawnPositions:
            matrix[item[0]][item[1]] = 1
        for item in self.WhitePawnPositions:
            matrix[item[0]][item[1]] = 2
        return matrix

    def utility(self, turn):
        if self.function == 0:
            return 0
        elif self.function == 1:
            return self.offensiveHeuristic1(turn)
        elif self.function == 2:
            return self.defensiveHeuristic1(turn)
        elif self.function == 3:
            return self.offensiveHeuristic2(turn)
        elif self.function == 4:
            return self.defensiveHeuristic2(turn)


    def winningscore(self, turn):
        winningvalue = 200
        if turn == 1:
            if self.isgoalstate() == 1:
                return winningvalue
            elif self.isgoalstate() == 2:
                return -winningvalue
            else:
                return 0
        elif turn == 2:
            if self.isgoalstate() == 2:
                return winningvalue
            elif self.isgoalstate() == 1:
                return -winningvalue
            else:
                return 0


    def isgoalstate(self, type=0):
        if type == 0:
            if 0 in [item[0] for item in self.WhitePawnPositions] or len(self.BlackPawnPositions) == 0:
                return 2
            if self.height - 1 in [item[0] for item in self.BlackPawnPositions] or len(self.WhitePawnPositions) == 0:
                return 1
            return 0
        else:
            count = 0
            for i in self.BlackPawnPositions:
                if i[0] == 7:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.WhitePawnPositions:
                if i[0] == 0:
                    count += 1
            if count == 3:
                return True
            if len(self.BlackPawnPositions) <= 2 or len(self.WhitePawnPositions) <= 2:
                return True
        return False


    def myScore(self, turn):
        if turn == 1:
            return len(self.BlackPawnPositions) \
                   + sum(pos[0] for pos in self.BlackPawnPositions)

        elif turn == 2:
            return len(self.WhitePawnPositions) \
                   + sum(7 - pos[0] for pos in self.WhitePawnPositions)


    def opponentScore(self, turn):
        if turn == 1:
            return len(self.WhitePawnPositions) \
                   + sum(7 - pos[0] for pos in self.WhitePawnPositions)

        elif turn == 2:
            return len(self.BlackPawnPositions) \
                   + sum(pos[0] for pos in self.BlackPawnPositions)
            

    def offensiveHeuristic1(self, turn):
        return 2*(30-self.opponentScore(turn))+random.random()/10               

    def defensiveHeuristic1(self, turn):
        return 2*self.myScore(turn)+random.random()/10
               
    def offensiveHeuristic2(self, turn):
        return 1 * self.myScore(turn) - 2 * self.opponentScore(turn)

    def defensiveHeuristic2(self, turn):
        return 2 * self.myScore(turn) - 2 * self.opponentScore(turn)
class MinimaxAgent:
    
    def __init__(self, BoardRepresentation, turn, depth, function, type=0):
        self.BoardRepresentation = BoardRepresentation
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.blocks = 0
        self.piece_num = 0


    def max_value(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MINNUM
        for action in state.available_actions():
            v = max(v, self.min_value(state.transfer(action), depth + 1))
            self.blocks += 1
        return v



    def min_value(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MAXNUM
        for action in state.available_actions():
            v = min(v, self.max_value(state.transfer(action), depth + 1))
            self.blocks += 1

        return v


    def minimax_decision(self):
        final_action = None
        if self.type == 0:
            startingState = State(BoardRepresentation=self.BoardRepresentation, turn=self.turn, function=self.function)
        else:
            startingState = State(BoardRepresentation=self.BoardRepresentation, turn=self.turn, function=self.function, height=3, width=10)
        v = MINNUM
        for action in startingState.available_actions():
            self.blocks += 1
            newState = startingState.transfer(action)
            if newState.isgoalstate():
                final_action = action
                break
            minresult = self.min_value(newState, 1)
            if minresult > v:
                final_action = action
                v = minresult
        if self.turn == 1:
            self.piece_num = startingState.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = startingState.transfer(final_action).black_num
        print(final_action.getString())
        return startingState.transfer(final_action), self.blocks, self.piece_num






class AlphaBetaAgent: 
    def __init__(self, BoardRepresentation, turn, depth, function, type=0):
        self.BoardRepresentation = BoardRepresentation
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.blocks = 0
        self.piece_num = 0

    def max_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MINNUM
        actions = state.available_actions()
        actions = sorted(state.available_actions(), key=lambda action: 0, reverse=True)
 
        for action in actions:
            self.blocks += 1

            v = max(v, self.min_value(state.transfer(action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MAXNUM
        actions = state.available_actions()
        actions = sorted(state.available_actions(), key=lambda action: 0)

        for action in actions:
            self.blocks += 1

            v = min(v, self.max_value(state.transfer(action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    
    def alpha_beta_decision(self):
        final_action = None
        if self.type == 0:
            startingState = State(BoardRepresentation=self.BoardRepresentation, turn=self.turn, function=self.function)
        else:
            startingState = State(BoardRepresentation=self.BoardRepresentation, turn=self.turn, function=self.function, height=4, width=10)
        v = MINNUM
        for action in startingState.available_actions():
            self.blocks += 1

            newState = startingState.transfer(action)
            if newState.isgoalstate():
                final_action = action
                break
            minresult = self.min_value(newState, MINNUM, MAXNUM, 1)
            if minresult > v:
                final_action = action
                v = minresult
        print(v)
        if self.turn == 1:
            self.piece_num = startingState.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = startingState.transfer(final_action).black_num
        print(final_action.getString())
        return startingState.transfer(final_action), self.blocks, self.piece_num

class BreakthroughGame:

    def __init__(self):
        """ _init_ initializes all variables for the game, including declaring board dimensions, piece placement, and setting metrics to zero. The game clock is also started."""
        
        pygame.init()
        
        self.width, self.height = 700, 560
        self.sizeofcell = int(560/8)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        self.screen.fill([255, 255, 255])
        self.board = 0
        self.Pawn_Black_Color = 0
        self.Pawn_White_Color = 0
        self.reset = 0
        self.trophy = 0
        self.BoardRepresentation = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        self.gameStatus = 0
        self.turn = 1
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        self.total_blocks_1 = 0
        self.total_blocks_2 = 0
        self.total_time_1 = 0
        self.total_time_2 = 0
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece = 0

        pygame.display.set_caption("Breakthrough Game")

        self.clock = pygame.time.Clock()
        self.initgraphics()

    def run(self):
        """Run the game"""

        self.clock.tick(90)

        self.screen.fill([255, 255, 255])

        if self.gameStatus in  [5,6,7,8,9,10]:
            player1search = 2
            player2search = 2

            if self.gameStatus == 5:
                player1search = 1
                player1heur = 1
                player2heur = 1
            elif self.gameStatus == 6:
                player1heur = 3
                player2heur = 2
            elif self.gameStatus == 7:
                player1heur = 4
                player2heur = 1
            elif self.gameStatus == 8:
                player1heur = 3
                player2heur = 1
            elif self.gameStatus == 9:
                player1heur = 4
                player2heur = 2
            elif self.gameStatus == 10:
                player1heur = 3
                player2heur = 4

            if self.turn == 1:
                start = time.process_time()
                self.ai_move(player1search, player1heur)
                self.total_time_1 += (time.process_time() - start)
                self.total_step_1 += 1
                print('Total number of steps by Player 1  = ', self.total_step_1,
                        'Total number of steps traversed by Player 1  = ', self.total_blocks_1, "\n",
                        'Average blocks traversed per move by Player 1 = ', self.total_blocks_1 / self.total_step_1,
                        'Average time taken per step by Player 1  = ', self.total_time_1 / self.total_step_1, "\n",
                        'Player 1 has captured = ', self.eat_piece)
            elif self.turn == 2:
                start = time.process_time()
                self.ai_move(player2search, player2heur)
                self.total_time_2 += (time.process_time() - start)
                self.total_step_2 += 1
                print('Total number of steps by Player 2 = ', self.total_step_2,
                        'Total number of steps traversed by Player 2 = ', self.total_blocks_2, "\n",
                        'Average blocks traversed per move by Player 2 = ', self.total_blocks_2 / self.total_step_2,
                        'Average time taken per step by Player 2 = ', self.total_time_2 / self.total_step_2, "\n",
                        'Player 2 has captured ', self.eat_piece)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):  
                self.BoardRepresentation = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]
                self.turn = 1
                self.gameStatus = 0

            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(1, event.pos):
                self.gameStatus = 5
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(2, event.pos):
                self.gameStatus = 6
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(3, event.pos):
                self.gameStatus = 7
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(4, event.pos):
                self.gameStatus = 8
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(5, event.pos):
                self.gameStatus = 9
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(6, event.pos):
                self.gameStatus = 10

        self.display()
        pygame.display.flip()

    def initgraphics(self):
        self.board = pygame.image.load_extended(os.path.join('imagesFolder', 'chessboard.jpg'))
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.Pawn_Black_Color = pygame.image.load_extended(os.path.join('imagesFolder', 'Pawn_Black_Color.png'))
        self.Pawn_Black_Color = pygame.transform.scale(self.Pawn_Black_Color, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.Pawn_White_Color = pygame.image.load_extended(os.path.join('imagesFolder', 'Pawn_White_Color.png'))
        self.Pawn_White_Color = pygame.transform.scale(self.Pawn_White_Color, (self.sizeofcell - 20, self.sizeofcell - 20))
        self.reset = pygame.image.load_extended(os.path.join('imagesFolder', 'reset.png'))
        self.reset = pygame.transform.scale(self.reset, (80, 80))
        self.trophy = pygame.image.load_extended(os.path.join('imagesFolder', 'trophy.png'))
        self.trophy = pygame.transform.scale(self.trophy, (250, 250))
        self.matchup1 = pygame.image.load_extended(os.path.join('imagesFolder', '1.png'))
        self.matchup1 = pygame.transform.scale(self.matchup1, (90, 70))
        self.matchup2 = pygame.image.load_extended(os.path.join('imagesFolder', '2.png'))
        self.matchup2 = pygame.transform.scale(self.matchup2, (90, 70))
        self.matchup3 = pygame.image.load_extended(os.path.join('imagesFolder', '3.png'))
        self.matchup3 = pygame.transform.scale(self.matchup3, (90, 70))
        self.matchup4 = pygame.image.load_extended(os.path.join('imagesFolder', '4.png'))
        self.matchup4 = pygame.transform.scale(self.matchup4, (90, 70))
        self.matchup5 = pygame.image.load_extended(os.path.join('imagesFolder', '5.png'))
        self.matchup5 = pygame.transform.scale(self.matchup5, (90, 70))
        self.matchup6 = pygame.image.load_extended(os.path.join('imagesFolder', '6.png'))
        self.matchup6 = pygame.transform.scale(self.matchup6, (90, 70))

    def display(self):
        self.screen.blit(self.board, (0, 0))
        self.screen.blit(self.reset, (590, 20))
        self.screen.blit(self.matchup1, (587, 100))
        self.screen.blit(self.matchup2, (587, 175))
        self.screen.blit(self.matchup3, (587, 250))
        self.screen.blit(self.matchup4, (587, 325))
        self.screen.blit(self.matchup5, (587, 400))
        self.screen.blit(self.matchup6, (587, 475))
        for i in range(8):
            for j in range(8):
                if self.BoardRepresentation[i][j] == 1:
                    self.screen.blit(self.Pawn_Black_Color, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
                elif self.BoardRepresentation[i][j] == 2:
                    self.screen.blit(self.Pawn_White_Color, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))

        if self.gameStatus == 1:
            if self.BoardRepresentation[self.ori_x][self.ori_y] == 1:
                x1 = self.ori_x + 1
                y1 = self.ori_y - 1
                x2 = self.ori_x + 1
                y2 = self.ori_y + 1
                x3 = self.ori_x + 1
                y3 = self.ori_y
                if y1 >= 0 and self.BoardRepresentation[x1][y1] != 1:
                    self.screen.blit(
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                if y2 <= 7 and self.BoardRepresentation[x2][y2] != 1:
                    self.screen.blit(
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                if x3 <= 7 and self.BoardRepresentation[x3][y3] == 0:
                    self.screen.blit(
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

            if self.BoardRepresentation[self.ori_x][self.ori_y] == 2:
                x1 = self.ori_x - 1
                y1 = self.ori_y - 1
                x2 = self.ori_x - 1
                y2 = self.ori_y + 1
                x3 = self.ori_x - 1
                y3 = self.ori_y
                if y1 >= 0 and self.BoardRepresentation[x1][y1] != 2:
                    self.screen.blit(
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                if y2 <= 7 and self.BoardRepresentation[x2][y2] != 2:
                    self.screen.blit(
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                if x3 >= 0 and self.BoardRepresentation[x3][y3] == 0:
                    self.screen.blit(
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

        if self.gameStatus == 3:
            self.screen.blit(self.trophy, (100, 100))

            font = pygame.font.Font('freesansbold.ttf', 32)

            if self.turn == 1:
                color = "White Pawns"
            elif self.turn == 2:
                color = "Black Pawns"
            content = color + " win"
            text = font.render(content, True, (0, 0, 0), (255, 255, 255)) 
            textRect = text.get_rect() 
            textRect.center = (self.width // 3, self.height // 2)
            self.screen.blit(text, textRect)
        

    def isreset(self, pos):
        x, y = pos
        if 670 >= x >= 590 and 20 <= y <= 100:
            return True
        return False

    def ismatchup(self, matchup, pos):
        x, y = pos
        if 587 <= x <= 677 and (100 + ((matchup - 1) * 70)) <= y <= (175 + ((matchup - 1) * 70)):
            return True
        return False

    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.ai_move_minimax(evaluation)
        elif searchtype == 2:
            return self.ai_move_alphabeta(evaluation)

    def ai_move_minimax(self, function_type):
        board, blocks, piece = MinimaxAgent(self.BoardRepresentation, self.turn, 3, function_type).minimax_decision()
        self.BoardRepresentation = board.getMatrix()
        if self.turn == 1:
            self.total_blocks_1 += blocks
            self.turn = 2
        elif self.turn == 2:
            self.total_blocks_2 += blocks
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.gameStatus = 3

    def ai_move_alphabeta(self, function_type):
        board, blocks, piece = AlphaBetaAgent(self.BoardRepresentation, self.turn, 4, function_type).alpha_beta_decision()
        self.BoardRepresentation = board.getMatrix()
        if self.turn == 1:
            self.total_blocks_1 += blocks
            self.turn = 2
        elif self.turn == 2:
            self.total_blocks_2 += blocks
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.gameStatus = 3

    def isgoalstate(self, base=0):
        if base == 0:
            if 2 in self.BoardRepresentation[0] or 1 in self.BoardRepresentation[7]:
                return True
            else:
                for line in self.BoardRepresentation:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.BoardRepresentation[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.BoardRepresentation[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.BoardRepresentation:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False

def main():
    game = BreakthroughGame()
    while 1:
        game.run()
    while 0:
        print("La Fin")

if __name__ == '__main__': 
    main()