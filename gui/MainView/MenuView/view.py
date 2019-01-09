""" doc """
from tkinter import Toplevel, Label, OptionMenu, Button, Frame, StringVar, Entry
from gui.MainView.MenuView.CategoryView.view import CategoryFrame


class CategoryEditor(Toplevel):
    """ doc """

    def __init__(self, master, main):
        self.property = {}
        self.master = master
        self.main = main
        super(CategoryEditor, self).__init__(master)
        self.title('类别编辑器')
        self.wm_attributes("-topmost", 1)

        self.frame = Frame(self)
        self.frame.grid(row=0, column=0)
        Label(self.frame, text='通道编号:').grid(row=0, column=0)
        self.port_var = StringVar()
        port_list = list(self.main.setting['port'].keys())
        if len(port_list) > 0:
            self.port_var.set(port_list[0])
        else:
            port_list = ['无标签']
        self.option_menu = OptionMenu(self.frame, self.port_var, *port_list)
        self.option_menu.grid(row=0, column=1)
        self.display_button = Button(self.frame, text='显示', command=self.refresh)
        self.display_button.grid(row=0, column=2)
        self.save_button = Button(self.frame, text='保存', command=self.save)
        self.save_button.grid(row=0, column=3)

        self.info_frame = Frame(self)
        self.frame.grid(row=1, column=0)
        self.info_label = Label(self.info_frame, text='已保存')
        self.info_label.grid(row=0, column=0)

        self.main_frame = CategoryFrame(self, self.main)
        self.refresh()

        self.edit_frame = Frame(self)
        Label(self.edit_frame, text='名称').grid(row=0, column=0)
        Label(self.edit_frame, text='值').grid(row=0, column=1)

        self.name_var = StringVar()
        Entry(self.edit_frame, textvariable=self.name_var).grid(row=1, column=0)

        self.value_var = StringVar()
        Entry(self.edit_frame, textvariable=self.value_var).grid(row=1, column=1)

        Button(self.edit_frame, text='更新', command=self.update_property)

    def update_property(self):
        self.info_label['text'] = '未保存'
        if self.main_frame.port_id in self.main.setting['port'].keys():
            self.main.setting['port'][self.main_frame.port_id]['property'][self.name_var.get()] = self.value_var.get()
            self.main_frame.refresh(self.main_frame.port_id)

    def save(self):
        self.info_label['text'] = '已保存'
        self.main.read_json.save_setting()

    def refresh(self):
        self.main_frame.refresh(self.port_var.get())
