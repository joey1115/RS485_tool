from tkinter import Frame, Scrollbar, Button, N, E, W, S, DISABLED
from tkinter.ttk import Treeview
from public.InitView.PortView.TopView.view import PortAdd, PortEdit


class PortTableFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(PortTableFrame, self).__init__(self.master)
        self.grid(row=0, column=0)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky=N + E + W + S)
        self.port_tree_view = Treeview(
            self,
            columns=('c1', 'c2', 'c3', 'c4'),
            show="headings",
            yscrollcommand=self.scrollbar.set,
            height=10,
            selectmode='browse'
        )
        self.port_tree_view.grid(row=0, column=0)
        self.port_tree_view.column('c1', width=100, anchor='center')
        self.port_tree_view.column('c2', width=100, anchor='center')
        self.port_tree_view.column('c3', width=100, anchor='center')
        self.port_tree_view.column('c4', width=100, anchor='center')
        self.port_tree_view.heading('c1', text='通道编号')
        self.port_tree_view.heading('c2', text='串口名称')
        self.port_tree_view.heading('c3', text='设备地址')
        self.port_tree_view.heading('c4', text='数据编号')
        self.scrollbar.configure(command=self.port_tree_view.yview)

    def clear(self):
        self.port_tree_view.delete(*self.port_tree_view.get_children())

    def refresh(self):
        if 'port' in self.main.setting.keys():
            for port_key in self.main.setting['port'].keys():
                port_setting = self.main.setting['port'][port_key]
                self.port_tree_view.insert(
                    '',
                    'end',
                    values=(
                        port_key,
                        port_setting['serial_id'],
                        port_setting['device_id'],
                        port_setting['data_id']
                    ),
                    text=port_key
                )


class PortButtonFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(PortButtonFrame, self).__init__(self.master)
        self.grid(row=0, column=1)

        self.add_button = Button(self, text='添加', command=self.add, state=DISABLED)
        self.add_button.grid(row=0, column=0)

        self.edit_button = Button(self, text='编辑', command=self.edit, state=DISABLED)
        self.edit_button.grid(row=1, column=0)

        self.delete_button = Button(self, text='删除', command=self.delete, state=DISABLED)
        self.delete_button.grid(row=2, column=0)

        self.add_top = None
        self.edit_top = None

    def add(self):
        try:
            self.add_top.destroy()
        except AttributeError:
            pass
        self.add_top = PortAdd(self.master, self.main)

    def edit(self):
        try:
            self.edit_top.destroy()
        except AttributeError:
            pass
        item_id = self.master.port_table_frame.port_tree_view.selection()
        if len(item_id) > 0:
            port_id = self.master.port_table_frame.port_tree_view.item(item_id[0])['text']
            self.edit_top = PortEdit(self.master, self.main, port_id)

    def delete(self):
        item_id = self.master.port_table_frame.port_tree_view.selection()
        if len(item_id) > 0:
            port_id = self.master.port_table_frame.port_tree_view.item(item_id[0])['text']
            self.main.setting['port'].pop(port_id)
            self.master.port_table_frame.port_tree_view.delete(item_id)
