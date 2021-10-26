import sys

from PyQt5.QtWidgets import QApplication

from hst.components import HstGUI


def main():
    app = QApplication(sys.argv)
    gui = HstGUI()
    gui.show()
    app.exec_()


if __name__ == '__main__':
    main()
