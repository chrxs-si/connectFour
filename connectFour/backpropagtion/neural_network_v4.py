import math
import json
import numpy as np
from PIL import Image
import random
import threading
import os
from itertools import islice

#region activtion functions
def sigmoid(x):
    if x > 709:
        return 1.0
    elif x < -709:
        return 0.0 
    return float(1 / (1 + np.exp(-x)))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    return float(np.maximum(0, x))

def relu_derivative(x):
    return float(np.where(x > 0, 1, 0))

def tanh(x):
    return float(np.tanh(x))

def tanh_derivative(x):
    return float(1 - np.tanh(x) ** 2)

def leaky_relu(x, alpha=0.01):
    return float(np.where(x > 0, x, alpha * x))
    
def leaky_relu_derivative(x, alpha=0.01):
    return 1.0 if x > 0 else alpha

def softmax(x):
    exps = np.exp(x - np.max(x))
    return exps / np.sum(exps, axis=-1, keepdims=True)

#endregion

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Umwandlung von NumPy-Array in Liste
        return super(NumpyEncoder, self).default(obj)

class NeuralNetwork:
    def __init__(self):
        self.path = None
        self.info = True
        self.training_ids = []
        self.weights = []
        self.biases = []
        self.outputs = []

    def initialize(self, layers, init_method='random', activation_function="leaky_relu", output_activation_function="softmax"):
        self.activation_function = activation_function
        self.output_activation_function = output_activation_function
        self.layers = layers
        self.init_method = init_method
        self.initialize_weights()
        self.initialize_biases()

    def set_path(self, path):
        self.path = path

    def save(self):
        if self.path == None: print("no path set"); return
        self.save(self.path)

    def save(self, path):
        with open(path, "w") as file:
            json.dump({"layers": self.layers, 
                       "weights": self.weights, 
                       "biases": self.biases, 
                       "init_method": self.init_method, 
                       "activation_function": self.activation_function,
                       "output_activation_function": self.output_activation_function
                       }, file, cls=NumpyEncoder)

    def load(self):
        if self.path == None: print("no path set"); return
        return self.load(self.path)

    def load(self, path=None):
        if path == None: path = self.path
        with open(path, "r") as file:
            data = json.load(file)

        self.layers = data['layers']
        self.weights = data['weights']
        self.biases = data['biases']
        self.init_method = data['activation_function']
        self.activation_function = data['activation_function']
        self.output_activation_function = data['output_activation_function']
        print("neuronal network has been loaded.")
        return self
 
    def initialize_weights(self):
        for i in range(len(self.layers) - 1):
            shape = (self.layers[i + 1], self.layers[i])
            if self.init_method == 'random':
                layer_weights = np.random.rand(*shape) * 0.01
            elif self.init_method == 'xavier':
                layer_weights = np.random.randn(*shape) * np.sqrt(1.0 / self.layers[i])
            elif self.init_method == 'he':
                layer_weights = np.random.randn(*shape) * np.sqrt(2.0 / self.layers[i])
            else:
                raise ValueError("unknown method to initialize")
            self.weights.append(layer_weights.tolist())

    def initialize_biases(self):
        for i in range(len(self.layers) - 1):
            shape = (self.layers[i + 1])
            if self.init_method == 'random':
                layer_biases = np.random.rand(shape) * 0.01
            elif self.init_method == 'xavier':
                layer_biases = np.zeros(shape)
            elif self.init_method == 'he':
                layer_biases = np.zeros(shape) 
            else:
                raise ValueError("unknown method to initialize")
            self.biases.append(layer_biases.tolist())

    def activation(self, x, function):
        return globals()[function](x)

    def activation_derivative(self, x, function):
        return globals()[function + "_derivative"](x)

    def forward (self, input):
        #if (len(input) != len(self.layers[0])):
        #    raise ValueError("input and first layer are not the same size.")

        self.outputs = [input]
        self.zs = [] # leaky relu Pre-Aktivierungen (z = Wx + b)
        #Berechnen der Input-Layer
        layer_output = []
        layer_zs = []
        for neuron in range(len(self.biases[0])):
            z = 0
            #Muliplizieren aus vorheringen Layer mit den Gewichten
            for weight in range(len(self.weights[0][neuron])):
                z += self.outputs[0][weight] * self.weights[0][neuron][weight]
            #Addieren des Bias
            z += self.biases[0][neuron]

            layer_zs.append(z)
            layer_output.append(self.activation(z, self.activation_function))#Hier ist es möglich die Aktivierungsfunktion für den ersten layer zu ändern
        self.zs.append(layer_zs)
        self.outputs.append(layer_output)

        #Sollte hier die gleiche Aktivierungsfunktion für alle Layer (inklusive input und output Layer) benutzt werden:
        #Die entsprechende Berechnung (input und output layer) kann gelöscht werden, hier kann range(1, len(self.biases) - 1) mit range(len(self.biases)) ersetzt werden
        #Berechnen der Hidden-Layer
        for layer in range(1, len(self.biases) - 1):
            layer_output = []
            layer_zs = []
            for neuron in range(len(self.biases[layer])):
                z = 0
                #Muliplizieren aus vorheringen Layer mit den Gewichten
                for weight in range(len(self.weights[layer][neuron])):
                    z += self.outputs[layer][weight] * self.weights[layer][neuron][weight]
                #Addieren des Bias
                z += self.biases[layer][neuron]
                layer_zs.append(z)
                layer_output.append(self.activation(z, self.activation_function))#Hier ist es möglich die Aktivierungsfunktion für die hidden layer zu ändern
            self.zs.append(layer_zs)
            self.outputs.append(layer_output)

        #Berechnen der Output-Layer
        logits = []
        for neuron in range(len(self.biases[-1])):
            z = 0
            for weight in range(len(self.weights[-1][neuron])):
                z += self.outputs[-1][weight] * self.weights[-1][neuron][weight]
            z += self.biases[-1][neuron]
            logits.append(z)

        self.zs.append(logits)

        # Softmax einmal auf den gesamten Vektor
        layer_output = softmax(np.array(logits)).tolist()
        self.outputs.append(layer_output)

        return self.outputs[-1]

    def backward(self, targets, learning_rate):
        if len(targets) != len(self.biases[-1]):
            raise ValueError("target and output layer are not the same size.")

        # Berechnung des Fehlers für die Output-Schicht
        delta = np.array(self.outputs[-1]) - np.array(targets)
        deltas = [delta]

        # Backpropagation durch die versteckten Schichten
        for layer in range(len(self.weights) - 1, 0, -1):
            error = np.dot(np.array(self.weights[layer]).T, deltas[0])
            z = np.array(self.zs[layer - 1])
            deriv = np.array([self.activation_derivative(v, self.activation_function) for v in z])
            delta = error * deriv
            deltas.insert(0, delta)

        # Gewichte und Biases aktualisieren
        for layer in range(len(self.weights)):
            weight_updates = np.outer(deltas[layer], self.outputs[layer])
            self.weights[layer] = np.array(self.weights[layer]) - learning_rate * weight_updates
            self.biases[layer] = np.array(self.biases[layer]) - learning_rate * deltas[layer]         

    def train(self, inputs, targets, epochs, learning_rate=0.002, batch_size=32, training_id=0):
        self.training_ids.append(training_id)

        #Iterieren durch alle epochen
        for epoch in range(epochs):
            total_loss = 0

            #Daten shufflen für jede Epoche um anschließend zufällige batches zu erstellen
            combined_lists = list(zip(inputs, targets))
            random.shuffle(combined_lists)
            shuffled_inputs, shuffled_targets = zip(*combined_lists)

            #Iterieren durch jeden Batch
            for batch in range(0, len(inputs), batch_size):
                #Batch aus den shuffled Daten erstellen
                batch_inputs = shuffled_inputs[batch:batch+batch_size]
                batch_targets = shuffled_targets[batch:batch+batch_size]

                batch_loss = 0

                #Iterieren durch alle Daten des Batches
                for input, target in zip(batch_inputs, batch_targets):
                    self.forward(input)
                    self.backward(target, learning_rate)
                    loss = 0.0
                    for j in range(len(self.outputs[-1])):
                        loss -= target[j] * math.log(self.outputs[-1][j] + 1e-9)
                    batch_loss += loss

                total_loss += batch_loss / len(batch_inputs)

                if self.info: print(f"epoch {epoch + 1} -> batch {batch + batch_size}/{len(inputs)}")

                if training_id not in self.training_ids: return #Abbrechen falls der thread abgebrochen wurde
            
            if self.info: print(f"epoch {epoch + 1}/{epochs}, loss: {total_loss:.4f}")

            #Speichern
            if (self.path != None):
                self.save(self.path)


def getNeuralNetworkMove(cf):
    nn = NeuralNetwork()
    nn.load("connectFour/backpropagtion/nn_models/nn_2.json")

    board = []
    for row in cf.field:
        for cell in row:
            board.append(cell)

    normalized_board, _ = normalize_board(board + ["0"])  # Dummy best_row value
    prediction = nn.forward(normalized_board)
    return prediction.index(max(prediction))


def normalize_board(input):
    board = input[:42]
    best_row = input[42]
    normalized_best_row = [0] * 7
    normalized_best_row[int(best_row)] = 1

    normalized_board = []
    for cell in board:
        cell = int(cell)
        if cell == 0:
            normalized_board.extend([0, 0])
        elif cell == 1:
            normalized_board.extend([1, 0])
        elif cell == 2:
            normalized_board.extend([0, 1])

    return normalized_board, normalized_best_row

# initialize neural network

nn = NeuralNetwork()

data_base_path = "connectFour/backpropagtion/training_data/"
data_paths = [
    (data_base_path + "training_data_depth_10_(1).csv", 25900),
    (data_base_path + "training_data_depth_10_(2).csv", 24100),
    (data_base_path + "training_data_depth_10_(3).csv", 43800),
    (data_base_path + "training_data_depth_10_(4).csv", 41800),
    (data_base_path + "training_data_depth_10_(5).csv", 54800),
    (data_base_path + "training_data_depth_10_(6).csv", 57000),
    ]

starting_path = 0
save_index = 20 # new save index. If last is nn_2.json, set to 3
nn_base_path = "connectFour/backpropagtion/nn_models/"

loading_nn_path = "connectFour/backpropagtion/nn_models/nn_6.json"
new_nn_path = "connectFour/backpropagtion/nn_models/nn_7.json"
data_path = "connectFour/backpropagtion/training_data/training_data_depth_10_(6).csv"
lines_starting_at = 0

# initialize and save a new neural network
if False:
    nn.initialize(
        layers=[84, 128, 64, 7],
        init_method="he",
        activation_function="leaky_relu",
        output_activation_function="softmax"
    )

    nn.set_path(loading_nn_path)

    nn.save(loading_nn_path)

# load an existing neural network
current_data_index = starting_path
while True:

    print("loading neural network from: " + nn_base_path + f"nn_{save_index - 1}.json")
    nn.load(nn_base_path + f"nn_{save_index - 1}.json")

    # load data  
    data = []
    path, lines = data_paths[current_data_index]
    print ("loading data from: " + path + " with lines: " + str(lines))

    with open(path, "r") as datei:
        for zeile in islice(datei, lines_starting_at, lines):
            data.append(zeile.strip())

    input_data = []
    target_data = []
    for i in range(len(data)):
         
        normalized_board, normalized_best_row = normalize_board(data[i].replace(",", ""))
        input_data.append(normalized_board)
        target_data.append(normalized_best_row)

    nn.path = nn_base_path + f"nn_{save_index}.json"

    nn.train(
        inputs=input_data,
        targets=target_data,
        epochs=5,
        learning_rate=0.005,
        batch_size=16,
    )

    nn.save(nn_base_path + f"nn_{save_index}.json")
    print("saved neural network to: " + nn_base_path + f"nn_{save_index}.json")
    print("trained with data from: " + path + " lines: " + str(lines))
    print("------------------------------------------------------------\n")

    lines_starting_at = 0
    save_index += 1
    current_data_index = (current_data_index + 1) % len(data_paths)