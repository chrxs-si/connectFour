from game import connectFour
from random import randint
from copy import deepcopy

MAX_DEPTH = 5  # Maximum depth for the Minimax algorithm

def minmaxStep(oldcf, player, depth=0):
  pointPaths = [] # indicates how good each path is; if the path is not finished yet, it gets 0 points

  if depth > MAX_DEPTH:
    return heuristik(oldcf, player)
  
  #print(oldcf.field)

  for row in range(len(oldcf.field)):

    cf = deepcopy(oldcf)

    win = None
    # Check if the row still has space
    if cf.field[row][0] == 0: 
      # Play the next move
      win = cf.chooseRow(row)
    else:
      # The row is already full, so it's a draw
      win = -1

    # No end of game reached yet
    if win == 0:
      pointPaths.append(minmaxStep(cf, player, depth + 1))
    # Draw
    elif win == -1:
      pointPaths.append(0)
    # A player has won
    else:
      point = (1 if win == player else -1) * (MAX_DEPTH - depth + 2)   # Points awarded for win or loss
      pointPaths.append(point)
      break

  if (depth == 0):
    return pointPaths
  
  if depth % 2 == 0:
    # Player's turn: maximize
    return max(pointPaths)
  else:
    # Opponent's turn: minimize
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
  # check in which row a move can actually be made
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
