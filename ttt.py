import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import algorithms
import operator
from training import train_as_X, train_as_O
import sys

def evaluate_win_status(game_board):
    for x in range(3):
        if game_board[x, 0] == game_board[x, 1] == game_board[x, 2] != 0:
            return game_board[x, 0]  # -
        elif game_board[0, x] == game_board[1, x] == game_board[2, x] != 0:
            return game_board[0, x]  # |
        elif game_board[0, 0] == game_board[1, 1] == game_board[2, 2] != 0:
            return game_board[0, 0]  # \
        elif game_board[0, 2] == game_board[1, 1] == game_board[2, 0] != 0:
            return game_board[0, 2]  # /
    if np.count_nonzero(game_board) < 9:
        return 0  # Not Finished
    return 3  # Draw


def initialize_game(player_x, player_o, multi_algorithm=True):

    total_time_x = 0
    total_time_o = 0

    grids = np.zeros((3, 3), int)  
    player_turn = 2  

    while evaluate_win_status(grids) == 0:
        if player_turn == 2:
            action, time_elapsed_x = player_x.move_with_time(grids, player_turn)
            total_time_x = total_time_x + time_elapsed_x
            grids[action[0], action[1]] = 2
            player_turn = 1

        else:
            if multi_algorithm:
                action, time_elapsed_o = player_o.move_with_time(grids, player_turn)
                total_time_o = total_time_o + time_elapsed_o
            else:
                action = player_o.get_move(grids, player_turn)
            grids[action[0], action[1]] = 1
            player_turn = 2
            algorithms.GUIInteract().gui_show_status(grids)
            time.sleep(0.3)

    evaluate_final_score = algorithms.score_eval(grids, 2)
    algorithms.GUIInteract().gui_final_state(grids, evaluate_final_score)
    time.sleep(1)
    if multi_algorithm:
        return (
            evaluate_final_score,
            total_time_x,
            total_time_o,
        ) 
    else:
        return evaluate_final_score, total_time_x

def minimax_vs_default(totalgames):

  X_player = algorithms.Minimax()
  O_player = algorithms.DefaultOpponent()
  results_s = []
  final_time_x = 0
  for i in range(totalgames):
      res, elapsed_time_x = initialize_game(X_player, O_player, False)
      results_s.append(res)
      final_time_x = final_time_x + elapsed_time_x

  win_count = operator.countOf(results_s, 1)
  loss_count = operator.countOf(results_s, -1)
  draw_count = operator.countOf(results_s, 0)

  print("Total Games", totalgames)
  print("Wins : ", win_count)
  print("Losses : ", loss_count)
  print("Draws : ", draw_count)
  print("Average time to complete Moves in 1 game (Minimax) : ", (final_time_x / 100) * 1000)
  sys.exit(0)

def qlearning_vs_default(totalgames, qlearning_training_no):

  Q = train_as_X(algorithms.Q_learning_algorithm(), algorithms.Random(), qlearning_training_no)

  X_player = algorithms.Q_learning_algorithm(Q,0)
  O_player = algorithms.DefaultOpponent()
  results_s = []
  final_time_x = 0
  for i in range(totalgames):
      res, elapsed_time_x = initialize_game(X_player, O_player, False)
      results_s.append(res)
      final_time_x = final_time_x + elapsed_time_x

  win_count = operator.countOf(results_s, 1)
  loss_count = operator.countOf(results_s, -1)
  draw_count = operator.countOf(results_s, 0)

  print("Total Games", totalgames)
  print("Wins : ", win_count)
  print("Losses : ", loss_count)
  print("Draws : ", draw_count)
  print("Average time to complete Moves in 1 game (Q - learn) : ", (final_time_x / 100) * 1000)
  sys.exit(0)

def minimax_vs_qlearning(totalgames, qlearning_training_no):

  Q = train_as_X(algorithms.Q_learning_algorithm(), algorithms.Random(), qlearning_training_no)

  X_player = algorithms.Q_learning_algorithm(Q,0)
  O_player = algorithms.Minimax()
  results_s = []
  final_time_m = 0
  final_time_c = 0
  for i in range(totalgames):
      res, elapsed_time_m, elapsed_time_c= initialize_game(X_player, O_player, True)
      results_s.append(res)
      final_time_m = final_time_m + elapsed_time_m
      final_time_c = final_time_c + elapsed_time_c

  win_count = operator.countOf(results_s, 1)
  loss_count = operator.countOf(results_s, -1)
  draw_count = operator.countOf(results_s, 0)

  print("Total Games", totalgames)
  print("Wins : ", win_count)
  print("Losses : ", loss_count)
  print("Draws : ", draw_count)
  print("Average time to complete Moves in 1 game (Minimax) : ", (final_time_m / 100) * 1000)
  print("Average time to complete Moves in 1 game (Q- learn) : ", (final_time_c / 100) * 1000)
  sys.exit(0)

def main():
  
  minimax_vs_default(5)
  qlearning_vs_default(5,10000)
  minimax_vs_qlearning(5,10000)
  

if __name__ == "__main__":

  main();




    