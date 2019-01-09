from tkinter import Canvas, Frame, Scrollbar, N, E, W, S, Label
from public.LabelView.view import DataLabelFrame


class DataCanvas(Canvas):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(DataCanvas, self).__init__(self.master, width=self.main.x-200, height=self.main.y-200, bg='white')
        self.grid(row=0, column=0, sticky=N + S + W + E)
        self.category_data_frame = DataFrame(self, self.main)
        self.create_window((0, 0), window=self.category_data_frame, anchor='nw')
        self.category_data_frame.bind("<Configure>", self.scrollbar_function)

    def scrollbar_function(self, event):
        self.configure(scrollregion=self.bbox("all"))

    def display(self):
        self.category_data_frame.destroy()
        self.category_data_frame = DataFrame(self, self.main)
        self.create_window((0, 0), window=self.category_data_frame, anchor='n')
        self.category_data_frame.bind("<Configure>", self.scrollbar_function)


class ScrollBar(Scrollbar):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(ScrollBar, self).__init__(self.master)
        self.grid(row=0, column=1, sticky=N + E + W + S)


class DataFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(DataFrame, self).__init__(self.master, bg='white')
        self.row_frames = {}
        self.main.category_row = 0
        self.main.category_data_label = {}
        self.main.category_ports = []
        for key in self.main.result.keys():
            self.main.category_key = key
            self.row_frames[self.main.category_row] = RowFrame(self, self.main)
            self.main.category_row += 1

    def refresh(self, port_id, data):
        self.row_frames[(port_id - 1) // self.main.page_num].refresh(port_id, data)


class RowFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(RowFrame, self).__init__(self.master, bg='white')
        self.grid(row=self.main.category_row, column=0)
        Label(self, text=self.main.category_key).grid(row=0, column=0)

        self.main.label_row = 0
        self.main.label_column = 0
        count = 0

        for port in self.main.result[self.main.category_key]:
            row = count // self.main.label_column_num
            column = count % self.main.label_column_num + 1
            count += 1
            self.main.category_ports.append(port)
            self.main.category_data_label[port] = DataLabelFrame(self, self.main, port, row, column)
            self.main.category_data_label[port].refresh({
                'type': '',
                'value': 0,
                'unit': '',
                'msg': '',
                'time': 0,
                'range': 1,
                'color': 'grey'
            })
