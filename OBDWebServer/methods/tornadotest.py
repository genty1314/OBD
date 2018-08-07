import tornado.ioloop
import tornado.web

class ConfirmHandler(tornado.web.RequestHandler):
    def post(self):
        


application = tornado.web.Application([
    (r"/", ConfirmHandler),
])


if __name__ == "__main__":
    port = 8888
    application.listen(port)
    print(port)
    tornado.ioloop.IOLoop.instance().start()
