""" doc """
import queue
from gui.view import Init, Main
from readdata import Read1, Read2, Read3
from readjson import ReadJSON
from win32api import GetSystemMetrics


class Project:
    """ doc """
    def __init__(self):
        self.threads = {}
        self.flags = {
            'ui': False,
            'label_ui': False,
            'category_ui': False,
            'table_ui': False,
            'time': False,
            'status': False,
            'data': False,
            'launch': False,
            'run': False
        }
        self.property = {}
        self.property_num = 1
        self.time_label = None
        self.serial_label = None
        self.x = GetSystemMetrics(0)
        self.y = GetSystemMetrics(1)
        self.label_column_num = (self.x - 400) // 120
        self.label_row_num = (self.y - 100) // 100
        self.alarm = {}
        self.error = {}
        self.page_label_num = self.label_row_num * self.label_column_num
        self.page_num = 0
        self.label_row = 0
        self.label_column = 0
        self.property_label = None
        self.property_label_prop = {}
        self.property_label_id = 1
        self.category_row = 0
        self.category_key = ''
        self.label_data = {}
        self.label_view = None
        self.category_data_label = {}
        self.category_ports = []
        self.info_status_label = None
        self.first_alarm = 0
        self.temp_data = {}
        self.ports = []
        self.label_data_frame = {}
        self.read_data = {}
        self.data_queue = queue.Queue(maxsize=128)
        self.read_data['新探头'] = Read1(self)
        self.read_data['老主机'] = Read2(self)
        self.read_data['二路'] = Read3(self, 2)
        self.read_data['四路'] = Read3(self, 4)
        self.read_json = ReadJSON(self)
        self.setting = {'port': {}, 'serial': {}}
        self.keywords = []
        self.category_key = ''
        self.result = {}
        self.protocol = {}
        self.main = None
        self.init = None
        self.length = 60

        self.start()

    def start(self):
        self.init = Init(self)
        if self.flags['launch']:
            self.main = Main(self)

    @staticmethod
    def function_adaptor(func, *arguments):
        """ doc """
        return lambda event, fun=func, args=arguments: fun(event, *args)


if __name__ == '__main__':
    Project()
