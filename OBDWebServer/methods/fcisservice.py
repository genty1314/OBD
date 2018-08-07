#!/usr/bin/env Python
# coding=utf-8
import requests
import base64
import datetime


class FcisService(): #接收FCIS接口反馈
    """docstring for ClassName"""
    def __init__(self,url):
        self.address = address

    def local(self,method,req,img): #FCIS本地调用的接口
        return res

    def remote(self,method,req,img):#FCIS异地调用的接口，需要同时配备图片下载地址
        try:
            print("fci post start: "+str(datetime.datetime.now()))
            url = self.address +"/"+ method
            headers={"content-type": "multipart/form-data"}
            files = {"file": img}
            print(str(files))
            temp = requests.post(url,files = files, data = req)
            res = dict(temp.headers)
            #res["code"] = "752BL/GJ157/GF021/OBD0001"
            #res["name"] = "瓦厂13号居民楼后墙/GF021/OBD0001"
            #res["address"] = "测试地址"
            #res["GPS"] = "测试GPS"
            #res["ports_occupy"] = res["Ports_occupy"]#[1, 0, 1, 1, 0, 0, 0, 0, 1]
            if temp.text == "noimg":
                res["Ports_occupy"] = ""
                res["body"] = temp.text
            else:
                res["body"] = temp.content
            print("fci post finish: "+str(datetime.datetime.now()))
            return res
        except Exception as e:
            print(e) 

# if __name__ == '__main__':
#     address = "http://127.0.0.1:8080"
#     method = "analyze"
#     #req = "/analyze?pic=555&port_direction=up&zero_position=left&sort=anticlockwise"
#     req = {
#     'pic': 'zh',
#     'port_direction': 'up',
#     'zero_position': 'left',
#     'sort': 'anticlockwise',
# }
#     test = FcisService(address)
#     print(test.remote(method,req))

address = "http://127.0.0.1:23333"

fcisservice = FcisService(address)
