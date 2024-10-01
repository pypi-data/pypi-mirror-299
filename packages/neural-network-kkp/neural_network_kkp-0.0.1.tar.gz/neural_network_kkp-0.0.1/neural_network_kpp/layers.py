import numpy as np


class DenseLayer:
    def __init__(self, input_size, output_size, activation_func):
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.biases = np.zeros((1, output_size))
        self.activation_func = activation_func

    def forward(self, inputs):
        self.inputs = inputs
        self.z = np.dot(inputs, self.weights) + self.biases
        self.a = self.activation_func(self.z)
        return self.a


class ReLU:
    def __call__(self, z):
        return np.maximum(0, z)


class Sigmoid:
    def __call__(self, z):
        return 1 / (1 + np.exp(-z))


class Tanh:
    def __call__(self, z):
        return np.tanh(z)