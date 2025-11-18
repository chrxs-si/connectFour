from game import connectFour
from game import copyGameWithoutPyGame
from game import analyseGame
import time
import pygame
import subprocess
import threading
from rnd import getRandomMove
from minmax import getMinMaxMove
from monteCarloTreeSearch import getMonteCarloTreeSearchMove
from neuroevolution import getNeuroEvolutioneSearchMove
from heuristik import getHeuristikMove

def getMinMaxMove_c(cf):
  path = "./connectFour/minmax.exe"
  data = str(cf.currentPlayer) + ' ' + ' '.join(str(cf.field[row][col]) for row in range(len(cf.field)) for col in range(len(cf.field[0])))

  try:
    ergebnis = subprocess.run(
          [path, "7 0"], # [MAX_DEPTH] [debug_level]
          input=data,
          check=False,  # Löst eine Ausnahme aus, wenn die EXE einen Fehlercode zurückgibt
          capture_output=True,
          text=True
      )
    
    stdout = ergebnis.stdout.strip()
    tokens = stdout.split()
    #print(f"STDOUT:\n{stdout}")
    print(tokens[-2])
    path = int(tokens[-1])

    return path
    
  except subprocess.CalledProcessError as e:
      print(f"Fehler beim Starten der EXE: {e}")
      print(f"Fehlerausgabe: \n{e.stderr}")
  except FileNotFoundError:
      print(f"Fehler: Die Datei {path} wurde nicht gefunden.")

def game_thread():
      cf.startScreen()

# set player types here
# Options: human, minmax_py, minmax_c, random, montecarlo, neuroevolution heuristik
player = ['human', 'heuristik']

playerTime = [0, 0]
playerMoves = [0, 0]

points = [0, 0, 0, 0]

# set game rounds
for round in range(1):

  cf = connectFour(True)

  gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
  gameThread.start()

  # start game loop
  while (cf.active or cf.open) and cf.win == 0:
    startTime = time.time()

    if player[cf.currentPlayer - 1] == 'human':
      action = False
      while action == False:
        for event in pygame.event.get():
          if event.type == pygame.MOUSEBUTTONDOWN:
            action = True
            pos = pygame.mouse.get_pos()
            pos = cf.convertCoordinateToRow(pos[0])
            cf.chooseRow(pos) 
          if event.type == pygame.QUIT:
            action = True
            cf.active = False
    elif player[cf.currentPlayer - 1] == 'minmax_py':
      cf.chooseRow(getMinMaxMove(copyGameWithoutPyGame(cf)))
    elif player[cf.currentPlayer - 1] == 'minmax_c':
      cf.chooseRow(getMinMaxMove_c(copyGameWithoutPyGame(cf)))
    elif player[cf.currentPlayer - 1] == 'random':
      cf.chooseRow(getRandomMove(copyGameWithoutPyGame(cf)))
    elif player[cf.currentPlayer - 1] == 'montecarlo':
      cf.chooseRow(getMonteCarloTreeSearchMove(copyGameWithoutPyGame(cf)))
    elif player[cf.currentPlayer - 1] == 'neuroevolution':
      cf.chooseRow(getNeuroEvolutioneSearchMove(copyGameWithoutPyGame(cf)))
    elif player[cf.currentPlayer - 1] == 'heuristik':
      cf.chooseRow(getHeuristikMove(copyGameWithoutPyGame(cf)))

    endTime = time.time()

    playerMoves[cf.currentPlayer - 1] += 1
    playerTime[cf.currentPlayer - 1] += (endTime - startTime)
    print(f"took {endTime - startTime:.2f} s")

  # print game stats
  points[cf.win + 1] += 1
  print(f'\nSpieler 1 ({player[0]}): {points[2]}, Spieler 2 ({player[1]}): {points[3]}, Unentschieden: {points[0]}')
  print(f'durchschnittliche Züge pro Spiel: {sum(playerMoves) / (round + 1)}')
  print(f'durchschnittliche Zeit pro Zug gesamt: Spieler 1 ({player[1]}): {playerTime[0] / playerMoves[0]:.2f} s, Spieler 2 ({player[0]}): {playerTime[1] / playerMoves[1]:.2f} s')
  print('-'*20)

# wait to close game window
while cf.open:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      cf.open = False