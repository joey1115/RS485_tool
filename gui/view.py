""" doc """
from tkinter import Tk
from gui.MainView.view import InfoFrame, DataFrame, MenuBar
from public.InitView.view import FileFrame, SerialFrame, PortFrame, ButtonFrame
from thread import TimeThread, DataThread, UIThread, StatusThread


class Init(Tk):
    """ doc """
    def __init__(self, main):
        self.main = main
        super(Init, self).__init__()
        self.title('配置')

        self.file_frame = FileFrame(self, self.main)
        self.main.serial_frame = SerialFrame(self, self.main)
        self.main.port_frame = PortFrame(self, self.main)
        self.button_frame = ButtonFrame(self, self.main)

        self.mainloop()


class Main(Tk):
    """ doc """
    def __init__(self, main):
        self.main = main
        super(Main, self).__init__()
        self.title("System")
        self.rowconfigure(0, weight=1)
        size = '%dx%d+%d+%d' % (self.main.x-100, self.main.y-200, 50, 50)
        self.geometry(size)

        MenuBar(self, self.main)
        self.info_frame = InfoFrame(self, self.main)
        self.data_frame = DataFrame(self, self.main)

        self.main.threads['time'] = TimeThread(self.main)
        self.main.threads['data'] = DataThread(self.main)
        self.main.threads['ui'] = UIThread(self.main)
        self.main.threads['status'] = StatusThread(self.main)

        self.main.flags['launch'] = False
        self.main.flags['ui'] = True
        self.main.flags['time'] = True
        self.main.flags['label_ui'] = True
        self.main.flags['category_ui'] = True
        self.main.flags['table_ui'] = True
        self.main.flags['status'] = True
        self.main.flags['data'] = True

        self.mainloop()
