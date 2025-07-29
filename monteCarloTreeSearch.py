from random import randint
from copy import deepcopy

ITERATIONS = 400

def monteCarloStep(oldcf):
  pointPaths = [0] * oldcf.fieldwidth
  cfPaths = [None] * oldcf.fieldwidth
  cf = deepcopy(oldcf)
  path = []
  # Choose a random row that is not already full
  available_rows = [i for i in range(len(cf.field)) if cf.field[i][0] == 0]
  if not available_rows:
    return [0, path]  # No moves possible
  row = available_rows[randint(0, len(available_rows) - 1)]

  win = cf.chooseRow(row)
  path.append(row)
  cfPaths[row] = cf
  if win != 0:
    return [win, pointPaths, cfPaths]  # Return the winner and the path taken
  
  # Continue playing randomly until the game ends
  win, pointPaths[row], cfPaths[row] = monteCarloStep(cf)
  return [win, pointPaths, cfPaths]



def findBestMove(oldcf, player):
  pointPaths = [0] * oldcf.fieldwidth
  paths = [None] * oldcf.fieldwidth
  for i in range(ITERATIONS):
    # Wähle eine zufällige row, die in paths noch None ist und nicht voll ist
    available_rows = [row for row in range(oldcf.fieldwidth) if paths[row] is None and oldcf.field[row][0] == 0]
    if not available_rows:
      continue  # Keine gültigen Züge mehr für diese Iteration
    row = available_rows[randint(0, len(available_rows) - 1)]
    cf = deepcopy(oldcf)
    win = cf.chooseRow(row)
    if win == 0:
      win, path = playRandomGame(cf)
    pointPaths[row] += 1 if win == player else -1
    paths[row] = [row]
    else:


    win, path = playRandomGame(cf)
    

def getMonteCarloTreeSearchMove(cf, prints=True):
  pointPaths = []

  if prints: print(path)

  return path
