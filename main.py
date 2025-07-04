from game import connectFour
from game import copyGameWithoutPyGame
import pygame
import threading
from rnd import getRandomMove
from minmax import getMinMaxMove

def game_thread():
      cf.startScreen()

#human, minmax, random
player = ['human', 'minmax']

points = [0, 0, 0]

for round in range(5):
  cf = connectFour(True)

  gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
  gameThread.start()

  while (cf.active or cf.open) and cf.win == 0:
    if player[cf.currentPlayer - 1] == 'human':
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          pos = pygame.mouse.get_pos()
          pos = cf.convertCoordinateToRow(pos[0])
          cf.chooseRow(pos) 
        if event.type == pygame.QUIT:
          cf.active = False
    if player[cf.currentPlayer - 1] == 'minmax':
      #pygame.time.wait(2000)
      cf.chooseRow(getMinMaxMove(copyGameWithoutPyGame(cf)))
    if player[cf.currentPlayer - 1] == 'random':
      cf.chooseRow(getRandomMove(copyGameWithoutPyGame(cf)))

  points[cf.win] += 1
  print(f'Spieler 1: {points[1]}, Spieler 2: {points[2]}, Unentschieden: {points[0]}')

while cf.open:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      cf.open = False