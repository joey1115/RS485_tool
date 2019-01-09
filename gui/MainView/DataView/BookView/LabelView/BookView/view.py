from tkinter import Frame, NW
from public.LabelView.view import DataLabelFrame


class LabelView(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(LabelView, self).__init__(self.master)
        self.grid(row=0, column=0, sticky=NW)

    def create_label(self, port_id, count):
        row = count // self.main.label_column_num
        column = count % self.main.label_column_num
        self.main.label_data_frame[port_id] = DataLabelFrame(self, self.main, port_id, row, column)
