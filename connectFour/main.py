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
from minmax_alpha_beta import getMinMaxAlphaBetaMove

def getMinMaxMove_c(cf):
  path = "./connectFour/minmax.exe"
  data = str(cf.currentPlayer) + ' ' + ' '.join(str(cf.field[row][col]) for row in range(len(cf.field)) for col in range(len(cf.field[0])))

  try:
    ergebnis = subprocess.run(
          [path, "9 0"], # [MAX_DEPTH] [debug_level]
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


def getMinMaxMove_c_alpha_beta(cf):
  path = "./connectFour/minmax_alpha_beta.exe"
  data = str(cf.currentPlayer) + ' ' + ' '.join(str(cf.field[row][col]) for row in range(len(cf.field)) for col in range(len(cf.field[0])))

  try:
    ergebnis = subprocess.run(
          [path, "9 0"], # [MAX_DEPTH] [debug_level]
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
# Options: human, minmax_py, minmax_c, minmax_py_alpha_beta, minmax_c_alpha_beta, random, montecarlo, neuroevolution, heuristik
player = ['minmax_py', 'minmax_c']

playerTime = [0, 0]
playerMoves = [0, 0]

points = [0, 0, 0, 0]

# set game rounds
for round in range(10):

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
    elif player[cf.currentPlayer - 1] == 'minmax_py_alpha_beta':
      cf.chooseRow(getMinMaxAlphaBetaMove(copyGameWithoutPyGame(cf)))
    elif player[cf.currentPlayer - 1] == 'minmax_c_alpha_beta':
      cf.chooseRow(getMinMaxMove_c_alpha_beta(copyGameWithoutPyGame(cf)))
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
  G,R,Y,C,B,RS = "\033[92m","\033[91m","\033[93m","\033[96m","\033[1m","\033[0m"
  p1c = G if points[2] > points[3] else R if points[2] < points[3] else Y
  p2c = G if points[3] > points[2] else R if points[3] < points[2] else Y
  print(f"\n{p1c}{B}Spieler 1 ({player[0]}): {points[2]}{RS}, {p2c}{B}Spieler 2 ({player[1]}): {points[3]}{RS}, {Y}Unentschieden: {B}{points[0]}{RS}")
  print(f"{C}durchschnittliche Züge pro Spiel: {RS}{sum(playerMoves)/(round+1):.2f}")
  print(f"{C}durchschnittliche Zeit pro Zug gesamt:{RS} Spieler 1 ({player[0]}): {B}{playerTime[0]/playerMoves[0]:.2f} s{RS}, Spieler 2 ({player[1]}): {B}{playerTime[1]/playerMoves[1]:.2f} s{RS}")

  print('-'*20)

# wait to close game window
while cf.open:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      cf.open = False