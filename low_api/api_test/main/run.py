import unittest
import requests
from excJson import ExcJson
from getCommond import GetCommond
from excConfig import ExcConfig
from excJson import ExcJson
import os, sys, json,re
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
        self.get_cc = ExcJson()
        self.get_Config = ExcConfig()
        self.list =[]#commond list
        self.lastContext = {}# 最终的 context 上下文
        self.Cookies = {}# cookie 处理
        self.number = 0 #成功个数 统计用


    def engine(self):
        #请求引擎
        result =''
        cookie=''
        for comond_name, comond_value in self.commond.items():

            # url = self.get_Commond.get_commond_Url(self.commond)
            # method = self.get_Commond.get_commond_Method(self.commond)
            # header = self.get_Commond.get_commond_Header(self.commond)
            # params = self.get_Commond.get_commond_Params(self.commond)
            
            name = self.get_cc.getName(comond_value)
            requir = self.get_cc.getRequire(comond_value)
            # print('start:' + name)

            url = self.get_cc.getUrl(comond_value)
            method = self.get_cc.getMethod(comond_value)
            header = self.get_cc.getHeader(comond_value)
            Params = self.get_cc.getParams(comond_value)

            if self.Cookies:
                for key,value in self.Cookies.items():
                    if requir == key:
                        cookie = value
            else:
                cookie = ''


            if comond_name not in self.list:       
                req = requests.Session()
  
                if method == "post":
                    result = req.post(url = url, data=Params,headers=header,cookies = cookie )
                elif method == "get":
                    result = req.get(url=url, params=Params, headers=header,cookies = cookie)
                elif method =="delete":
                    result =req.delete(url=url, data=Params, headers=header,cookies = cookie)
                self.Cookies[name]= result.cookies 
                
                self.list.append(comond_name)
            else:
                continue

        return result
    def result(self):
        ''' 执行用例   并返回上下文 '''

        result = self.engine()
        #打印返回数据
        print(result.text)
        json =result.json()

        commond_name = self.list[-1]

        yl_name = self.get_Commond.get_commond_name(self.commond,commond_name)
        returnG = self.get_Commond.get_commond_Return(self.commond,commond_name)
        context = self.get_Commond.get_commond_Context(self.commond,commond_name)
        #是否存在数字 .shuzi. 格式
        def hasNumbers(inputString):
            return  bool(re.search(r'/^\.\d*\.$/', inputString))

        #断言 
        Result = True
        for reName , reVal  in returnG.items():
            #如果存在数字
            if hasNumbers(reName):
                # 获得数字  并进行分割  先取到数字之前的  根据数字取之后的
                number  = '.'+ re.findall(r'\d+', reName)[-1] + '.'
                name_all = reName.split(number)
                
                if '.' in name_all[0]:
                    mm = '["' + name_all[0] + '"]'
                    key  ='json' + mm.replace('.','"]["') 
                    
                    value = eval(key)
                    list = value[int(re.findall(r'\d+', reName)[-1])]
                    
                    if '.' in name_all[-1]:
                        key  ='list' +'["' +name_all[-1].replace('.','"]["') + '"]'
                        print(key)
                        vv = eval(key)
                        
                        if vv != reVal:
                            print(yl_name+ ':测试不通过！  '+reName +':返回结果为：' + str(vv) + '  不是：' + str(reVal))
                            Result = False
                            break
                        
                    else:
                        tt = '["' + list + '"]'
                        key = 'list'+ tt
                        vv = eval(key)
                        if vv != reVal:
                            print(yl_name+ ':测试不通过！  '+reName +':返回结果为：' + str(vv) + '  不是：' + str(reVal))
                            Result = False
                            break
                        
            else:
                #如果没有数字  即不存在list  直接取值
                name = '["' + reName + '"]'
                if '.' in reName:
                    key  ='json' + name.replace('.','"]["') 
                    value = eval(key)
                    if value != reVal:
                        print(yl_name+ ':测试不通过！  '+reName +':返回结果为：' + str(value) + '  不是：' + str(reVal))
                        Result = False
                        break
                else:
                    key = 'json' + name
                    value = eval(key)
                    if value != reVal:
                        print(yl_name + ':测试不通过！  '+reName +':返回结果为：' + str(value) + '  不是：' + str(reVal))
                        Result = False
                        break
        if Result:
            self.number +=1
            print(yl_name + "测试通过！")

        # 上下文处理   讲value(获取其值) ： key 的形式 保存到lastlist 中 
        try:
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
        except TypeError:
            print("程序终止：" + yl_name+ "有错误！ 请调试")
        return self.lastContext
    def update(self):
        ''' 
        更新待执行命令 根据require 判断依赖  根据依赖添加到待执行命令中 
        context 把所有待执行命令 更新上下文
        '''
        dic = self.result()
        va = []
        for value in self.commond.values():
                va.append(value['name'])
                
            
        for name,v in self.map.items():
            self.commond.update({name: v})
            self.json.deleteMap(self.map , name)
            break
        # print("map:",self.map) 
        # print("comond:",self.commond)              
       
        #{{.}} 上下文格式调整  将commond 中的数据进行更换
        for key, va in dic.items():
            name = "{{." + key + "}}"
            for kk ,value in self.commond.items():
                
                if isinstance(value,str) and name in str(value):
                    self.commond[key] = value.replace(name,va)
                    continue
                elif isinstance(value,dict):
                    for aa,vv in value.items():
                        if name in str(vv) and isinstance(vv,str) :
                            value[aa]  = vv.replace(name,va)
                        elif isinstance(vv,dict):
                            for bb,mm in vv.items():
                                if name in str(mm):
                                    vv[bb] = mm.replace(name, va)
        
        return self.commond
    def start(self):
        #开始执行
        number = 0
        all = 0
        for i in range(len(self.map)+1):
            number += 1
            all = len(self.map)+1
            self.update()
        print("汇总：一共执行："+ str(self.get_cc.getNumber()) +" 个用例！"
            "成功了："+ str(self.number) +" 个用例！"
            "失败了："+ str(self.get_cc.getNumber() - self.number) +" 个用例！")
   



if __name__ == '__main__':
    run = Run("ceshi.json").start()
