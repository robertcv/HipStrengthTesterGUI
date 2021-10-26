import os

from serial import Serial
from serial.tools.list_ports import grep


def get_ports():
    """Get available serial connections"""
    serial_ports = []
    if os.name == 'nt':
        serial_ports = list(grep(r'COM*'))
    elif os.name == 'posix':
        serial_ports = list(grep(r'USB*'))

    return [p.device for p in serial_ports]


class Connection(object):
    """Create a connection to serial"""
    def __init__(self, port, baud=9600, timeout=1):
        self.ser = Serial()
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.timeout = timeout

        self.is_open = False

    def open(self):
        self.ser.open()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.is_open = True

    def readline(self):
        if not self.is_open:
            self.open()
        l = self.ser.readline()
        while not l:
            l = self.ser.readline()
        return l

    def write(self, string):
        if not self.is_open:
            self.open()
        self.ser.write(string)

    def close(self):
        self.ser.close()
        self.is_open = False


if __name__ == '__main__':

    ports = list(get_ports())

    con = Connection(ports[0])
    while True:
        print(con.readline())
