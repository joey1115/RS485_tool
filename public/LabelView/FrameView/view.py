from tkinter import Label, LEFT, Canvas, NW
import time


class DataLabel(Label):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(DataLabel, self).__init__(self.master, bg='white', justify=LEFT)
        self.grid(row=0, column=0, sticky=NW)
        self['text'] = "气体名称: \n读数: \n状态: \n更新时间: 00:00:00"

    def refresh(self, data):
        self['text'] = "气体名称: %s\n读数: %3.2f %s\n状态: %s\n更新时间: %s" % (
            data['type'],
            data['value'],
            data['unit'],
            data['msg'],
            self.time_decode(data['time'])
        )

    def time_decode(self, t):
        return time.strftime("%H:%M:%S", time.localtime(t))


class DataCanvas(Canvas):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(DataCanvas, self).__init__(master, width=15, height=self.main.length, bg="white")
        self.grid(row=0, column=1, sticky=NW)
        self.rect_id = self.create_rectangle(0, 0, 30, self.main.length)

    def refresh(self, data):
        temp_length = int(self.main.length * (1 - data['value']/data['range']))
        self.coords(self.rect_id, 0, temp_length, 30, self.main.length)
        self.itemconfig(self.rect_id, fill=data['color'], outline=data['color'])
