from tkinter import Toplevel, Label, StringVar, Entry, OptionMenu, IntVar, Frame, Button, DISABLED
import serial.tools.list_ports


class SerialAdd(Toplevel):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(SerialAdd, self).__init__()
        self.title('串口编辑器')

        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0)

        Label(self.main_frame, text='串口名称').grid(row=0, column=0)
        self.name_var = StringVar()
        self.name_var.set('新串口')
        self.name_entry = Entry(self.main_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1)

        Label(self.main_frame, text='COM选择').grid(row=1, column=0)
        self.com_var = StringVar()
        com_list = [com[0] for com in list(serial.tools.list_ports.comports())]
        if len(com_list) == 0:
            com_list = ['无可用COM']
        self.com_var.set(com_list[0])
        self.com_option = OptionMenu(self.main_frame, self.com_var, *com_list)
        self.com_option.grid(row=1, column=1)

        Label(self.main_frame, text='波特率').grid(row=2, column=0)
        self.baudrate_var = IntVar()
        self.baudrate_var.set(9600)
        self.baudrate_entry = Entry(self.main_frame, textvariable=self.baudrate_var)
        self.baudrate_entry.grid(row=2, column=1)

        Label(self.main_frame, text='停止位').grid(row=3, column=0)
        self.stopbits_var = StringVar()
        self.stopbits_var.set("1")
        self.stopbits_option = OptionMenu(self.main_frame, self.stopbits_var, "1", "1.5", "2")
        self.stopbits_option.grid(row=3, column=1)

        Label(self.main_frame, text='校验位').grid(row=4, column=0)
        self.parity_var = StringVar()
        self.parity_var.set("NONE")
        self.parity_option = OptionMenu(self.main_frame, self.parity_var, 'NONE', 'EVEN', 'ODD', 'SPACE', 'MARK')
        self.parity_option.grid(row=4, column=1)

        Label(self.main_frame, text='数据位').grid(row=5, column=0)
        self.bytesize_var = StringVar()
        self.bytesize_var.set("8")
        self.bytesize_option = OptionMenu(self.main_frame, self.bytesize_var, '5', '6', '7', '8')
        self.bytesize_option.grid(row=5, column=1)

        Label(self.main_frame, text='数据位').grid(row=6, column=0)
        self.protocol_var = StringVar()
        if 'protocol' in self.main.protocol.keys():
            protocol_list = list(self.main.protocol["protocol"].keys())
            if len(protocol_list) > 0:
                self.protocol_var.set(protocol_list[0])
            else:
                self.protocol_var.set("协议未配置")
        else:
            protocol_list = ['协议配置文件错误']
            self.protocol_var.set(protocol_list[0])
        self.protocol_option = OptionMenu(self.main_frame, self.protocol_var, *protocol_list)
        self.protocol_option.grid(row=6, column=1)

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
            if 'serial' not in self.main.setting.keys():
                self.main.setting['serial'] = {}
            self.main.setting['serial'][self.name_var.get()] = {
                "stopbits": self.stopbits_var.get(),
                "parity": self.parity_var.get(),
                "baudrate": self.baudrate_var.get(),
                "protocol_id": self.protocol_var.get(),
                "com": self.com_var.get(),
                "bytesize": self.bytesize_var.get()
            }
            self.main.serial_frame.refresh()
            self.destroy()

    def check(self):
        if self.name_var.get() in self.main.setting['serial'].keys():
            self.info_label['text'] = '串口名已存在'
            return False
        if len(self.com_var.get()) > 3 and self.com_var.get().find('COM') == 0:
            try:
                int(self.com_var.get()[3:])
            except ValueError:
                self.info_label['text'] = 'COM不正确'
                return False
        else:
            self.info_label['text'] = 'COM不正确'
            return False
        try:
            self.baudrate_var.get()
        except ValueError:
            self.info_label['text'] = '波特率必须为整数'
            return False
        if self.protocol_var.get() == "协议配置文件错误":
            self.info_label['text'] = '协议配置文件错误'
        elif self.protocol_var.get() not in self.main.protocol['protocol'].keys():
            self.info_label['text'] = '协议名称不存在'
            return False
        if self.stopbits_var.get() not in ["1", "1.5", "2"]:
            self.info_label['text'] = '停止位错误'
            return False
        if self.bytesize_var.get() not in ["5", "6", "7", "8"]:
            self.info_label['text'] = '数据位错误'
            return False
        if self.stopbits_var.get() not in ["NONE", "EVEN", "ODD", "SPACE", "MARK"]:
            self.info_label['text'] = '校验位位错误'
            return False
        return True


class SerialEdit(Toplevel):
    def __init__(self, master, main, serial_id):
        self.master = master
        self.main = main
        super(SerialEdit, self).__init__()
        self.title('标签编辑器')

        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0)

        Label(self.main_frame, text='串口名称').grid(row=0, column=0)
        self.name_var = StringVar()
        self.name_var.set(serial_id)
        self.name_entry = Entry(self.main_frame, textvariable=self.name_var, state=DISABLED)
        self.name_entry.grid(row=0, column=1)

        Label(self.main_frame, text='COM选择').grid(row=1, column=0)
        self.com_var = StringVar()
        com_list = list(serial.tools.list_ports.comports())
        if len(com_list) == 0:
            com_list = ['无可用COM']
        self.com_var.set(self.main.setting['serial'][serial_id]['com'])
        self.com_option = OptionMenu(self.main_frame, self.com_var, *com_list)
        self.com_option.grid(row=1, column=1)

        Label(self.main_frame, text='波特率').grid(row=2, column=0)
        self.baudrate_var = IntVar()
        self.baudrate_var.set(self.main.setting['serial'][serial_id]['baudrate'])
        self.baudrate_entry = Entry(self.main_frame, textvariable=self.baudrate_var)
        self.baudrate_entry.grid(row=2, column=1)

        Label(self.main_frame, text='停止位').grid(row=3, column=0)
        self.stopbits_var = StringVar()
        self.stopbits_var.set(self.main.setting['serial'][serial_id]['stopbits'])
        self.stopbits_option = OptionMenu(self.main_frame, self.stopbits_var, "1", "1.5", "2")
        self.stopbits_option.grid(row=3, column=1)

        Label(self.main_frame, text='校验位').grid(row=4, column=0)
        self.parity_var = StringVar()
        self.parity_var.set(self.main.setting['serial'][serial_id]['parity'])
        self.parity_option = OptionMenu(self.main_frame, self.parity_var, 'NONE', 'EVEN', 'ODD', 'SPACE', 'MARK')
        self.parity_option.grid(row=4, column=1)

        Label(self.main_frame, text='数据位').grid(row=5, column=0)
        self.bytesize_var = StringVar()
        self.bytesize_var.set(self.main.setting['serial'][serial_id]['bytesize'])
        self.bytesize_option = OptionMenu(self.main_frame, self.bytesize_var, '5', '6', '7', '8')
        self.bytesize_option.grid(row=5, column=1)

        Label(self.main_frame, text='协议类型').grid(row=6, column=0)
        self.protocol_var = StringVar()
        if "protocol" in self.main.protocol.keys():
            protocol_list = list(self.main.protocol["protocol"].keys())
            self.protocol_var.set(self.main.setting['serial'][serial_id]['protocol_id'])
        else:
            protocol_list = ['协议配置文件错误']
            self.protocol_var.set(protocol_list[0])
        self.protocol_option = OptionMenu(self.main_frame, self.protocol_var, *protocol_list)
        self.protocol_option.grid(row=6, column=1)

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
            self.main.setting['serial'][self.name_var.get()] = {
                "stopbits": self.stopbits_var.get(),
                "parity": self.parity_var.get(),
                "baudrate": self.baudrate_var.get(),
                "protocol_id": self.protocol_var.get(),
                "com": self.com_var.get(),
                "bytesize": self.bytesize_var.get()
            }
            self.main.serial_frame.refresh()
            self.destroy()

    def check(self):
        if len(self.com_var.get()) > 3 and self.com_var.get().find('COM') == 0:
            try:
                int(self.com_var.get()[3:])
            except ValueError:
                self.info_label['text'] = 'COM不正确'
                return False
        else:
            return False
        try:
            self.baudrate_var.get()
        except ValueError:
            self.info_label['text'] = '波特率必须为整数'
            return False
        if self.protocol_var.get() == "协议配置文件错误":
            self.info_label['text'] = '协议配置文件错误'
        elif self.protocol_var.get() not in self.main.protocol['protocol'].keys():
            self.info_label['text'] = '协议名称不存在'
            return False
        if self.stopbits_var.get() not in ["1", "1.5", "2"]:
            self.info_label['text'] = '停止位错误'
            return False
        if self.bytesize_var.get() not in ["5", "6", "7", "8"]:
            self.info_label['text'] = '数据位错误'
            return False
        if self.stopbits_var.get() not in ["NONE", "EVEN", "ODD", "SPACE", "MARK"]:
            self.info_label['text'] = '校验位位错误'
            return False
        return True
