from connect import Connection, get_ports
from connection_thread import DoubleLoadCellConnectionThread

from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QWidget,\
    QVBoxLayout, QLabel, QFileDialog, QLineEdit, QDialog, QPushButton,\
    QGridLayout, QComboBox, QDialogButtonBox
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QIcon


LEFT_ADD, RIGHT_ADD, LEFT_ABD, RIGHT_ABD = 0, 1, 2, 3
LEFT, RIGHT, ADDUCTOR, ABDUCTOR = 0, 1, 2, 3


class BodyWidget(QWidget):
    """The body part of the gui. Displays the force"""

    save_sig = pyqtSignal()
    start_stop_adductor = pyqtSignal()
    start_stop_abductor = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.forces = [QLabel("0 N") for _ in range(4)]
        self.ratios = [QLabel("0") for _ in range(4)]

        font = self.forces[0].font()
        font.setBold(True)
        font.setPointSize(40)

        for label in self.forces + self.ratios:
            label.setFont(font)

        font.setPointSize(10)
        self.adductor_button = QPushButton("Start")
        self.adductor_button.setFont(font)
        self.adductor_button.clicked.connect(self.start_stop_adductor.emit)

        self.abductor_button = QPushButton("Start")
        self.abductor_button.setFont(font)
        self.abductor_button.clicked.connect(self.start_stop_abductor.emit)

        self.save_button = QPushButton("SAVE")
        self.save_button.setFont(font)
        self.save_button.clicked.connect(self.save_sig.emit)

        font.setPointSize(20)
        font.setBold(False)
        l = QLabel("LEFT")
        l.setFont(font)
        r = QLabel("RIGHT")
        r.setFont(font)
        ra1 = QLabel("RATIO")
        ra1.setFont(font)
        ra2 = QLabel("RATIO")
        ra2.setFont(font)
        ad = QLabel("ADDUCTOR")
        ad.setFont(font)
        ab = QLabel("ABDUCTOR")
        ab.setFont(font)

        grid = QGridLayout()
        grid.addWidget(l, 0, 2)
        grid.addWidget(r, 0, 3)
        grid.addWidget(ra1, 0, 4)

        grid.addWidget(self.adductor_button, 1, 0)
        grid.addWidget(ad, 1, 1)
        grid.addWidget(self.forces[LEFT_ADD], 1, 2)
        grid.addWidget(self.forces[RIGHT_ADD], 1, 3)
        grid.addWidget(self.ratios[ADDUCTOR], 1, 4)

        grid.addWidget(self.abductor_button, 2, 0)
        grid.addWidget(ab, 2, 1)
        grid.addWidget(self.forces[LEFT_ABD], 2, 2)
        grid.addWidget(self.forces[RIGHT_ABD], 2, 3)
        grid.addWidget(self.ratios[ABDUCTOR], 2, 4)

        grid.addWidget(ra2, 3, 1)
        grid.addWidget(self.ratios[LEFT], 3, 2)
        grid.addWidget(self.ratios[RIGHT], 3, 3)

        v = QVBoxLayout()
        v.setContentsMargins(30, 30, 30, 30)
        v.addLayout(grid)
        v.addWidget(self.save_button)

        self.setLayout(v)


class Subject:

    class SubjectWidget(QDialog):
        def __init__(self):
            super().__init__()

            self.subject = None

            self.name_label = QLineEdit()
            self.birth_date_label = QLineEdit()
            self.height_label = QLineEdit()
            self.weight_label = QLineEdit()
            self.dominant_foot_label = QLineEdit()

            grid = QGridLayout()
            grid.addWidget(QLabel("Name: "), 0, 0)
            grid.addWidget(self.name_label, 0, 1)

            grid.addWidget(QLabel("birth_date: "), 1, 0)
            grid.addWidget(self.birth_date_label, 1, 1)

            grid.addWidget(QLabel("height: "), 2, 0)
            grid.addWidget(self.height_label, 2, 1)

            grid.addWidget(QLabel("weight: "), 3, 0)
            grid.addWidget(self.weight_label, 3, 1)

            grid.addWidget(QLabel("dominant_foot: "), 4, 0)
            grid.addWidget(self.dominant_foot_label, 4, 1)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel)

            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.close)

            main_layout = QVBoxLayout()
            main_layout.addLayout(grid)
            main_layout.addWidget(button_box)
            self.setLayout(main_layout)

        def accept(self):
            self.subject = Subject(self.name_label.text(),
                                   self.birth_date_label.text(),
                                   self.height_label.text(),
                                   self.weight_label.text(),
                                   self.dominant_foot_label.text())
            self.close()

    def __init__(self, name, birth_date, height, weight, dominant_foot):
        self.name = name
        self.birth_date = birth_date
        self.height = height
        self.weight = weight
        self.dominant_foot = dominant_foot
        self.forces = [0 for _ in range(4)]

    def new_force(self, force, ftype):
        self.forces[ftype] = max(self.forces[ftype], force)

    def get_max_force(self, ftype):
        return self.forces[ftype]

    def get_ratio(self, rtype):
        try:
            return self._get_ratio(rtype)
        except ZeroDivisionError:
            return 0

    def _get_ratio(self, rtype):
        if rtype == LEFT:
            return self.forces[LEFT_ADD] / self.forces[LEFT_ABD]
        elif rtype == RIGHT:
            return self.forces[RIGHT_ADD] / self.forces[RIGHT_ABD]
        elif rtype == ADDUCTOR:
            return self.forces[LEFT_ADD] / self.forces[RIGHT_ADD]
        elif rtype == ABDUCTOR:
            return self.forces[LEFT_ABD] / self.forces[RIGHT_ABD]

    def get_string(self):
        return ",".join(map(str, [self.name] +
                                 self.forces +
                                 [self.get_ratio(i) for i in range(4)]))


BAUDS = [
    '4800',
    '9600',
    '14400',
    '19200',
    '28800',
    '38400',
    '57600',
    '115200',
    '230400',
    '1000000',
]


class ConnectionSettings(QDialog):

    def __init__(self, port=None, baud="9600"):
        super().__init__()

        self.port = port
        self.baud = baud

        current_ports = get_ports()
        self.port_comboBox = QComboBox()
        self.port_comboBox.addItems(current_ports)
        if self.port in current_ports:
            self.port_comboBox.setCurrentText(self.port)

        self.baud_comboBox = QComboBox()
        self.baud_comboBox.addItems(BAUDS)
        self.baud_comboBox.setCurrentText(self.baud)

        grid = QGridLayout()
        grid.addWidget(QLabel("Port: "), 0, 0)
        grid.addWidget(self.port_comboBox, 0, 1)

        grid.addWidget(QLabel("Baud: "), 1, 0)
        grid.addWidget(self.baud_comboBox, 1, 1)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def accept(self):
        self.port = self.port_comboBox.currentText()
        self.baud = self.baud_comboBox.currentText()
        self.close()


class HstGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 200, 100)
        self.setWindowTitle('Hip Strength Tester')

        self.save_file = None
        self.current_subject = None  # type: Subject
        self.current_type = ADDUCTOR

        self.port = None
        self.baud = 9600
        self.connection = None
        self.connection_thread = None

        self._init_menu()
        self._init_body()

    def _init_body(self):
        self.body = BodyWidget()
        self.body.save_sig.connect(self.save_subject)
        self.body.start_stop_adductor.connect(self.start_stop_adductor)
        self.body.start_stop_abductor.connect(self.start_stop_abductor)

        self.setCentralWidget(self.body)

        self.resultsTimer = QTimer()
        self.resultsTimer.timeout.connect(self.update_display)
        self.resultsTimer.setInterval(30)

    def _init_menu(self):
        new_measurements_action = QAction(QIcon.fromTheme('document-new'),
                                      'New measurements', self)
        new_measurements_action.setShortcut('Ctrl+N')
        new_measurements_action.triggered.connect(self.setup_new_measurements)

        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.closeEvent)

        new_subject_action = QAction('New subject', self)
        new_subject_action.triggered.connect(self.setup_new_subject)

        save_subject_action = QAction('Save subject', self)
        save_subject_action.triggered.connect(self.save_subject)

        open_connection_action = QAction(
            QIcon.fromTheme('media-playback-start'), 'Connect', self)
        open_connection_action.triggered.connect(self.connection_open)

        close_connection_action = QAction(
            QIcon.fromTheme('media-playback-stop'), 'Disconnect', self)
        close_connection_action.triggered.connect(self.connection_close)

        tare_action = QAction('Tare', self)
        tare_action.triggered.connect(self.tare)

        main_menu = self.menuBar()

        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(new_measurements_action)
        file_menu.addAction(quit_action)

        subject_menu = main_menu.addMenu('&Subject')
        subject_menu.addAction(new_subject_action)
        subject_menu.addAction(save_subject_action)

        connection_menu = main_menu.addMenu('&Connection')
        connection_menu.addAction(open_connection_action)
        connection_menu.addAction(close_connection_action)
        connection_menu.addAction(tare_action)

    def update_display(self):
        for i in range(4):
            self.body.forces[i].setText(
                f"{self.current_subject.get_max_force(i)} N")
            self.body.ratios[i].setText(
                f"{self.current_subject.get_ratio(i):.2f}")

    def check_for_measurements(self):
        if self.save_file == None:
            QMessageBox.warning(self, "Stop!",
                                "First create new measurements!")
            return False
        return True

    def setup_new_measurements(self):
        file_location = QFileDialog.getSaveFileName(self, 'Save File', ".csv")
        if file_location[0]:
            self.save_file = file_location[0]
            with open(self.save_file, "w") as file:
                file.write("name,F_left_add,F_right_add,F_left_abd,F_right_abd,R_left,R_right,R_add,R_abd\n")

    def check_for_subject(self):
        if self.current_subject == None:
            QMessageBox.warning(self, "Stop!",
                                "First create new subject!")
            return False
        return True

    def setup_new_subject(self):
        if not self.check_for_measurements():
            return

        dialog = Subject.SubjectWidget()
        dialog.exec_()
        self.current_subject = dialog.subject

    def save_subject(self):
        if not self.check_for_subject():
            return

        with open(self.save_file, "a") as file:
            file.write(self.current_subject.get_string() + "\n")

        self.clear()

    def clear(self):
        for i in range(4):
            self.body.forces[i].setText("0 N")
            self.body.ratios[i].setText("0")

        self.current_subject = None

    def start_stop_adductor(self):
        self.current_type = ADDUCTOR

    def start_stop_abductor(self):
        self.current_type = ABDUCTOR

    def new_data(self, data):
        f1, f2 = int(data[0]), int(data[1])
        if self.current_type == ADDUCTOR:
            self.current_subject.new_force(f1, LEFT_ADD)
            self.current_subject.new_force(f2, RIGHT_ADD)
        elif self.current_type == ABDUCTOR:
            self.current_subject.new_force(f1, LEFT_ABD)
            self.current_subject.new_force(f2, RIGHT_ABD)

    def is_connected(self):
        return self.connection is not None and self.connection_thread is not None

    def check_for_connection(self):
        if not self.is_connected():
            QMessageBox.warning(self, "Stop!",
                                "First connect to device!")
            return False
        return True

    def connection_open(self):
        if not self.check_for_subject():
            return

        dialog = ConnectionSettings(self.port, str(self.baud))
        dialog.exec_()
        self.port = dialog.port
        self.baud = int(dialog.baud)
        if not self.port:
            QMessageBox.warning(self, "Warning!",
                                "No connection available!")
            return

        if self.is_connected():
            self.connection_close()

        self.connection = Connection(self.port, self.baud)
        self.connection.open()
        self.connection_thread = DoubleLoadCellConnectionThread(self.connection,
                                                                self.new_data)
        self.connection_thread.start()
        self.resultsTimer.start()

    def connection_close(self):
        if self.is_connected():
            self.connection_thread.quit()
            self.connection.close()
        self.resultsTimer.stop()

    def tare(self):
        if self.check_for_connection():
            self.connection_thread.tare()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    gui = HstGUI()
    gui.show()
    sys.exit(app.exec_())
