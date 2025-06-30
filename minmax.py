from game import connectFour
from random import randint
from copy import deepcopy

MAX_DEPTH = 1

def stepDeeper(cf, player, depth=0):
  pointPaths = [] # gibt an welcher Pfad wie gut ist; ist der Pfad noch nicht zu Ende gibt es 0 Punkte
  gamePaths = [] # speichert die Spiele nach jedem Move

  for row in range(len(cf.field)):
    # Testen ob Reihe noch Platz hat und die maximale Tiefe noch nicht erreicht ist
    win = None
    if cf.field[row][0] == 0 and depth < MAX_DEPTH: 
      # Den nächsten Move spielen
      win = cf.chooseRow(row)
    else:
      # Die Reihe ist schon voll, daher unentschieden
      win = -1

    #Noch kein Spielende erreicht
    if win == 0:
      stepDeeperResult = stepDeeper(deepcopy(cf), player, depth + 1)
      pointPaths.append(stepDeeperResult[0])
      gamePaths.append(stepDeeperResult[1])
    #Unentschieden
    elif win == -1:
      pointPaths.append(0)
      gamePaths.append(None)
    #Ein Spieler hat gewonnen
    else:
      pointPaths.append(-2 if win == player else 1)
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

def chooseBestPath(points):
  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  return indizes[randint(0, len(indizes) - 1)]

def getMinMaxMove(cf):
  pointPaths = stepDeeper(cf, cf.currentPlayer)
  print(f'pointPaths: {pointPaths[0]}\n')
  points = []
  for path in pointPaths[0]:
    points.append(calculatePaths(path))
  print(f'points: {points}\n')
  path = chooseBestPath(points)
  return path
