import numpy as np


class DenseLayer:
    def __init__(self, input_size, output_size, activation_func, weights_initializer='random',
                 biases_initializer='zeros'):
        self.activation_func = activation_func

        if weights_initializer == 'random':
            self.weights = np.random.randn(input_size, output_size) * 0.01
        elif weights_initializer == 'xavier':
            self.weights = np.random.randn(input_size, output_size) * np.sqrt(1 / input_size)
        elif weights_initializer == 'he':
            self.weights = np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        elif weights_initializer == 'normal':
            self.weights = np.random.normal(0, 1, (input_size, output_size))
        else:
            raise ValueError(f"Unknown weights initializer: {weights_initializer}")

        if biases_initializer == 'zeros':
            self.biases = np.zeros((1, output_size))
        elif biases_initializer == 'ones':
            self.biases = np.ones((1, output_size))
        elif biases_initializer == 'normal':
            self.biases = np.random.normal(0, 1, (1, output_size))
        else:
            raise ValueError(f"Unknown biases initializer: {biases_initializer}")

    def forward(self, inputs):
        self.inputs = inputs
        self.z = np.dot(inputs, self.weights) + self.biases
        self.a = self.activation_func(self.z)
        return self.a
