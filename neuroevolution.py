import random
from copy import deepcopy
import numpy as np
import math
import json
from game import connectFour
import os

class NeuralNetwork:
  save_interval = 0
  path = None

  def __init__(self):
    self.layers = []
    self.weights = []
    self.biases = []
    self.activationfunction = []

  def set_save_intervall(self, interval):
      self.save_interval = interval
      if (self.path == None):
          print("can't save the nn, due to no given path.")

  def set_path(self, path):
    self.path = path

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
      json.dump({'layers': self.layers, 'weights': self.weights, 'biases': self.biases, 'path': self.path, 'save_interval': self.save_interval}, file)

  def load(self, path):
    with open(path, "r") as file:
      daten = json.load(file)

    self.layers = daten['layers']
    self.weights = daten['weights']
    self.biases = daten['biases']
    self.path = daten['path']
    self.save_interval = daten['save_interval']
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
    self.nn.initialize([fieldwidth*fieldheight, 64, 32, fieldwidth], ['ReLU', 'ReLU', 'linear'])
  
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
  
  def mutate(self, mutationFactor):
    self.nn.weights = self.mutateLists(self.nn.weights, mutationFactor)

    self.nn.biases = self.mutateLists(self.nn.biases, mutationFactor)

    #weightsArray = np.array(self.nn.weights)
    #weightNoise = np.random.uniform(-mutationFactor, mutationFactor, size=weightsArray.shape)
    #self.nn.weights = (weightsArray * weightNoise).tolist()

    #biasesArray = np.array(self.nn.biases)
    #biasNoise = np.random.uniform(-mutationFactor, mutationFactor, size=biasesArray.shape)
    #self.nn.biases = (biasesArray * biasNoise).tolist()

  def mutateLists(self, input, mutationFactor):
      if isinstance(input, list):
          return [self.mutateLists(item, mutationFactor) for item in input]
      else:
          return input + random.uniform(-mutationFactor, mutationFactor)

  def calculateRow(self, field, printOutput=True):
    flattenField = [element for zeile in field for element in zeile]
    points = self.nn.forward(flattenField)

    #bereits volle Reihen aussortieren
    for row in range(len(field)):
      if field[row][0] != 0: points[row] = -10000

    if printOutput: print(f'neuroevolution points: {points}')
    maxPoints = max(points)
    indizes = [i for i, wert in enumerate(points) if wert == maxPoints]
    return indizes[random.randint(0, len(indizes) - 1)]



AGENTS_PER_GENERATION = 100
AGENT_FIGHT_ROUNDS = 10
KEEP_AGENTS = 5
MUTATION_FACTOR = 0.1

def playGame(agentA, agentB):
  cf = connectFour(False)
  win = 0
  while win == 0:
    if cf.currentPlayer == 1:
      cf.chooseRow(agentA.calculateRow(cf.field, False))
    else:
      cf.chooseRow(agentB.calculateRow(cf.field, False))
  return win

def agentFight(agentA, agentB):
  points = [0, 0]
  for round in range(AGENT_FIGHT_ROUNDS):
    win = playGame(agentA, agentB)
    if win == 1:
      points[0] += 1 
      points[1] -= 1
    elif win == 2:
      points[1] += 1 
      points[0] -= 1
  return points

def findBestAgents(agents):
  while len(agents) > KEEP_AGENTS:
    points = agentFight(agents[0], agents[1])
    agents.pop(points.index(max(points)))
  return agents

def developAgents(startAgents, generations):
  for gen in range(generations):
    print(f'generation {gen}')
    newAgent = Agent()
    newAgent.crossover(startAgents)
    agents = [newAgent]

    for i in range(AGENTS_PER_GENERATION): agents.append(deepcopy(newAgent))
    for a in agents: a.mutate(MUTATION_FACTOR)
  
    startAgents = findBestAgents(agents)

  bestAgent = Agent()
  bestAgent.crossover(startAgents)
  return bestAgent


path = 'saves/neuroevolutionAgent.json'

agent = Agent()

if (os.path.exists(path)):
    agent.load(path)
else:
    agent.initNN(7, 6)

agent = developAgents([agent], 100)

agent.save(path)