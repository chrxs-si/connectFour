import math
import random
import json
import time


class NeuralNetwork:
    save_interval = 0
    path = None

    def __init__(self):
        self.layers = []
        self.weights = []
        self.biases = []

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
        
    def initialize(self, layers):
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
        nn_str = ""
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
                output.append(self.softsign(x))
            self.outputs.append(output)
        return self.outputs[-1]
    
    def backward(self, targets, leaning_rate):
        if (len(targets) != len(self.biases[-1])):
            print("Fehler: Target-Anzahl ist nicht korrekt.")
            return

        errors = [None] * len(self.outputs)

        #Fehler in Ausgabeschicht
        errors[-1] = []
        for output in range (len(self.outputs[-1])):
            errors[-1].append((self.outputs[-1][output] - targets[output]) * self.softsign_derivative(self.outputs[-1][output]))

        errors[-1] = [(self.outputs[-1][i] - targets[i]) * self.softsign_derivative(self.outputs[-1][i])
                      for i in range(len(targets))]

        #Fehler in versteckten Shichten
        for layer in range(len(self.outputs) - 2, 0, -1):
            layer_errors = []
            for knot in range (len(self.outputs[layer])):
                error = 0
                for weight in range (len(errors[layer + 1])):
                    error += errors[layer + 1][weight] * self.weights[layer][knot][weight]
                error *= self.softsign_derivative(self.outputs[layer][knot])
                layer_errors.append(error)
            errors[layer] = layer_errors

        #Biases und Gewichte updaten
        for layer in range(len(self.weights)):
            for knot in range(len(self.weights[layer])):
                for weight in range(len(self.weights[layer][knot])):
                    self.weights[layer][knot][weight] -= leaning_rate * errors[layer + 1][weight] * self.outputs[layer][knot]
            for knot in range(len(self.biases[layer])):
                self.biases[layer][knot] -= leaning_rate * errors[layer + 1][knot]

    def train(self, inputs, targets, epochs, learning_rate):
        start_training_time = time.time()

        for epoch in range(epochs):
            total_error = 0
            for x, y in zip(inputs, targets):
                self.forward(x)
                self.backward(y, learning_rate)
                for i in range(len(y)):
                    total_error += (self.outputs[-1][i] - y[i])**2
            print(f"Epoch {epoch + 1}/{epochs}, Fehler: {total_error:.4f}")

            #neuronal network wird regelmäßig gespeichert
            if (self.path != None and self.save_interval != 0 and epoch % self.save_interval == 0):
                self.save(self.path)
                t = time.time() - start_training_time
                print("nn has been saved. Time: " + str(int(t)) + "s")
        t = time.time() - start_training_time
        print("finished training. Time: " + str(int(t)) + "s")
            