from threading import Thread
import time


class TimeThread(Thread):
    def __init__(self, main):
        self.main = main
        super(TimeThread, self).__init__(target=self.work)
        self.setDaemon(True)
        self.start()

    def work(self):
        while True:
            time.sleep(1)
            if self.main.flags['time']:
                self.main.time_label['text'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class DataThread(Thread):
    def __init__(self, main):
        self.main = main
        super(DataThread, self).__init__(target=self.work)
        self.setDaemon(True)
        self.start()

    def work(self):
        while True:
            time.sleep(1)
            if self.main.flags['data']:
                for serial_key in self.main.setting['serial'].keys():
                    serial_setting = self.main.setting['serial'][serial_key]
                    self.main.read_data[serial_key].process(serial_key, serial_setting)


class StatusThread(Thread):
    def __init__(self, main):
        self.main = main
        super(StatusThread, self).__init__(target=self.work)
        self.setDaemon(True)
        self.start()

    def work(self):
        while True:
            time.sleep(0.1)
            if self.main.flags['status']:
                alarm = sum(self.main.alarm.values())
                error = sum(self.main.error.values())
                self.main.info_status_label.refresh(alarm, error, self.main.first_alarm)


class UIThread(Thread):
    def __init__(self, main):
        self.main = main
        self.queue = self.main.data_queue
        super(UIThread, self).__init__(target=self.work)
        self.setDaemon(True)
        self.start()

    def work(self):
        while True:
            if self.main.flags['ui']:
                if not self.queue.empty():
                    temp = self.queue.get()
                    port_id = temp[0]
                    data = temp[1]

                    if self.main.flags['label_ui']:
                        self.main.label_view.refresh(port_id, data)

                    if self.main.flags['category_ui']:
                        self.main.category_view.refresh(port_id, data)

                    serial_id = self.main.setting['port'][port_id]['serial_id']
                    protocol_id = self.main.setting['serial'][serial_id]['protocol_id']
                    map = self.main.protocol['protocol'][protocol_id]['ui']
                    if map[data['msg']] == '1':
                        self.main.alarm[port_id] = False
                        self.main.error[port_id] = False
                    elif map[data['msg']] == '2':
                        self.main.alarm[port_id] = True
                        self.main.error[port_id] = False
                    elif map[data['msg']] == '3':
                        self.main.alarm[port_id] = True
                        self.main.error[port_id] = False
                    elif map[data['msg']] == '4':
                        self.main.alarm[port_id] = False
                        self.main.error[port_id] = True
                    else:
                        self.main.alarm[port_id] = False
                        self.main.error[port_id] = False

                    if self.main.first_alarm == 0 and map[data['msg']] == '2' and map[data['msg']] == '3':
                        self.main.first_alarm = port_id
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)