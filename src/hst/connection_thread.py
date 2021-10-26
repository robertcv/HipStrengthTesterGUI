from PyQt5.QtCore import QThread, pyqtSignal


class DoubleLoadCellConnectionThread(QThread):
    sig = pyqtSignal(tuple)

    def __init__(self, con, sig_receiver):
        super().__init__()
        self.con = con
        self.sig.connect(sig_receiver)
        self.stop = False
        self._tare = False

    def tare(self):
        self._tare = True

    def run(self):
        # sometimes there is some data stuck in the buffer
        # trow away some of the first sent lines
        for i in range(50):
            self.con.readline()

        while not self.stop:
            try:
                s = self.con.readline()
                t, f1, f2 = s.rstrip().split(b',')
                self.sig.emit((float(t), abs(int(f1)), abs(int(f2))))
            except:
                pass
            if self._tare:
                self.con.write(b't')
                self._tare = False
