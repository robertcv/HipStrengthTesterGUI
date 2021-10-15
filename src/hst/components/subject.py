from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, \
    QRadioButton, QButtonGroup, QHBoxLayout
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator


class SubjectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name_label = QLineEdit()
        self.birth_date_label = QLineEdit()
        date_reg = QRegExp("(0[1-9]|[12][0-9]|3[01]{1,2}).(0[1-9]|[12]{1,2}).(19[0-9][0-9]|20[0-9][0-9])")
        date_val = QRegExpValidator(date_reg)
        self.birth_date_label.setValidator(date_val)

        self.height_label = QLineEdit()
        self.height_label.setValidator(QIntValidator(0, 300))

        self.weight_label = QLineEdit()
        self.weight_label.setValidator(QIntValidator(0, 500))

        self.dominant_foot = QButtonGroup()
        self.dominant_foot.setExclusive(True)
        self.dominant_foot_left = QRadioButton("Left")
        self.dominant_foot_right = QRadioButton("Right")
        self.dominant_foot.addButton(self.dominant_foot_left, 0)
        self.dominant_foot.addButton(self.dominant_foot_right, 1)
        h = QHBoxLayout()
        h.addWidget(self.dominant_foot_left)
        h.addWidget(self.dominant_foot_right)

        grid = QGridLayout()
        grid.addWidget(QLabel("Name: "), 0, 0)
        grid.addWidget(self.name_label, 0, 1)

        grid.addWidget(QLabel("Birth date: "), 1, 0)
        grid.addWidget(self.birth_date_label, 1, 1)

        grid.addWidget(QLabel("Height: "), 2, 0)
        grid.addWidget(self.height_label, 2, 1)

        grid.addWidget(QLabel("Weight: "), 3, 0)
        grid.addWidget(self.weight_label, 3, 1)

        grid.addWidget(QLabel("Dominant foot: "), 4, 0)
        grid.addLayout(h, 4, 1)

        self.setLayout(grid)
        self.layout().setContentsMargins(30, 30, 30, 15)
        self.layout().setSpacing(15)
