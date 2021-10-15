from typing import Optional

from hst.data import Data

import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class PlotsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.left_plot = PlotWidget()
        self.right_plot = PlotWidget()

        v = QHBoxLayout()
        v.setContentsMargins(30, 15, 30, 30)
        v.addWidget(self.left_plot)
        v.addSpacing(30)
        v.addWidget(self.right_plot)
        self.setLayout(v)

    def update_plots(self, left_data: Data, right_data: Data):
        self.left_plot.update_plot(left_data)
        self.right_plot.update_plot(right_data)


class PlotWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.plot_item = self.plot()
        self.start_line = None  # type: Optional[pg.InfiniteLine]

        self.setMouseEnabled(False, False)  # disable moving plot with mouse
        self.setMenuEnabled(False)  # disable right click menu
        self.hideButtons()  # hide "A" button in bottom left corner

    def add_target_line(self, target):
        self.start_line = pg.InfiniteLine(
            pos=target,
            angle=90,
            pen=pg.mkPen(color="k", style=Qt.DashLine)
        )
        self.plotItem.vb.addItem(self.start_line)

    def update_plot(self, data: Data):
        self.plot_item.setData(data.x, data.y)

    def clear_graph(self):
        self.plot_item.setData([], [])
