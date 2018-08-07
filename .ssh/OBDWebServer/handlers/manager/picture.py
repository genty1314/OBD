#! /usr/bin/env python
# coding=utf-8
# 后台管理员图片操作接口
import os  
import datetime
import hashlib
import random
import string
import json
import tornado.web
import tornado.escape
import methods.db as db
from methods.QRCode import QRCode
from handlers.base import ManagerBaseHandler
from methods.fcisservice import fcisservice
from methods.patch import patch2excl, patch2imgzip
import json
import base64
from xpinyin import Pinyin
#端口位置和方向转换
port_analyze = {
                "-1":[None,None],
                "0":[0,2],
                "1":[0,3],
                "2":[1,2],
                "3":[1,3],
                "4":[2,0],
                "5":[2,1],
                "6":[3,0],
                "7":[3,1],
                }

#图片管理主界面(get)，图片添加(post)删除(delete)API
class ManagerPictures(ManagerBaseHandler):
    @tornado.web.authenticated 
    def get(self):
        self.xsrf_form_html()
        self.render("manager_pics_add.html")

    @tornado.web.authenticated 
    def post(self):
        self.xsrf_form_html()
        if(self.request.files["file"][0]):
            upp = self.get_argument("upload_port_pos",default="-1")
            us = self.get_argument("upload_sort",default=None)
            GPS = self.get_argument("GPS",default="")
            address = self.get_argument("address",default="")
            OBDCode = self.get_argument("OBDCode",default="")
            #保存图片
            data=self.request.files["file"][0]
            #time = datetime.datetime.now() #sql time: .strftime("%Y-%m-%d %H:%M:%S")
            md5 = hashlib.md5()
            md5.update(data["body"])
            md5encode = md5.hexdigest()
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            extension = data["filename"].split(".")[-1]
            head = data["filename"].rstrip("."+extension)
            #将文件名中文转化为拼音
            pinyin = Pinyin()
            head = pinyin.get_pinyin(head)
            #中文转拼音结束
            savename = head + "_" + md5encode + ran_str + "." + extension #time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+data["filename"].split(".")[-1]
            with open(os.path.join("static","uploadpic",savename),"wb") as up:            
                    up.write(data["body"])   
            QR = QRCode(os.path.join("static","uploadpic",savename))
            if(address):
                QR["address"] = address
            if (OBDCode):
                QR["code"] = OBDCode
            if(GPS):
                QR["GPS"] = GPS                                           
            #插入数据库
            pic = db.Picture(code = str(QR["code"]),
                             name = str(QR["name"]),
                             address = str(QR["address"]),
                             GPS = str(QR["GPS"]),
                             port_direction = port_analyze[upp][0],
                             zero_port_pos = port_analyze[upp][1],
                             port_sort = us,
                             picture_path = os.path.join("uploadpic",savename),
                             manager_id = self.get_secure_cookie("manager_id"))
            s=db.session()
            s.add(pic)
            s.commit()
            s.close()
            self.write("success")
        else:
            self.write("error")        

    @tornado.web.authenticated
    def delete(self):#删除图片
        self.xsrf_form_html()
        pictureid = self.get_argument("pictureid",default="")
        s=db.session()
        pic = s.query(db.Picture).get(pictureid)
        if pic.id :
            if (pic.picture_path):
                if os.path.exists(os.path.join("static",pic.picture_path)):
                    os.remove(os.path.join("static",pic.picture_path))
            if (pic.confirmed_picture_path):
                if os.path.exists(os.path.join("static",pic.confirmed_picture_path)):
                    os.remove(os.path.join("static",pic.confirmed_picture_path))
            s.delete(pic)
            s.commit()
            s.close()
            self.write(pictureid)
        else:
            self.write("-1")

#图片编辑主界面(get),图片编辑(post)API
class ManagerPicturesEdit(ManagerBaseHandler):
    @tornado.web.authenticated 
    def get(self):
        self.xsrf_form_html()
        pictureid = self.get_argument("pictureid",default="")
        s=db.session()
        picture_infos = s.query( db.Picture ).filter_by(id = pictureid ).first() 
        s.close()
        print(picture_infos.confirmed_picture_path)
        self.render("manager_pic_edit.html",picture = picture_infos)
    
    @tornado.web.authenticated 
    def post(self):
        self.xsrf_form_html()
        try:
            picture = tornado.escape.json_decode(self.request.body)
            s=db.session()
            picture_infos = s.query( db.Picture ).filter_by(id = picture["id"] ).first()
            picture_infos.name = picture["name"]
            picture_infos.address = picture["address"]
            picture_infos.port_direction = picture["port_direction"]
            picture_infos.zero_port_pos = picture["zero_port_pos"]
            picture_infos.port_sort = picture["port_sort"]
            picture_infos.port_sort = picture["port_sort"]
            picture_infos.manager_id = self.get_secure_cookie("manager_id")
            s.commit()
            s.close()
        except Exception as e:
            self.write(str(e))
        else:
            self.write("success")      

#批量导出OBD数据(get excl)和图片(post zip)为
class ManagerPicturesPatchOutput(ManagerBaseHandler):
    @tornado.web.authenticated 
    def post(self):
        self.xsrf_form_html()
        obd = self.get_argument("obd",default="excl")
        page_index = int(self.get_argument("page",default="1"))
        limit = int(self.get_argument("limit",default="30"))
        is_correct = int(self.get_argument("is_correct",default="1"))
        keyword = self.get_argument("keyword",default="")
        start_date = self.get_argument("start_date",default="1970-01-01")
        end_date = self.get_argument("end_date",default="3000-12-31")
        ids = self.get_argument("ids",default="")
        idslist = ids.split(',')
        # 时间判断
        if start_date == "":
            start_date = default="1970-01-01"
        if end_date == "":
            end_date = default="3000-12-31"
        print(ids)
        # 数据判断条件
        if idslist != ['']:
            filters = {db.Picture.id.in_(idslist)}
        else:
            filters = {
                db.or_(db.Picture.name.like('%'+keyword+'%'),
                       db.Picture.code.like('%'+keyword+'%'),
                       db.Picture.address.like('%'+keyword+'%'),
                       ),
                db.Picture.create_time.between(start_date+" 00:00:00", end_date+" 23:59:59")
            }
        s=db.session()

        # count = s.query(db.Picture).filter(*filters).count()
        
        # if page_index < 1 or count == 0:
        #     page_index = 1
        # elif limit*page_index > count:
        #     page_index = int((count + limit -1) / limit);
        
        #asc升序
        # 这样子写的话输出就是正常的list内容
        # pictures = s.query(db.Picture.id,
        #                    db.Picture.code,
        #                    db.Picture.name,
        #                    db.Picture.address,
        #                    db.Picture.GPS,
        #                    db.Picture.port_direction,
        #                    db.Picture.zero_port_pos,
        #                    db.Picture.port_sort,
        #                    db.Picture.picture_path,
        #                    db.Picture.confirmed_picture_path,
        #                    db.Picture.ports_occupy,
        #                    db.Picture.is_correct,
        #                    db.Picture.uncorrect_msg,
        #                    db.Picture.create_time,
        #                    db.Picture.update_time,
        #                    db.Picture.user_id,
        #                    db.Picture.manager_id).order_by(db.Picture.create_time.desc()).filter(*filters).all()
        pictures = s.query(db.Picture).order_by(db.Picture.create_time.desc()).filter(*filters).all()
        s.close()

        print(pictures)
        #导出excl或图片zip数据
        path = 'tmp'
        if obd == 'imgzip':
            filename = patch2imgzip(pictures,path)
        else:
            filename = patch2excl(pictures,path)
        self.write({"filename":filename}) 

    @tornado.web.authenticated 
    def get(self):
        self.xsrf_form_html()
        filename = self.get_argument("filename",default="")
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+filename)
        #读取的模式需要根据实际情况进行修改
        if filename == "":
            self.finish()

        path = 'tmp'
        with open(os.path.join(path,filename), 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        os.remove(os.path.join(path,filename))
        #记得finish
        self.finish()

#图片验证API
class ManagerPicturesConfirm(ManagerBaseHandler):
    @tornado.web.authenticated 
    def post(self):
        self.xsrf_form_html() 
        pictureid = self.get_argument("pictureid",default="")
        print("++++++++++"+pictureid)
        s = db.session();
        OBD = s.query( db.Picture ).filter_by(id = pictureid ).first(); #s.query(db.Picture).filter(db.Picture.id ==  pictureid).first()
        if(OBD):
            OBDInfo = OBD.__dict__
            code =  OBDInfo["code"]
            #需要添加confimed的代码
            req = {"port_direction":OBDInfo["port_direction"],
                   "zero_port_pos": OBDInfo["zero_port_pos"],
                   "port_sort":OBDInfo["port_sort"]}
            #"method"为深度学习对应的API
            fci = fcisservice.remote("",req,open(os.path.join("static",OBDInfo["picture_path"]), 'rb'))

            if fci["body"] == "noimg" or fci["body"] == "detectbusy" or fci["body"] == "":
                confirmed_picture_path = ""
                ports_occupy = ""
                print("confirmed_picture_path unexists\n")                             
            else:
                md5 = hashlib.md5()
                confirmdata = fci["body"]
                ports_occupy = str(fci["Ports_occupy"])
                md5.update(confirmdata)
                md5encode = md5.hexdigest()
                onamelist = OBDInfo["picture_path"].split("/")[-1].split(".")
                confirmname = "".join(onamelist[0:len(onamelist)-1]) + ports_occupy + "." + onamelist[-1] #time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+OBDInfo["picture_path"].split(".")[-1]
                confirmed_picture_path = os.path.join("confirmedpic",confirmname)
                with open(os.path.join("static",confirmed_picture_path),"wb") as up:            
                        up.write(confirmdata)   
            
            #对端口识别和二维码识别的判断
            res = {}
            is_correct = 0
            if fci["body"] == "detectbusy":
                res["msg"] = "detectbusy"
            else:
                if confirmed_picture_path == "" and code == "":
                    res["msg"] = "AllFail"
                elif confirmed_picture_path != "" and code == "":
                    res["msg"] = "QrcodeFail"
                elif confirmed_picture_path == "" and code != "":
                    res["msg"] = "DetectFail"
                else:
                    is_correct = 1
                    res["msg"] = "success"

            # 插入新的数据到数据库
            OBD.ports_occupy = ports_occupy
            OBD.is_correct = is_correct
            OBD.uncorrect_msg = res["msg"]
            OBD.confirmed_picture_path = confirmed_picture_path
            OBD.manager_id = self.get_secure_cookie("manager_id")
            s.commit()
            s.close()

            #返回json，获取信息
            #del res["body"]
            res["id"] = pictureid
            res["confirmed_picture_path"] = os.path.join(confirmed_picture_path)
            res["ports_occupy"] = ports_occupy
            time = datetime.datetime.now() #sql time: .strftime("%Y-%m-%d %H:%M:%S")
            res["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            res["manager_id"] = bytes.decode(self.get_secure_cookie("manager_id"))
            self.write(res)
        else:
            self.write(tornado.escape.json_encode({"msg":"false"}))
        # self.xsrf_form_html()
        # pictureid = self.get_argument("pictureid",default="")
        # if pictureid != "":
        #     s=db.session()
        #     picture_infos = s.query( db.Picture ).filter_by(id = pictureid ).first()
        #     if(os.path.exists(os.path.join("static",picture_infos.picture_path))):
        #         body = open(os.path.join("static",picture_infos.picture_path),'rb').read()
        #         bodybase64 = str(base64.b64encode(body))
        #         print(bodybase64)
        #         pic = {"imgFile":[{"filename":picture_infos.picture_path.split("/")[-1],
        #                            "content_type": "img/"+picture_infos.picture_path.split(".")[-1],
        #                            "body":body }]}
        #         req = {"port_direction":picture_infos.port_direction,
        #                "zero_port_pos":picture_infos.zero_port_pos,
        #                "port_sort":picture_infos.port_sort}
        #         req["imgFile"] = [{"filename":picture_infos.picture_path.split("/")[-1],
        #                            "content_type": "img/"+picture_infos.picture_path.split(".")[-1],
        #                            "body":bodybase64 }]
        #         with open("./input.json","w",encoding='utf-8') as json_file:
        #             json.dump(req,json_file,ensure_ascii=False)
        #         res = fcisservice.remote("method", req, pic)

        #         confirmdata = res["imgFile"][0]
        #         if confirmdata:
        #             time = datetime.datetime.now() #sql time: .strftime("%Y-%m-%d %H:%M:%S")
        #             md5 = hashlib.md5()
        #             md5.update(confirmdata["body"])
        #             md5encode = md5.hexdigest()
        #             confirmname = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+confirmdata["filename"].split(".")[-1]
        #             if (picture_infos.confirmed_picture_path != None):
        #                 os.remove(os.path.join("static",picture_infos.confirmed_picture_path))
        #             with open(os.path.join("static","confirmedpic",confirmname),"wb") as up:            
        #                 up.write(confirmdata["body"])
        #             picture_infos.code = res["code"]
        #             picture_infos.name = res["name"]
        #             picture_infos.address = res["address"]
        #             picture_infos.GPS = res["GPS"]
        #             picture_infos.confirmed_picture_path = os.path.join("confirmedpic",confirmname)
        #             picture_infos.manager_id = self.get_secure_cookie("manager_id")
        #             s.commit()
        #             s.close()
        #             #返回json，获取信息
        #             time = datetime.datetime.now()
        #             del res["imgFile"]
        #             res["confirmed_picture_path"] = os.path.join("confirmedpic",confirmname)
        #             res["update_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        #             res["msg"] = "success"
        #             res["manager_id"] = bytes.decode(self.get_secure_cookie("manager_id"))
        #             # res.update(tornado.escape.json_encode(req))
        #             self.write(res)
        #         else:
        #             s.close()
        #             self.write(tornado.escape.json_encode({"msg":"false"}))
        #     else:
        #         s.close()
        #         self.write(tornado.escape.json_encode({"msg":"false"}))
        # else:
        #     self.write(tornado.escape.json_encode({"msg":"false"}))