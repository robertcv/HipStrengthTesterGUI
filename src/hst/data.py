from collections import namedtuple

import numpy as np

MEAN_ROLLING_SIZE = 5

DataSet = namedtuple('DataSet', ['x', 'y'])


def derivative_gradient(data: DataSet) -> DataSet:
    x = np.array(data.x)
    y = np.array(data.y)
    return DataSet(x=x, y=np.gradient(y, x))


def rolling_window(y: np.ndarray, n: int):
    y = np.array(y)
    shape = y.shape[:-1] + (y.shape[-1] - n + 1, n)
    strides = y.strides + (y.strides[-1],)
    return np.lib.stride_tricks.as_strided(y, shape=shape, strides=strides)


def reduce_x(x: np.ndarray, n: int):
    x = np.array(x)
    edge = n // 2
    if n % 2 == 1:
        return x[edge:-edge]
    else:
        return x[edge:(-edge + 1)]


def mean_filter(data: DataSet) -> DataSet:
    x = np.array(data.x)
    y = np.array(data.y)
    w = rolling_window(y, MEAN_ROLLING_SIZE)
    x = reduce_x(x, MEAN_ROLLING_SIZE)
    return DataSet(x=x, y=np.mean(w, axis=1))


class Data:
    def __init__(self):
        self.raw_x = []
        self.raw_y = []

    @property
    def x(self):
        return np.array(self.raw_x)

    @property
    def y(self):
        return np.array(self.raw_y)

    def add_new(self, x, f):
        self.raw_x.append(x)
        self.raw_y.append(f)

    def calc_stats(self):
        pass

    def clear(self):
        self.raw_x = []
        self.raw_y = []
