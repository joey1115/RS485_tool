from tkinter import Label, LabelFrame, N, E, W, S
from gui.MainView.InfoView.PropertyView.view import PropertyLabel
from gui.MainView.InfoView.StatusView.view import StatusLabel


class TimeLabel(Label):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(TimeLabel, self).__init__(self.master)
        self.grid(row=0, column=0)
        self['text'] = '2017-11-09 10:00:00'


class StatusLabelFrame(LabelFrame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(StatusLabelFrame, self).__init__(self.master)
        self.grid(row=1, column=0, sticky=N + E + W + S)
        self['text'] = '当前状态'
        self.main.info_status_label = StatusLabel(self, self.main)


class PropertyLabelFrame(LabelFrame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(PropertyLabelFrame, self).__init__(self.master)
        self.grid(row=2, column=0, sticky=N + E + W + S)
        self['text'] = '通道属性'
        self.main.property_label = PropertyLabel(self, self.main)
