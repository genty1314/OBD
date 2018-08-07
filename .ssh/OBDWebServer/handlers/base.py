#! /usr/bin/env python
# coding=utf-8

import io
import tornado.web
import methods.check_code as check_code
from methods.session import Session


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.session=Session(self)

    # def on_connection_close(self):
    #     if self.stream_request_body:
    #         self.handler.on_connection_close()
    #     else:
    #         print("on_connection_close")
    #         self.xsrf_form_html()
    #         self.clear_all_cookies()
    #         self.chunks = None
    
    def get(self):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            self.write('error:' + str(status_code))



class ManagerBaseHandler(BaseHandler):

    def get_current_user(self): #重写get_current_user供 @tornado.web.authenticated使用实现对manager管理员的验证
        return self.get_secure_cookie("manager_id")

    def get_login_url(self):  #管理员认证失败时返回到管理员登录界面
        return "/managerlogin"

class UserBaseHandler(BaseHandler):

    def get_current_user(self): #重写get_current_user供 @tornado.web.authenticated使用实现对user用户的验证
        return self.get_secure_cookie("user_id")

    def get_login_url(self):  #用户认证失败时返回到另一个与管理员登录不同的界面
        return "/userlogin"

#验证码
class check_codeHandler(BaseHandler):
    def get(self, *args, **kwargs):#生成图片并返回
        mstream=io.BytesIO()
        #创建图片 并写入验证码
        img,code=check_code.create_validate_code()
        #讲图片对象写入到mastream
        img.save(mstream,'GIF')
        self.session['CheckCode']=code
        #为每个用户保存验证码
        self.write(mstream.getvalue())
        #返回图片给客户端