from PyQt5.QtCore import QThread, pyqtSignal


class DoubleLoadCellConnectionThread(QThread):
    sig = pyqtSignal(tuple)

    def __init__(self, con, sig_receiver):
        super().__init__()
        self.con = con
        self.sig.connect(sig_receiver)
        self._tare = False

    def tare(self):
        self._tare = True

    def run(self):
        try:
            f1, f2 = self.con.readline().rstrip().split(b',')
            self.sig.emit(float(f1), float(f2))
        except:
            pass
        if self._tare:
            self.con.write(b't')
            self._tare = False
