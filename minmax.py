from game import connectFour
from random import randint
from copy import deepcopy

MAX_DEPTH = 7  # Maximale Tiefe für den Minimax-Algorithmus

def minmaxStep(oldcf, player, depth=0):
  pointPaths = [] # gibt an welcher Pfad wie gut ist; ist der Pfad noch nicht zu Ende gibt es 0 Punkte

  if depth > MAX_DEPTH:
    return heuristik(oldcf, player)
  
  #print(oldcf.field)

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
      pointPaths.append(minmaxStep(cf, player, depth + 1))
    #Unentschieden
    elif win == -1:
      pointPaths.append(0)
    #Ein Spieler hat gewonnen
    else:
      point = (1 if win == player else -1) * (MAX_DEPTH - depth + 2)   # Punktevergabe bei Gewinn oder Verlust
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

def heuristik(cf, player):
  cf.winner_lenght = 3
  player1 = cf.checkWinner(1)
  player2 = cf.checkWinner(2)
  cf.winner_lenght = 4
  if player1 > 0 or player2 > 0:
    return 1 if max([player1, player2]) == player else -1
  return 0

def chooseBestPath(cf, points):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -10000

 
  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  row = indizes[randint(0, len(indizes) - 1)]
  print(f'minmax - row: {row}, points: {points}')
  return row

def getMinMaxMove(cf):
  print('calculating ...')
  path = chooseBestPath(cf, minmaxStep(cf, cf.currentPlayer))

  return path
