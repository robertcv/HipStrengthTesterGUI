from hst.connect import get_ports

from PyQt5.QtWidgets import QVBoxLayout, QLabel,  QDialog, QPushButton,\
    QGridLayout, QComboBox, QDialogButtonBox


class ConnectionSettingsDialog(QDialog):
    def __init__(self, port=None):
        super().__init__()
        self.setWindowTitle("Connection settings!")

        self.port = port

        current_ports = get_ports()
        self.port_comboBox = QComboBox()
        self.port_comboBox.addItems(current_ports)
        if self.port in current_ports:
            self.port_comboBox.setCurrentText(self.port)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh)

        grid = QGridLayout()
        grid.addWidget(QLabel("Port: "), 0, 0)
        grid.addWidget(self.port_comboBox, 0, 1)
        grid.addWidget(self.refresh_button, 0, 2)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def refresh(self):
        self.port_comboBox.clear()
        self.port_comboBox.addItems(get_ports())

    def accept(self):
        self.port = self.port_comboBox.currentText()
        self.close()
