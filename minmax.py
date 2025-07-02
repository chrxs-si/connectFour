from game import connectFour
from random import randint
from copy import deepcopy

MAX_DEPTH = 4  # Maximale Tiefe für den Minimax-Algorithmus

def stepDeeper(oldcf, player, depth=0, r=0):
  pointPaths = [] # gibt an welcher Pfad wie gut ist; ist der Pfad noch nicht zu Ende gibt es 0 Punkte
  gamePaths = [] # speichert die Spiele nach jedem Move

  if depth > MAX_DEPTH:
    return [0, oldcf]

  for row in range(len(oldcf.field)):

    cf = deepcopy(oldcf)

    win = None
    # Testen ob Reihe noch Platz hat
    if cf.field[row][0] == 0: 
      # Den nächsten Move spielen
      win = cf.chooseRow(row)
    else:
      # Die Reihe ist schon voll, daher unentschieden
      win = -1

    #Noch kein Spielende erreicht
    if win == 0:
      stepDeeperResult = stepDeeper(deepcopy(cf), player, depth + 1, row)
      pointPaths.append(stepDeeperResult[0])
      gamePaths.append(stepDeeperResult[1])
    #Unentschieden
    elif win == -1:
      pointPaths.append(0)
      gamePaths.append(None)
    #Ein Spieler hat gewonnen
    else:
      point = ((MAX_DEPTH - depth + 1) * (1 if win == player else -1))  # Punktevergabe bei Gewinn oder Verlust
      pointPaths.append(point)
      gamePaths.append(None)
  
  return [pointPaths, gamePaths]

def calculatePaths(pointPaths, depth=0):
  # Wenn das aktuelle Element kein Listentyp ist, ist es ein Endwert (1, 0, -1)
  if not isinstance(pointPaths, list):
    return pointPaths

  # Minimax: Maximieren für eigenen Zug (gerade Tiefe), Minimieren für Gegner (ungerade Tiefe)
  if depth % 2 == 0:
    # Spieler am Zug: Maximieren
    return min(calculatePaths(path, depth + 1) for path in pointPaths)
  else:
    # Gegner am Zug: Minimieren
    return max(calculatePaths(path, depth + 1) for path in pointPaths)

def chooseBestPath(cf, points):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -10000

  print(f'points: {points}')
  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  return indizes[randint(0, len(indizes) - 1)]

def getMinMaxMove(cf):
  pointPaths = stepDeeper(cf, cf.currentPlayer)
  points = []
  for path in pointPaths[0]:
    points.append(calculatePaths(path))
  path = chooseBestPath(cf, points)
  print(path)

  return path
