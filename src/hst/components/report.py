from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QAbstractItemView, QHBoxLayout, QHeaderView,
                             QTableWidget, QTableWidgetItem, QWidget)

from hst.data import ReportData

ROW_HEADER = ["MAX FORCE", "MAX SLOPE", "100ms SLOPE", "200ms SLOPE"]


class ReportsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.left_report = ReportTableWidget()
        self.right_report = ReportTableWidget()

        v = QHBoxLayout()
        v.setContentsMargins(30, 15, 30, 30)
        v.addWidget(self.left_report)
        v.addSpacing(30)
        v.addWidget(self.right_report)
        self.setLayout(v)

    def update_tables(self, repetition: int,
                      left_data: ReportData, right_data: ReportData):
        self.left_report.update_table(repetition, left_data)
        self.right_report.update_table(repetition, right_data)

    def clear(self):
        self.left_report.clear()
        self.right_report.clear()


class CenterAlignedItem(QTableWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextAlignment(Qt.AlignCenter)


class ReportTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._insert_initial_data()

        # set alignment
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # disable cell selection
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)

        # remove scrollbars
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # resize cells to fit widget
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _insert_initial_data(self):
        self.setRowCount(len(ROW_HEADER))
        self.setColumnCount(1)

        self.setVerticalHeaderLabels(ROW_HEADER)
        self.setHorizontalHeaderLabels(["AVG"])

        for i in range(len(ROW_HEADER)):
            self.setItem(i, 0, CenterAlignedItem("NA"))
            self.item(i, 0).setBackground(Qt.lightGray)

    def update_table(self, repetition: int, report_data: ReportData):
        self.setColumnCount(self.columnCount() + 1)

        new_column_idx = self.columnCount() - 2
        self.setHorizontalHeaderItem(new_column_idx, CenterAlignedItem(str(repetition)))
        self.setItem(0, new_column_idx, CenterAlignedItem(f"{report_data.max_force:.0f}"))
        self.setItem(1, new_column_idx, CenterAlignedItem(f"{report_data.max_angel:.2f}"))
        self.setItem(2, new_column_idx, CenterAlignedItem(f"{report_data.first_angle:.2f}"))
        self.setItem(3, new_column_idx, CenterAlignedItem(f"{report_data.second_angle:.2f}"))

        self._update_avg_values()

    def _update_avg_values(self):
        column_count = self.columnCount()
        self.setHorizontalHeaderItem(column_count - 1,
                                     CenterAlignedItem("AVG"))
        for i in range(len(ROW_HEADER)):
            # get values from this row
            val = [float(self.item(i, j).text()) for j in range(column_count - 1)]
            avg = sum(val) / (column_count - 1)
            if ROW_HEADER[i] == "MAX FORCE":
                self.setItem(i, column_count - 1, CenterAlignedItem(f"{avg:.0f}"))
            else:
                self.setItem(i, column_count - 1, CenterAlignedItem(f"{avg:.2f}"))
            self.item(i, column_count - 1).setBackground(Qt.lightGray)

    def clear(self):
        super().clear()
        self._insert_initial_data()

    def sizeHint(self):
        return QSize(700, 300)


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    gui = ReportTableWidget()
    gui.update_table(1, ReportData("", 1000, 0.52, 0.233, 0.234444))
    gui.update_table(2, ReportData("", 1200, 0.32, 0.453, 0.5444))
    gui.clear()
    gui.show()
    sys.exit(app.exec_())
