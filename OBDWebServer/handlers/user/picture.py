#!/usr/bin/env Python
# coding=utf-8
# 前台用户图片操作接口

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
from handlers.base import UserBaseHandler
from methods.fcisservice import fcisservice
from xpinyin import Pinyin
#图片验证API
class UserPictureConfirm(UserBaseHandler):

####图片上传及验证#######################################
    @tornado.web.authenticated 
    def post(self):
        self.xsrf_form_html() 
        data = self.request.files["file"][0]
        if(data):
            pd = self.get_argument("port_direction",default="0")
            zpp = self.get_argument("zero_port_pos",default="2")
            ps = self.get_argument("port_sort",default="0")
            GPS = self.get_argument("GPS",default="")
            address = self.get_argument("address",default="")
            OBDCode = self.get_argument("OBDCode",default="")

            #保存原始图片
            # time = datetime.datetime.now() #sql time: .strftime("%Y-%m-%d %H:%M:%S")
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
            print(extension)
            savename = head + "_" + md5encode + ran_str + "." + extension #time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+data["filename"].split(".")[-1]
            picture_path = os.path.join("uploadpic",savename)
            #写入文件
            with open(os.path.join("static",picture_path),"wb") as up:            
                    up.write(data["body"])
            
            #需要添加confimed的代码
            req = {"port_direction":pd,
                   "zero_port_pos":zpp,
                   "port_sort":ps}
            #"method"为深度学习对应的API
            fci = fcisservice.remote("",req,open(os.path.join("static",picture_path), 'rb'))
            QR = QRCode(os.path.join("static",picture_path))
            if(address):
                QR["address"] = address
            if (OBDCode):
                QR["code"] = OBDCode
            if(GPS):
                QR["GPS"] = GPS
            if fci["body"] == "noimg" or fci["body"] == "detectbusy" or fci["body"] == "":
                confirmed_picture_path = ""
                ports_occupy = ""
                print("confirmed_picture_path unexists\n")                             
            else:
                confirmdata = fci["body"]
                ports_occupy = str(fci["Ports_occupy"])
                confirmname = head + "_" + md5encode + ran_str + ports_occupy + "." + extension#time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+data["filename"].split(".")[-1]
                confirmed_picture_path = os.path.join("confirmedpic",confirmname)
                with open(os.path.join("static",confirmed_picture_path),"wb") as up:            
                        up.write(confirmdata)   
            
            # 查询旧的数据
            oldOBDsql = db.session().query(db.Picture).order_by(db.Picture.create_time.desc()).filter(db.Picture.code ==  str(QR["code"]) and db.Picture.is_correct == 1).first()
            oldOBDInfo = {}
            if oldOBDsql:
                oldOBDInfo = oldOBDsql.__dict__
                oldOBDInfo["msg"] = "success"
                #调整数据
                del oldOBDInfo["_sa_instance_state"]
                oldOBDInfo["create_time"] = str(oldOBDsql.create_time)
                oldOBDInfo["update_time"] = str(oldOBDsql.update_time)
            else:
                oldOBDInfo["msg"] = "nodata"
            


            #对端口识别和二维码识别的判断
            res = {}
            is_correct = 0
            if fci["body"] == "detectbusy":
                res["msg"] = "detectbusy"
            else:
                if confirmed_picture_path == "" and QR["code"] == "":
                    res["msg"] = "AllFail"
                elif confirmed_picture_path != "" and QR["code"] == "":
                    res["msg"] = "QrcodeFail"
                elif confirmed_picture_path == "" and QR["code"] != "":
                    res["msg"] = "DetectFail"
                else:
                    is_correct = 1
                    res["msg"] = "success"

            # 插入新的数据到数据库
            pic = db.Picture(code = str(QR["code"]),
                             name = str(QR["name"]),
                             address = str(QR["address"]),
                             GPS = str(QR["GPS"]),
                             port_direction = pd,
                             zero_port_pos = zpp,
                             port_sort = ps,
                             ports_occupy = ports_occupy,
                             is_correct = is_correct,
                             uncorrect_msg = res["msg"],
                             picture_path = picture_path,
                             confirmed_picture_path = confirmed_picture_path,
                             user_id = self.get_secure_cookie("user_id"))
            s=db.session()
            s.add(pic)
            s.flush()
            res["id"] = pic.id
            s.commit()
            s.close()

            #返回json，获取信息
            #del res["body"]
            res["oldOBDInfo"] = oldOBDInfo
            res["code"] = str(QR["code"])
            res["name"] = str(QR["name"])
            res["address"] = str(QR["address"])
            res["GPS"] = str(QR["GPS"])
            res["confirmed_picture_path"] = os.path.join(confirmed_picture_path)
            res["picture_path"] = os.path.join(picture_path)
            res["ports_occupy"] = ports_occupy
            self.write(res)
        else:
            self.write(tornado.escape.json_encode({"msg":"false"}))

####图片信息补充#######################################
    @tornado.web.authenticated 
    def put(self):
        self.xsrf_form_html()
        picid = self.get_argument("picid",default="")
        code = self.get_argument("code",default="")
        name = self.get_argument("name",default="")
        address = self.get_argument("address",default="")
        is_correct = self.get_argument("is_correct",default="")
        if picid !="":
            s=db.session()
            pic = s.query(db.Picture).filter(db.Picture.id == picid).first()
            if code != "":
                pic.code = code
            if name != "":
                pic.name = name
            if address != "":
                pic.address = address
            if is_correct != "":
                pic.is_correct = is_correct
                if is_correct == "1":
                    pic.uncorrect_msg = "success"
            s.commit()
            s.close()
            res = "success"
        else:
            res = "failed"
        self.write(res)

####图片报错#######################################
    @tornado.web.authenticated 
    def get(self):
        self.xsrf_form_html()
        picid = self.get_argument("picid",default="")
        uncorrect_msg = self.get_argument("uncorrect_msg",default="")
        if picid !="":
            s=db.session()
            pic = s.query(db.Picture).filter(db.Picture.id == picid).first()
            pic.is_correct = 0
            pic.uncorrect_msg = uncorrect_msg
            self.write("图片报错成功！")
        else:
            self.write("图片报错失败！")

####图片备注API#######################################
class UserOBDNoteSubmit(UserBaseHandler):

####图片备注#######################################
    @tornado.web.authenticated 
    def post(self):
        self.xsrf_form_html()
        obd_code = self.get_argument("obd_code",default="")
        res = {}       
        if obd_code !="":
            note_category = self.get_argument("note_category",default="0")
            note = self.get_argument("note",default="")
            note = db.Obdnote(obd_code = obd_code,
                              note_category = note_category,
                              note = note
                              )
            time = datetime.datetime.now() #sql time: .strftime("%Y-%m-%d %H:%M:%S")
            md5 = hashlib.md5()
            if "img_1" in self.request.files:
                img = self.request.files["img_1"][0]
                notepic = img["body"]
                md5.update(notepic)
                md5encode = md5.hexdigest()
                notepicname = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+img["filename"].split(".")[-1]
                notepic_path = os.path.join("notepic",notepicname)
                with open(os.path.join("static",notepic_path),"wb") as up:            
                        up.write(notepic)
                note.pic1_path = notepic_path
                print(img["filename"])
            else:
                note.pic1_path = ""

            if "img_2" in self.request.files:
                img = self.request.files["img_2"][0]
                notepic = img["body"]
                md5.update(notepic)
                md5encode = md5.hexdigest()
                notepicname = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+img["filename"].split(".")[-1]
                notepic_path = os.path.join("notepic",notepicname)
                with open(os.path.join("static",notepic_path),"wb") as up:            
                        up.write(notepic)
                note.pic2_path = notepic_path
            else:
                note.pic2_path = ""

            if "img_3" in self.request.files:
                img = self.request.files["img_3"][0]
                notepic = img["body"]
                md5.update(notepic)
                md5encode = md5.hexdigest()
                notepicname = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+img["filename"].split(".")[-1]
                notepic_path = os.path.join("notepic",notepicname)
                with open(os.path.join("static",notepic_path),"wb") as up:            
                        up.write(notepic)
                note.pic3_path = notepic_path
                print(img["filename"])
            else:
                note.pic3_path = ""

            s=db.session()
            s.add(note)
            s.flush()
            res["id"] = note.id
            s.commit()
            s.close()
            res["msg"] = "备注成功！"
            print(res["msg"])
            self.write(tornado.escape.json_encode(res["msg"]))
        else:
            res["id"] = ""
            res["msg"] = "备注出错！"
            print(res["msg"])
            self.write(tornado.escape.json_encode(res["msg"]))
        # self.write(tornado.escape.json_encode("ok"))

    @tornado.web.authenticated 
    def put(self):
        self.xsrf_form_html()
        obd_code = self.get_argument("obd_code",default="")
        data = self.request.files["file"][0]
         #保存图片
        time = datetime.datetime.now() #sql time: .strftime("%Y-%m-%d %H:%M:%S")
        md5 = hashlib.md5()

        md5.update(data["body"])
        md5encode = md5.hexdigest()
        savename = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+data["filename"].split(".")[-1]
        picture_path = os.path.join("notepic",savename)
        #写入文件
        with open(os.path.join("static",picture_path),"wb") as up:            
                up.write(data["body"])
        self.write("ok")

#图片对比验证主界面(get)图片对比验证(post)API
# class UserPictureCompare(UserBaseHandler):
#     @tornado.web.authenticated 
#     def get(self):
#         self.xsrf_form_html()
#         self.render("user_compare.html")

#     @tornado.web.authenticated 
#     def post(self):
#         self.xsrf_form_html()
#         dataBefore = self.request.files["imgFileBefore"][0]
#         dataAfter = self.request.files["imgFileAfter"][0]

#         if(dataBefore & dataAfter):
#             pd = self.get_argument("port_direction",default="0")
#             zpp = self.get_argument("zero_port_pos",default="2")
#             ps = self.get_argument("port_sort",default="0")

#             #需要添加confimed的代码
#             req = {"port_direction":pd,"zero_port_pos":zpp,"port_sort":ps}
#             resBefore = fcisservice.remote("managerlogin",req , dataBefore)
#             resAfter = fcisservice.remote("managerlogin",req , dataAfter)

#             #if(res)判断
#             confirmdataBefore = resBefore["imgFile"][0]
#             confirmdataAfter = resAfter["imgFile"][0]

#             #保存图片
#             time = datetime.datetime.now() #sql time: .strftime("%Y-%m-%d %H:%M:%S")
#             md5 = hashlib.md5()

#             md5.update(dataBefore["body"])
#             md5encode = md5.hexdigest()
#             savenameBefore = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+dataBefore["filename"].split(".")[-1]

#             md5.update(confirmdataBefore["body"])
#             md5encode = md5.hexdigest()
#             confirmnameBefore = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+dataBefore["filename"].split(".")[-1]

#             md5.update(data["body"])
#             md5encode = md5.hexdigest()
#             savenameAfter = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+dataAfter["filename"].split(".")[-1]

#             md5.update(confirmdata["body"])
#             md5encode = md5.hexdigest()
#             confirmnameAfter = time.strftime("%Y_%m_%d_%H_%M_%S")+"_"+md5encode+"."+dataAfter["filename"].split(".")[-1]

#             # #写入文件
#             with open(os.path.join("static","uploadpic",savenameBefore),"wb") as up:            
#                     up.write(dataBefore["body"])
#             with open(os.path.join("static","confirmedpic",confirmnameBefore),"wb") as up:            
#                     up.write(confirmdataBefore["body"])
#             with open(os.path.join("static","uploadpic",savenameAfter),"wb") as up:            
#                     up.write(dataAfter["body"])
#             with open(os.path.join("static","confirmedpic",confirmnameAfter),"wb") as up:            
#                     up.write(confirmdataAfter["body"])   


    
#             # #插入数据库
#             picBefore = db.Picture(code = resBefore["code"],
#                             name = resBefore["name"],
#                             address = resBefore["address"],
#                             GPS = resBefore["GPS"],
#                             port_direction = pd,
#                             zero_port_pos = zpp,
#                             port_sort = ps,
#                             picture_path = os.path.join("uploadpic",savenameBefore),
#                             confirmed_picture_path = os.path.join("confirmedpic",confirmnameBefore),
#                             user_id = self.get_secure_cookie("user_id"))

#             picAfter = db.Picture(code = resAfter["code"],
#                             name = resAfter["name"],
#                             address = resAfter["address"],
#                             GPS = resAfter["GPS"],
#                             port_direction = pd,
#                             zero_port_pos = zpp,
#                             port_sort = ps,
#                             picture_path = os.path.join("uploadpic",savenameAfter),
#                             confirmed_picture_path = os.path.join("confirmedpic",confirmnameAfter),
#                             user_id = self.get_secure_cookie("user_id"))
#             s=db.session()
#             s.add(picBefore)
#             s.add(picAfter)
#             s.commit()
#             s.close()
#             #返回json，获取信息
#             # del res["imgFile"]
#             # res["confirmed_picture_path"] = os.path.join("uploadpic",savename)
#             # res["picture_path"] = os.path.join("confirmedpic",confirmname)
#             # res["msg"] = "success"
#             # print(res["code"])
#             # res.update(tornado.escape.json_encode(req))
#             self.write("res")
#         else:
#             self.write(tornado.escape.json_encode({"msg":"false"}))
