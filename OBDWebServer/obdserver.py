#!/usr/bin/env Pythonc
# coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
import os
from application import application

from tornado.options import define, options

define("port", default = 8001, help = "run on the given port", type = int)
define("log_path", default='/tmp', help="log path ", type=str)
# def deltmp():
#     rootdir = 'tmp'
#     list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
#     for i in range(0,len(list)):
#            path = os.path.join(rootdir,list[i])
#            if os.path.isfile(path):
#                  os.remove(path)
#     print('tmp deleted!\n')
#     print(list)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print ("Development server is running at https://127.0.0.1:%s" % options.port)
    print ("Quit the server with Control-C")
    
    # tornado.ioloop.PeriodicCallback(deltmp, 2*60*60*1000).start() # start scheduler 每隔2h执行一次deltep清除tmp文件夹缓存
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()