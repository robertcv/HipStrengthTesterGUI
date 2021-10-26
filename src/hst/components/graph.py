from typing import Optional

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from hst.data import Data

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class PlotsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.left_plot = PlotWidget()
        self.right_plot = PlotWidget()

        v = QHBoxLayout()
        v.setContentsMargins(30, 15, 30, 15)
        v.addWidget(self.left_plot)
        v.addSpacing(30)
        v.addWidget(self.right_plot)
        self.setLayout(v)

    def update_plots(self, left_data: Data, right_data: Data):
        self.left_plot.update_plot(left_data)
        self.right_plot.update_plot(right_data)

    def clear(self):
        self.left_plot.clear_graph()
        self.right_plot.clear_graph()


class PlotWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.plot_item = self.plot()
        self.start_line = None  # type: Optional[pg.InfiniteLine]

        self.setMouseEnabled(True, False)  # disable moving plot with mouse
        self.setMenuEnabled(False)  # disable right click menu
        self.hideButtons()  # hide "A" button in bottom left corner

    def add_starter_line(self, start_pos: float):
        if self.start_line is None:
            self.start_line = pg.InfiniteLine(
                pos=start_pos,
                angle=90,
                pen=pg.mkPen(color="k", style=Qt.DashLine),
                movable=True,
            )
            self.plotItem.vb.addItem(self.start_line)

    def get_target_line(self) -> Optional[float]:
        if self.start_line is not None:
            return self.start_line.value()

    def update_plot(self, data: Data):
        self.plot_item.setData(data.x, data.y)

    def clear_graph(self):
        self.plot_item.setData([], [])
        if self.start_line is not None:
            self.plotItem.vb.removeItem(self.start_line)
            self.start_line = None
        self.plotItem.vb.setRange(xRange=(0, 1), yRange=(0, 1), padding=0, disableAutoRange=False)
        self.plotItem.vb.enableAutoRange(axis='x')
