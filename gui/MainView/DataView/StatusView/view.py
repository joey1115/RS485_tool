from tkinter import Label, LEFT


class StatusLabel(Label):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(StatusLabel, self).__init__(self.master, bg='white', justify=LEFT)
        self.grid(row=0, column=0)
        self['text'] = "正在读取"
