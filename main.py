import pygame
from sys import exit
import math
from queue import PriorityQueue

pygame.init()

WIDTH = 800
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Rat in a maze")
clock = pygame.time.Clock()

#color variables
RED = (85,107,47)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQ = (64,224,208)

#class for drawing all the squares, coloring them
class Squares():
  def __init__(self, row, col, width, total_rows):
    self.row = row
    self.col = col
    self.width = width
    self.total_rows = total_rows
    self.x = row*width
    self.y = col*width
    self.color = WHITE
    self.neighbours = []
  
  def get_pos(self):
    return self.row, self.col

  # @classmethod
  def get_coor(self):
    return (self.x, self.y)

  def is_closed(self):
    return self.color == RED

  def is_open(self):
    return self.color == GREEN

  def is_barrier(self):
    return self.color == BLACK

  def is_start(self):
    return self.color == ORANGE
  
  def is_end(self):
    return self.color == TURQ

  def is_path(self):
    return self.color == PURPLE

  def reset(self):
    self.color = WHITE

  def make_closed(self):
    self.color = RED

  def make_open(self):
    self.color = GREEN

  def make_barrier(self):
    self.color = BLACK

  def make_start(self):
    self.color = ORANGE

  def make_end(self):
    self.color = TURQ 

  def make_path(self):
    self.color = PURPLE

  def draw(self, win):
    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
  
  def update_neigh(self, grid):
    #there will be 4 neighbours of any square given no neigh is a barrier, and we add those neigs to the list
    #down neigh
    if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
      self.neighbours.append(grid[self.row+1][self.col])
    #up neigh
    if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
      self.neighbours.append(grid[self.row-1][self.col])
    #left neigh
    if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
      self.neighbours.append(grid[self.row][self.col-1])
    #right neigh
    if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
      self.neighbours.append(grid[self.row][self.col+1])    

  def __lt__(self, other):
    return False

#H(n) function, cant go diagonally here since we have square
#blocks, we used manhattan dist which goes through strict
#90 degree turns to find dist
def H(p1,p2):
  x1,y1 = p1  #where p1, p2 are tuples
  x2,y2 = p2

  return abs(x1-x2) + abs(y1-y2)

def get_path(came_from, current, draw):
  #keep in mind that the came_from dict has both the key and value as a Square Object type so
  while current in came_from:
    current = came_from[current]
    current.make_path() # colors it
    draw()

#the A* path finding algo here
def algorithm(draw_, grid, start_sq, end_sq):
  count = 0
  open_set = PriorityQueue()
  open_set.put((0, count, start_sq))

  came_from = {}  # gives all the nodes from where we traced our path, stored as dict, neigh node: current node
  
  g_score = {sq: float("inf") for row in grid for sq in row}  # a dict of all the sq objects and their G(n) score
  g_score[start_sq] = 0  # setting the G(n) value for n=start_node be 0 

  f_score = {sq: float("inf") for row in grid for sq in row} # a dict of all the sq objects and their F(n) score
  f_score[start_sq] = H(start_sq.get_pos(), end_sq.get_pos())  #since F(n) = G(n) + H(n), and G(n) for start node is 0, F(start) = H(start)

  open_set_nodes = {start_sq} 


  while not open_set.empty():
    current = open_set.get()[2] # gets the node(sq) object
    open_set_nodes.remove(current)

    if current != start_sq:
      current.make_closed() # makes it red
      if current == end_sq:
        end_sq.make_path()

    if current == end_sq:
      get_path(came_from, end_sq, draw_)
      end_sq.make_end()
      return True

    for neigh in current.neighbours:
      temp_g_score = g_score[current] + 1 #assuming all edges have a value of 1

      if temp_g_score < g_score[neigh]:
        came_from[neigh] = current # adding key:value pairs to the came_from dict
        g_score[neigh] = temp_g_score
        f_score[neigh] = temp_g_score + H(start_sq.get_pos(), end_sq.get_pos())
        if neigh not in open_set_nodes:
          count += 1
          open_set.put((f_score[neigh], count, neigh))
          open_set_nodes.add(neigh)  # where open_set_nodes is a set 
          neigh.make_open()  #turning that green

    draw_()


#representation of the grid which is drawn to the screen
def make_grid(rows, width):  #width is the net width of the screen
  grid = []
  gap = width // rows
  for i in range(rows):
    grid.append([])
    for j in range(rows):
      sq = Squares(i,j,gap,rows)
      grid[i].append(sq)

  return grid

#drawing the grids
def draw_grid(win, rows, width):
  gap = width//rows
  for i in range(rows):
    pygame.draw.line(win, GREY,  (0,i*gap), (width,i*gap))
    for j in range(rows):
      pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
  win.fill(WHITE)

  for row in grid:
    for sq in row:
      sq.draw(win)  #since each elements in a list within
      #a grid list is a Square obj

  draw_grid(win, rows, width)
  pygame.display.update()

  #this method hence involves us calling draw() method of the
  #Square class to draw to these squares,and also drawing the
  #grid lines by calling the draw_grid method

def get_clicked_pos(pos, rows, width):
  gap = width //rows
  y,x = pos

  row = y//gap
  col = x//gap

  return row, col
  

#font
test_font = pygame.font.Font('font\Pixeltype.ttf', 50)

#for 'Rat in a maze' title at start page
starting_text_surface = test_font.render('Rat in a maze', False, 'Black')
starting_text_rect = starting_text_surface.get_rect(center = (400, 50))

#for start title button
starting_text_surface_1 = test_font.render('START', False, 'Yellow')
starting_text_rect_1 = starting_text_surface_1.get_rect(center = (400, 200))

#for restart title button
restart_text_surface = test_font.render('GO TO HOME SCREEN', False, 'Black')
restart_text_rect = restart_text_surface.get_rect(center = (400, 200))

#for 'go to stats page' button
stats_surface = test_font.render('GO TO STATS PAGE', False, 'Black')
stats_rect = stats_surface.get_rect(center=(500, 700))

#rat
rat_ = pygame.image.load('snail.png')
rat = pygame.transform.scale(rat_, (30,15))

#instructions
inst = test_font.render('Select the start and end points', False,'Black')
inst_rect = inst.get_rect(center=(400,400))
inst1 = test_font.render('draw the walls', False,'Black')
inst_rect1 = inst1.get_rect(center=(400,440))
inst2 = test_font.render('hit the space bar for the rat to solve the maze', False,'Black')
inst_rect2 = inst2.get_rect(center=(400,480))

# hit the spcace bar for the rat to solve the maze


def main(win, width):
  #game variables
  game_active = True  #corresponds to the actual game screen
  start = True   #corresponds to the start window
  algo_started = False #shows if the algo has started

  ROWS = 30
  grid = make_grid(ROWS, width)

  start_sq = None
  end_sq = None

  #event loop
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

      if start:
        if event.type == pygame.MOUSEBUTTONDOWN and starting_text_rect_1.collidepoint(event.pos):  # for click action
          start = False
          algo_started = True

      elif game_active and start == False:  #main screen

        if pygame.mouse.get_pressed()[0]:
          pos = pygame.mouse.get_pos()
          row,col = get_clicked_pos(pos, ROWS, width)
          sq = grid[row][col]  #assigning Square obj of a certain sq in the grid to sq variable

          if not start_sq and sq != end_sq:
            start_sq = sq
            start_sq.make_start()
            
            rat_rect = rat.get_rect(topleft=start_sq.get_coor())

          elif not end_sq and sq != start_sq:
            end_sq = sq
            end_sq.make_end()

          elif sq != start_sq and sq != end_sq:
            sq.make_barrier()

        elif pygame.mouse.get_pressed()[2]:
          pos = pygame.mouse.get_pos()
          row,col = get_clicked_pos(pos, ROWS, width)
          sq = grid[row][col]
          sq.reset()

          if sq == start_sq:
            start_sq = None
          elif sq == end_sq:
            end_sq = None      
        
        #here the A* algorithm is called
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE and start_sq and end_sq:
            for row in grid:
              for sq in row:
                sq.update_neigh(grid)

            algorithm(lambda: draw(win, grid, ROWS, width), grid, start_sq, end_sq)  # calling the A* algorithm          
            algo_started = False

      if event.type == pygame.MOUSEBUTTONDOWN and stats_rect.collidepoint(event.pos):
        game_active = False  # for restarting once the algo is done runnning

        
      #restart case
      if game_active != True and algo_started == False:
        if event.type == pygame.MOUSEBUTTONDOWN and restart_text_rect.collidepoint(event.pos):
          #creating a blank slate once restart button is hit
          start_sq = None
          end_sq = None
          grid = make_grid(ROWS, width)
          game_active = True
          start = True
          start_time = pygame.time.get_ticks()/1000

    #main code window
    if game_active and start == False:
      if algo_started:
        draw(win, grid, ROWS, width)
        try:
          win.blit(rat,rat_rect)
        except UnboundLocalError:
          pass      
        try:
          t = (pygame.time.get_ticks()/1000) - start_time
        except UnboundLocalError:
          t = pygame.time.get_ticks()/1000

      else:
        screen.blit(stats_surface, stats_rect)  #go to stats page button


    #restart window
    if game_active == False and start == False:
      screen.fill('Yellow')
      screen.blit(restart_text_surface, restart_text_rect)
      time_surf = test_font.render(f"{t} s taken by rat to solve the maze", False, (64,64,64))
      time_rect = time_surf.get_rect(center=(400,400))
      screen.blit(time_surf,time_rect)
      
    #start window
    if start == True:
      screen.fill((94, 129, 162))
      screen.blit(starting_text_surface, starting_text_rect)
      screen.blit(starting_text_surface_1, starting_text_rect_1)
      screen.blit(inst,inst_rect)
      screen.blit(inst1, inst_rect1)
      screen.blit(inst2, inst_rect2)      

    
    pygame.display.update()
    clock.tick(60)


if __name__ == "__main__":
  main(screen, WIDTH)