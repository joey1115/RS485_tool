from tkinter import Frame, NW

from gui.MainView.DataView.BookView.LabelView.view import LabelBook

from gui.MainView.DataView.BookView.CategoryView.view import DataCanvas, ScrollBar


class DataLabelView(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(DataLabelView, self).__init__(self.master)
        self.grid(row=0, column=0, sticky=NW)
        self.label_book = LabelBook(self, self.main)
        for port_key in self.main.setting['port'].keys():
            self.refresh(
                port_key,
                {
                    'type': '',
                    'value': 0,
                    'unit': '',
                    'msg': '',
                    'time': 0,
                    'range': 1,
                    'color': 'grey'
                }
            )

    def refresh(self, port_id, data):
        self.main.label_data_frame[port_id].refresh(data)


class CategoryView(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(CategoryView, self).__init__(self.master)
        self.grid(row=0, column=0, sticky=NW)

        self.data_canvas = DataCanvas(self, self.main)
        self.scrollbar = ScrollBar(self, self.main)

        self.data_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.data_canvas.yview)

    def refresh(self, port_id, data):
        if port_id in self.main.category_ports:
            self.main.category_data_label[port_id].refresh(data)