import random
from copy import deepcopy
from game import connectFour
import math


def evaluateGameState(cf, player, row):
  other_player = (player % 2) + 1
  cf_hight = len(cf.field[row])
  cf_wight = len(cf.field)

  col = 0
  while cf.field[row][col] == 0:
    col += 1

    if col >= cf_hight: break

  points = 0

  directions = [
    [0, 1],
    [-1, 1],
    [-1, 0],
    [-1, -1],
    [0, -1],
    [1, -1],
    [1, 0]
  ]

  for direction in directions:
    for i in range(1, 3):
      current_col = col+direction[1]*i
      current_row = row+direction[0]*i
      if current_col < 0 or current_col >= cf_hight: break
      if current_row < 0 or current_row >= cf_wight: break
      if cf.field[current_row][current_col] != player: break
      else: points += i**3

  return points


def evaluateMoveInRow(cf, row):
  player = cf.currentPlayer
  win = cf.chooseRow(row)

  if win == -2: return -10000
  if win == -1: 0
  if win == player: return 50
  
  # no win yet
  points = evaluateGameState(cf, player, row)
  points += evaluateGameState(cf, cf.currentPlayer, row)

  return points


def evaluateMoves(cf):
  pointPaths = []
  for row in range(len(cf.field)):
    points = evaluateMoveInRow(deepcopy(cf), row)
    pointPaths.append(points)

  return pointPaths


def chooseBestPath(cf, points, printOut):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -10000

  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  row = indizes[random.randint(0, len(indizes) - 1)]
  if printOut: print(f'monteCarlo - row: {row}, points: {points}')
  return row


def getHeuristikMove(cf, printOut=True):
  if printOut: print('calculating ...')
  pointPaths = evaluateMoves(cf)
  path = chooseBestPath(cf, pointPaths, printOut)
  return path