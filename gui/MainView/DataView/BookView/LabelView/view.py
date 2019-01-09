from tkinter import NW
from tkinter.ttk import Notebook
from gui.MainView.DataView.BookView.LabelView.BookView.view import LabelView


class LabelBook(Notebook):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(LabelBook, self).__init__(master)
        self.grid(row=0, column=0, sticky=NW)
        self.frames = []
        self.data_label_id = []
        count = 0
        for port_key in self.main.setting['port'].keys():
            if count == 0:
                self.frames.append(LabelView(self, self.main))
                self.add(self.frames[-1], text='标签页%d' % len(self.frames))
            self.frames[-1].create_label(port_key, count)
            count += 1
            count = count % self.main.page_label_num
