from tkinter import Frame, NW
from tkinter.ttk import Notebook

from gui.MainView.DataView.BookView.view import DataLabelView, CategoryView

from gui.MainView.DataView.StatusView.view import StatusLabel


class StatusFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(StatusFrame, self).__init__(self.master)
        self.master.columnconfigure(0, weight=3)
        self.grid(row=0, column=0, sticky=NW)
        self.main.status_label = StatusLabel(self, self.main)


class DataBook(Notebook):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(DataBook, self).__init__(master)
        self.grid(row=1, column=0, sticky=NW)

        self.main.label_view = DataLabelView(self, self.main)
        self.add(self.main.label_view, text='标签模式')

        self.main.category_view = CategoryView(self, self.main)
        self.add(self.main.category_view, text='分类模式')
