from game import connectFour
from random import randint
from copy import deepcopy

MAX_DEPTH = 4

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
      point = (1 if win == player else -1)# * (MAX_DEPTH - depth + 1)
      pointPaths.append(point)
      gamePaths.append(None)
  
  return [pointPaths, gamePaths]

def calculatePaths(pointPaths):
  pointSums = []
  if isinstance(pointPaths, list):
    for path in pointPaths:
      pointSums.append(calculatePaths(path))
  else:
    return pointPaths

  return sum(pointSums)

def chooseBestPath(cf, points):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -100000

  print(f'points: {points}\n')

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
