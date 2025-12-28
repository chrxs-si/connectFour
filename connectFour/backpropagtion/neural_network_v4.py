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
    x = np.clip(x, -709, 709)
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    return 1 - np.tanh(x) ** 2

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_derivative(x, alpha=0.01):
    return np.where(x > 0, 1.0, alpha)

def softmax(x):
    x = x - np.max(x, axis=-1, keepdims=True)
    exps = np.exp(x)
    return exps / np.sum(exps, axis=-1, keepdims=True)

#endregion

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
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

    def save(self, path=None):
        if path == None: path = self.path
        with open(path, "w") as file:
            json.dump({"layers": self.layers, 
                       "weights": self.weights, 
                       "biases": self.biases, 
                       "init_method": self.init_method, 
                       "activation_function": self.activation_function,
                       "output_activation_function": self.output_activation_function
                       }, file, cls=NumpyEncoder)

    def load(self, path=None):
        if path == None: path = self.path
        with open(path, "r") as file:
            data = json.load(file)

        self.layers = data['layers']
        self.weights = [np.array(w) for w in data['weights']]
        self.biases = [np.array(b) for b in data['biases']]
        self.init_method = data['init_method']
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
            self.weights.append(layer_weights)

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
            self.biases.append(layer_biases)

    def activation(self, x, function):
        return globals()[function](x)

    def activation_derivative(self, x, function):
        return globals()[function + "_derivative"](x)

    def forward(self, input):
        a = np.array(input)
        self.outputs = [a]
        self.zs = []

        for i in range(len(self.weights) - 1):
            z = self.weights[i] @ a + self.biases[i]
            self.zs.append(z)
            a = self.activation(z, self.activation_function)
            self.outputs.append(a)

        # Output-Layer
        z = self.weights[-1] @ a + self.biases[-1]
        self.zs.append(z)
        a = globals()[self.output_activation_function](z)
        self.outputs.append(a)

        return a

    def backward(self, targets):
        y = np.array(targets)

        delta = self.outputs[-1] - y
        deltas = [delta]

        for l in range(len(self.weights) - 1, 0, -1):
            z = self.zs[l - 1]
            deriv = globals()[self.activation_function + "_derivative"](z)
            delta = self.weights[l].T @ deltas[0] * deriv
            deltas.insert(0, delta)

        grad_w = []
        grad_b = []

        for l in range(len(self.weights)):
            grad_w.append(np.outer(deltas[l], self.outputs[l]))
            grad_b.append(deltas[l])

        return grad_w, grad_b   

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
                grad_w_sum = [np.zeros_like(w) for w in self.weights]
                grad_b_sum = [np.zeros_like(b) for b in self.biases]

                for input, target in zip(batch_inputs, batch_targets):
                    self.forward(input)
                    grad_w, grad_b = self.backward(target)

                    for l in range(len(self.weights)):
                        grad_w_sum[l] += grad_w[l]
                        grad_b_sum[l] += grad_b[l]

                    pred = self.outputs[-1]
                    batch_loss += -np.sum(target * np.log(pred + 1e-9))

                batch_len = len(batch_inputs)

                for l in range(len(self.weights)):
                    self.weights[l] -= learning_rate * (grad_w_sum[l] / batch_len)
                    self.biases[l] -= learning_rate * (grad_b_sum[l] / batch_len)

                total_loss += batch_loss / len(batch_inputs)

                # if self.info: print(f"epoch {epoch + 1} -> batch {batch + batch_size}/{len(inputs)}")

                if training_id not in self.training_ids: return #Abbrechen falls der thread abgebrochen wurde
            
            if self.info: print(f"epoch {epoch + 1}/{epochs}, loss: {total_loss:.4f}")

            #Speichern
            if (self.path != None):
                self.save(self.path)


def getNeuralNetworkMove(cf):
    nn = NeuralNetwork()
    nn.load("connectFour/backpropagtion/nn_models/nn_354.json")

    board = []
    for row in cf.field:
        for cell in row:
            board.append(cell)

    normalized_board, _ = normalize_board(board + ["0"])  # Dummy best_row value
    prediction = nn.forward(normalized_board)
    return int(np.argmax(prediction))


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
    (data_base_path + "training_data_depth_10_(0).csv", 59250),
    (data_base_path + "training_data_depth_10_(1).csv", 25900),
    (data_base_path + "training_data_depth_10_(2).csv", 24100),
    (data_base_path + "training_data_depth_10_(3).csv", 43800),
    (data_base_path + "training_data_depth_10_(4).csv", 41800),
    (data_base_path + "training_data_depth_10_(5).csv", 54800),
    (data_base_path + "training_data_depth_10_(6).csv", 57000),
    ]

starting_path = 0
save_index = 322 # last save index. If last is nn_2.json, set to 2
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

save_counter = 0
while False:

    print("loading neural network from: " + nn_base_path + f"nn_{save_index}.json")
    nn.load(nn_base_path + f"nn_{save_index}.json")

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

    input_data = np.array(input_data, dtype=np.float32)
    target_data = np.array(target_data, dtype=np.float32)

    nn.train(
        inputs=input_data,
        targets=target_data,
        epochs=10,
        learning_rate=0.001,
        batch_size=32,
    )

    lines_starting_at = 0
    save_counter = (save_counter + 1) % len(data_paths)
    if save_counter == 0:
        save_index += 1

    nn.save(nn_base_path + f"nn_{save_index}.json")
    print("saved neural network to: " + nn_base_path + f"nn_{save_index}.json")
    print("trained with data from: " + path + " lines: " + str(lines))
    print("------------------------------------------------------------\n")

    current_data_index = (current_data_index + 1) % len(data_paths)