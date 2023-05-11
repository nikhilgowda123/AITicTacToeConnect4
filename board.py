from copy import deepcopy
from random import choice
from sys import exit as sys_exit
import time
from numpy import NINF, flip, random, zeros
from pygame import QUIT, display, draw
from pygame import event as pygame_event
from pygame import font
from pygame import init as pygame_init
from pygame import time as pygame_time
from alpha_beta_pruning import (default_opponent_move, get_q_childs, get_best_move,get_moves)


WHITE = (255, 255, 255)
BLACK = (255, 255, 255)
CIRCLE_BLACK = (0, 0, 0)
BLUE = (0, 163, 255)
GREEN = (76, 175, 80)
GREY = (128,128,128)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)


class gameConnect4:

    def __init__(self, nb_rows=6, nb_cols=7):
        self.rows = nb_rows
        self.cols = nb_cols
        self.board = zeros((nb_rows, nb_cols))
        self.game_over = False
        self.turn = 0
        self.winner = None

    def play_the_move(self, row, col, symb):
        self.board[row][col] = symb

    def revert_the_move(self, row, col, symb):
        self.board[row][col] = 0
        self.turn = 1 - self.turn

    def is_move_correct(self, col):
        return self.board[self.rows-1][col] == 0

    def is_row_free(self, col):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r

    def display_board(self):
        print(flip(self.board, 0))

    def is_win(self, piece):
        for c in range(self.cols-3):
            for r in range(self.rows):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        for c in range(self.cols):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        for c in range(self.cols-3):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        for c in range(self.cols-3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    def check_game_draw(self):
        flag = 0
        for colno in range(self.cols):
            for rowno in range(self.rows):
                if self.board[rowno][colno] == 0 :
                    flag = 1
                    break
        
        if flag == 0:
            return True
        
        else:
            return False


    def write_tic_tac_toe_board(self, screen, compare_no):
        if compare_no == 1:
            COLOR_1 = BLUE
            COLOR_2 = GREY
        if compare_no == 2:
            COLOR_1 = GREY
            COLOR_2 = GREEN
        if compare_no == 3:
            COLOR_1 = BLUE
            COLOR_2 = GREEN
        height = (self.rows+1) * SQUARESIZE

        for c in range(self.cols):
            for r in range(self.rows):
                draw.rect(
                    screen, WHITE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                draw.circle(screen, CIRCLE_BLACK, (int(
                    c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS, 1)

        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] == 1:
                    draw.circle(screen, COLOR_1, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif self.board[r][c] == 2:
                    draw.circle(screen, COLOR_2, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        display.update()



    def play_minimax_vs_default(self):
        exec_time = 0
        pygame_init()
        win_number = 0
        w = self.cols * SQUARESIZE
        h = (self.rows+1) * SQUARESIZE
        dimension = (w, h)

        screen = display.set_mode(dimension)
        self.write_tic_tac_toe_board(screen,1)
        display.update()

        display_font = font.Font('freesansbold.ttf',50)

        while not self.game_over:
            for event in pygame_event.get():
                if event.type == QUIT:
                    sys_exit()
                draw.rect(screen, WHITE, (0, 0, w, SQUARESIZE))
                if self.turn == 0:
                    start = time.time()
                    col = get_best_move(self)
                    end = time.time()
                    exec_time = exec_time+(end-start)

                    row = self.is_row_free(col)
                    self.play_the_move(row, col, 1)

                    if self.is_win(1):
                        label = display_font.render("Minimax wins!", 1, BLUE)
                        screen.blit(label, (w/4, 10))
                        self.game_over = True
                        self.write_tic_tac_toe_board(screen,1)
                        win_number = 1
                        return win_number,exec_time
                    self.write_tic_tac_toe_board(screen,1)
                    self.turn = 1 - self.turn

                display.update()
                if self.turn == 0:
                    pass

                else:
                    col = default_opponent_move(self)
                    if self.is_move_correct(col):
                        row = self.is_row_free(col)
                        self.play_the_move(row, col, 2)

                        if self.is_win(2):
                            display_font = font.Font('freesansbold.ttf',25)
                            label = display_font.render(
                                "Default Opponent Wins!", 1, GREY)
                            screen.blit(label, (w/4, 10))
                            self.game_over = True
                            self.write_tic_tac_toe_board(screen,1)
                            win_number = 2
                            return win_number,exec_time

                    self.write_tic_tac_toe_board(screen,1)
                    self.turn = 1 - self.turn
                
                if self.check_game_draw():
                    label = display_font.render("Game Draw", 1, BLACK)
                    screen.blit(label, (w/4, 10))
                    self.game_over = True
                    self.write_tic_tac_toe_board(screen,1)
                    win_number = 3
                    return win_number,exec_time

        pygame_time.wait(2000)


    def grids_into_string(self):
        s = ''

        for row in range(self.rows):
            for col in range(self.cols):
                s += str(int(self.board[row][col]))

        return s

    def string_to_grids(self, board_string):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = float(board_string[self.cols*row+col])

    def q_learning_algorithm(self, qdict, eps_0):
        ALPHA_VALUE = 0.5
        GAMMA_VALUE = 0.9
        while not self.game_over:
            hasExplored = False
            if not self.turn:
                col = get_best_move(self)
                row = self.is_row_free(col)
                self.play_the_move(row, col, 1)
                if self.is_win(1):
                    self.game_over = True
                    self.winner = 0
                self.turn = 1
            else:
                state = self.grids_into_string()
                coups = get_moves(self)
                minimax_moves = get_q_childs(self)[1]

                max_q_value = NINF
                chosen_column = 0

                try:
                    qdict[state]
                except:
                    qdict[state] = [0]*self.cols

                Q_list = deepcopy(qdict[state])
                eps = random.uniform(0, 1)

                if eps < eps_0:
                    hasExplored = True
                    chosen_column = choice(list(coups))
                else:
                    for col in range(self.cols):
                        if col not in coups:
                            Q_list[col] = NINF
                    chosen_column = Q_list.index(max(Q_list))

                previous_q_value = (1-ALPHA_VALUE)*Q_list[chosen_column]

                row = self.is_row_free(chosen_column)
                self.play_the_move(row, chosen_column, 2)
                self.turn = 0

                if self.is_win(2):
                    qdict[state][chosen_column] = 1
                    self.winner = 1
                    self.game_over = True
                elif not minimax_moves:
                    self.game_over = True
                    reward = 1/42
                    if not hasExplored:
                        update_value = previous_q_value + ALPHA_VALUE*reward
                        qdict[state][chosen_column] = float(
                            f'{update_value:.5f}')
                else:
                    move = minimax_moves[str(chosen_column)]
                    row = self.is_row_free(move)
                    self.play_the_move(row, move, 1)
                    self.turn = 1
                    if self.is_win(1):
                        qdict[state][chosen_column] = -1
                        self.winner = 0
                        self.game_over = True
                    else:
                        try:
                            max_q_value = max(
                                [qdict[self.grids_into_string()][col] for col in get_moves(self)])
                        except:
                            qdict[state] = [0]*self.cols
                            max_q_value = 0
                        reward = 1/42
                        if not hasExplored:
                            update_value = previous_q_value + ALPHA_VALUE*reward + ALPHA_VALUE*GAMMA_VALUE*max_q_value
                            qdict[state][chosen_column] = float(
                                f'{update_value:.5f}')

    def play_qlearn_vs_default(self, qdict):
        pygame_init()
        win_number = 0
        exec_time = 0
        w = self.cols * SQUARESIZE
        h = (self.rows+1) * SQUARESIZE
        dimension = (w, h)

        screen = display.set_mode(dimension)
        self.write_tic_tac_toe_board(screen, 2)
        display.update()

        displayFont = font.Font('freesansbold.ttf',25)

        while not self.game_over:
            for event in pygame_event.get():
                if event.type == QUIT:
                    sys_exit()
                draw.rect(screen, WHITE, (0, 0, w, SQUARESIZE))

                if self.turn == 1:
                    state = self.grids_into_string()
                    start = time.time()
                    try:
                        score = qdict[state]
                        col = score.index(max(score))
                    except:
                        col = choice(list(get_moves(self)))
                    end = time.time()
                    exec_time = exec_time+(end-start)
                    row = self.is_row_free(col)
                    self.play_the_move(row, col, 2)

                    if self.is_win(2):
                        label = displayFont.render("Q-Agent wins!", 1, GREEN)
                        screen.blit(label, (w/4, 10))
                        self.game_over = True
                        self.write_tic_tac_toe_board(screen, 2)
                        win_number = 1
                        return win_number, exec_time
                    self.write_tic_tac_toe_board(screen, 2)
                    self.turn = 1 - self.turn
                display.update()
                if self.turn:
                    pass

                else:
                    col = default_opponent_move(self)
                    if self.is_move_correct(col):
                        row = self.is_row_free(col)
                        self.play_the_move(row, col, 1)

                        if self.is_win(1):
                            displayFont = font.Font('freesansbold.ttf',25)
                            label = displayFont.render(
                                "Default Player Wins!", 1, GREY)
                            screen.blit(label, (w/4, 10))
                            self.game_over = True
                            self.write_tic_tac_toe_board(screen, 2)
                            win_number = 2
                            return win_number, exec_time

                    self.write_tic_tac_toe_board(screen, 2)
                    self.turn = 1 - self.turn
                if self.check_game_draw():
                    label = displayFont.render("Game Draw", 1, BLACK)
                    screen.blit(label, (w/4, 10))
                    self.game_over = True
                    self.write_tic_tac_toe_board(screen,1)
                    win_number = 3
                    return win_number, exec_time

        pygame_time.wait(2000)

    def play_qlearn_vs_minimax(self, qdict):

        pygame_init()
        win_number = 0
        time_exec_minimax= 0
        time_exec_qlearning = 0
        w = self.cols * SQUARESIZE
        h = (self.rows+1) * SQUARESIZE
        size = (w, h)

        screen = display.set_mode(size)
        self.write_tic_tac_toe_board(screen, 3)
        display.update()

        displayFont = font.Font('freesansbold.ttf',50)

        while not self.game_over:
            for event in pygame_event.get():
                if event.type == QUIT:
                    sys_exit()
                draw.rect(screen, WHITE, (0, 0, w, SQUARESIZE))
                if self.turn == 0:
                    start_m = time.time()
                    col = get_best_move(self)
                    end_m = time.time()
                    time_exec_minimax = time_exec_minimax + (end_m-start_m)
                    row = self.is_row_free(col)
                    self.play_the_move(row, col, 1)

                    if self.is_win(1):
                        label = displayFont.render("Minimax wins!", 1, BLUE)
                        screen.blit(label, (w/4, 10))
                        self.game_over = True
                        self.write_tic_tac_toe_board(screen, 3)
                        win_number = 1
                        return win_number, time_exec_minimax, time_exec_qlearning

                    self.write_tic_tac_toe_board(screen, 3)
                    self.turn = 1 - self.turn

                display.update()
                if self.turn == 0:
                    pass

                else:
                    if self.turn == 1:
                        state = self.grids_into_string()
                    start_c = time.time()
                    try:
                        score = qdict[state]
                        col = score.index(max(score))
                    except:
                        col = choice(list(get_moves(self)))
                    end_c = time.time()
                    time_exec_qlearning  = time_exec_qlearning + (end_c-start_c)
                    if self.is_move_correct(col):
                        row = self.is_row_free(col)
                        self.play_the_move(row, col, 2)

                        if self.is_win(2):
                            label = displayFont.render(
                                "Q-Learning Wins!", 1, GREEN)
                            screen.blit(label, (w/4, 10))
                            self.game_over = True
                            self.write_tic_tac_toe_board(screen, 3)
                            win_number = 2
                            return win_number, time_exec_minimax, time_exec_qlearning

                    self.write_tic_tac_toe_board(screen, 3)
                    self.turn = 1 - self.turn
            

                if self.check_game_draw():
                    label = displayFont.render("Game Draw", 1, BLACK)
                    screen.blit(label, (w/4, 10))
                    self.game_over = True
                    self.write_tic_tac_toe_board(screen, 3)
                    win_number = 3
                    return win_number, time_exec_minimax, time_exec_qlearning
            

        pygame_time.wait(2000)
