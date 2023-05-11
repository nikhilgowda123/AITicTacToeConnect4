import copy
import numpy as np
import matplotlib.pyplot as plt
from random import randint, choice, uniform
import math


def get_moves(gameConnect4):
    L = set()
    for col in range(gameConnect4.cols):
        if gameConnect4.is_move_correct(col):
            L.add(col)
    if not L:
        gameConnect4.game_over = True
    return L


def fixed(gameConnect4):
    S_State = 0
    signal = {1: 1, 2: -1}
    better_pos = [{'1110', '1101', '1011', '0111'},
                      {'2220', '2202', '2022', '0222'}]
    win_pos = ['1111', '2222']

    for circ in [1, 2]:

        for r in range(gameConnect4.rows):
            ROW = str(int(gameConnect4.board[r][0]))
            for c in range(1, gameConnect4.cols):
                ROW += str(int(gameConnect4.board[r][c]))
            for start_index in range(len(ROW) - 3):
                if ROW[start_index:start_index + 4] in better_pos[circ-1]:
                    S_State += signal[circ]*10
                if ROW[start_index:start_index + 4] in win_pos[circ-1]:
                    S_State += signal[circ]*1000
        for c in range(gameConnect4.cols):
            COL = str(int(gameConnect4.board[0][c]))
            for r in range(1, gameConnect4.rows):
                COL += str(int(gameConnect4.board[r][c]))
            for start_index in range(len(COL) - 3):
                if COL[start_index:start_index + 4] in better_pos[circ-1]:
                    S_State += signal[circ]*10
                if COL[start_index:start_index + 4] in win_pos[circ-1]:
                    S_State += signal[circ]*1000

        for c in range(gameConnect4.cols-3):
            for r in range(gameConnect4.rows-3):
                DIAG = str(int(gameConnect4.board[r][c]))
                for i in range(1, 4):
                    DIAG += str(int(gameConnect4.board[r+i][c+i]))
                for start_index in range(len(DIAG) - 3):
                    if DIAG[start_index:start_index + 4] in better_pos[circ-1]:
                        S_State += signal[circ]*10
                    if DIAG[start_index:start_index + 4] in win_pos[circ-1]:
                        S_State += signal[circ]*1000

        for c in range(gameConnect4.cols-3):
            for r in range(3, gameConnect4.rows):
                DIAG = str(int(gameConnect4.board[r][c]))
                for i in range(1, 4):
                    DIAG += str(int(gameConnect4.board[r-i][c+i]))
                for start_index in range(len(DIAG) - 3):
                    if DIAG[start_index:start_index + 4] in better_pos[circ-1]:
                        S_State += signal[circ]*10
                    if DIAG[start_index:start_index + 4] in win_pos[circ-1]:
                        S_State += signal[circ]*1000

    return S_State


def get_child(Connect4):
    dict_child = {}
    for col in get_moves(Connect4):
        child = copy.deepcopy(Connect4)
        row = child.is_row_free(col)
        children_circ = Connect4.turn + 1
        child.play_the_move(row, col, children_circ)
        child.turn = 1 - Connect4.turn
        if child.is_win(children_circ) or not get_moves(child):
            child.game_over = True
        dict_child[str(col)] = child
    if not dict_child and not Connect4.game_over:
        Connect4.game_over = True
    return dict_child


def get_q_childs(Connect4):

    dict_child = {}
    minimaxMoves = {}
    for col in get_moves(Connect4):
        child = copy.deepcopy(Connect4)
        row = child.is_row_free(col)
        children_circ = Connect4.turn + 1
        child.play_the_move(row, col, children_circ)
        child.turn = 1 - Connect4.turn
        if child.is_win(children_circ) or not get_moves(child):
            child.game_over = True
        else:
            col2 = get_best_move(child)
            minimaxMoves[str(col)] = col2
            row2 = child.is_row_free(col2)
            piece = child.turn + 1
            child.play_the_move(row2, col2, piece)
            child.turn = 1 - Connect4.turn
            if child.is_win(piece) or not get_moves(child):
                child.game_over = True

        dict_child[str(col)] = child
    if not dict_child and not Connect4.game_over:
        Connect4.game_over = True
    return dict_child, minimaxMoves


def minimax_algorithm(gameConnect4, depth, alpha, beta, maximizingPlayer=None):
    if maximizingPlayer == None:
        if not gameConnect4.turn:
            maximizingPlayer = True
        else:
            maximizingPlayer = False

    if not depth or gameConnect4.game_over:
        return fixed(gameConnect4)

    elif maximizingPlayer:
        maxEval = -float('inf')
        for Child in get_child(gameConnect4).values():
            eval = minimax_algorithm(Child, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval

    else:
        minEval = float('inf')
        for Child in get_child(gameConnect4).values():
            eval = minimax_algorithm(Child, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def default_opponent_move(gameConnect4):

    for col in range(gameConnect4.cols):
        if gameConnect4.is_move_correct(col):
            row = gameConnect4.is_row_free(col)
            gameConnect4.play_the_move(row, col, 1)
            if gameConnect4.is_win(1):
                gameConnect4.revert_the_move(row, col, 1)
                return col
            gameConnect4.revert_the_move(row, col, 1)

    for col in range(gameConnect4.cols):
        if gameConnect4.is_move_correct(col):
            row = gameConnect4.is_row_free(col)
            gameConnect4.play_the_move(row, col, 2)
            if gameConnect4.is_win(2):
                gameConnect4.revert_the_move(row, col, 2)
                return col
            gameConnect4.revert_the_move(row, col, 2)

    valid_moves = []
    for col in range(gameConnect4.cols):
        if gameConnect4.is_move_correct(col):
            valid_moves.append(col)
    return choice(valid_moves)

def is_nan_list(scores):
    for score in scores:
        if math.isnan(score):
            return True
            break
        else:
            return False

def get_best_move(gameConnect4):
    if not gameConnect4.game_over:
        all_moves = get_moves(gameConnect4)
        epsilon = uniform(0, 1)
        if epsilon < 0.2:
            return choice(list(all_moves))
        else:
            if not gameConnect4.turn:
                scores = [-float('inf')]*gameConnect4.cols
            else:
                scores = [float('inf')]*gameConnect4.cols

            childrens = get_child(gameConnect4)
            for can_play_move in childrens.keys():
                scores[int(can_play_move)] = minimax_algorithm(childrens[can_play_move], 3, -float('inf'),
                                                     float('inf'), not childrens[can_play_move].turn)

            move_scores = scores.index(max(scores))

            for column in range(gameConnect4.cols):
                if column not in all_moves:
                    scores[column] = float('nan')

            if gameConnect4.turn == 0:
                if abs(np.nanmean(scores)) != float('inf'):
                    if max(scores) == int(np.nanmean(scores)):
                        if not max(scores) and 3 in all_moves:
                            move = 3
                            return move
                        else:
                            move = choice(list(all_moves))
                            return move
                    else:
                        move = move_scores
                        return move
                else:
                    gameConnect4.display_board()
                    move = choice(list(all_moves))
                    return move
            else:
                move = scores.index(min(scores))
                return move
