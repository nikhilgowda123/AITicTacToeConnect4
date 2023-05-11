import numpy as np 
import pandas as pd
from tqdm import tqdm

import matplotlib.pyplot as plt 

import algorithms
from algorithms import win_eval

def train_as_X(X_player,O_player,episodes,plot=False):
  t = tqdm(desc='Training Q-Learning Algorithm! for '+str(episodes)+' Games. PLEASE WAIT!!')

  results = []
  for episode in range(episodes):
    board = np.zeros((3,3),int)   

    while win_eval(board) == 0:   
      move = X_player.get_move(board,2)

      S = np.copy(board)     
      A = move

      board[move[0],move[1]] = 2
      
      if win_eval(board) != 0:
        reward = algorithms.score_eval(board,2)
        prev = X_player.q_storage(S,X_player.shape_it(A))
        X_player.q_table[(X_player.conceal(S),X_player.shape_it(A))] = prev + X_player.alpha * (reward + X_player.gamma*reward - prev)
        break

      move = O_player.get_move(board,1)
      board[move[0],move[1]] = 1

      S1 = np.copy(board)

      X_player.epsilon = 0   
      A1 = X_player.get_move(board,2)
      X_player.epsilon = 0.2 if episode <0.95*episodes else 0

      reward = algorithms.score_eval(board,2)
      X_player.learn(S,A,S1,A1,reward)
    
    results.append([episode,algorithms.score_eval(board,2)]) 

    t.update(1)
  t.close()
  
  win = []
  lose = []
  draw = []

  for el in results:
    if el[1] == 1:
      win.append([el[0],1])
      lose.append([el[0],0])
      draw.append([el[0],0])
    elif el[1] == -1:
      win.append([el[0],0])
      lose.append([el[0],1])
      draw.append([el[0],0])
    elif el[1] == 0:
      win.append([el[0],0])
      lose.append([el[0],0])
      draw.append([el[0],1])


  if plot:
    df = pd.DataFrame(results,columns=['Episode','Result'])
    dfwin = pd.DataFrame(win,columns=['Episode','Result'])
    dflose = pd.DataFrame(lose,columns=['Episode','Result'])
    dfdraw = pd.DataFrame(draw,columns=['Episode','Result'])

    import pickle
    pickle.dump([df,dfwin,dflose,dfdraw], open("train_stats.pkl","wb"))
    span = int(0.05*episodes)

    smaw = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smal = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smad = dfwin.rolling(window=span, min_periods=span).mean()[:span]

    restw = dfwin[span:]
    restl = dflose[span:]
    restd = dfdraw[span:]

    win = pd.concat([smaw, restw]).ewm(span=span, adjust=False).mean()
    lose = pd.concat([smal, restl]).ewm(span=span, adjust=False).mean()
    draw = pd.concat([smad, restd]).ewm(span=span, adjust=False).mean()

    plt.plot(win.Episode,win.Result, label='Win')
    plt.plot(lose.Episode,lose.Result, label='Loss')
    plt.plot(draw.Episode,draw.Result, label='Draw')
    plt.legend()
    plt.xlabel('Episode')
    plt.ylabel('Result')
    plt.ylim(0,1)
    plt.show()

  return(X_player.q_table)      

def train_as_O(X_player,O_player,episodes,plot=False):
  t = tqdm(desc='Training Q-Learning Algorithm! for '+str(episodes)+' Games. PLEASE WAIT!!')

  results = []
  for episode in range(episodes):
    board = np.zeros((3,3),int)   

    move = X_player.get_move(board,2)

    while win_eval(board) == 0:   
      move = O_player.get_move(board,1)

      S = np.copy(board)     
      A = move

      board[move[0],move[1]] = 1
      
      if win_eval(board) != 0:
        reward = algorithms.score_eval(board,1)
        prev = O_player.q(S,O_player.format(A))
        O_player.q_table[(O_player.encode(S),O_player.format(A))] = prev + O_player.alpha * (reward + O_player.gamma*reward - prev)
        break

      move = X_player.get_move(board,2)
      board[move[0],move[1]] = 2

      S1 = np.copy(board)

      O_player.epsilon = 0  
      A1 = O_player.get_move(board,1)
      O_player.epsilon = 0.2 if episode < 0.95*episodes else 0

      reward = algorithms.score_eval(board,1)
      O_player.learn(S,A,S1,A1,reward)
    
    results.append([episode,algorithms.score_eval(board,1)])  
    t.update(1)
  t.close()
  
  win = []
  lose = []
  draw = []

  for el in results:
    if el[1] == 1:
      win.append([el[0],1])
      lose.append([el[0],0])
      draw.append([el[0],0])
    elif el[1] == -1:
      win.append([el[0],0])
      lose.append([el[0],1])
      draw.append([el[0],0])
    elif el[1] == 0:
      win.append([el[0],0])
      lose.append([el[0],0])
      draw.append([el[0],1])


  if plot:
    df = pd.DataFrame(results,columns=['Episode','Result'])
    dfwin = pd.DataFrame(win,columns=['Episode','Result'])
    dflose = pd.DataFrame(lose,columns=['Episode','Result'])
    dfdraw = pd.DataFrame(draw,columns=['Episode','Result'])

    import pickle
    pickle.dump([df,dfwin,dflose,dfdraw], open("train_stats.pkl","wb"))
    span = int(0.05*episodes)

    smaw = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smal = dfwin.rolling(window=span, min_periods=span).mean()[:span]
    smad = dfwin.rolling(window=span, min_periods=span).mean()[:span]

    restw = dfwin[span:]
    restl = dflose[span:]
    restd = dfdraw[span:]

    win = pd.concat([smaw, restw]).ewm(span=span, adjust=False).mean()
    lose = pd.concat([smal, restl]).ewm(span=span, adjust=False).mean()
    draw = pd.concat([smad, restd]).ewm(span=span, adjust=False).mean()

    expw = dfwin.Result.ewm(span=span, adjust=False).mean()
    expl = dflose.Result.ewm(span=span, adjust=False).mean()    
    expd = dfdraw.Result.ewm(span=span, adjust=False).mean()

    plt.plot(lose.Episode,lose.Result, label='Win') 
    plt.plot(win.Episode,win.Result, label='Loss')
    plt.plot(draw.Episode,draw.Result, label='Draw')
    plt.legend()
    plt.xlabel('Episode')
    plt.ylabel('Result')
    plt.ylim(0,1)
    plt.show()

  return(O_player.q_table)   
