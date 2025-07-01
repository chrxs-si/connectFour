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
    # Testen ob Reihe noch Platz hat und die maximale Tiefe noch nicht erreicht ist

    cf = deepcopy(oldcf)
    win = None
    if cf.field[row][0] == 0: 
      # Den nächsten Move spielen
      win = cf.chooseRow(row)
    else:
      # Die Reihe ist schon voll, daher unentschieden
      win = -1
    ####if depth == 0: print('')
    ####print(f'depth: {depth}, row: {row},  win: {win}, currentPlayer: {cf.currentPlayer}')
    #Die Maximale Tiefe wurde erreicht

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
      point = (3 if win == player else -2)# * (MAX_DEPTH - depth + 1)
      pointPaths.append(point)
      gamePaths.append(None)
  
  ####print(f'depth: {depth}, row: {r},  pointPath: {pointPaths}')
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
  ####print('-'*10)
  ####print(cf.field)
  pointPaths = stepDeeper(cf, cf.currentPlayer)
  ####print(f'\npointPaths: {pointPaths[0]}\n')
  points = []
  for path in pointPaths[0]:
    points.append(calculatePaths(path))
  print(f'points: {points}\n')
  path = chooseBestPath(points)
  return path
