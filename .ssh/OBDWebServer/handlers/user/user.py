#!/usr/bin/env Python
# coding=utf-8
#前台用户基本接口
from methods.statics import DEFAULT_PROFILE_PHOTO
import os  
import tornado.escape
import hashlib
import random
import string
import datetime
import methods.db as db
from handlers.base import UserBaseHandler
from xpinyin import Pinyin

#前台用户登录界面(get)登录(post)API
class UserLoginHandler(UserBaseHandler):    #继承 base.py 中的类 BaseHandler
    def get(self):
        self.xsrf_form_html()#内部用 self.xsrf_form_html()生成
        if(self.get_secure_cookie("user_id")):
            self.redirect("/")
        else:
            self.render("user_login.html")

    def post(self):  #https://127.0.0.1:8000/userlogin?user_email=A&password=1994&remember_me=false
        self.xsrf_form_html()  #内部用 self.xsrf_form_html()生成
        user_email = self.get_argument("user_email",default="")
        password = self.get_argument("password",default="")#明文sha1哈希之后再从用户传过来
        remember_me = self.get_argument("remember_me",default="false")
        code = self.get_argument("check_code",default="false")
        check_code = self.session['CheckCode']
        if code.upper()==check_code.upper():
            s=db.session()
            user_infos = s.query( db.User ).filter_by(email = user_email ).first() 
            if user_infos:
                user_id = user_infos.id
                db_pwd = user_infos.password
                if str(db_pwd) == str(password):
                    if user_infos.is_active ==1:
                        respon = {"errno": 1,
                                  "err": self.get_argument('next', default='/')}
                        self.set_current_user(user_id,user_infos.username,remember_me)    #将当前用户名写入 cookie，方法见下面
                        user_infos.last_login = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        s.add(user_infos)
                        s.commit()
                        s.close()
                        self.write(tornado.escape.json_encode(respon))
                    else:
                        respon = {"errno": -1,
                                  "err": "该用户未激活，请联系管理员"}
                        s.close()
                        self.write(tornado.escape.json_encode(respon))
                else:
                    respon = {"errno": -1,
                              "err": "账号或者密码错误"}
                    print(db_pwd+"\n"+password)
                    s.close()
                    self.write(tornado.escape.json_encode(respon))
            else:
                respon = {"errno": -1,
                          "err": "账号或者密码错误"}
                s.close()
                self.write(tornado.escape.json_encode(respon))
        else:
            respon = {"errno": -1,
                          "err": "验证码错误"}
            self.write(tornado.escape.json_encode(respon))

    def set_current_user(self, user_id, user_name, remember_me):
        if user_id:
            if remember_me == "true":
                self.set_secure_cookie("user_name", tornado.escape.json_encode(user_name), httponly=True)    #secure=True需要在https中加入
                self.set_secure_cookie("user_id", tornado.escape.json_encode(user_id), httponly=True)    #secure=True需要在https中加入
            else:
                self.set_secure_cookie("user_name", tornado.escape.json_encode(user_name), expires_days = None, httponly=True)#secure=True需要在https中加入
                self.set_secure_cookie("user_id", tornado.escape.json_encode(user_id), expires_days = None, httponly=True)#secure=True需要在https中加入
        else:
            self.clear_cookie("user_name")
            self.clear_cookie("user_id")

#前台用户登出(get)
class UserLogoutHandler(UserBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        self.clear_all_cookies()
        self.redirect("/userlogin")

#用户信息界面
class UserInformationHandler(UserBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        user_id = tornado.escape.json_decode(self.get_secure_cookie("user_id"))
        s=db.session()
        user_infos = s.query( db.User ).filter_by(id = user_id ).first() 
        s.close()
        self.render("user_info.html",user_infos = user_infos,)
    
    @tornado.web.authenticated
    def post(self):   
        self.xsrf_form_html()
        try:
            user = tornado.escape.json_decode(self.request.body)
            # print(user)
            s=db.session()
            user_infos = s.query( db.User ).filter_by(id = user["id"] ).first()
            if ((user_infos.password == user["password"])):
                if user["change_password"]!="":
                    print(user["change_password"])
                    user_infos.password = str(user["change_password"])
                    respon = {"errno": 1,
                              "err": "密码修改成功，请重新登录"}
                if user_infos.username != user["username"]:
                    user_infos.username = str(user["username"])
                    respon = {"errno": 0,
                              "err": "用户名修改为: \""+ str(user["username"]) + "\""}
            # user_infos.is_active = user["is_active"]
            # user_infos.create_time = user["create_time"]
            # user_infos.last_login = user["last_login"]
                s.commit()
                s.close()
                self.write(respon)
            else:
                respon = {"errno": -1,
                          "err": "密码错误"}
                self.write(respon)
        except Exception as e:
            respon = {"errno": -1,
                      "err": str(e)}
            self.write(respon)

    @tornado.web.authenticated
    def put(self):
        self.xsrf_form_html()
        user_id = tornado.escape.json_decode(self.get_secure_cookie("user_id"))
        if(self.request.files["file"][0] and (user_id != "")):
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
            with open(os.path.join("static","profilephoto",savename),"wb") as up:            
                    up.write(data["body"])
            # print(user)
            s=db.session()
            user_infos = s.query( db.User ).filter_by(id = user_id ).first()
            if (user_infos.profilephoto != DEFAULT_PROFILE_PHOTO) and (os.path.exists("static/"+user_infos.profilephoto)):
                os.remove("static/"+user_infos.profilephoto)
            user_infos.profilephoto = "profilephoto/"+savename
            s.commit()
            s.close()
            res = {"msg":"上传成功"}
            self.write(res)
        else:
            res = {"msg":"上传错误"}
            self.write(res)
#用户注册界面(get)用户注册(post)API
class UserRegisterHandler(UserBaseHandler):
    def get(self):
        self.xsrf_form_html()
        self.render("user_register.html")
    def post(self):
        self.xsrf_form_html()
        user_email = self.get_argument("user_email",default="")
        user_name = self.get_argument("user_name",default="")
        password = self.get_argument("password",default="")#明文sha1哈希之后再从用户传过来
        if user_email:
            try:
                adduser = db.User(email = user_email,
                             username = user_name,
                             password = password)
                s=db.session()
                s.add(adduser)
                s.commit()
                s.close()
                respon = {"errno": 1,
                          "err": "用户已注册，请联络管理员激活"}
                self.write(tornado.escape.json_encode(respon))
            except Exception as e:
                respon = {"errno": -1,
                          "err": e}
                self.write(tornado.escape.json_encode(respon))
        else:
            respon = {"errno": -1,
                          "err": "用户注册失败"}
            self.write(tornado.escape.json_encode(respon))
            
#用户注册邮箱验证(post)
class UserCheckEmailHandler(UserBaseHandler):
    def post(self):
        self.xsrf_form_html()
        user_email = self.get_argument("user_email",default="")
        if(user_email != ""):
            s=db.session()
            user_infos = s.query( db.User ).filter_by( email = user_email ).all()
            s.close()
            if(user_infos):
                respon = {"errno": -1,
                          "err": "该邮箱已注册"}
                self.write(tornado.escape.json_encode(respon))
            else:
                respon = {"errno": 1,
                          "err": "可以使用"}
                self.write(tornado.escape.json_encode(respon))
        else:
            respon = {"errno": -1,
                          "err": "邮箱为空"}
            self.write(tornado.escape.json_encode(respon))
        
#用户主界面[图片智能识别页面](get)
class UserIndexHandler(UserBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        self.redirect("/useobdlistpage")

#用户业务查询页面(get)
class UserOBDListHandler(UserBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        user_id = tornado.escape.json_decode(self.get_secure_cookie("user_id"))
        page_index = int(self.get_argument("page",default="1"))
        limit = int(self.get_argument("limit",default="15"))
        keyword = self.get_argument("keyword",default="")
        start_date = self.get_argument("start_date",default="1970-01-01")
        end_date = self.get_argument("end_date",default="3000-12-31")
        if start_date == "":
            start_date = default="1970-01-01"
        if end_date == "":
            end_date = default="3000-12-31"

        # 数据判断条件
        filters = {
                db.Picture.user_id == user_id, #只允许查询自己的业务
                db.Picture.is_correct == 1, #只允许查询自己的业务

                db.or_(db.Picture.name.like('%'+keyword+'%'),
                       db.Picture.code.like('%'+keyword+'%'),
                       db.Picture.address.like('%'+keyword+'%'),
                       ),
                db.Picture.create_time.between(start_date+" 00:00:00", end_date+" 23:59:59")
        }
        s=db.session()
        count = s.query(db.Picture).filter(*filters).count()

        if page_index < 1 or count == 0:
            page_index = 1
        elif limit*page_index > count:
            page_index = int((count + limit -1) / limit);
        #asc升序
        pictures = s.query(db.Picture).order_by(db.Picture.create_time.desc()).filter(*filters).limit(limit).offset((page_index-1)*limit).all()
        s.close()

        s = db.session()
        user_infos = s.query( db.User ).filter_by(id = user_id ).first() 
        s.close()
        if start_date == "1970-01-01":
            start_date = ""
        if end_date == "3000-12-31":
            end_date = ""
        self.render("user_OBDList.html",user_infos = user_infos, page_index = page_index,count = count,limit = limit, keyword = keyword, start_date = start_date, end_date = end_date, pictures = pictures)

#用户图片端口占用页面(get)
class UserConfirmHandler(UserBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        user_id = tornado.escape.json_decode(self.get_secure_cookie("user_id"))
        s=db.session()
        user_infos = s.query( db.User ).filter_by(id = user_id ).first() 
        s.close()
        self.render("user_confirm.html", user_infos = user_infos)