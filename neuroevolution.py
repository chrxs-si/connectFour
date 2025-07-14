import random
from copy import deepcopy
import numpy as np
import math
import json
from game import connectFour
import os
import threading
from rnd import getRandomMove

class NeuralNetwork:

  def __init__(self):
    self.layers = []
    self.weights = []
    self.biases = []
    self.activationfunction = []
    self.gen = 0

  # Aktivierungsfunktionen
  def softsign(self, x):
    return x / (1 + abs(x))
  
  def softsign_derivative(self, x):
    return 1 / (1 + abs(x))**2

  def sigmoid(self, x):
    if x > 709:
      return 1.0
    elif x < -709:
      return 0.0 
        
    return 1 / (1 + math.exp(-x))

  def sigmoid_derivative(self, x):
    sig = self.sigmoid(x)
    return sig * (1 - sig)
  
  def Tanh(self, x):
    a = math.pow(math.e, x)
    b = math.pow(math.e, -x)
    return (a-b)/(a+b)

  def ReLU(self, x):
    if x < 0:
      return 0
    else:
      return x
      
  def initialize(self, layers, activationfunction):
    self.activationfunction = activationfunction
    self.layers = layers
    self.initialize_weights()
    self.initialize_biases()
  
  def initialize_weights(self):
    for i in range(len(self.layers) - 1):
      weight_matrix = [[random.uniform(-1, 1) for _ in range(self.layers[i + 1])]
                        for _ in range(self.layers[i])]
      self.weights.append(weight_matrix)

  def initialize_biases(self):
    for i in range(len(self.layers) - 1):
      bias_vector = [random.uniform(-1, 1) for _ in range(self.layers[i + 1])]
      self.biases.append(bias_vector)

  def save(self, path):
    #nn_str = str(self.layers) + "\n-\n" + str(self.weights) + "\n-\n" + str(self.biases)
    with open(path, "w") as file:
      json.dump({'gen': self.gen, 'layers': self.layers, 'weights': self.weights, 'biases': self.biases, 'activationfunction': self.activationfunction}, file)

  def load(self, path):
    with open(path, "r") as file:
      daten = json.load(file)

    self.layers = daten['layers']
    self.weights = daten['weights']
    self.biases = daten['biases']
    self.activationfunction = daten['activationfunction']
    self.gen = daten['gen']
    print("neuronal network has been loaded.")

  def forward(self, input):
      if (len(input) != len(self.weights[0])):
          print("Fehler: Input-Anzahl ist nicht korrekt.")
          return
      
      self.outputs = [input]
      for layer in range(len(self.biases)):
        output = []
        for knot in range(len(self.biases[layer])):
          x = 0
          for weight in range(len(self.weights[layer])):
            x += self.outputs[layer][weight] * self.weights[layer][weight][knot]
          x += self.biases[layer][knot]
          if (self.activationfunction[layer] == 'ReLU'):
            x = self.ReLU(x)
          elif (self.activationfunction[layer] == 'Tanh'):
            x = self.Tanh(x)
          elif (self.activationfunction[layer] == 'softsign'):
            x = self.softsign(x)
          elif (self.activationfunction[layer] == 'sigmoid'):
            x = self.sigmoid(x)
          elif (self.activationfunction[layer] == 'linear'):
            pass
          output.append(x)
        self.outputs.append(output)
      return self.outputs[-1]



class Agent:
  strength = 0
  nn = None

  def __init__(self):
    pass

  def load(self, path):
    self.nn = NeuralNetwork()
    self.nn.load(path)

  def save(self, path):
    self.nn.save(path)
  
  def initNN(self, fieldwidth, fieldheight):
    self.nn = NeuralNetwork()
    self.nn.initialize([fieldwidth*fieldheight + fieldwidth, 64, 32, fieldwidth], ['ReLU', 'ReLU', 'linear'])
  
  def crossover(self, parents):
    self.nn = parents[0].nn

    allWeights = []
    for parent in parents: allWeights.append(parent.nn.weights)
    self.nn.weights = self.crossoverLists(allWeights)

    allBiases = []
    for parent in parents: allBiases.append(parent.nn.biases)
    self.nn.biases = self.crossoverLists(allBiases)

  def crossoverLists(self, elements):
    # Wenn alle Elemente Zahlen sind, bilde den Durchschnitt
    if all(isinstance(el, (int, float)) for el in elements):
      return sum(elements) / len(elements)

    # Andernfalls rekursiv über die Struktur iterieren
    result = []
    for i in range(len(elements[0])):  # Länge der ersten Liste auf dieser Ebene
      sub_elements = [el[i] for el in elements]
      result.append(self.crossoverLists(sub_elements))
    return result
  
  def mutate(self, mutationFactor, mutationRate):
    self.nn.weights = self.mutateLists(self.nn.weights, mutationFactor, mutationRate)
    self.nn.biases = self.mutateLists(self.nn.biases, mutationFactor * 0.5, mutationRate)

  def mutateLists(self, input, mutationFactor, mutationRate):
    if isinstance(input, list):
      return [self.mutateLists(item, mutationFactor, mutationRate) for item in input]
    else:
      if input > 3: input = 3
      elif input < -3: input = -3
      elif input == 0: input = random.uniform(-mutationFactor, mutationFactor)
      if np.random.rand() < mutationRate:
        return input + np.random.normal(0, mutationFactor)
      return input

  def calculateRows(self, field, errorCalculaions=0):
    flattenField = [element for zeile in field for element in zeile]
    for row in field: flattenField.append( -1 if row[-1] == 0 else (1 if row[0] != 0 else 0)) #-1 falls Spalte leer; 0 falls Spalte nicht voll; 1 falls Spalte voll
    points = self.nn.forward(flattenField)

    #bereits volle Reihen aussortieren
    if DEEP_DEBUG: print(f'errorCalculaions: {errorCalculaions}')
    for errors in range(errorCalculaions):
      points[points.index(max(points))] = -10000

    if DEEP_DEBUG: print(f'neuroevolution points: {points}')
    return points
  
  def getAgentMove(self, cf):
    row = self.calculateRows(cf.field)
    return row.index(max(row))




AGENTS_PER_GENERATION = 400
ADD_RANDOM_AGENTS = 10
AGENT_FIGHT_ROUNDS = 2
KEEP_AGENTS = 5 #mindestens 2
MUTATION_FACTOR = 0.1
MUTATION_RATE = 0.1

GENERATIONS = 20
DEBUG = True
DEEP_DEBUG = False
DEBUG_SCREEN = True

def playGame(agentA, agentB):

  cf = connectFour(DEBUG_SCREEN)

  if DEBUG_SCREEN: 
    def game_thread():
      cf.startScreen()
    gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
    gameThread.start()

  win = 0
  points = [0, 0]
  error = 0
  while win == 0 or win == -2:
    player = cf.currentPlayer
    if cf.currentPlayer == 1:
      row = agentA.calculateRows(cf.field, error)
      row = row.index(max(row))
      if DEEP_DEBUG: print(row)
      win = cf.chooseRow(row)
    else:
      row = agentB.calculateRows(cf.field, error)
      row = row.index(max(row))
      if DEEP_DEBUG: print(row)
      win = cf.chooseRow(row)

    #bewertung
    if win == -2: #ungültiger Zug
      points[player - 1] -= 10
      error += 1

    else:
      error = 0
      if win == 0: #noch kein Ergebnis
        cf.winner_lenght -= 1
        if cf.checkWinner(player) == player: #3-er Reihe
          points[player - 1] += 3
        cf.winner_lenght += 1

      if win != 0: #Spiel zu Ende
        for row in cf.field:
          if player in row and row[0] == 0: #für jede genutzte und nicht volle Reihe Punkte, außer für die erste genutze Reihe
            points[player - 1] += 5
        points[player - 1] -= 5

        if win == player: #gewonnen
          points[player - 1] += 10
          points[player % 2] -= 10
  
  if DEBUG: print(f'fight points: {points}')
  agentA.strength += points[0]
  agentB.strength += points[1]
  if DEEP_DEBUG: print(f'strength: agentA: {agentA.strength}, agentB: {agentB.strength}')

def agentFight(agentA, agentB, rounds):
  for round in range(rounds):
    playGame(agentB, agentA)
    playGame(agentA, agentB)

def findBestAgents(agents):
  for i in range(-1, len(agents) - 1):
    agentFight(agents[i], agents[i + 1], AGENT_FIGHT_ROUNDS)
  
  bestAgents = []
  for i in range(KEEP_AGENTS):
    bestAgent = agents[0]
    for agent in agents:
      if agent.strength > bestAgent.strength: bestAgent = agent
    bestAgents.append(agents.pop(agents.index(bestAgent)))

  if DEBUG:
    bestStrength = []
    for agent in bestAgents: bestStrength.append(agent.strength)
    print(f'bestStrength: {bestStrength}')

  return bestAgents

def developAgents(startAgents, generations):
  for gen in range(generations):
    print(f'generation {gen}')
    gen = startAgents[0].nn.gen
    newAgent = Agent()
    newAgent.crossover(startAgents)
    agents = [newAgent]

    for i in range(AGENTS_PER_GENERATION): 
      agents.append(deepcopy(newAgent))

    for i in range(ADD_RANDOM_AGENTS):
      new = Agent()
      new.initNN(7, 6)
      agents.insert(int(AGENTS_PER_GENERATION / ADD_RANDOM_AGENTS * i), new)

    for a in agents: 
      a.nn.gen = gen + 1
      a.strength = 0
      a.mutate(MUTATION_FACTOR, MUTATION_RATE)
  
    startAgents = findBestAgents(agents)

  print('done')
  bestAgent = Agent()
  bestAgent.crossover(startAgents)
  return bestAgent


base_path = os.path.dirname(__file__)
path = os.path.join(base_path, "saves", "neuroevolutionAgent4.json")

agent = Agent()

if (os.path.exists(path)):
    agent.load(path)
else:
    agent.initNN(7, 6)

agent = developAgents([agent], GENERATIONS)

agent.save(path)