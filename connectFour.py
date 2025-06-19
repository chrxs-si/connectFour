import pygame
import threading

class connectFour:
  BLACK = (0,0,0)
  WHITE = (255, 255, 255)
  RED = (181, 36, 11) #1
  YELLOW = (201, 160, 24) #2
  playerColors = [RED, YELLOW]
  currentPlayer = 1
  winner_lenght = 4

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
    self.drawBackground()
    self.drawCoins()
    while True:
      pass
  
  def addCoin(self, row, player):
    y = self.fieldheight - 1
    while self.field[row][y] != 0:
      y -= 1
      if y < 0: return False
    
    self.field[row][y] = player

  def drawBackground(self):
    self.screen.fill(self.BLACK)
    thickness = 4

    rectwidth = self.screenwidth / self.fieldwidth
    for x in range(1, self.fieldwidth):
      pygame.draw.line(self.screen, self.WHITE, (rectwidth * x, 0), (rectwidth * x, self.screenheight), thickness)

    rectheight = self.screenheight / self.fieldheight
    for y in range(1, self.fieldheight):
      pygame.draw.line(self.screen, self.WHITE, (0, rectheight * y), (self.screenwidth, rectheight * y), thickness)

    pygame.display.flip()

  def drawCoins(self):
    rectwidth = self.screenwidth / self.fieldwidth
    rectheight = self.screenheight / self.fieldheight
    for x in range(len(self.field)):
      for y in range(len(self.field[x])):
        if self.field[x][y] != 0:
          pygame.draw.circle(self.screen, self.playerColors[self.field[x][y] - 1], (rectwidth * x + rectwidth / 2, rectheight * y + rectwidth / 2), self.coinRadius)
    pygame.display.flip()

  def convertCoordinateToRow(self, xCoordinate):
    x = int(xCoordinate / (self.screenwidth / self.fieldwidth))
    return x
  
  def chooseRow(self, row):
    self.addCoin(row, self.currentPlayer)
    self.drawBackground()
    self.drawCoins()
    win = self.checkWinner(self.currentPlayer)
    print(f'winner: {win}')
    self.currentPlayer = self.currentPlayer % 2 + 1

  def checkWinner(self, player):
    print(self.field)
    for x in range(0, self.fieldwidth):
      for y in range(self.fieldheight - 1, self.fieldheight - self.winner_lenght - 1, -1):
        # horizontal
        i = 0
        print(f'x: {x}; y: {y}; i: {i}; player: {self.field[x + i][y]}')
        while self.field[x + i][y] == player:
          print(f'x: {x}; y: {y}; i: {i}; player: {self.field[x + i][y]}')
          if i >= self.winner_lenght - 1: return player
          i+=1
        # vertical
        i = 0
        while self.field[x][y - i] == player:
          if i >= self.winner_lenght - 1: return player
          i+=1
        # diagonal
        i = 0
        while self.field[x + i][y - i] == player:
          if i >= self.winner_lenght - 1: return player
          i+=1
    return 0
  


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