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
    self.untriedMoves = []  # Noch nicht ausprobierte Züge
    for i in range(len(cf.field)):
      if cf.field[i][0] == 0:
        self.untriedMoves.append(i)


def monteCarloStep(parentNode, move=None, player=None, depth=0):
  node = MCTSNode(deepcopy(parentNode.cf), parent=parentNode, move=move)

  # Choose a random row that is not already full
  row = parentNode.untriedMoves[randint(0, len(parentNode.untriedMoves) - 1)]
  parentNode.untriedMoves.remove(row)

  win = node.cf.chooseRow(row)
  if win == 0:
    node.children.append(monteCarloStep(node, row, player, depth+1)) # Spiel noch nicht zu Ende
    node.wins += node.children[-1].wins
  elif win == -1:
    node.wins = 0 # unentschieden
  else:
    node.wins = 1 if win == player else -1 # Spieler gewinnt

  return node


def dicoverPaths(path):
    available_rows = [i for i in range(len(cf.field)) if cf.field[i][0] == 0 and path]
    row = available_rows[randint(0, len(available_rows) - 1)]


def findBestMove(cf, player):

  node = MCTSNode(deepcopy(cf))
  while len(node.untriedMoves) > 0:
    node.children.append(monteCarloStep(node, move=None, player=player, depth=0))
    node.wins += node.children[-1].wins
    node.visits += 1
    print(f'node.wins: {node.wins}, node.visits: {node.visits}, node.untriedMoves: {node.untriedMoves}')

      


    

def getMonteCarloTreeSearchMove(cf, prints=True):
  pointPaths = []
  path = 0
  if prints: print(path)

  return path

cf = connectFour(False)

findBestMove(cf, cf.currentPlayer)