import unittest
import requests
from excJson import ExcJson
from getCommond import GetCommond
from excConfig import ExcConfig
import os, sys, json
import time
import collections

# parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, parentdir)

class Run(object):
    
    def __init__(self,filename):
        
        self.json = ExcJson(filename)
        self.map = self.json.getMap()
        self.commond = collections.OrderedDict()
        self.commond = self.json.getCommond() 
        self.get_Commond = GetCommond()
        self.get_Config = ExcConfig()
        self.list =[]#commond list
        self.lastContext = {}# 最终的 context 上下文


    def engine(self):
        #请求引擎
        result =''
        for key, value in self.commond.items():
            if key in self.list:
                continue
            else:
                name = self.get_Commond.get_commond_name(self.commond)
                url = self.get_Commond.get_commond_Url(self.commond)
                method = self.get_Commond.get_commond_Method(self.commond)
                header = self.get_Commond.get_commond_Header(self.commond)
                params = self.get_Commond.get_commond_Params(self.commond)
                returnG = self.get_Commond.get_commond_Return(self.commond)
                context = self.get_Commond.get_commond_Context(self.commond)
                require = self.get_Commond.get_commond_Require(self.commond)


                req = requests.Session()
                
                if method == "post":
                    result = req.post(url = url, data=params,headers=header)
                elif method == "get":
                    result = req.get(url=url, data=params, headers=header)
                elif method =="delete":
                    result =req.delete(url=url, data=params, headers=header)
                
            self.list.append(key)
        return result
    def result(self):
        ''' 执行用例   并返回上下文 '''

        result = self.engine()
        #打印返回数据
        # print(result.text)
        json =result.json()
        yl_name = self.get_Commond.get_commond_name(self.commond)
        returnG = self.get_Commond.get_commond_Return(self.commond)
        context = self.get_Commond.get_commond_Context(self.commond)
        
        #断言 
        Result = True
        for reName , reVal  in returnG.items():
            name = '["' + reName + '"]'
            if '.' in reName:
                key  ='json' + name.replace('.','"]["') 
                value = eval(key)
                if value != reVal:
                    print(yl_name+ '测试不通过！  '+reName +'返回结果为：' + value + '  不是：' + reVal)
                    Result = False
                    break
            else:
                key = 'json' + name
                value = eval(key)
                if value != reVal:
                    print(yl_name + '测试不通过！  '+reName +'返回结果为：' + value + '  不是：' + reVal)
                    Result = False
                    break
        if Result:
            print(yl_name + "测试通过！")

        # 上下文处理   讲value(获取其值) ： key 的形式 保存到lastlist 中 
        if context != "":
            for cName,cValue in context.items():
                name = '["' + cName + '"]'
                if '.' in cName:
                    key  ='json' + name.replace('.','"]["') 
                    value = eval(key)
                    self.lastContext[cValue] = value
                else:
                    key = 'json' + name
                    value = eval(key)            
                    self.lastContext[cValue] = value
        
        return self.lastContext
    def update(self,dic):
        ''' 
        更新待执行命令 根据require 判断依赖  根据依赖添加到待执行命令中 
        context 把所有待执行命令 更新上下文
        '''
        print('--------------')
        print(dic)

        va = ""
        for value in self.commond.values():
                va = value['name']
                if va == "" or va == None:
                    print("name 值不能为空，且必须存在。")
                    break
        for require,v in self.map.items():            
                vv = v['name']
                if require == va:
                    self.commond.update({vv: v})
                    
        for key , va in dic.items():
            name = "{{." + key +"}}"
            for kk in self.commond.values():
                if kk.__contains__(name):
                    kk.replace(name,va)
                else:
                    for vv in self.commond.values():
                        if vv.__contains__(name):
                            vv.replace(name,va)
                        else:
                            pass
        print(self.commond)
        return self.commond
    def start(self):
        #开始执行
        for i in range(len(self.map)+1):
            print(i)
            re = self.result()
            self.update(re)

   



if __name__ == '__main__':
    run = Run("ceshi.json").start()
    
    # for k,v in commond.items():
    #     print(k+"-------------")
    #     print(v)
