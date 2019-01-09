from tkinter import Label, LEFT


class StatusLabel(Label):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(StatusLabel, self).__init__(self.master, bg='white', justify=LEFT)
        self.grid(row=0, column=0)
        self['text'] = '报警总数:\n故障总数:\n首报通道:\n'
        self.property = {}

    def refresh(self, alarm, error, port_id):
        self.property = self.main.read_json.get_property(port_id)

        temp = '报警总数: %d\n故障总数: %d\n首报通道:\n' % (alarm, error)
        if port_id > 0:
            temp += ' -通道编号: %s' % port_id
            for key in self.property.keys():
                temp += '\n -%s: %s' % (key, self.property[key])
        else:
            temp += ' -通道编号:'

        self['text'] = temp
