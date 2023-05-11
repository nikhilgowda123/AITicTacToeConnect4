from math import inf
import numpy as np
import time
import random


class GUIInteract:
    

    def __init__(self):
        import tic_tac_toe_gui  

        self.gui = (
            tic_tac_toe_gui.gui()
        )  

    def move(self, board, turn):  
        self.board = board
        self.update_screen()

        move = self.selection()

        self.board[move[0], move[1]] = turn
        self.update_screen()
        return move

    def update_screen(self):  
        self.gui.draw_board()
        self.gui.draw_xo(self.board)

    def selection(self):  
        return self.gui.play()

    def gui_final_state(self, board, final_eval_score):  
        self.gui.draw_line(board, final_eval_score)
        
        

    def gui_show_status(self, board):
        self.gui.show_status(board)


class DefaultOpponent:


    def get_move(self, board, turn):
        self.board = board
        winning_move = self.check_winning_move(turn)
        if winning_move is not None:
            return winning_move
        blocking_move = self.check_blocking_move(turn)
        if blocking_move is not None:
            return blocking_move
        possible_moves = np.argwhere(self.board == 0)
        move = np.random.permutation(possible_moves)[0]
        return tuple(move)

    def check_winning_move(self, turn):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    self.board[row][col] = turn
                    if win_eval(self.board) == turn:
                        self.board[row][col] = 0
                        return row, col
                    self.board[row][col] = 0
        return None

    def check_blocking_move(self, turn):
        antiturn = 2 if turn == 1 else 1
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    self.board[row][col] = antiturn
                    if win_eval(self.board) == antiturn:
                        self.board[row][col] = 0
                        return row, col
                    self.board[row][col] = 0
        return None


class Random:

    def get_move(self, board, turn):
        self.board = board
        possible_moves = np.argwhere(
            self.board == 0
        )  
        move = np.random.permutation(possible_moves)[
            0
        ]  

        return (move[0], move[1])  


def win_eval(board):  
    """Fonction qui évalue une grille et renvoie : 0 si la partie n'est pas finie, 1 si O gagne, 2 si X gagne ou 3 si match nul"""

    board = (
        np.array(board) if type(board) == list else board
    )  

    for x in range(3):
        if board[x, 0] == board[x, 1] == board[x, 2] != 0:
            return board[x, 0]  
        elif board[0, x] == board[1, x] == board[2, x] != 0:
            return board[0, x]  
        elif board[0, 0] == board[1, 1] == board[2, 2] != 0:
            return board[0, 0]  
        elif board[0, 2] == board[1, 1] == board[2, 0] != 0:
            return board[0, 2]  
    if np.count_nonzero(board) < 9:
        return 0  
    return 3  


def score_eval(board, turn):
    antiturn = 0
    if turn == 1:
        antiturn = 2
    elif turn == 2:
        antiturn = 1

    if win_eval(board) == antiturn: 
        score = -1
    elif win_eval(board) == turn: 
        score = 1
    else:
        score = 0
    return score


def minimax_alpha_beta(board, depth, turn, alpha, beta, maximizing_player=True):
    if depth == 0 or win_eval(board) != 0:
        return score_eval(board, turn)
    
    if maximizing_player:
        max_score = -inf
        for move in np.argwhere(board == 0):
            board[move[0], move[1]] = turn
            score = minimax_alpha_beta(board, depth-1, turn, alpha, beta, False)
            board[move[0], move[1]] = 0
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score
    else:
        min_score = inf
        for move in np.argwhere(board == 0):
            board[move[0], move[1]] = 3 - turn
            score = minimax_alpha_beta(board, depth-1, turn, alpha, beta, True)
            board[move[0], move[1]] = 0
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score


def best_move(board, turn):

    best_score = -inf
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                board[row, col] = turn

                score = minimax_alpha_beta(
                    board, list(np.ravel(board)).count(0), turn, -float("inf"), float("inf"), False
                ) 

                board[row, col] = 0
                best_score = max(best_score, score)
                if best_score == score:
                    move = (row, col)
    return move

def best_move_with_time(board, turn):

    start = time.time()
    best_score = -inf
    for row in range(3):
        for col in range(3):
            if board[row, col] == 0:
                board[row, col] = turn

                score = minimax_alpha_beta(
                    board, list(np.ravel(board)).count(0), turn, -float("inf"), float("inf"), False
                ) 

                board[row, col] = 0
                best_score = max(best_score, score)
                if best_score == score:
                    move = (row, col)
    end = time.time()
    return move, (end-start)


class Minimax:

    def get_move(self, board, turn):
        return best_move(board, turn)
    
    def move_with_time(self, board, turn):
        return best_move_with_time(board, turn)


class Q_learning_algorithm:
  def __init__(self,Q={},epsilon=0.3, alpha=0.2, gamma=0.9):
    self.q_table = Q
    self.epsilon = epsilon    
    self.alpha = alpha         
    self.gamma = gamma         

  def conceal(self,state):      
    s = ''
    for row in range(3):
      for col in range(3):
        s += str(state[row,col])
    return s

  def interpret(self,s):          
    return np.array([[int(s[0]),int(s[1]),int(s[2])],[int(s[3]),int(s[4]),int(s[5])],[int(s[6]),int(s[7]),int(s[8])]])

  def shape_it(self,action):        
    if type(action) == int:
      return action
    else:
      return 3*action[0] + action[1]

  def probable_actions(self,board):
    ''' retourne tous les indices de valeur 0 '''
    return [i for i in range(9) if self.conceal(np.array(board))[i]=='0']

  def q_storage(self,state,action):
    action = self.shape_it(action)
    if (self.conceal(state),action) not in self.q_table:
      self.q_table[(self.conceal(state),action)] = 1    
    return self.q_table[(self.conceal(state),action)]

  def get_move(self,board,turn):
    self.board = board
    actions = self.probable_actions(board)
    
    if random.random() < self.epsilon:        
      self.last_move = random.choice(actions)
      self.last_move = (self.last_move//3,self.last_move%3) 
      return self.last_move
    
    q_values = [self.q_storage(self.board, a) for a in actions]
    
    if turn == 2:  
      max_q = max(q_values)
    else:          
      max_q = min(q_values)

    if q_values.count(max_q) > 1:       
      best_actions = [i for i in range(len(actions)) if q_values[i] == max_q]
      i = np.random.permutation(best_actions)[0]
    else:
      i = q_values.index(max_q)

    self.last_move = actions[i]
    self.last_move = (self.last_move//3,self.last_move%3)
    return self.last_move

  def move_with_time(self,grid,turn):
    start = time.time()
    self.board = grid
    actions = self.probable_actions(grid)
    
    if random.random() < self.epsilon:        
      self.last_move = random.choice(actions)
      self.last_move = (self.last_move//3,self.last_move%3) 
      return self.last_move
    
    q_values = [self.q_storage(self.board, a) for a in actions]
    
    if turn == 2:   
      max_q = max(q_values)
    else:           
      max_q = min(q_values)

    if q_values.count(max_q) > 1:      
      best_actions = [i for i in range(len(actions)) if q_values[i] == max_q]
      i = np.random.permutation(best_actions)[0]
    else:
      i = q_values.index(max_q)

    self.last_move = actions[i]
    self.last_move = (self.last_move//3,self.last_move%3)
    end = time.time()
    return self.last_move, (end-start)


  def learn(self, S, A, S1, A1, reward):
    A = self.shape_it(A)
    A1 = self.shape_it(A1)

    prev = self.q_storage(S, A)
    maxnewq = self.q_storage(S1, A1)

    S = self.conceal(S)
    S1 = self.conceal(S1)

    self.q_table[(S, A)] = prev + self.alpha * (
        reward + self.gamma * maxnewq - prev
    )
