#!/usr/bin/env Python
# coding=utf-8

from url import url
import base64, uuid
import tornado.web
import os

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "2o1C6oiVQgKsXzcyGt3928ZQ7a0660l0n0uQRRM4gt0=",#base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    #xsrf_cookies = True, #在handler内部用 self.xsrf_form_html()生成
    #login_url = '/managerlogin', #在base.py中使用def get_login_url(self):实现
    # ,ssl_options={#https访问配置
    #    "certfile": os.path.join(os.path.abspath("."), "ssl/server.crt"),
    #    "keyfile": os.path.join(os.path.abspath("."), "ssl/server.key.unsecure"),}
    connect_timeout=20.0, #连接时长限制设置
    request_timeout=20.0,
    debug = True
    )

application = tornado.web.Application(
    handlers = url,
    **settings
    )