from tkinter import Frame, Scrollbar, Button, N, E, W, S, DISABLED
from tkinter.ttk import Treeview
from public.InitView.SerialView.TopView.view import SerialAdd, SerialEdit


class SerialTableFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(SerialTableFrame, self).__init__(self.master)
        self.grid(row=0, column=0)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky=N + E + W + S)
        self.serial_tree_view = Treeview(
            self,
            columns=('c1', 'c2'),
            show="headings",
            yscrollcommand=self.scrollbar.set,
            height=10,
            selectmode='browse'
        )
        self.serial_tree_view.grid(row=0, column=0)
        self.serial_tree_view.column('c1', width=100, anchor='center')
        self.serial_tree_view.column('c2', width=100, anchor='center')
        self.serial_tree_view.heading('c1', text='名称')
        self.serial_tree_view.heading('c2', text='端口')
        self.scrollbar.configure(command=self.serial_tree_view.yview)

    def clear(self):
        self.serial_tree_view.delete(*self.serial_tree_view.get_children())

    def refresh(self):
        if 'serial' in self.main.setting.keys():
            for serial_key in self.main.setting['serial'].keys():
                serial_setting = self.main.setting['serial'][serial_key]
                self.serial_tree_view.insert('', 'end', values=(serial_key, serial_setting['com']), text=serial_key)


class SerialButtonFrame(Frame):
    def __init__(self, master, main):
        self.master = master
        self.main = main
        super(SerialButtonFrame, self).__init__(self.master)
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
        self.add_top = SerialAdd(self.master, self.main)

    def edit(self):
        try:
            self.edit_top.destroy()
        except AttributeError:
            pass
        item_id = self.master.serial_table_frame.serial_tree_view.selection()
        if len(item_id) > 0:
            serial_id = self.master.serial_table_frame.serial_tree_view.item(item_id[0])['text']
            self.edit_top = SerialEdit(self.master, self.main, serial_id)

    def delete(self):
        item_id = self.master.serial_table_frame.serial_tree_view.selection()
        if len(item_id) > 0:
            serial_id = self.master.serial_table_frame.serial_tree_view.item(item_id[0])['text']
            self.main.setting['serial'].pop(serial_id)
            self.master.serial_table_frame.serial_tree_view.delete(item_id)
