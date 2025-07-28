from random import randint
from copy import deepcopy

GAMES_PER_ROW = 25

def testGame(cf, player, firstmove):
  win = cf.chooseRow(firstmove)

  while win == 0:
    possible_rows = []
    for row in range(len(cf.field)):
      if cf.field[row][0] == 0: possible_rows.append(row)

    win = cf.chooseRow(possible_rows[randint(0, len(possible_rows) - 1)])

  if win == -1: return 0
  return (1 if win == player else -1)

def chooseBestPath(cf, points, prints=True):
  if prints: print(f'montecarlo points: {points}')
  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  return indizes[randint(0, len(indizes) - 1)]

def getMonteCarloTreeSearchMove(cf, prints=True):
  pointPaths = []

  for row in range(len(cf.field)):
    pointPaths.append(0)
    if cf.field[row][0] == 0:
      for game in range(GAMES_PER_ROW):
        pointPaths[row] += testGame(deepcopy(cf), cf.currentPlayer, row)
    else:
      pointPaths[row] = -10000

  path = chooseBestPath(cf, pointPaths, prints)
  if prints: print(path)

  return path
