

dic = {"name": "登陆","url": "{{.host}}/login"}
dic1= {"a":dic}
dic2={"b":dic1}
d = {"{{.host}}":"127.0.0.1"}

print(dic2)

for k,v in dic2.items():

    for key, value in v.items():

        for kk, vv in value.items():
            
            for ke , va in d.items():
                
                value[kk] = vv.replace(ke,va)
print(dic2)
            

a1 = "{{.host}}/login"
if "{{.host}}" in a1:
    a =a1.replace('{{.host}}','127.0.0.1')
print(a)


str = "www.w3cschool.cc"
print ("菜鸟教程旧地址：", str)
print ("菜鸟教程新地址：", str.replace("w3cschool.cc", "runoob.com"))