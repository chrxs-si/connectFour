import pygame
import threading
import minmax

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
    self.open = True
    self.moves = 0
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
    while self.active:
      self.draw()
    print('end')
    self.draw()
    while self.open:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE]:
        print('close')
        self.open = False

    
  def addCoin(self, row, player):
    y = self.fieldheight - 1
    while self.field[row][y] != 0:
      y -= 1
      if y < 0: return False
    
    self.field[row][y] = player

  def draw(self):
    self.drawBackground()
    self.drawCoins()
    pygame.display.flip()

  def drawBackground(self):
    self.screen.fill(self.BLACK)
    thickness = 4

    rectwidth = self.screenwidth / self.fieldwidth
    if self.active == False: return
    for x in range(1, self.fieldwidth):
      pygame.draw.line(self.screen, self.WHITE, (rectwidth * x, 0), (rectwidth * x, self.screenheight), thickness)

    rectheight = self.screenheight / self.fieldheight
    for y in range(1, self.fieldheight):
      pygame.draw.line(self.screen, self.WHITE, (0, rectheight * y), (self.screenwidth, rectheight * y), thickness)

  def drawCoins(self):
    rectwidth = self.screenwidth / self.fieldwidth
    rectheight = self.screenheight / self.fieldheight
    for x in range(len(self.field)):
      for y in range(len(self.field[x])):
        if self.field[x][y] != 0:
          pygame.draw.circle(self.screen, self.playerColors[self.field[x][y] - 1], (rectwidth * x + rectwidth / 2, rectheight * y + rectwidth / 2), self.coinRadius)

  def convertCoordinateToRow(self, xCoordinate):
    x = int(xCoordinate / (self.screenwidth / self.fieldwidth))
    return x
  
  def chooseRow(self, row): #returns: -1 = draw; 1 = player 1 wins; 2 = player 2 wins
    if self.active == False: return
    self.addCoin(row, self.currentPlayer)
    self.moves += 1
    win = self.checkWinner(self.currentPlayer)
    if win != 0: 
      print(f'winner: {win}')
      self.active = False
      return win
    self.currentPlayer = self.currentPlayer % 2 + 1
    return None
    

  def checkWinner(self, player):
    for x in range(0, self.fieldwidth):
      for y in range(self.fieldheight - 1, self.fieldheight - self.winner_lenght - 1, -1):
        # horizontal
        i = 0
        while self.field[x + i][y] == player:
          i+=1
          if i >= self.winner_lenght: return player
          if x + i >= self.fieldwidth: break

        # vertical
        i = 0
        while self.field[x][y - i] == player:
          i+=1
          if i >= self.winner_lenght: return player
          if y - i < 0: break

        # diagonal links-unten nach rechts-oben
        i = 0
        while self.field[x + i][y - i] == player:
          i+=1
          if i >= self.winner_lenght: return player
          if x + i >= self.fieldwidth or y - i < 0: break
            
        # diagonal rechts-unten nach rechts-unten
        i = 0
        while self.field[x - i][y - i] == player:
          i+=1
          if i >= self.winner_lenght: return player
          if x + i < 0 or y - i < 0: break

    if self.moves >= self.fieldheight * self.fieldwidth: return -1
    return 0
  

def startPlannedGame(moves):
  print('play: ' + str(moves))
  cf = connectFour()
  gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
  gameThread.start()
  for move in moves:
    win = cf.chooseRow(move)
    if win != 0:
      return win


cf = connectFour()

def game_thread():
    cf.start()

gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
gameThread.start()


#human, minmax
player = ['human', 'minmax']

while cf.open:
  print(cf.currentPlayer)
  if player[cf.currentPlayer - 1] == 'human':
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos = cf.convertCoordinateToRow(pos[0])
        cf.chooseRow(pos)
      if event.type == pygame.QUIT:
        cf.active = False
  if player[cf.currentPlayer - 1] == 'minmax':
    pass