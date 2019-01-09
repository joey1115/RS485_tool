import json
import os


class ReadJSON:
    def __init__(self, main):
        self.main = main
        self.dir = os.path.abspath(os.curdir)
        self.port_file = self.dir + "\\conf\\conf.json"
        self.protocol_file = self.dir + "\\conf\\protocol.json"

    def read_protocol(self):
        file = open(self.protocol_file, encoding='utf-8')
        protocol = json.load(file)
        file.close()
        return protocol

    def save_setting(self, setting):
        file = open(self.port_file, 'w', encoding='utf-8')
        file.write(json.dumps(setting, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': ')))
        file.close()

    def get_setting(self):
        file = open(self.port_file, encoding='utf-8')
        setting = json.load(file)
        file.close()
        return setting

    def get_keywords(self):
        keywords = []
        file = open(self.port_file, encoding='utf-8')
        setting = json.load(file)
        for port_key in setting['port'].keys():
            port = setting['port'][port_key]
            for key in port['property'].keys():
                if key not in keywords:
                    keywords.append(key)
        return keywords

    def get_result(self, keyword):
        result = {}
        file = open(self.port_file, encoding='utf-8')
        setting = json.load(file)
        for port_key in setting['port'].keys():
            port = setting['port'][port_key]
            for key in port['property'].keys():
                if key == keyword:
                    if port['property'][key] not in result.keys():
                        result[port['property'][key]] = []
                    result[port['property'][key]].append(port_key)
        return result

    def get_property(self, port_id):
        prop = {}
        file = open(self.port_file, encoding='utf-8')
        setting = json.load(file)
        for port_key in setting['port'].keys():
            port = setting['port'][port_key]
            if port_id == port_key:
                prop = port['property']
        return prop

    # def get_serial_name(self, num):
    #     serial_name = ''
    #     file = open(self.port_file, encoding='utf-8')
    #     setting = json.load(file)
    #     for setting in setting['serial']:
    #         if num == setting['ID']:
    #             serial_name = setting['name']
    #     return serial_name
