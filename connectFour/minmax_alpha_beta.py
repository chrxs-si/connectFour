from game import connectFour
from random import randint
from copy import deepcopy

MAX_DEPTH = 4  # Maximum depth for the Minimax algorithm

def minmaxStep(oldcf, player, depth=0, alpha=float('-inf'), beta=float('inf')):
  pointPaths = [] # indicates how good each path is; if the path is not finished yet, it gets 0 points

  if depth > MAX_DEPTH:
    return heuristik(oldcf, player)
  
  #print(oldcf.field)

  isMaxStep = (depth % 2 == 0)

  bestValue = float('-inf') if isMaxStep else float('inf')

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
      value = minmaxStep(cf, player, depth + 1, alpha, beta)
    # Draw
    elif win == -1:
      value = 0
    # A player has won
    else:
      value = (1 if win == player else -1) * (MAX_DEPTH - depth + 2)   # Points awarded for win or loss
      break

    # Maximierer
    if isMaxStep:
        bestValue = max(bestValue, value)
        alpha = max(alpha, bestValue)
    # Minimierer
    else:
        bestValue = min(bestValue, value)
        beta = min(beta, bestValue)

    # Pruning
    if beta <= alpha:
        break
  
  if depth > 0:
      return bestValue
  else:
      # Obere Ebene: für jede mögliche Spalte Bewertung berechnen
      move_values = []

      for i in range(len(oldcf.field)):
          # Wenn die Spalte voll ist → extrem schlechter Wert
          if oldcf.field[i][0] != 0:
              move_values.append(-10000)
              continue

          # Board kopieren und Zug ausführen
          newcf = deepcopy(oldcf)
          newcf.chooseRow(i)

          # Bewertung dieses Zuges berechnen
          value = minmaxStep(newcf, player, 1, alpha, beta)
          move_values.append(value)

      return move_values

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

def getMinMaxAlphaBetaMove(cf):
  print('calculating ...')
  path = chooseBestPath(cf, minmaxStep(cf, cf.currentPlayer, 0, float('-inf'), float('inf')))

  return path
