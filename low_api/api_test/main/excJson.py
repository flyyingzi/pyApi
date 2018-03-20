# 解析json

import json
import collections
from excConfig import ExcConfig

class ExcJson(object):

    '''
    json 数据解析

    Name        string                 `json:"name" description:"名称"`
    URL         string                 `json:"url" description:"请求地址"`
    Method      string                 `json:"method" description:"请求方式"`
    Require     string                 `json:"require" description:"前置需求"`
    ContentType string                 `json:"contenttype" description:"ContentType"`
    RequestLua  []string               `json:"requestlua" description:"请求前调用的lua文件"`
    Header      map[string]string      `json:"header" description:"请求头"`
    URLParams   *json.RawMessage       `json:"urlparams" description:"url请求参数"`
    Params      *json.RawMessage       `json:"params" description:"请求参数"`
    Return      map[string]interface{} `json:"return" description:"期望返回"`
    ReturnLua   []string               `json:"returnlua" description:"期望返回lua验证"`
    NextLua     []string               `json:"nextjs" description:"执行后续命令前调用的lua文件"`
    Context     map[string]string      `json:"context" description:"上下文"`
    SubCommand  []*Command             `json:"subcommand" description:"子命令"`
    '''
    def __init__(self,jsonFile='ceshi.json'):
        self.config = ExcConfig()

        f = open(jsonFile, 'r', encoding='utf-8')
        self.load_dict = json.load(f)
        f.close()

    def getNumber(self):
        
        return len(self.load_dict)

    def getMap(self):
        #没执行的命令
        map = collections.OrderedDict()
        for all in self.load_dict:
            name = self.getName(all)
            require = self.getRequire(all)
            if all.__contains__('require'):
               map.update({name:all})
        return map

    def deleteMap(self, dic ,name):

        dic.pop(name)

    def getCommond(self):
        commond={}
        for all in self.load_dict:
            name = self.getName(all)
            #  print(name)
            url = self.getUrl(all)
            method = self.getMethod(all)

            header = self.getHeader(all)
            params = self.getParams(all)
            returnG = self.getReturn(all)
            context = self.getContext(all)
            require = self.getRequire(all)
            if all.__contains__('require') == False:
                commond[name] = all 
        return commond

    def getName(self,dict):
        name =""
        for k, v in dict.items():
            if k == "name":
                name = v
        return name


    def getUrl(self,dict):
        url = {}
        vaules = self.config.return_Value()
        host = vaules["HOST"]
        for key, value in dict.items():
            if key == "url":
                    if "{{.HOST}}" in value:
                        url = value.replace('{{.HOST}}',host)
                    else:    
                        url = value
        return url


    def getMethod(self,dict):
        value = ""
        for k, v in dict.items():
            if k == "method":
                value = v
        return value


    def getHeader(self,dict):
        header = {}

        for k, v in dict.items():
            if k == "header":
                header = v
        header.update(self.config.return_Header())
        return header


    def getRequire(self,dict):
        value = ""
        for k, v in dict.items():
            if k == "require":
                value = v
        return value


    def getParams(self,dict):
        params = {}
        for key, value in dict.items():
            if key == "params" or key == "urlparams":
                        params = value  
        params.update(self.config.return_Body()) 
        return params


    def getReturn(self,dict):
        value = ""
        for k, v in dict.items():
            if k == "return":
                value = v
        return value


    def getContext(self,dict):
        value = ""
        for k, v in dict.items():
            if k == "context":
                value = v
        return value


           
if __name__ == '__main__':

    commond = ExcJson("ceshi.json")
    s = commond.getMap()
    print(s)
   