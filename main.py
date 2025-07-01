from game import connectFour
from game import copyGameWithoutPyGame
import pygame
import threading
from rnd import getRandomMove
from minmax import getMinMaxMove

def game_thread():
      cf.startScreen()

cf = connectFour(True)

gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
gameThread.start()


#human, minmax, random
player = ['random', 'minmax']

while cf.active or cf.open:
  if player[cf.currentPlayer - 1] == 'human':
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos = cf.convertCoordinateToRow(pos[0])
        cf.chooseRow(pos)
      if event.type == pygame.QUIT:
        cf.active = False
  if player[cf.currentPlayer - 1] == 'minmax':
    cf.chooseRow(getMinMaxMove(copyGameWithoutPyGame(cf)))
  if player[cf.currentPlayer - 1] == 'random':
    cf.chooseRow(getRandomMove(copyGameWithoutPyGame(cf)))