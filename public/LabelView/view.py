from tkinter import LabelFrame, W, E, N, S
from public.LabelView.FrameView.view import DataLabel, DataCanvas


class DataLabelFrame(LabelFrame):
    def __init__(self, master, main, port_id, row, column):
        self.master = master
        self.main = main
        self.row = row
        self.column = column
        super(DataLabelFrame, self).__init__(self.master, bg='grey')
        self.grid(row=self.row, column=self.column, sticky=N+E+W+S)
        self['text'] = '通道编号: %s' % port_id
        self.bind('<Button-1>', self.main.function_adaptor(self.refresh_label, port_id))
        self.data_label = DataLabel(self, self.main)
        self.data_canvas = DataCanvas(self, self.main)

    def refresh(self, data):
        self.data_label.refresh(data)
        self.data_canvas.refresh(data)

    def refresh_label(self, event, port_id):
        self.main.property_label.set(port_id, self.main.read_json.get_property(port_id))
