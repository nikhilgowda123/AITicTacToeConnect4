import pygame,sys
import time

pygame.init()
screen = pygame.display.set_mode((600,600))
screen_color = (255, 255, 255)

def board_pos(x,y,size=200):
  ''' Take coordinates (x,y) as parameters and return row and column '''
  for a in range(1,4):
    if x < size*a:
      col = a-1
      break
  for a in range(1,4):
    if y < size*a:
      row = a-1
      break
  return (row,col)

class gui:
  def __init__(self):
    self.display = pygame.display.set_mode((600, 640))  # increased height to make room for text
    self.color = (161, 184, 203)
    self.X_color = (0, 163, 255)
    self.O_color = (128,128,128)
    self.line_color = (204, 0, 0)
    self.size = 200
    self.font = pygame.font.SysFont('Arial', 40)  # create font object
    self.text = self.font.render('Tic Tac Toe', True, (0, 0, 0))  # render text as surface

  def draw_board(self, final_eval_score):
    screen.fill(screen_color)
    ''' Draw an empty 3x3 grid '''
    for row in range(3):
      for col in range(3):
        pygame.draw.rect(self.display, self.color, (row*self.size,col*self.size+self.font.get_height(),self.size,self.size),1)
    
    if(final_eval_score==0):
      self.text = self.font.render('Draw!', True, (0, 0, 0))
    if(final_eval_score==1):
      self.text = self.font.render('Win!', True, (0, 0, 0))
    if(final_eval_score==-1):
      self.text = self.font.render('Lose!', True, (0, 0, 0))
    self.display.blit(self.text, ((self.display.get_width() - self.text.get_width()) // 2, 0))  # blit text surface onto window surface
    pygame.display.update()


  def draw_xo(self,board, final_eval_score, from_draw_line=True):
    screen.fill(screen_color)
    self.draw_board(final_eval_score)
    ''' Draws the X's and O's from a given grid as a numpy matrix (array) '''
    for row in range(3):
      for col in range(3):
        x_center = int(col*self.size + self.size/2)
        y_center = int(row*self.size+self.font.get_height() + self.size/2)
        if board[row,col] == 1:      # O
          pygame.draw.circle(self.display,self.O_color,(x_center,y_center),70,5) #Draw a circle in the center of the box
        elif board[row,col] == 2:    # X
          pygame.draw.line(self.display,self.X_color,(x_center-75,y_center-75),(x_center+75,y_center+75),5) # Draw 2 lines for
          pygame.draw.line(self.display,self.X_color,(x_center-75,y_center+75),(x_center+75,y_center-75),5) # form an X
    if from_draw_line:
      pygame.display.update()

  def draw_line(self, board, final_eval_score):
    self.draw_xo(board, final_eval_score, False)
    ''' draw a line if 3 squares follow each other '''
    for x in range(3):
      if board[x,0] == board[x,1] == board[x,2] != 0: # -
        start_pos = (int(self.size/2), int((x+0.5)*self.size+self.font.get_height()))
        end_pos = (int(2.5*self.size), int((x+0.5)*self.size+self.font.get_height()))
        pygame.draw.line(self.display,self.line_color,start_pos,end_pos,10)

      if board[0,x] == board[1,x] == board[2,x] != 0: # |
        start_pos = (int((x+0.5)*self.size), int(self.size/2+self.font.get_height()))
        end_pos = (int((x+0.5)*self.size), int(2.5*self.size+self.font.get_height()))
        pygame.draw.line(self.display,self.line_color,start_pos,end_pos,10)

      if board[0,0] == board[1,1] == board[2,2] != 0: # \
        start_pos = (int(self.size/2), int(self.size/2+self.font.get_height()))
        end_pos = (int(2.5*self.size), int(2.5*self.size+self.font.get_height()))
        pygame.draw.line(self.display,self.line_color,start_pos,end_pos,10)

      if board[0,2] == board[1,1] == board[2,0] != 0: # /
        start_pos = (int(2.5*self.size), int(self.size/2+self.font.get_height()))
        end_pos = (int(self.size/2), int(2.5*self.size+self.font.get_height()))
        pygame.draw.line(self.display,self.line_color,start_pos,end_pos,10)

    pygame.display.update()

  def show_status(self, board):
    screen.fill(screen_color)
    ''' Show the current status of the board '''
    for row in range(3):
      for col in range(3):
        pygame.draw.rect(self.display, self.color, (row*self.size,col*self.size+self.font.get_height(),self.size,self.size),1)
        x_center = int(col*self.size + self.size/2)
        y_center = int(row*self.size+self.font.get_height() + self.size/2)
        if board[row,col] == 1:      # O
          pygame.draw.circle(self.display,self.O_color,(x_center,y_center),75,5) #Draw a circle in the center of the box
        elif board[row,col] == 2:    # X
          pygame.draw.line(self.display,self.X_color,(x_center-75,y_center-75),(x_center+75,y_center+75),5) # Draw 2 lines for
          pygame.draw.line(self.display,self.X_color,(x_center-75,y_center+75),(x_center+75,y_center-75),5) # form an X
    self.display.blit(self.text, ((self.display.get_width() - self.text.get_width()) // 2, 0))  # blit text surface onto window surface
    pygame.display.update()

  def play(self):
    screen.fill(screen_color)
    ''' Take mouse clicks into account '''
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is pressed
            (x,y) = pygame.mouse.get_pos()
            return board_pos(x,y,self.size)
  time.sleep(0.05)
            

