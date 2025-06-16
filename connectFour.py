import pygame
import threading

class connectFour:
  BLACK = (0,0,0)
  WHITE = (255, 255, 255)
  RED = (181, 36, 11) #1
  YELLOW = (201, 160, 24) #2
  playerColors = [RED, YELLOW]

  def __init__(self):
    pygame.init()

    self.active = True
    self.screenheight = 600
    self.screenwidth = 700
    self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
    self.fieldheight = 6
    self.fieldwidth = 7
    self.coinRadius = 45
    self.field = self.createField(self.fieldwidth, self.fieldheight)
    self.player = 1

    pygame.font.init()
    self.font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("connectFour")

  def createField(self, width, height):
    field = []
    for x in range(width):
      field.append([])
      for y in range(height):
        field[x].append(0)
    return(field)
  
  def start(self):
    self.loop()

  def loop(self):
    self.addCoin(0, 2)
    self.addCoin(0, 1)
    self.addCoin(1, 1)
    self.addCoin(1, 2)
    self.addCoin(1, 2)
    self.drawBackground()
    self.drawCoins()
    while True:
      pass
  
  def addCoin(self, row, player):
    y = self.fieldheight - 1
    while self.field[row][y] != 0:
      y -= 1
      if y <= 0: return False
    
    self.field[row][y] = player

  def drawBackground(self):
    self.screen.fill(self.WHITE)
    thickness = 4

    rectwidth = self.screenwidth / self.fieldwidth
    for x in range(1, self.fieldwidth):
      pygame.draw.line(self.screen, self.BLACK, (rectwidth * x, 0), (rectwidth * x, self.screenheight), thickness)

    rectheight = self.screenheight / self.fieldheight
    for y in range(1, self.fieldheight):
      pygame.draw.line(self.screen, self.BLACK, (0, rectheight * y), (self.screenwidth, rectheight * y), thickness)

    pygame.display.flip()

  def drawCoins(self):
    rectwidth = self.screenwidth / self.fieldwidth
    rectheight = self.screenheight / self.fieldheight
    for x in range(len(self.field)):
      for y in range(len(self.field[x])):
        if self.field[x][y] != 0:
          pygame.draw.circle(self.screen, self.playerColors[self.field[x][y] - 1], (rectwidth * x + rectwidth / 2, rectheight * y + rectwidth / 2), self.coinRadius)
    pygame.display.flip()

  def convertCoordinateToRow(self, pos):
    return int(pos / self.fieldwidth)

  


cf = connectFour()

def game_thread():
    cf.start()


gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
gameThread.start()

while cf.active:
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      pos = cf.convertCoordinateToRow(pos[0])
      cf.chooseRow(pos)
    if event.type == pygame.QUIT:
      cf.active = False