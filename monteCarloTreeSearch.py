from random import randint
from copy import deepcopy
from game import connectFour

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

def monteCarloGameStep(parentNode, player=None, depth=0):
  # Choose a random row that is not already full
  if parentNode.untriedMoves:
    row = parentNode.untriedMoves[randint(0, len(parentNode.untriedMoves) - 1)]
    parentNode.untriedMoves.remove(row)
  else:
    return None

  node = MCTSNode(deepcopy(parentNode.cf), parent=parentNode, move=row)

  win = node.cf.chooseRow(row)
  if win == 0:
    node.children.append(monteCarloGameStep(node, player, depth+1))
  elif win == -1:
    node.wins = 0
  else:
    node.wins = 1 if win == player else -1

  return node

def calculateChildUTC(parent):
    if parent.visits == 0:
        return [0] * len(parent.children)
    utc_values = []
    for child in parent.children:
        if child.visits == 0:
            utc_values.append(float('inf'))
        else:
            utc_value = (child.wins / child.visits) + (2 * (parent.visits ** 0.5) / child.visits)
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
    current_node = node
    if len(current_node.untriedMoves) > 0:
      current_node = monteCarloGameStep(current_node, player=player, depth=0)
    else:
      while len(current_node.children) > 0:
        utc_values = calculateChildUTC(current_node)
        max_utc_index = utc_values.index(max(utc_values))
        current_node = current_node.children[max_utc_index]

    # Expand the node
    if len(current_node.untriedMoves) > 0:
      current_node = monteCarloGameStep(current_node, player=player, depth=0)

    # Backpropagate the results
    result = current_node.wins
    while current_node is not None:
      current_node.visits += 1
      current_node.wins += result
      current_node = current_node.parent

  print(f'node.visits: {node.visits}, node.wins: {node.wins}, node.children: {len(node.children)}, node.untriedMoves: {len(node.untriedMoves)}')
  points = [0] * len(cf.field)
  for child in node.children:
    points[child.move] = child.wins / child.visits if child.visits > 0 else 0
    print(f'Child move: {child.move}, visits: {child.visits}, wins: {child.wins}')
  parent = node
  while len(parent.children) > 0:
    print(f'Child move: {child.move}, visits: {child.visits}, wins: {child.wins}')
    parent = parent.children[0]
  return points
  
def chooseBestPath(cf, points):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -10000

  print(f'monte Carlo points: {points}')
  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  return indizes[randint(0, len(indizes) - 1)]


def getMonteCarloTreeSearchMove(cf):
  pointPaths = calculateMoves(cf)
  path = chooseBestPath(cf, pointPaths)
  print(path)
  return path

cf = connectFour(False)

getMonteCarloTreeSearchMove(cf)