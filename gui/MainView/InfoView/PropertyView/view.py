from tkinter import Label, LEFT


class PropertyLabel(Label):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(PropertyLabel, self).__init__(self.master, bg='white', justify=LEFT)
        self.grid(row=0, column=0)
        self['text'] = '通道编号:\n'

    def set(self, port_id, prop):
        temp_text = "通道编号: %s\n" % port_id
        for key in prop.keys():
            temp_text += "%s: %s\n" % (key, prop[key])
        self['text'] = temp_text
