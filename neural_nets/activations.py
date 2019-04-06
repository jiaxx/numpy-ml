from abc import ABC, abstractmethod
import numpy as np


class Activation(ABC):
    def __init__(self, **kwargs):
        super().__init__()

    @abstractmethod
    def fn(self, z):
        raise NotImplementedError

    @abstractmethod
    def grad(self, x, **kwargs):
        raise NotImplementedError


class Sigmoid(Activation):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Sigmoid"

    def fn(self, z):
        return 1 / (1 + np.exp(-z))

    def grad(self, x):
        return self.fn(x) * (1 - self.fn(x))


class ReLU(Activation):
    """
    ReLU units can be fragile during training and can "die". For example, a
    large gradient flowing through a ReLU neuron could cause the weights to
    update in such a way that the neuron will never activate on any datapoint
    again. If this happens, then the gradient flowing through the unit will
    forever be zero from that point on. That is, the ReLU units can
    irreversibly die during training since they can get knocked off the data
    manifold.

    For example, you may find that as much as 40% of your network can be "dead"
    (i.e. neurons that never activate across the entire training dataset) if
    the learning rate is set too high. With a proper setting of the learning
    rate this is less frequently an issue.

    - Andrej Karpathy
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "ReLU"

    def fn(self, z):
        return np.clip(z, 0, np.inf)

    def grad(self, x):
        return (x > 0).astype(int)


class Tanh(Activation):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Tanh"

    def fn(self, z):
        return np.tanh(z)

    def grad(self, x):
        return 1 - np.tanh(x) ** 2


class Linear(Activation):
    def __init__(self, slope=1):
        self.slope = slope
        super().__init__()

    def __str__(self):
        return "Linear"

    def fn(self, z):
        return self.slope * z

    def grad(self, x):
        return self.slope * np.ones_like(x)


class Softmax(Activation):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Softmax"

    def fn(self, z):
        # center data to avoid overflow
        e_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return e_z / e_z.sum(axis=1, keepdims=True)

    def grad(self, z):
        pass

    #      p = self.fn(z)
    #      gr = np.outer(p, 1 - p)
    #      np.fill_diagonal(gr, [pi * (1 - pi) for pi in p])
    #      return gr