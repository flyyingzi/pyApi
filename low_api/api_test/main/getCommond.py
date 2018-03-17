from excConfig import ExcConfig

'''
    get  commond  
    根据config文件 header  添加header  body  添加到body 中
    {{.example}} 这种格式
'''
class GetCommond:

    def __init__(self):
        self.config = ExcConfig()

    def get_commond_name(self,dict):
        name =""
        for k, v in dict.items():
            for key, value in v.items():
                if key == "name":
                    name = value
        return name


    def get_commond_Url(self,dict):
        url = {}
        vaules = self.config.return_Value()
        host = vaules["HOST"]
        for k, v in dict.items():
            for key,value in v.items():
                if key == "url":
                    if "{{.HOST}}" in value:
                        url = value.replace('{{.HOST}}',host)
                    else:    
                        url = value
        return url


    def get_commond_Method(self,dict):
        method = ""
        for k, v in dict.items():
            for key,value in v.items():
                if key == "method":
                    method = value
        return method


    def get_commond_Header(self,dict):
        header = {}

        for k, v in dict.items():
            for key,value in v.items():
                if key == "header":
                    header = value
        header.update(self.config.return_Header())
        return header


    def get_commond_Require(self,dict):
        require = ""
        for k, v in dict.items():
            for key,value in v.items():
                if key == "require":
                    require = value
        return require


    def get_commond_Params(self,dict):
        params = {}
        for k, v in dict.items():
            for key,value in v.items():
                if key == "params" or key == "urlparams":
                    params = value
        params.update(self.config.return_Body()) 
        return params


    def get_commond_Return(self,dict):
        value1 = ""
        for k, v in dict.items():
            for key,value in v.items():
                if key == "return":
                    value1 = value
        return value1


    def get_commond_Context(self,dict):
        context = ""
        for k, v in dict.items():
            if v.__contains__('context'):
                for key,value in v.items():
                    if key == "context":
                        context = value
            else:
                context = ""
        return context

if __name__ == '__main__':
    ff = GetCommond().get_commond_Header()
    print(ff)