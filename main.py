"""
sound resouces:
https://pixabay.com/users/floraphonic-38928062/
"""

import pygame
from pygame.color import Color
from random import randint
import sys

class Visualizer:
  SCREEN_WIDTH  = 560
  SCREEN_HEIGHT = 560
  FPS = 60
  CELL_SIZE = 20
  GRID_ROWS = SCREEN_HEIGHT // CELL_SIZE
  GRID_COLS = SCREEN_WIDTH // CELL_SIZE

  def __init__(self):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)

    self.screen        = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    self.sound         = pygame.mixer.Sound('./sound.mp3')
    self.clock         = pygame.time.Clock()
    self.screen_grid   = [ [(255, 255, 255) for y in range(self.SCREEN_HEIGHT)] for x in range(self.SCREEN_WIDTH) ]
    self.current_color = (0, 0, 255)
    self.grid_iterator = None

  def draw_grid(self):
    for row in range(self.GRID_ROWS):
      for col in range(self.GRID_COLS):
        pygame.draw.rect(
          self.screen, 
          self.screen_grid[row][col],
          (row * self.CELL_SIZE, col * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 
          1, 10
        )

  def clear_grid(self):
    self.screen_grid   = [ [(255, 255, 255) for y in range(self.SCREEN_HEIGHT)] for x in range(self.SCREEN_WIDTH) ]
    self.grid_iterator = None

  def get_gridpos(self, pos):
    col, row = pos[0] // self.CELL_SIZE, pos[1] // self.CELL_SIZE
    if (col >= self.GRID_COLS or row >= self.GRID_ROWS):
      return None, None
    return col, row

  def put_color(self, pos, color):
    col, row = pos[0] // self.CELL_SIZE, pos[1] // self.CELL_SIZE
    if (col >= self.GRID_COLS or row >= self.GRID_ROWS):
      return 
    self.screen_grid[col][row] = color


  def floodfill(self, start_pos):
    old_color = self.screen_grid[start_pos[0]][start_pos[1]]
    stack = [start_pos]
    while len(stack) > 0:
      x, y = stack.pop(0)
      if self.screen_grid[x][y] != old_color:
        continue
      self.screen_grid[x][y] = self.current_color
      self.sound.play()
      if x > 0:
        stack.append((x-1, y))
      if x < self.GRID_COLS - 1:
        stack.append((x+1, y))
      if y > 0:
        stack.append((x, y-1))
      if y < self.GRID_ROWS - 1:
        stack.append((x, y+1))
      yield self.screen_grid.copy()


  def run(self):
    while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
              self.current_color = ( randint(0, 255), randint(0, 255), randint(0, 255) )     
            elif event.key == pygame.K_f:
              position = self.get_gridpos(pygame.mouse.get_pos())
              self.grid_iterator = self.floodfill(position)
            elif event.key == pygame.K_c:
              self.clear_grid()

      mouse = pygame.mouse
      if mouse.get_pressed()[0]:
        self.put_color(mouse.get_pos(), self.current_color)
      elif mouse.get_pressed()[2]:
        self.put_color(mouse.get_pos(), (255, 255, 255))

      if self.grid_iterator is not None:
        try:
          self.screen_grid = next(self.grid_iterator)
        except StopIteration:
          pass


      self.draw_grid()

      pygame.display.update()
      self.clock.tick(self.FPS) 
   


if __name__ == "__main__":
  app = Visualizer()
  app.run()

