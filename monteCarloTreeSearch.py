from random import randint
from copy import deepcopy
from game import connectFour

ITERATIONS = 400

def monteCarloStep(oldcf, player, depth=0):
  cf = deepcopy(oldcf)
  cfPaths = []
  for i in range(len(cf.field)): 
    cfPaths.append([None, None])  #contains cf and path list with for the next depth
  print(f'cfPath: {cfPaths}')

  # Choose a random row that is not already full
  available_rows = [i for i in range(len(cf.field)) if cf.field[i][0] == 0]
  row = available_rows[randint(0, len(available_rows) - 1)]
  print(row)

  win = cf.chooseRow(row)
  print(f'win: {win}, depth: {depth}')
  cfPaths[row][0] = cf
  if win == 0: # Continue playing randomly until the game ends
    cfPaths[row][1] = monteCarloStep(cf, player, depth+1) # Spiel noch nicht zu Ende
  elif win == -1:
    cfPaths[row][1] = 0 # unentschieden
  else:
    cfPaths[row][1] = 1 if win == player else -1 # Spieler gewinnt

  print(f'depth: {depth}')

  print(f'cfPath: {cfPaths}\n\n')
  return cfPaths


def dicoverPaths(path):
    available_rows = [i for i in range(len(cf.field)) if cf.field[i][0] == 0 and path]
    row = available_rows[randint(0, len(available_rows) - 1)]



def findBestMove(cf, player):

  parentsPaths = monteCarloStep(cf, player)
  print(parentsPaths)
  
  while parentsPaths[1] == None or None in parentsPaths[1]:
    available_rows = [i for i in range(len(cf.field)) if parentsPaths[1][i][0] is None]
    row = available_rows[randint(0, len(available_rows) - 1)]
    parentsPaths[1] = monteCarloStep(parentsPaths[0], player)
  print(parentsPaths)

    


    

def getMonteCarloTreeSearchMove(cf, prints=True):
  pointPaths = []
  path = 0
  if prints: print(path)

  return path

cf = connectFour(False)

findBestMove(cf, cf.currentPlayer)