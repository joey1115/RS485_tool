from crc import crc16
from serial import *


class ModBus(Serial):
    def __init__(self):
        super(ModBus, self).__init__()
        self.command = []
        self.reg = 0
        self.response = bytes()
        self.crc = crc16()
        self.serial_bytesize = {
            '5': FIVEBITS,
            '6': SIXBITS,
            '7': SEVENBITS,
            '8': EIGHTBITS
        }

        self.serial_stopbits = {
            '1': STOPBITS_ONE,
            '1.5': STOPBITS_ONE_POINT_FIVE,
            '2': STOPBITS_TWO
        }

        self.serial_parity = {
            'NONE': PARITY_NONE,
            'EVEN': PARITY_EVEN,
            'ODD': PARITY_ODD,
            'SPACE': PARITY_SPACE,
            'MARK': PARITY_MARK
        }

    def set_command(self, cmd):
        self.command = cmd
        self.reg = (cmd[4] << 8) + cmd[5]

    def set_com(self, setting):
        self.port = setting['com']
        self.baudrate = int(setting['baudrate'])
        self.bytesize = self.serial_bytesize[setting['bytesize']]
        self.parity = self.serial_parity[setting['parity']]
        self.stopbits = self.serial_stopbits[setting['stopbits']]
        self.timeout = 0.04

    def run(self):
        self.write(bytes(self.crc.createarray(self.command)))
        self.response = self.read((self.reg << 2) + 5)

    def crc_check(self):
        if len(self.response) == 5 or len(self.response) == self.reg * 2 + 5:
            return self.crc.calcrc([n for n in self.response])
        else:
            return False


class JHFK(Serial):
    def __init__(self):
        super(JHFK, self).__init__()
        self.command = []
        self.response = []
        self.serial_bytesize = {
            '5': FIVEBITS,
            '6': SIXBITS,
            '7': SEVENBITS,
            '8': EIGHTBITS
        }

        self.serial_stopbits = {
            '1': STOPBITS_ONE,
            '1.5': STOPBITS_ONE_POINT_FIVE,
            '2': STOPBITS_TWO
        }

        self.serial_parity = {
            'NONE': PARITY_NONE,
            'EVEN': PARITY_EVEN,
            'ODD': PARITY_ODD,
            'SPACE': PARITY_SPACE,
            'MARK': PARITY_MARK
        }

    def set_command(self, cmd):
        self.command = cmd

    def set_com(self, setting):
        self.port = setting['com']
        self.baudrate = setting['baudrate']
        self.bytesize = self.serial_bytesize[setting['bytesize']]
        self.parity = self.serial_parity[setting['parity']]
        self.stopbits = self.serial_stopbits[setting['stopbits']]
        self.timeout = 0.1

    def run(self):
        self.write(bytes(self.command))
        temp = self.read(53)
        self.response = [n for n in temp]

    def check(self):
        if len(self.response) == 53:
            if self.response[-1] == 3 and self.response[0:3] == self.command[0:3]:
                return True
            else:
                return False
        else:
            return False
