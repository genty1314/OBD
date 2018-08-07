#!/usr/bin/env Python
# coding=utf-8

from methods.statics import DEFAULT_PROFILE_PHOTO
import os  
import tornado.web
import tornado.escape
import hashlib
import random
import string
import datetime
import methods.db as db
from handlers.base import ManagerBaseHandler
from xpinyin import Pinyin

#后台管理员登入
class ManagerLoginHandler(ManagerBaseHandler):    #继承 base.py 中的类 BaseHandler
    def get(self):
        self.xsrf_form_html()#内部用 self.xsrf_form_html()生成
        if(self.get_secure_cookie("manager_id")):
            self.redirect("/manager")
        else:
            self.render("manager_login.html")

    def post(self):
        self.xsrf_form_html() #内部用 self.xsrf_form_html()生成
        manager_email = self.get_argument("manager_email",default="")
        password = self.get_argument("password",default="")
        remember_me = self.get_argument("remember_me",default="false")
        next_page = self.get_argument("next",default="/manager")

        #user_infos = mrd.select_table(table="manager",column="*",condition="email",value=manager_email)
        s = db.session()
        user_infos = s.query( db.Manager ).filter_by(email = manager_email ).first()
        manager_id = user_infos.id
        if user_infos:
            db_pwd = user_infos.password
            if str(db_pwd) == str(password):
                if user_infos.is_active ==1:
                    respon = {"error": 0,
                              "data": next_page}
                    self.set_current_user(manager_id,user_infos.managername,remember_me)    #将当前用户名写入 cookie，方法见下面
                    user_infos.last_login = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    s.add(user_infos)
                    s.commit()
                    s.close()
                    self.write(tornado.escape.json_encode(respon))
                else:
                    respon = {"error": 1,
                              "data": "该用户未激活，请联系管理员"}
                    s.close()
                    self.write(tornado.escape.json_encode(respon))
            else:
                respon = {"error": 1,
                          "data": "账号或者密码错误"}
                s.close()
                self.write(tornado.escape.json_encode(respon))
        else:
            respon = {"error": 1,
                      "data": "账号或者密码错误"}
            s.close()
            self.write(tornado.escape.json_encode(respon))

    def set_current_user(self, manager_id,manager_name,remember_me):
        if manager_id:
            if remember_me == "true":
                self.set_secure_cookie("manager_name", tornado.escape.json_encode(manager_name),httponly=True)    #secure=True需要在https中加入
                self.set_secure_cookie("manager_id", tornado.escape.json_encode(manager_id),httponly=True)    #secure=True需要在https中加入
            else:
                self.set_secure_cookie("manager_name", tornado.escape.json_encode(manager_name),expires_days=None,httponly=True)#secure=True需要在https中加入
                self.set_secure_cookie("manager_id", tornado.escape.json_encode(manager_id),expires_days=None,httponly=True)#secure=True需要在https中加入
        else:
            self.clear_cookie("manager_name")
            self.clear_cookie("manager_id")

#后台管理员登出
class ManagerLogoutHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        self.clear_all_cookies()
        self.redirect("/managerlogin")

#后台主界面
class ManagerIndexHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        manager_id = tornado.escape.json_decode(self.get_secure_cookie("manager_id"))
        s=db.session()
        manager_infos = s.query( db.Manager ).filter_by(id = manager_id ).first() 
        manager_name=manager_infos.managername
        level = manager_infos.level
        self.render("manager_main.html", managername = manager_name,level = level,manager_infos=manager_infos)  #  self.render() 读取html，传向前端，同时可以穿参数level 
        s.close()
        

#后台管理员信息界面
class ManagerInformationHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        manager_id = tornado.escape.json_decode(self.get_secure_cookie("manager_id"))
        s=db.session()
        manager_infos = s.query( db.Manager ).filter_by(id = manager_id ).first() 
        s.close()
        self.render("manager_info.html",manager_infos = manager_infos,)
    
    @tornado.web.authenticated
    def post(self):   
        self.xsrf_form_html()
        try:
            manager = tornado.escape.json_decode(self.request.body)
            # print(manager)
            s=db.session()
            manager_infos = s.query( db.Manager ).filter_by(id = manager["id"] ).first()
            if ((manager_infos.password == manager["password"])):
                if manager["change_password"]!="":
                    manager_infos.password = str(manager["change_password"])
                if manager_infos.managername != manager["managername"]:
                    manager_infos.managername = str(manager["managername"])
            # manager_infos.is_active = manager["is_active"]
            # manager_infos.create_time = manager["create_time"]
            # manager_infos.last_login = manager["last_login"]
                s.commit()
                s.close()
                self.write("修改成功")
            else:
                self.write("密码错误")
        except Exception as e:
            self.write(str(e))

    @tornado.web.authenticated
    def put(self):
        self.xsrf_form_html()
        manager_id = tornado.escape.json_decode(self.get_secure_cookie("manager_id"))
        if(self.request.files["file"][0] and (manager_id != "")):
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
            # print(manager)
            s=db.session()
            manager_infos = s.query( db.Manager ).filter_by(id = manager_id ).first()
            if (manager_infos.profilephoto != DEFAULT_PROFILE_PHOTO) and (os.path.exists("static/"+manager_infos.profilephoto)):
                os.remove("static/"+manager_infos.profilephoto)
            manager_infos.profilephoto = "profilephoto/"+savename
            s.commit()
            s.close()
            res = {"msg":"上传成功"}
            self.write(res)
        else:
            res = {"msg":"上传错误"}
            self.write(res)

#后台二级图片管理界面
class ManagerPicManagementHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        page_index = int(self.get_argument("page",default="1"))  #获取前端中page参数，默认为1
        limit = int(self.get_argument("limit",default="15"))    #获取前端中limit参数，默认15
        is_correct = int(self.get_argument("is_correct",default="1"))
        keyword = self.get_argument("keyword",default="")
        start_date = self.get_argument("start_date",default="1970-01-01")
        end_date = self.get_argument("end_date",default="3000-12-31")
        if start_date == "":
            start_date = default="1970-01-01"
        if end_date == "":
            end_date = default="3000-12-31"
        # 数据判断条件
        filters = {
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
        # pictures = s.query(db.Picture).order_by(db.Picture.create_time.desc()).filter(*filters).limit(limit).offset((page_index-1)*limit).all()
        s.close()
        if start_date == "1970-01-01":
            start_date = ""
        if end_date == "3000-12-31":
            end_date = ""
        self.render("pics_management.html",page_index = page_index,count = count,limit = limit, keyword = keyword, start_date = start_date, end_date = end_date)#, pictures = pictures)

#后台图片获取OBD内容
class ManagerGetOBDList(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        page_index = int(self.get_argument("page",default="1"))
        limit = int(self.get_argument("limit",default="30"))
        is_correct = int(self.get_argument("is_correct",default="1"))
        keyword = self.get_argument("keyword",default="")
        start_date = self.get_argument("start_date",default="1970-01-01")
        end_date = self.get_argument("end_date",default="3000-12-31")
        if start_date == "":   #给时间赋予初始值
            start_date = default="1970-01-01"
        if end_date == "":
            end_date = default="3000-12-31"
        # 数据判断条件
        filters = {
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

        if start_date == "1970-01-01":
            start_date = ""
        if end_date == "3000-12-31":
            end_date = ""
            #转变成json文件格式
        result_dict = [u.column_dict() for u in pictures]
        
        res = {"code":0,
               "msg":"",
               "count":count,
               "data": result_dict}
        # self.render("pics_management.html",page_index = page_index,count = count,limit = limit, keyword = keyword, start_date = start_date, end_date = end_date, pictures = pictures)
        self.write(res)

#后台用户管理界面
class ManagerUserManagementHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        page_index = int(self.get_argument("page",default="1"))
        limit = int(self.get_argument("limit",default="30"))
        keyword=self.get_argument("keyword",default="")
        # data = tornado.escape.json_decode(self.request.body)
        # if "page" in self.request.arguments:      #pyhton3 新特性不支持has_key
        #page_index = int(self.get_argument("page",default="1"))   
        # if "limit" in self.request.arguments:
        #page_size = int(self.get_argument("limit",default="15"))
           
        filters ={
                     db.or_(db.User.id.like("%"+keyword+"%"),
                                db.User.email.like("%"+keyword+"%"),
                                db.User.username.like("%"+keyword+"%"),
                               ),
                    # db.User.create_time.between(create_time+"00:00:00",last_login+"00:00:00"),
        }
        s=db.session()
        count = s.query(db.User).filter(*filters).count()
        if page_index<1 or count==0:
                    page_index=1
        elif limit*page_index >count :
                    page_index=int((count +limit-1)/limit );

                                                                       #asc升序
        #users = s.query(db.User).order_by(db.User.create_time.desc()).filter(*filters).limit(page_size).offset((page_index-1)*page_size).all()
        users = s.query(db.User).order_by(db.User.create_time.desc()).filter(*filters).limit(limit).offset((page_index-1)*limit).all()
        s.close()
        self.render("users_management.html",page_index = page_index,count = count,limit=limit ,keyword=keyword,users=users)

    @tornado.web.authenticated   
    def delete(self):
        self.xsrf_form_html()
        user_id = self.get_argument("user_id",default="")
        s = db.session()
        user = s.query( db.User ).filter_by(id = user_id).first()
        if(user.id):
            s.delete(user)
            s.commit()
            s.close()
            self.write(user_id)
        else:
            s.close()
            self.write("-1")

#后台用户OBD数据
class UserGetOBDList(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        page_index = int(self.get_argument("page",default="1"))
        limit = int(self.get_argument("limit",default="30"))
        is_correct = int(self.get_argument("is_correct",default="1"))
        keyword = self.get_argument("keyword",default="")
        create_time=self.get_argument("create_time",default="1970-01-0-1")
        last_login=self.get_argument("last_login",default="3000-12-31")
        if create_time=="":
            create_time="1970-01-01"
        if last_login=="":
            last_login="3000-12-31"

        # 数据判断条件
        filters = {
                db.or_(db.User.id.like('%'+keyword+'%'),
                       db.User.email.like('%'+keyword+'%'),
                       db.User.username.like('%'+keyword+'%'),
                       db.User.is_active.like('%'+keyword+'%')
                       ),
                db.User.create_time.between(create_time+" 00:00:00", last_login+" 23:59:59")
        }
        s=db.session()
        count = s.query(db.User).filter(*filters).count()
        if page_index < 1 or count == 0:
            page_index = 1
        elif limit*page_index > count:
            page_index = int((count + limit -1) / limit);
        #asc升序
        users = s.query(db.User).order_by(db.User.create_time.desc()).filter(*filters).limit(limit).offset((page_index-1)*limit).all()
        s.close()
        if create_time=="1970-01-01":
            create_time=""
        if  last_login=="3000-12-31":
            last_login=""

            #转变成json文件格式
        result_dict = [u.column_dict() for u in users]
        
        res = {"code":0,
               "msg":"",
               "count":count,
               "data": result_dict}
        # self.render("pics_management.html",page_index = page_index,count = count,limit = limit, keyword = keyword, start_date = start_date, end_date = end_date, pictures = pictures)
        self.write(res)

#用户添加界面
class ManagerUserAddHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        self.render("manager_user_add.html")

    def post(self):
        self.xsrf_form_html()
        email = self.get_argument("email",default="")
        if email != "":
            s = db.session()
            user = s.query( db.User ).filter_by( email = email ).first()
            s.close()
            if user:
                res = {"errno":"-1","err":"该邮箱已注册"}
                self.write(res)
            else:
                user_name = self.get_argument("user_name",default="")
                password = self.get_argument("password",default="")
                is_active = self.get_argument("is_active",default="")
                print(user_name+"/"+password+"/"+is_active)
                if (user_name != "") & (password != "") & (is_active != ""):

                    adduser = db.User(email = email,
                                      username = user_name,
                                      password = password,
                                      is_active = is_active)
                    s=db.session()
                    s.add(adduser)
                    s.commit()
                    s.close()
                    res = {"errno":"1","err":"用户成功添加"}
                    self.write(res)
                else:
                    res = {"errno":"-1","err":"请填写完整信息"}
                    self.write(res)
                    
        else:
            res = {"errno":"-1","err":"请输入邮箱"}
            self.write(res)

#用户修改界面
class ManagerUserEditHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        user_id = self.get_argument("user_id",default="")
        s=db.session()
        user_infos = s.query( db.User ).filter_by(id = (user_id) ).first() 
        s.close()
        self.render("manager_user_edit.html",user_infos = user_infos)

    @tornado.web.authenticated
    def post(self):
        self.xsrf_form_html()
        user_id = self.get_argument("user_id",default="")
        password = self.get_argument("password",default="")
        if ((user_id != "") & (password != "")):
            s=db.session()
            user_infos = s.query( db.User ).filter_by(id = int(user_id) ).first()
            user_infos.password = password
            s.commit()
            s.close()
            res = {"errno":"1"}
            self.write(res)
        else:
            res = {"errno":"-1"}
            self.write(res)

#后台用户激活API
class ManagerUserActiveHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def post(self):
        self.xsrf_form_html() #内部用 self.xsrf_form_html()生成
        user_id = self.get_argument("user_id",default="")
        is_active = self.get_argument("is_active",default="")
        if((user_id != "") & (is_active != "")):  #返回的id和active不为空时
            s=db.session()  #连接数据库
            user_infos = s.query( db.User ).filter_by(id = int(user_id) ).first()  #user_infos接收对应id数据
            user_infos.is_active = int(is_active)  #更改is_active，并commit。
            s.commit()
            s.close()
            res = {"errno":"1"}
        else:
            res = {"errno":"-1"}
        self.write(res)

#后台管理员管理界面
class ManagerManagementHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        page_index = int(self.get_argument("page",default="1"))
        limit = int(self.get_argument("limit",default="30"))
        keyword=self.get_argument("keyword",default="")
        # data = tornado.escape.json_decode(self.request.body)
        # if "page" in self.request.arguments:      #pyhton3 新特性不支持has_key
        #page_index = int(self.get_argument("page",default="1"))   
        # if "limit" in self.request.arguments:
        #page_size = int(self.get_argument("limit",default="15"))
           
        filters ={
                     db.or_(db.Manager.id.like("%"+keyword+"%"),
                                db.Manager.email.like("%"+keyword+"%"),
                                db.Manager.managername.like("%"+keyword+"%"),
                               ),
                    # db.User.create_time.between(create_time+"00:00:00",last_login+"00:00:00"),
        }
        s=db.session()
        count = s.query(db.Manager).filter(*filters).count()
        if page_index<1 or count==0:
                    page_index=1
        elif limit*page_index >count :
                    page_index=int((count +limit-1)/limit );

                                                                       #asc升序
        #users = s.query(db.User).order_by(db.User.create_time.desc()).filter(*filters).limit(page_size).offset((page_index-1)*page_size).all()
        managers = s.query(db.Manager).order_by(db.Manager.create_time.desc()).filter(*filters).limit(limit).offset((page_index-1)*limit).all()
        s.close()
        self.render("managers_management.html",page_index = page_index,count = count,limit=limit ,keyword=keyword,managers=managers)

    @tornado.web.authenticated   
    def delete(self):
        self.xsrf_form_html()
        manager_id = self.get_argument("manager_id",default="")
        s = db.session()
        manager = s.query( db.Manager ).filter_by(id = manager_id).first()
        if(manager.id):
            s.delete(manager)
            s.commit()
            s.close()
            self.write(manager_id)
        else:
            s.close()
            self.write("0")

#获取后台管理员数据
class ManagerManagementList(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        page_index = int(self.get_argument("page",default="1"))
        limit = int(self.get_argument("limit",default="30"))
        is_correct = int(self.get_argument("is_correct",default="1"))
        keyword = self.get_argument("keyword",default="")
        create_time=self.get_argument("create_time",default="1970-01-0-1")
        last_login=self.get_argument("last_login",default="3000-12-31")
        if create_time=="":
            create_time="1970-01-01"
        if last_login=="":
            last_login="3000-12-31"

        # 数据判断条件
        filters = {
                db.or_(db.Manager.id.like('%'+keyword+'%'),
                       db.Manager.email.like('%'+keyword+'%'),
                       db.Manager.managername.like('%'+keyword+'%'),
                       db.Manager.is_active.like('%'+keyword+'%')
                       ),
                db.Manager.create_time.between(create_time+" 00:00:00", last_login+" 23:59:59"),
                ~db.Manager.id.in_([int(self.get_secure_cookie("manager_id"))]),

        }
        s=db.session()
        count = s.query(db.Manager).filter(*filters).count()
        if page_index < 1 or count == 0:
            page_index = 1
        elif limit*page_index > count:
            page_index = int((count + limit -1) / limit);
        #asc升序
        managers = s.query(db.Manager).order_by(db.Manager.create_time.desc()).filter(*filters).limit(limit).offset((page_index-1)*limit).all()
        s.close()
        if create_time=="1970-01-01":
            create_time=""
        if  last_login=="3000-12-31":
            last_login=""

            #转变成json文件格式
        result_dict = [u.column_dict() for u in managers]
        
        res = {"code":0,
               "msg":"",
               "count":count,
               "data": result_dict}
        # self.render("pics_management.html",page_index = page_index,count = count,limit = limit, keyword = keyword, start_date = start_date, end_date = end_date, pictures = pictures)
        self.write(res)

#管理员添加界面
class ManagerAddHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        self.render("manager_add.html")

    def post(self):
        self.xsrf_form_html()
        email = self.get_argument("email",default="")
        if email != "":   #email不为空
            s = db.session()   #连接数据库
            manager = s.query( db.Manager ).filter_by( email = email ).first()
            s.close()
            if manager:   #如果manager存在说明数据已存在，返回：邮箱已注册
                res = {"errno":"-1","err":"该邮箱已注册"}
                self.write(res)
            else:  #否则接收相应信息
                manager_name = self.get_argument("manager_name",default="")
                password = self.get_argument("password",default="")
                is_active = self.get_argument("is_active",default="")
                level = self.get_argument("level",default="")
                print(manager_name+"/"+password+"/"+is_active)
                if (manager_name != "") & (password != "") & (is_active != ""):
                    #名字，密码，激活状态不为空时，s.add（）把用户数据写入数据库中并commit
                    addmanager = db.Manager(email = email,
                                      managername = manager_name,
                                      password = password,
                                      is_active = is_active,
                                      level =level )
                    s=db.session()
                    s.add(addmanager)
                    s.commit()
                    s.close()
                    res = {"errno":"1","err":"用户成功添加"}
                    self.write(res)
                else:
                    res = {"errno":"-1","err":"请填写完整信息"}
                    self.write(res)
                    
        else:
            res = {"errno":"-1","err":"请输入邮箱"}
            self.write(res)

#管理员修改界面
class ManagerEditHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.xsrf_form_html()
        manager_id = self.get_argument("manager_id",default="")
        s=db.session()
        manager_infos = s.query( db.Manager ).filter_by(id = int(manager_id) ).first() 
        s.close()
        self.render("manager_edit.html",manager_infos = manager_infos)

    @tornado.web.authenticated
    def post(self):
        self.xsrf_form_html()
        manager_id = self.get_argument("manager_id",default="")
        password = self.get_argument("password",default="")
        level=self.get_argument("level",default="")
        if ((manager_id != "") & (password != "")):
            s=db.session()
            manager_infos = s.query( db.Manager ).filter_by(id = int(manager_id) ).first()
            manager_infos.password = password
            manager_infos.level = level
            s.commit()
            s.close()
            res = {"errno":"1"}
            self.write(res)
        else:
            res = {"errno":"-1"}
            self.write(res)

#管理员修改权限界面
class ManagerEditLevelHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def post(self):
        self.xsrf_form_html()
        level=self.get_argument("level",default="")
        manager_id=self.get_argument("manager_id",default="") 
        s=db.session()
        manager_infos = s.query( db.Manager ).filter_by(id = int(manager_id) ).first()
        manager_infos.level = level
        s.commit()
        s.close()

#后台管理员激活API
class ManagerActiveHandler(ManagerBaseHandler):
    @tornado.web.authenticated
    def post(self):
        self.xsrf_form_html() #内部用 self.xsrf_form_html()生成
        manager_id = self.get_argument("manager_id",default="")
        is_active = self.get_argument("is_active",default="")
        if((manager_id != "") & (is_active != "")):
            s=db.session()
            manager_infos = s.query( db.Manager ).filter_by(id = manager_id ).first()
            manager_infos.is_active = int(is_active)
            s.commit()
            s.close()
            res = {"errno":"1"}
        else:
            res = {"errno":"0"}
        self.write(res)

# #后台角色管理界面
# class ManagerPicManagementHandler(ManagerBaseHandler):