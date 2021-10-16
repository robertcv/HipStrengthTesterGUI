from collections import namedtuple

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, \
    QRadioButton, QButtonGroup, QHBoxLayout, QPushButton, QCompleter
from PyQt5.QtCore import QRegExp, Qt, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QIntValidator


SubjectInfo = namedtuple(
    'SubjectInfo',
    ['name', 'birth', 'height', 'weight', 'foot', 'exercise', 'repetition']
)
EXERCISES = [
    "addukcija 90°", "abdukcija 90°", "notranja rotacija", "zunanja rotacija",
    "nordic hamstring", "addukcija 0°", "abdukcija 0°",
    "plantarna fleksija", "dorzalna fleksija", "izteg kolena", "upogib kolena",
]


class LabelLineEdit(QWidget):
    """Create a widget that holds line edit field with its label."""
    def __init__(self, text, line_edit: QLineEdit, text_width=150, edit_width=200):
        super().__init__()
        label = QLabel(text)
        label.setFixedWidth(text_width)
        line_edit.setMinimumWidth(edit_width)

        h = QHBoxLayout()
        h.addWidget(label)
        h.addWidget(line_edit)
        h.setContentsMargins(0, 0, 0, 0)
        self.setLayout(h)


class SubjectWidget(QWidget):
    new_subject_sig = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.name_edit = QLineEdit()
        self.birth_date_edit = QLineEdit()
        date_reg = QRegExp("(0[1-9]|[12][0-9]|3[01]{1,2}).(0[1-9]|[12]{1,2}).(19[0-9][0-9]|20[0-9][0-9])")
        date_val = QRegExpValidator(date_reg)
        self.birth_date_edit.setValidator(date_val)

        self.height_edit = QLineEdit()
        self.height_edit.setValidator(QIntValidator(0, 300))

        self.weight_edit = QLineEdit()
        self.weight_edit.setValidator(QIntValidator(0, 500))

        self.dominant_foot = QButtonGroup()
        self.dominant_foot.setExclusive(True)
        self.dominant_foot_left = QRadioButton("Left")
        self.dominant_foot_right = QRadioButton("Right")
        self.dominant_foot.addButton(self.dominant_foot_left, 0)
        self.dominant_foot.addButton(self.dominant_foot_right, 1)
        h = QHBoxLayout()
        h.addWidget(QLabel("Dominant foot:"))
        h.addStretch()
        h.addWidget(self.dominant_foot_left)
        h.addStretch()
        h.addWidget(self.dominant_foot_right)
        h.addStretch()

        self.new_btn = QPushButton("New Subject")
        self.new_btn.clicked.connect(self.new_subject)

        self.exercise_edit = QLineEdit()
        exercise_completer = QCompleter(EXERCISES)
        exercise_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.exercise_edit.setCompleter(exercise_completer)

        self.repetition_edit = QLineEdit("1")
        self.repetition_edit.setEnabled(False)

        grid = QGridLayout()
        grid.addWidget(LabelLineEdit("Name:", self.name_edit), 0, 0)
        grid.addWidget(LabelLineEdit("Birth date:", self.birth_date_edit), 0, 2)

        grid.addWidget(LabelLineEdit("Height:", self.height_edit), 1, 0)
        grid.addWidget(LabelLineEdit("Weight:", self.weight_edit), 1, 2)

        grid.addLayout(h, 2, 0)
        grid.addWidget(LabelLineEdit("Repetition:", self.repetition_edit), 2, 2)

        grid.addWidget(LabelLineEdit("Exercise:", self.exercise_edit), 3, 0)
        grid.addWidget(self.new_btn, 3, 2)

        grid.setColumnMinimumWidth(0, 300)
        grid.setColumnStretch(0, 1)

        grid.setColumnMinimumWidth(1, 30)
        grid.setColumnStretch(1, 0)

        grid.setColumnMinimumWidth(2, 300)
        grid.setColumnStretch(2, 1)

        grid.setContentsMargins(30, 30, 30, 15)
        self.setLayout(grid)

    def get_subject_data(self) -> SubjectInfo:
        return SubjectInfo(
            self.name_edit.text(),
            self.birth_date_edit.text(),
            self.height_edit.text(),
            self.weight_edit.text(),
            "right" if self.dominant_foot.checkedId() else "left",
            self.exercise_edit.text(),
            self.repetition_edit.text()
        )

    def new_repetition(self):
        self.repetition_edit.setText(str(int(self.repetition_edit.text()) + 1))

    def new_subject(self):
        self.name_edit.setText("")
        self.birth_date_edit.setText("")
        self.height_edit.setText("")
        self.weight_edit.setText("")

        # uncheck the dominant foot radio buttons
        self.dominant_foot.setExclusive(False)
        self.dominant_foot_left.setChecked(False)
        self.dominant_foot_right.setChecked(False)
        self.dominant_foot.setExclusive(True)

        self.repetition_edit.setText("1")
        self.new_subject_sig.emit()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    gui = SubjectWidget()
    gui.show()
    sys.exit(app.exec_())
