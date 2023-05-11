from board import *
import operator
import ast
from pandas import read_csv
import sys

Q_learned_states = {}
table = read_csv('q_learned_states.csv')
for i in range(len(table['states'])):
    Q_learned_states[table['states'][i]] = ast.literal_eval(table['scores'][i])

def minimax_vs_default(totalgames):
    total_count = []
    total_time = 0
    for i in range(totalgames):
        game = gameConnect4()
        win_number, exec_time = game.play_minimax_vs_default()
        total_count.append(win_number)
        total_time = total_time+exec_time
        time.sleep(1)

    win_count = operator.countOf(total_count,1)
    loss_count = operator.countOf(total_count,2)
    draw_count = operator.countOf(total_count,3)


    print("Wins : ",win_count)
    print("Losses : ",loss_count)
    print("Draws : ",draw_count)
    print("Time ", (total_time/100)*1000)
    sys.exit(0)


def qlearning_vs_default(totalgames):

    total_count = []
    total_time = 0
    for i in range(totalgames):
        game = gameConnect4()
        win_number, exec_time = game.play_qlearn_vs_default(Q_learned_states)
        total_count.append(win_number)
        total_time = total_time+exec_time
        time.sleep(1)

    win_count = operator.countOf(total_count,1)
    loss_count = operator.countOf(total_count,2)
    draw_count = operator.countOf(total_count,3)


    print("Wins : ",win_count)
    print("Losses : ",loss_count)
    print("Draws : ",draw_count)
    print("Time ", (total_time/100)*1000)
    sys.exit(0)

def minimax_vs_qlearning(totalgames):
    total_count = []
    total_time_m = 0
    total_time_c = 0
    for i in range(totalgames):
        game = gameConnect4()
        win_number, exec_time_m, exec_time_c = game.play_qlearn_vs_minimax(Q_learned_states)
        total_count.append(win_number)
        total_time_m = total_time_m+exec_time_m
        total_time_c = total_time_c+exec_time_c
        time.sleep(1)

    win_count = operator.countOf(total_count,1)
    loss_count = operator.countOf(total_count,2)
    draw_count = operator.countOf(total_count,3)


    print("Wins : ",win_count)
    print("Losses : ",loss_count)
    print("Draws : ",draw_count)

    print("Time Minimax", (total_time_m/100)*1000)
    print("Time Q Learning", (total_time_c/100)*1000)
    sys.exit(0)


def main():
  
  minimax_vs_default(1)
  qlearning_vs_default(1)
  minimax_vs_qlearning(1)
  

if __name__ == "__main__":

  main();
