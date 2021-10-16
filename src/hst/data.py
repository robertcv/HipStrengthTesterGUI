from collections import namedtuple

import numpy as np

MEAN_ROLLING_SIZE = 5

DataSet = namedtuple('DataSet', ['x', 'y'])
ReportData = namedtuple(
    'ReportData',
    ['max_force', 'max_angel', 'first_angle', 'second_angle']
)


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


def find_idx(array, value):
    return np.abs(array - value).argmin()


class Data:
    def __init__(self):
        self.raw_time = []
        self.raw_f = []
        self.offset = None

    @property
    def x(self) -> np.ndarray:
        return self.filtered().x

    @property
    def y(self) -> np.ndarray:
        return self.filtered().y

    def filtered(self):
        if len(self.raw_time) > MEAN_ROLLING_SIZE:
            return mean_filter(DataSet(x=self.raw_time, y=self.raw_f))
        return DataSet(x=self.raw_time, y=self.raw_f)

    def is_empty(self) -> bool:
        return not len(self.raw_time)

    def add_new(self, t: float, f: int):
        if self.offset is None:
            self.offset = t
        self.raw_time.append(t - self.offset)
        self.raw_f.append(f)

    def get_starter(self) -> float:
        data = self.filtered()
        # find time of greatest angle on graph -> max derivative
        t_max_angel = data.x[np.argmax(derivative_gradient(data).y)]
        # calculate time of the staring interval
        t_start_interval_1 = t_max_angel - 1
        t_start_interval_2 = t_max_angel - 0.5
        # select the interval, convert time into index
        starter_interval_values = data.y[find_idx(data.x, t_start_interval_1):
                                         find_idx(data.x, t_start_interval_2)]
        # calculate the starter value
        starter_y_value = np.mean(starter_interval_values) + \
                          3 * np.std(starter_interval_values)
        # starter point should be after starter interval
        data_after = DataSet(x=data.x[find_idx(data.x, t_start_interval_2):],
                             y=data.y[find_idx(data.x, t_start_interval_2):])
        # find graph value where it exceeds the starter value
        return data_after.x[np.argmax(data_after.y > starter_y_value)]

    def get_report(self, start_line: float) -> ReportData:
        data = self.filtered()
        start_idx = find_idx(data.x, start_line)

        max_force = np.max(data.y[start_idx:])
        max_force_angle = np.max(
            derivative_gradient(
                DataSet(x=data.x[start_idx:], y=data.y[start_idx:])
            ).y
        )

        # measure force angle 100ms after start
        first_force_idx = find_idx(data.x, start_line + 0.1)
        first_force_angle = \
            (data.y[first_force_idx] - data.y[start_idx]) / 0.1

        # measure force angle 200ms after start
        second_force_idx = find_idx(data.x, start_line + 0.2)
        second_force_angle = \
            (data.y[second_force_idx] - data.y[start_idx]) / 0.2

        return ReportData(max_force, max_force_angle,
                          first_force_angle, second_force_angle)

    def clear(self):
        self.raw_time = []
        self.raw_f = []
