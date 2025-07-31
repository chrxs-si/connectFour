import random
from copy import deepcopy
from game import connectFour
import math

ITERATIONS = 400

class MCTSNode:
  def __init__(self, cf, parent=None, move=None):
    self.cf = cf                # Spielzustand
    self.parent = parent              # Referenz zum Elternknoten
    self.children = []                # Liste von Kindknoten
    self.move = move                  # Der Zug, der zu diesem Zustand geführt hat
    self.visits = 0                   # Wie oft wurde dieser Knoten besucht?
    self.wins = 0                     # Wie viele Siege resultierten aus diesem Knoten?
    
    self.untriedMoves = []

    for i in range(len(cf.field)):
      if cf.field[i][0] == 0:
        self.untriedMoves.append(i)
    if parent is not None:
      if self not in parent.children:
        parent.children.append(self)

def monteCarloGameStep(parentNode, player, depth=0):
  # Choose a random row that is not already full
  row = None
  if parentNode.untriedMoves:
    row = parentNode.untriedMoves[random.randint(0, len(parentNode.untriedMoves) - 1)]
    parentNode.untriedMoves.remove(row)
  else:
    print('Parent node should habe untried moves.')
    return None

  node = MCTSNode(deepcopy(parentNode.cf), parent=parentNode, move=row)

  win = node.cf.chooseRow(row)
  if win == 0: # game hsn't ended
    return monteCarloGameStep(node, player, depth+1)

  # game end
  if win == -1: # no winner
    node.wins = 0.5
    print('draw!')
  else: # there is a winner
    node.wins = 1 if win == player else 0
    print('win!') if win == player else print('loose!')
  node.visits = 1

  return node

def calculateChildUTC(parent):
    if parent.visits == 0:
        print('parent should have visits if it has children')
        return [0] * len(parent.children)
    utc_values = []
    for child in parent.children:
        if child.visits == 0:
            utc_values.append(float('inf'))
        else:
            utc_value = (child.wins / child.visits) + (3 * math.sqrt(math.log(parent.visits) / child.visits))
            utc_values.append(utc_value)
    return utc_values

def calculateMoves(cf):
  player = cf.currentPlayer
  node = MCTSNode(deepcopy(cf)) #create root node with current game state

  for i in range(ITERATIONS):
    if i % 100 == 0:
      print(f'Iteration: {i}')
      print(f'node.visits: {node.visits}')

    # Select a node to expand
    endNode = None
    if len(node.untriedMoves) > 0:
      #expand Node for every row
      endNode = monteCarloGameStep(node, player=player)
    else:
      print(f'children: {len(node.children)}, visits: {node.visits}, wins: {node.wins}')
      currentNode = node
      while len(currentNode.children) > 0:
        utc_values = calculateChildUTC(currentNode)
        max_utc_index = utc_values.index(max(utc_values))
        currentNode = currentNode.children[max_utc_index]

      # Expand the node
      endNode = monteCarloGameStep(currentNode, player=player)
    
    # backpropagation
    currentNode = endNode
    while currentNode.parent is not None:
      currentNode = currentNode.parent
      currentNode.wins += endNode.wins
      currentNode.visits += 1
  
  #debug
  parent = node
  while len(parent.children) > 0:
    print(f'Child move: {parent.move}, visits: {parent.visits}, wins: {parent.wins}')
    parent = parent.children[random.randint(0, len(parent.children)-1)]

  print(f'node.visits: {node.visits}, node.wins: {node.wins}, node.children: {len(node.children)}, node.untriedMoves: {len(node.untriedMoves)}')
  points = [0] * len(cf.field)
  for child in node.children:
    points[child.move] = child.wins / child.visits if child.visits > 0 else 0
    print(f'child row {child.move}, wins: {child.wins}, visits: {child.visits}')

  return points
  
def chooseBestPath(cf, points):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -10000

  print(f'monte Carlo points: {points}')
  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  return indizes[random.randint(0, len(indizes) - 1)]


def getMonteCarloTreeSearchMove(cf):
  pointPaths = calculateMoves(cf)
  path = chooseBestPath(cf, pointPaths)
  print(path)
  return path

cf = connectFour(False)

getMonteCarloTreeSearchMove(cf)