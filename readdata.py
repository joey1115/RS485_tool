from modbus import ModBus, JHFK
import time
import random
import serial.serialutil


class Read1(ModBus):
    def __init__(self, main):
        super(Read1, self).__init__()
        self.main = main
        self.max_error_allowed = 256
        self.start = 0
        self.main.temp_data = {}
        self.type_list = ['value', 'stat', 'res', 'unit', 'type', 'range', 'first', 'second']
        self.data = {}
        self.data_queue = self.main.data_queue
        self.temp = []

    def __get_data_array(self, cmd):
        self.set_command(cmd)
        self.run()
        if self.crc_check():
            self.temp = []
            for i in range(3, 3+self.response[2], 2):
                self.temp.append((self.response[i] << 8) + self.response[i+1])
            return True
        else:
            return False

    def read_data_array(self, port):
        cmd = [1, 3, 0, 13, 0, 8]
        cmd[0] = port
        if self.__get_data_array(cmd):
            self.data[0]['time'] = time.time()
            for i in range(0, len(self.temp)):
                self.data[1][self.type_list[i]] = self.temp[i]
            return True
        else:
            return False

    def sim_read_data_array(self):
        self.data[0]['time'] = time.time()
        dummy_data = [8, 0, 0, 2, 17, 100, 25, 50]
        dummy_data[0] = random.random() * 100
        if dummy_data[0] > dummy_data[7]:
            dummy_data[1] = 3
        elif dummy_data[0] > dummy_data[6]:
            dummy_data[1] = 2
        else:
            dummy_data[1] = 0
        for i in range(0, 8):
            self.data[1][self.type_list[i]] = dummy_data[i]
        time.sleep(0.1)
        return True

    def process(self, serial_id, serial_setting):
        protocol = self.main.protocol['protocol'][serial_setting['protocol_id']]
        self.max_error_allowed = 15
        temp_data = {}
        try:
            if self.isOpen():
                self.close()
            self.set_com(serial_setting)
            self.open()
            flag = True
        except serial.serialutil.SerialException:
            flag = False
        ports = self.main.setting['port']
        for port_key in ports.keys():
            port = ports[port_key]
            if serial_id == port['serial_id'] and port['device_id'] not in temp_data.keys():
                temp_data[port['device_id']] = {}
                count = 0
                while True:
                    if count == 5 or (not flag):
                        for i in range(1, 9):
                            temp_data[port['device_id']][i] = {
                                'time': time.time(),
                                'type': '',
                                'value': 0,
                                'unit': '',
                                'msg': '连接失败',
                                'color': 'blue',
                                'range': 1
                            }
                        break
                    elif self.read_data_array(port['device_id']):
                        temp_type = protocol['type'][str(self.data[1]['type'])]
                        temp_msg = protocol['status'][str(self.data[1]['stat'])]
                        temp_unit = protocol['unit'][str(self.data[1]['unit'])]
                        temp_value = self.data[1]['value'] * (10 ** -(self.data[1]['res']))
                        temp_color = self.main.protocol['color'][protocol['ui'][temp_msg]]
                        temp_data[port['device_id']][1] = {
                            'time': self.data[0]['time'],
                            'type': temp_type,
                            'value': temp_value,
                            'unit': temp_unit,
                            'msg': temp_msg,
                            'color': temp_color,
                            'range': self.data[1]['range']
                        }
                        break
                    elif self.max_error_allowed == 15:
                        temp_data[port['device_id']][1] = {
                            'time': time.time(),
                            'type': '',
                            'value': 0,
                            'unit': '',
                            'msg': '连接失败',
                            'color': 'blue',
                            'range': 1
                        }
                        break
                    else:
                        count += 1
                        self.max_error_allowed -= 1
            if port['device_id'] in temp_data.keys():
                if port['data_id'] in temp_data[port['device_id']].keys():
                    self.data_queue.put([port_key, temp_data[port['device_id']][port['data_id']]])


class Read2(JHFK):
    def __init__(self, main):
        super(Read2, self).__init__()
        self.main = main
        self.max_error_allowed = 256
        self.temp = []
        self.data = {}
        for i in range(1, 9):
            self.data[i] = {
                'time': 0,
                'value': 0,
                'stat': 0
            }
        self.data_queue = self.main.data_queue
        self.main.temp_data = {}

    def __get_data_array(self, cmd):
        self.set_command(cmd)
        self.run()
        if self.check():
            self.temp = self.response
            return True
        else:
            return False

    def read_data_array(self, port):
        cmd = [2, 48, 48, 3]
        cmd[1] = port // 10 + 48
        cmd[2] = port % 10 + 48
        if self.__get_data_array(cmd):
            temp_time = time.time()
            for i in range(1, 9):
                start = 6 * i - 1
                self.data[i]['time'] = temp_time
                self.data[i]['stat'] = self.temp[start]
                self.data[i]['value'] = (self.temp[start + 1] & 0xF) * 100 + \
                                        (self.temp[start + 2] & 0xF) * 10 + \
                                        (self.temp[start + 3] & 0xF)
            return True
        else:
            return False

    def process(self, serial_id, serial_setting):
        protocol = self.main.protocol['protocol'][serial_setting['protocol_id']]
        self.max_error_allowed = 15
        temp_data = {}
        try:
            if self.isOpen():
                self.close()
            self.set_com(serial_setting)
            self.open()
            flag = True
        except serial.serialutil.SerialException:
            flag = False
        ports = self.main.setting['port']
        for port_key in ports.keys():
            port = ports[port_key]
            if serial_id == port['serial_id'] and port['device_id'] not in temp_data.keys():
                temp_data[port['device_id']] = {}
                count = 0
                while True:
                    if count == 5 or (not flag):
                        for i in range(1, 9):
                            temp_data[port['device_id']][i] = {
                                'time': time.time(),
                                'type': '',
                                'value': 0,
                                'unit': '',
                                'msg': '连接失败',
                                'color': 'blue',
                                'range': 1
                            }
                        break
                    elif self.read_data_array(port['device_id']):
                        for i in range(1, 9):
                            temp_msg = protocol['status'][str(self.data[i]['stat'])]
                            temp_unit = protocol['unit'][str(self.data[i]['stat'])]
                            temp_color = self.main.protocol['color'][protocol['ui'][temp_msg]]
                            temp_data[port['device_id']][i] = {
                                'time': self.data[i]['time'],
                                'type': '可燃气',
                                'value': self.data[i]['value'],
                                'unit': temp_unit,
                                'msg': temp_msg,
                                'color': temp_color,
                                'range': 100
                            }
                        break
                    elif self.max_error_allowed == 0:
                        for i in range(1, 9):
                            temp_data[port['device_id']][i] = {
                                'time': time.time(),
                                'type': '',
                                'value': 0,
                                'unit': 0,
                                'msg': '连接失败',
                                'color': 'blue',
                                'range': 1
                            }
                        break
                    else:
                        count += 1
                        self.max_error_allowed -= 1

            if port['device_id'] in temp_data.keys():
                if port['data_id'] in temp_data[port['device_id']].keys():
                    self.data_queue.put([port_key, temp_data[port['device_id']][port['data_id']]])


class Read3(ModBus):
    def __init__(self, main, num):
        super(Read3, self).__init__()
        self.main = main
        self.num = num
        self.max_error_allowed = 256
        self.start = 0
        self.main.temp_data = {}
        self.type_list = ['value', 'stat', 'res', 'unit', 'type', 'range', 'first', 'second']
        self.address_list = [13, 45, 77, 109, 141, 173, 205, 237]
        self.data = {}
        self.data_queue = self.main.data_queue
        self.temp = []

    def __get_data_array(self, cmd):
        self.set_command(cmd)
        self.run()
        if self.crc_check():
            self.temp = []
            for i in range(3, 3+self.response[2], 2):
                self.temp.append((self.response[i] << 8) + self.response[i+1])
            return True
        else:
            return False

    def read_data_array(self, device_id):
        self.data = {}
        for i in range(0, 8):
            cmd = [1, 3, 0, 13, 0, 8]
            cmd[0] = device_id
            cmd[5] = self.num
            cmd[3] = self.address_list[i]
            if self.__get_data_array(cmd):
                for j in range(0, len(self.temp)):
                    if (j + 1) not in self.data.keys():
                        self.data[j + 1] = {}
                    self.data[j + 1][self.type_list[i]] = self.temp[j]
            else:
                return False
        return True

    def sim_read_data_array(self):
        self.data[0]['time'] = time.time()
        dummy_data = [8, 0, 0, 2, 17, 100, 25, 50]
        dummy_data[0] = random.random() * 100
        if dummy_data[0] > dummy_data[7]:
            dummy_data[1] = 3
        elif dummy_data[0] > dummy_data[6]:
            dummy_data[1] = 2
        else:
            dummy_data[1] = 0
        for i in range(0, 8):
            self.data[1][self.type_list[i]] = dummy_data[i]
        time.sleep(0.1)
        return True

    def process(self, serial_id, serial_setting):
        protocol = self.main.protocol['protocol'][serial_setting['protocol_id']]
        self.max_error_allowed = 15
        temp_data = {}
        try:
            if self.isOpen():
                self.close()
            self.set_com(serial_setting)
            self.open()
            flag = True
        except serial.serialutil.SerialException:
            flag = False
        ports = self.main.setting['port']
        for port_key in ports.keys():
            port = ports[port_key]
            if serial_id == port['serial_id'] and port['device_id'] not in temp_data.keys():
                temp_data[port['device_id']] = {}
                count = 0
                while True:
                    if count == 5 or (not flag):
                        for i in range(1, self.num + 1):
                            temp_data[port['device_id']][i] = {
                                'time': time.time(),
                                'type': '',
                                'value': 0,
                                'unit': '',
                                'msg': '连接失败',
                                'color': 'blue',
                                'range': 1
                            }
                        break
                    elif self.read_data_array(port['device_id']):
                        temp_time = time.time()
                        for i in range(1, self.num + 1):
                            temp_type = protocol['type'][str(self.data[i]['type'])]
                            temp_msg = protocol['status'][str(self.data[i]['stat'])]
                            temp_unit = protocol['unit'][str(self.data[i]['unit'])]
                            temp_value = self.data[i]['value'] * (10 ** -(self.data[i]['res']))
                            temp_color = self.main.protocol['color'][protocol['ui'][temp_msg]]
                            temp_data[port['device_id']][i] = {
                                'time': temp_time,
                                'type': temp_type,
                                'value': temp_value,
                                'unit': temp_unit,
                                'msg': temp_msg,
                                'color': temp_color,
                                'range': self.data[i]['range']
                            }
                        break
                    elif self.max_error_allowed == 15:
                        for i in range(1, self.num + 1):
                            temp_data[port['device_id']][i] = {
                                'time': time.time(),
                                'type': '',
                                'value': 0,
                                'unit': '',
                                'msg': '连接失败',
                                'color': 'blue',
                                'range': 1
                            }
                        break
                    else:
                        count += 1
                        self.max_error_allowed -= 1
            if port['device_id'] in temp_data.keys():
                if port['data_id'] in temp_data[port['device_id']].keys():
                    self.data_queue.put([port_key, temp_data[port['device_id']][port['data_id']]])
