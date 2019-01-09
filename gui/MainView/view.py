""" doc """
import tkinter as tk
from tkinter import Frame, Menu
from gui.MainView.InfoView.view import TimeLabel, PropertyLabelFrame, StatusLabelFrame
from gui.MainView.MenuView.view import CategoryEditor
from gui.MainView.DataView.view import StatusFrame, DataBook


class MenuBar(Menu):
    """ doc """
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(MenuBar, self).__init__(self.master)

        tool_menu = Menu(self, tearoff=0)
        tool_menu.add_command(label='类别编辑器', command=self.category_editor)
        self.add_cascade(label='工具', menu=tool_menu)
        self.master['menu'] = self
        self.ceditor = None

    def category_editor(self):
        """ doc """
        try:
            self.ceditor.destroy()
        except NameError:
            pass
        except AttributeError:
            pass
        self.ceditor = CategoryEditor(self.master, self.main)


class InfoFrame(Frame):
    """ doc """
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(InfoFrame, self).__init__(self.master)
        self.master.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky=tk.NW)

        self.main.time_label = TimeLabel(self, self.main)
        self.status_label_frame = StatusLabelFrame(self, self.main)
        self.property_label_frame = PropertyLabelFrame(self, self.main)


class DataFrame(Frame):
    """doc"""
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(DataFrame, self).__init__(self.master)
        self.master.columnconfigure(0, weight=3)
        self.grid(row=0, column=1, sticky=tk.NW)
        self.status_frame = StatusFrame(self, self.main)
        self.data_book = DataBook(self, self.main)
