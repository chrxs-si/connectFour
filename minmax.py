from game import connectFour
from random import randint
from copy import deepcopy

MAX_DEPTH = 5  # Maximale Tiefe für den Minimax-Algorithmus

def stepDeeper(oldcf, player, depth=0):
  pointPaths = [] # gibt an welcher Pfad wie gut ist; ist der Pfad noch nicht zu Ende gibt es 0 Punkte

  if depth > MAX_DEPTH:
    return 0

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
      pointPaths.append(stepDeeper(cf, player, depth + 1))
    #Unentschieden
    elif win == -1:
      pointPaths.append(0)
    #Ein Spieler hat gewonnen
    else:
      point = ((MAX_DEPTH - depth + 1) * (1 if win == player else -1))  # Punktevergabe bei Gewinn oder Verlust
      pointPaths.append(point)
      break

  if (depth == 0):
    return pointPaths
  
  if depth % 2 == 0:
    # Spieler am Zug: Maximieren
    return max(pointPaths)
  else:
    # Gegner am Zug: Minimieren
    return min(pointPaths)


def chooseBestPath(cf, points):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -10000

  print(f'points: {points}')
  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  return indizes[randint(0, len(indizes) - 1)]

def getMinMaxMove(cf):
  path = chooseBestPath(cf, stepDeeper(cf, cf.currentPlayer))
  print(path)

  return path
