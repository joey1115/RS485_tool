from tkinter import Toplevel, Label, StringVar, Entry, OptionMenu, IntVar, Frame, Button, DISABLED


class PortAdd(Toplevel):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(PortAdd, self).__init__()
        self.title('标签编辑器')

        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0)

        Label(self.main_frame, text='通道编号').grid(row=0, column=0)
        self.port_var = StringVar()
        self.port_var.set('000')
        self.port_entry = Entry(self.main_frame, textvariable=self.port_var)
        self.port_entry.grid(row=0, column=1)

        Label(self.main_frame, text='串口名称').grid(row=1, column=0)
        self.serial_var = StringVar()
        serial = list(self.main.setting['serial'].keys())
        if len(serial) == 0:
            serial = ['无可用配置']
        self.serial_var.set(serial[0])
        self.serial_option = OptionMenu(self.main_frame, self.serial_var, *serial)
        self.serial_option.grid(row=1, column=1)

        Label(self.main_frame, text='设备地址').grid(row=2, column=0)
        self.device_var = IntVar()
        self.device_var.set(1)
        self.device_entry = Entry(self.main_frame, textvariable=self.device_var)
        self.device_entry.grid(row=2, column=1)

        Label(self.main_frame, text='数据地址').grid(row=3, column=0)
        self.data_var = IntVar()
        self.data_var.set(1)
        self.data_entry = Entry(self.main_frame, textvariable=self.data_var)
        self.data_entry.grid(row=3, column=1)

        self.info_frame = Frame(self)
        self.info_frame.grid(row=1, column=0)
        self.info_label = Label(self.info_frame, text='', fg='red')
        self.info_label.grid(row=0, column=0)

        self.button_frame = Frame(self)
        self.button_frame.grid(row=2, column=0)
        self.save_button = Button(self.button_frame, text='保存', command=self.save)
        self.save_button.grid(row=0, column=0)

    def save(self):
        if self.check():
            if 'port' not in self.main.setting.keys():
                self.main.setting['port'] = {}
            self.main.setting['port'][self.port_var.get()] = {
                "data_id": self.data_var.get(),
                "device_id": self.data_var.get(),
                "property": {},
                "serial_id": self.serial_var.get()
            }
            self.main.port_frame.refresh()
            self.destroy()

    def check(self):
        if self.port_var.get() in self.main.setting['port'].keys():
            self.info_label['text'] = '标签名已存在'
            return False
        if self.serial_var.get() not in self.main.setting['serial'].keys():
            self.info_label['text'] = '未找到串口配置'
            return False
        try:
            self.device_var.get()
        except ValueError:
            self.info_label['text'] = '设备地址必须为整数'
            return False
        try:
            self.data_var.get()
        except ValueError:
            self.info_label['text'] = '数据地址必须为整数'
            return False
        return True


class PortEdit(Toplevel):
    def __init__(self, master, main, port_id):
        self.master = master
        self.main = main
        super(PortEdit, self).__init__()
        self.title('标签编辑器')

        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0)

        Label(self.main_frame, text='通道编号').grid(row=0, column=0)
        self.port_var = StringVar()
        self.port_var.set(port_id)
        self.port_entry = Entry(self.main_frame, textvariable=self.port_var, state=DISABLED)
        self.port_entry.grid(row=0, column=1)

        Label(self.main_frame, text='串口名称').grid(row=1, column=0)
        self.serial_var = StringVar()
        serial = list(self.main.setting['serial'].keys())
        self.serial_var.set(self.main.setting['port'][port_id]['serial_id'])
        self.serial_option = OptionMenu(self.main_frame, self.serial_var, *serial)
        self.serial_option.grid(row=1, column=1)

        Label(self.main_frame, text='设备地址').grid(row=2, column=0)
        self.device_var = IntVar()
        self.device_var.set(self.main.setting['port'][port_id]['device_id'])
        self.device_entry = Entry(self.main_frame, textvariable=self.device_var)
        self.device_entry.grid(row=2, column=1)

        Label(self.main_frame, text='数据地址').grid(row=3, column=0)
        self.data_var = IntVar()
        self.data_var.set(self.main.setting['port'][port_id]['data_id'])
        self.data_entry = Entry(self.main_frame, textvariable=self.data_var)
        self.data_entry.grid(row=3, column=1)

        self.info_frame = Frame(self)
        self.info_frame.grid(row=1, column=0)
        self.info_label = Label(self.info_frame, text='', fg='red')
        self.info_label.grid(row=0, column=0)

        self.button_frame = Frame(self)
        self.button_frame.grid(row=2, column=0)
        self.save_button = Button(self.button_frame, text='保存', command=self.save)
        self.save_button.grid(row=0, column=0)

    def save(self):
        if self.check():
            self.main.setting['port'][self.port_var.get()] = {
                "data_id": self.data_var.get(),
                "device_id": self.device_var.get(),
                "property": {},
                "serial_id": self.serial_var.get()
            }
            self.main.port_frame.refresh()
            self.destroy()

    def check(self):
        if self.serial_var.get() not in self.main.setting['serial'].keys():
            self.info_label['text'] = '未找到串口配置'
            return False
        try:
            self.device_var.get()
        except ValueError:
            self.info_label['text'] = '设备地址必须为整数'
            return False
        try:
            self.data_var.get()
        except ValueError:
            self.info_label['text'] = '数据地址必须为整数'
            return False
        return True
