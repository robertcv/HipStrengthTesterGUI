from hst.connect import Connection, get_ports
from hst.connection_thread import DoubleLoadCellConnectionThread
from hst.components import ConnectionSettingsDialog, SubjectWidget, PlotsWidget
from hst.data import Data

from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QWidget,\
    QVBoxLayout, QLabel, QFileDialog, QLineEdit, QDialog, QPushButton,\
    QGridLayout, QComboBox, QDialogButtonBox, QRadioButton, QButtonGroup,\
    QHBoxLayout
from PyQt5.QtCore import QTimer, pyqtSignal, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator, QIntValidator


class HstGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 800, 500)
        self.setMinimumSize(1000, 1000)
        self.setWindowTitle('Hip Strength Tester v2')

        self.save_file = None
        self.left_data = Data()
        self.right_data = Data()

        self.port = None
        self.baud = 115200
        self.connection = None
        self.connection_thread = None

        self._init_menu()
        self._init_body()

    def _init_body(self):
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear)

        self.threshold_btn = QPushButton("Threshold")
        self.threshold_btn.clicked.connect(self.threshold)

        self.analyse_btn = QPushButton("Analyse")
        self.analyse_btn.clicked.connect(self.analyse)

        btns = QHBoxLayout()
        btns.addWidget(self.start_btn)
        btns.addWidget(self.stop_btn)
        btns.addWidget(self.clear_btn)
        btns.addWidget(self.threshold_btn)
        btns.addWidget(self.analyse_btn)
        btns.setContentsMargins(30, 15, 30, 15)

        self.subject = SubjectWidget()
        self.plots = PlotsWidget()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.subject)
        main_layout.addLayout(btns)
        main_layout.addWidget(self.plots)

        w = QWidget(self)
        w.setLayout(main_layout)
        self.setCentralWidget(w)

        self.resultsTimer = QTimer()
        self.resultsTimer.timeout.connect(self.update_plots)
        self.resultsTimer.setInterval(30)

    def _init_menu(self):
        new_measurements_action = QAction(
            QIcon.fromTheme('document-new'), 'New measurements', self)
        new_measurements_action.setShortcut('Ctrl+n')
        new_measurements_action.triggered.connect(self.setup_new_measurements)

        open_measurements_action = QAction(
            QIcon.fromTheme('document-open'), 'Open measurements', self)
        open_measurements_action.setShortcut('Ctrl+o')
        open_measurements_action.triggered.connect(self.open_measurements)

        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+q')
        quit_action.triggered.connect(self.closeEvent)

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
        file_menu.addAction(open_measurements_action)
        file_menu.addAction(quit_action)

        connection_menu = main_menu.addMenu('&Connection')
        connection_menu.addAction(open_connection_action)
        connection_menu.addAction(close_connection_action)
        connection_menu.addAction(tare_action)

    def update_plots(self):
        self.plots.update_plots(self.left_data, self.right_data)

    def start(self):
        pass

    def stop(self):
        pass

    def clear(self):
        pass

    def threshold(self):
        pass

    def analyse(self):
        pass

    def setup_new_measurements(self):
        pass

    def open_measurements(self):
        pass

    def new_data(self, data):
        x, lf, rf = data
        self.left_data.add_new(x, lf)
        self.right_data.add_new(x, rf)

    def is_connected(self):
        return self.connection is not None and self.connection_thread is not None

    def check_for_connection(self):
        if not self.is_connected():
            QMessageBox.warning(self, "Stop!",
                                "First connect to device!")
            return False
        return True

    def connection_open(self):
        dialog = ConnectionSettingsDialog(self.port)
        dialog.exec_()
        self.port = dialog.port
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
