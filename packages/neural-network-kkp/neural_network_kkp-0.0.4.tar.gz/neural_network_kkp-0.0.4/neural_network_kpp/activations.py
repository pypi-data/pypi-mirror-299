import numpy as np


class ReLU:
    def __call__(self, z):
        return np.maximum(0, z)


class Sigmoid:
    def __call__(self, z):
        return 1 / (1 + np.exp(-z))


class Tanh:
    def __call__(self, z):
        return np.tanh(z)
