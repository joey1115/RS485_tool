import os
from tkinter import LabelFrame, Frame, Button, filedialog, Label, DISABLED, NORMAL
from public.InitView.PortView.view import PortTableFrame, PortButtonFrame
from public.InitView.SerialView.view import SerialTableFrame, SerialButtonFrame


class FileFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(FileFrame, self).__init__(self.master)
        self.grid(row=0, column=0)
        self.file_label = Label(self, text='未选择协议')
        self.file_label.grid(row=0, column=0, columnspan=2)


class SerialFrame(LabelFrame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(SerialFrame, self).__init__(self.master, text='串口')
        self.grid(row=1, column=0)

        self.serial_table_frame = SerialTableFrame(self, self.main)
        self.serial_button_frame = SerialButtonFrame(self, self.main)

    def refresh(self):
        self.serial_table_frame.clear()
        self.serial_table_frame.refresh()


class PortFrame(LabelFrame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(PortFrame, self).__init__(self.master, text='通道')
        self.grid(row=1, column=1)

        self.port_table_frame = PortTableFrame(self, self.main)
        self.port_button_frame = PortButtonFrame(self, self.main)

    def refresh(self):
        self.port_table_frame.clear()
        self.port_table_frame.refresh()


class ButtonFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(ButtonFrame, self).__init__(self.master)
        self.grid(row=1, column=2)

        self.clear_button = Button(self, text='重置', command=self.clear)
        self.clear_button.grid(row=0, column=0)

        self.protocol_button = Button(self, text='协议', command=self.open_protocol)
        self.protocol_button.grid(row=1, column=0)

        self.fileopen_button = Button(self, text='打开', command=self.open_file, state=DISABLED)
        self.fileopen_button.grid(row=2, column=0)

        self.filesave_button = Button(self, text='保存', command=self.save_file, state=DISABLED)
        self.filesave_button.grid(row=3, column=0)

        self.launch_button = Button(self, text='启动', command=self.launch, state=DISABLED)
        self.launch_button.grid(row=4, column=0)

    def clear(self):
        self.main.setting = {}
        self.main.protocol = {}
        self.main.serial_frame.refresh()
        self.main.port_frame.refresh()
        self.master.file_frame.file_label['text'] = "未选择协议"
        self.protocol_button['state'] = NORMAL
        self.fileopen_button['state'] = DISABLED
        self.filesave_button['state'] = DISABLED
        self.launch_button['state'] = DISABLED
        self.main.serial_frame.serial_button_frame.add_button['state'] = DISABLED
        self.main.serial_frame.serial_button_frame.edit_button['state'] = DISABLED
        self.main.serial_frame.serial_button_frame.delete_button['state'] = DISABLED
        self.main.port_frame.port_button_frame.add_button['state'] = DISABLED
        self.main.port_frame.port_button_frame.edit_button['state'] = DISABLED
        self.main.port_frame.port_button_frame.delete_button['state'] = DISABLED

    def open_protocol(self):
        curdir = os.path.abspath(os.curdir)
        d = curdir + "\\conf"
        filename = filedialog.askopenfilename(filetypes=[("JSON file", "*.json*")], initialdir=d)
        if len(filename) > 0:
            self.main.read_json.protocol_file = filename
            self.main.protocol = self.main.read_json.read_protocol()

            self.master.file_frame.file_label['text'] = filename
            self.protocol_button['state'] = DISABLED
            self.fileopen_button['state'] = NORMAL
            self.filesave_button['state'] = NORMAL
            self.launch_button['state'] = NORMAL
            self.main.serial_frame.serial_button_frame.add_button['state'] = NORMAL
            self.main.serial_frame.serial_button_frame.edit_button['state'] = NORMAL
            self.main.serial_frame.serial_button_frame.delete_button['state'] = NORMAL
            self.main.port_frame.port_button_frame.add_button['state'] = NORMAL
            self.main.port_frame.port_button_frame.edit_button['state'] = NORMAL
            self.main.port_frame.port_button_frame.delete_button['state'] = NORMAL

    def open_file(self):
        curdir = os.path.abspath(os.curdir)
        d = curdir + "\\conf"
        filename = filedialog.askopenfilename(filetypes=[("JSON file", "*.json*")], initialdir=d)
        if len(filename) > 0:
            self.main.read_json.port_file = filename
            self.main.setting = self.main.read_json.get_setting()
            self.main.keywords = self.main.read_json.get_keywords()
            self.main.category_key = self.main.keywords[0]
            self.main.result = self.main.read_json.get_result(self.main.category_key)
            self.main.serial_frame.refresh()
            self.main.port_frame.refresh()

    def save_file(self):
        curdir = os.path.abspath(os.curdir)
        d = curdir + "\\conf"
        filename = filedialog.asksaveasfilename(filetypes=[("JSON file", "*.json*")], initialdir=d)
        if len(filename) > 0:
            if len(filename) < 5:
                filename += '.json'
            elif filename[-6:-1] != '.json':
                filename += '.json'
            self.main.read_json.port_file = filename
            self.main.read_json.save_setting(self.main.setting)

    def launch(self):
        self.main.flags['launch'] = True
        self.master.destroy()
