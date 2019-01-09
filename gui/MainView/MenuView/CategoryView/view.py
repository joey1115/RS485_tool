from tkinter import Frame, LabelFrame, Scrollbar, Button, N, W, E, S
from tkinter.ttk import Treeview


class CategoryFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(CategoryFrame, self).__init__(self.master)
        self.grid(row=2, column=0)

        self.label_frame = LabelFrame(self, text='通道: 000')
        self.label_frame.grid(row=0, column=0)
        self.scrollbar = Scrollbar(self.label_frame)
        self.scrollbar.grid(row=0, column=1, sticky=N + W + E +S)
        self.tree_view = Treeview(
            self.label_frame,
            columns=('c1', 'c2'),
            show="headings",
            yscrollcommand=self.scrollbar.set,
            height=10
        )
        self.tree_view.grid(row=0, column=0)

        self.tree_view.column('c1', width=200, anchor='center')
        self.tree_view.column('c2', width=200, anchor='center')

        self.tree_view.heading('c1', text='名称')
        self.tree_view.heading('c2', text='值')

        self.scrollbar.configure(command=self.tree_view.yview)

        self.frame = Frame(self.label_frame)
        self.frame.grid(row=0, column=2)

        Button(self.frame, text='删除', command=self.delete).grid(row=0, column=0)

    def refresh(self, port_id):
        self.master.info_label['text'] = '已保存'
        self.port_id = port_id
        self.tree_view.delete(*self.tree_view.get_children())
        self.label_frame['text'] = '通道编号: %s' % port_id
        prop = self.main.read_json.get_property(port_id)
        for key in prop.keys():
            self.tree_view.insert('', 'end', values=(key, prop[key]), text=key)

    def delete(self):
        self.master.info_label['text'] = '未保存'
        item_id = self.tree_view.selection()
        if len(item_id) > 0:
            property_id = self.tree_view.item(item_id[0])['text']
            self.main.setting['port'][self.port_id]['property'].pop(property_id)
            self.tree_view.delete(item_id)
