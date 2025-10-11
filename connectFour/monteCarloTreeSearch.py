import random
from copy import deepcopy
from game import connectFour
import math

ITERATIONS = 1000

class MCTSNode:
  def __init__(self, cf, parent=None, move=None):
    self.cf = cf                      # Spielzustand
    self.player = cf.currentPlayer    # Spieler der am Zug ist
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

def playGame(cf):
  while cf.win == 0:
    possibleMoves = [i for i in range(len(cf.field)) if cf.field[i][0] == 0]
    if len(possibleMoves) == 0:
      return -1  # Unentschieden
    row = random.choice(possibleMoves)
    cf.chooseRow(row)
  return cf.win

def monteCarloStep(parentNode):
  # Choose a random row that is not already full
  if parentNode.untriedMoves:
    row = random.choice(parentNode.untriedMoves)
    parentNode.untriedMoves.remove(row)
  else:
    print('Parent node should habe untried moves.')
    return None

  node = MCTSNode(deepcopy(parentNode.cf), parent=parentNode, move=row)

  node.cf.chooseRow(row)
  result = playGame(deepcopy(node.cf))

  # game end
  node.visits = 1
  if result == -1:
    node.wins = 0.2
  else:
    node.wins = 1 if result == node.player else 0

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
            utc_value = (child.wins / child.visits) + (1.41 * math.sqrt(math.log(parent.visits) / child.visits))
            utc_values.append(utc_value)
    return utc_values

def calculateMoves(cf):
  startingNode = MCTSNode(deepcopy(cf)) #create root node with current game state

  for i in range(ITERATIONS):
    # Select a node to expand
    endNode = None
    currentNode = startingNode
    while len(currentNode.untriedMoves) == 0 and len(currentNode.children) > 0:
      utc_values = calculateChildUTC(currentNode)
      max_utc_index = utc_values.index(max(utc_values))
      currentNode = currentNode.children[max_utc_index]

    # Expand the node
    endNode = monteCarloStep(currentNode)
    
    # backpropagation
    if endNode is not None:
      result = endNode.wins
      currentNode = endNode.parent
      while currentNode is not None:
        if currentNode.player == endNode.player:
          currentNode.wins += result
        else:
          currentNode.wins += 1 - result
        currentNode.visits += 1
        currentNode = currentNode.parent
  
  # Calculate points for each move
  points = [0] * len(cf.field)
  for child in startingNode.children:
    points[child.move] = child.wins / child.visits if child.visits > 0 else 0

  return points
  
def chooseBestPath(cf, points, printOut):
  #prüfen in welcher Reihe tatsächlich gespielt werden kann
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: points[row] = -10000

  maxPoints = max(points)
  indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
  row = indizes[random.randint(0, len(indizes) - 1)]
  if printOut: print(f'monteCarlo - row: {row}, points: {points}')
  return row


def getMonteCarloTreeSearchMove(cf, printOut=True):
  if printOut: print('calculating ...')
  pointPaths = calculateMoves(cf)
  path = chooseBestPath(cf, pointPaths, printOut)
  return path