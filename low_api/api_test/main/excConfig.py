import json
class ExcConfig(object):

    def __init__(self, config_file = 'config.cfg'):
        f = open(config_file, 'r', encoding='utf-8')
        self.value = json.load(f)
        f.close()

    def return_Value(self):
        value = {}
        for k,v in self.value.items():
            if k == 'Value':
                value = v
        return value

    def return_Header(self):
        value = {}
        for k,v in self.value.items():
            if k == 'Header':
                value = v
        return value

    def return_Body(self):
        value = {}
        for k,v in self.value.items():
            if k == 'Body':
                value = v
        return value





if __name__ == '__main__':
    a = ExcConfig().return_Body()
    b = ExcConfig().return_Value()
    c = ExcConfig().return_Header()
    print(a,b,c)