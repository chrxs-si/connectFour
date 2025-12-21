import math
import json
import numpy as np
from PIL import Image
import random
import threading
import os

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
    return float(np.where(x > 0, 1, alpha))

def softmax(x):
    exps = np.exp(x - np.max(x))
    return exps / np.sum(exps, axis=0, keepdims=True)

def softmax_derivative(x):
    s = softmax(x)
    return s * (1 - s) 

#endregion

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Umwandlung von NumPy-Array in Liste
        return super(NumpyEncoder, self).default(obj)

class NeuralNetworkManager:
    def __init__(self):
        self.nn = NeuralNetwork()
        self.train_threads = []
        self.inputs = None
        self.targets = None

        active = True
        while active:
            command = input("nnM>")
            command_split = command.split()

            if (command_split[0] == "help"):
                print("""
                        init [layer] # initializes network; layer e.g. 'init 1 3 2'
                        load [path] # loads network
                        train load [training_data_path] # loads trainings data
                        train start [epochs] # starts training with loaded data\n
                        train stop [thread_id=0] # stops training
                        train get # prints out all training id's
                        set_init [init_method] # sets init method
                        set_activation [activation_function] # sets set activation function
                        set_path [path] # sets save path
                        save # saves network
                        save [path] # saves network
                        info [True/False] # activate/deactivate output information
                        forward [path]
                        forward [input]
                        """)
            elif (command_split[0] == "init"):
                layer = []
                try:
                    for l in range(1, len(command_split)):
                        layer.append(int(command_split[l]))
                except:
                    print("wrong layer input. try e.g: 'init 3 5 4'")
                else:
                    self.initialize(layer)
            elif (command_split[0] == "load"):
                self.nn.path = command_split[1]
                print(f"set path {command_split[1]}")
            elif(command_split[0] == "train"):
                if (command_split[1] == "load"):
                    self.load_training_data(command_split[2])
                elif (command_split[1] == "start"):
                    self.start_training(int(command_split[2]))
                elif (command_split[1] == "stop"):
                    pass



    def initialize(self, layers, init_method='random', activation_function="leaky_relu"):
        self.nn.initialize(layers, init_method, activation_function)

    def set_init_method(self, init_method):
        self.nn.init_method = init_method

    def set_activation_function(self, activation_function):
        self.nn.activation_function = activation_function

    def set_save_path(self, path):
        self.nn.set_path(path)

    def save(self):
        if self.nn.path is None: print("no path set"); return
        self.save(self.nn.path)

    def save(self, path):
        with open(path, "w") as file:
            json.dump({"layers": self.nn.layers, 
                       "weights": self.nn.weights, 
                       "biases": self.nn.biases, 
                       "init_method": self.nn.init_method, 
                       "activation_function": self.nn.activation_function,
                       }, file, cls=NumpyEncoder)

    def load(self, path):

        with open(path, "r") as file:
            data = json.load(file)

        self.nn.layers = data['layers']
        self.nn.weights = data['weights']
        self.nn.biases = data['biases']
        self.nn.init_method = data['activation_function']
        self.nn.activation_function = data['activation_function']
        print("neuronal network has been loaded.")

    def load_training_data(self, path):
        with open(path, "r") as file:
            data = json.load(file)

        self.inputs = data[0]
        self.targets = data[1]

        print("loaded training data")

    def start_training(self, epochs, learning_rate=0.01, batch_size=32):
        if self.inputs == None or self.targets == None: print("no data loaded"); return
        return self.start_training(self.inputs, self.targets, epochs, learning_rate, batch_size)

    def start_training(self, path, epochs, learning_rate=0.01, batch_size=32):
        self.load_training_data(path)
        return self.start_training(self.inputs, self.targets, epochs, learning_rate, batch_size)

    def start_training(self, inputs, targets, epochs, learning_rate=0.01, batch_size=32):
        train_thread = threading.Thread(target=self.nn.train, args=(inputs, targets, epochs, learning_rate, batch_size, len(self.train_threads)), daemon=False)
        train_thread.start()

        self.train_threads.append(train_thread)
        print("started training")
        return len(self.train_threads) - 1

    def stop_all_trainings(self):
        pass

    def stop_training(self, thread_id=0):
        for i in range(self.train_threads):
            if not self.train_threads[i].is_alive(): self.train_threads.pop(i); i -= 1

        if thread_id >= len(self.train_threads): print("could not find thread_id"); return

        print(f"stopping the training {thread_id}...")
        self.nn.training_ids.remove(thread_id)
        self.train_threads[thread_id].join()
        self.train_threads.pop(thread_id)
        print("stopped training " + str(thread_id))

    def get_thread_ids(self):
        for i in range(self.train_threads):
            if not self.train_threads[i].is_alive(): self.train_threads.pop(i); i -= 1
        return self.train_threads

    def set_info(self, active):
        self.nn.info = active

    def forward(self, input):
        out = self.nn.forward(input)
        print(out)
        return out


class NeuralNetwork:
    def __init__(self):
        self.path = None
        self.info = True
        self.training_ids = []
        self.weights = []
        self.biases = []
        self.outputs = []

    def initialize(self, layers, init_method='random', activation_function="leaky_relu"):
        self.activation_function = activation_function
        self.layers = layers
        self.init_method = init_method
        self.initialize_weights()
        self.initialize_biases()

    def set_path(self, path):
        self.path = path
 
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
        #Berechnen der Input-Layer
        layer_output = []
        for neuron in range(len(self.biases[0])):
            x = 0
            #Muliplizieren aus vorheringen Layer mit den Gewichten
            for weight in range(len(self.weights[0][neuron])):
                x += self.outputs[0][weight] * self.weights[0][neuron][weight]
            #Addieren des Bias
            x += self.biases[0][neuron]
            layer_output.append(self.activation(x, self.activation_function))#Hier ist es möglich die Aktivierungsfunktion für den ersten layer zu ändern
        self.outputs.append(layer_output)

        #Sollte hier die gleiche Aktivierungsfunktion für alle Layer (inklusive input und output Layer) benutzt werden:
        #Die entsprechende Berechnung (input und output layer) kann gelöscht werden, hier kann range(1, len(self.biases) - 1) mit range(len(self.biases)) ersetzt werden
        #Berechnen der Hidden-Layer
        for layer in range(1, len(self.biases) - 1):
            layer_output = []
            for neuron in range(len(self.biases[layer])):
                x = 0
                #Muliplizieren aus vorheringen Layer mit den Gewichten
                for weight in range(len(self.weights[layer][neuron])):
                    x += self.outputs[layer][weight] * self.weights[layer][neuron][weight]
                #Addieren des Bias
                x += self.biases[layer][neuron]
                layer_output.append(self.activation(x, self.activation_function))#Hier ist es möglich die Aktivierungsfunktion für die hidden layer zu ändern
            self.outputs.append(layer_output)

        #Berechnen der Output-Layer
        layer_output = []
        for neuron in range(len(self.biases[-1])):
            x = 0
            #Muliplizieren aus vorheringen Layer mit den Gewichten
            for weight in range(len(self.weights[-1][neuron])):
                x += self.outputs[-1][weight] * self.weights[-1][neuron][weight]
            #Addieren des Bias
            x += self.biases[-1][neuron]
            layer_output.append(self.activation(x, self.activation_function)) #Hier ist es möglich die Aktivierungsfunktion für den letzten layer zu ändern
        self.outputs.append(layer_output)

        return self.outputs[-1]

    def backward(self, targets, learning_rate):
        if len(targets) != len(self.biases[-1]):
            raise ValueError("target and output layer are not the same size.")

        # Berechnung des Fehlers für die Output-Schicht
        output_errors = np.array(self.outputs[-1]) - np.array(targets)
        deltas = [output_errors * np.array([self.activation_derivative(x, self.activation_function) for x in self.outputs[-1]])]

        # Backpropagation durch die versteckten Schichten
        for layer in range(len(self.weights) - 1, 0, -1):
            error = np.dot(np.array(self.weights[layer]).T, deltas[0])
            delta = error * np.array([self.activation_derivative(x, self.activation_function) for x in self.outputs[layer]])
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
                    for j in range(len(self.outputs[-1])):
                        batch_loss += (self.outputs[-1][j] - target[j])**2

                total_loss += batch_loss / len(batch_inputs)

                if self.info: print(f"epoch {epoch + 1} -> batch {batch + batch_size}/{len(inputs)}")

                if training_id not in self.training_ids: return #Abbrechen falls der thread abgebrochen wurde
            
            if self.info: print(f"epoch {epoch + 1}/{epochs}, loss: {total_loss:.4f}")

            #Speichern
            if (self.path != None):
                self.save(self.path)


def normalize_board(input):
    board = input[:42]
    winner = input[42]

    if winner == -1:
        board = [-x for x in board]
        target = [1]
    elif winner == 1:
        target = [1]
    else:
        target = [0]

nn = NeuralNetwork()

nn.initialize(
    layers=[42, 64, 64, 1],
    init_method="he",
    activation_function="leaky_relu"
)