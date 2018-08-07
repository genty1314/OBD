#这个字典必须定制成为全局变量用来保存用户的信息，如果是局部变量，
# 那么http请求断开下次用户登录这个用户信息就会消失
container={}

        #把Sesson封装起来
class Session:
    def __init__(self,handler):
        self.handler=handler
        self.random_str=None  #用户连接初始化随机数
    def __genarate_random_str(self):   #创建随机字符串
        import hashlib
        import time
        #首先通过md5生成随机数据，电脑中的数据都是16进制保存的
        obj=hashlib.md5()
        obj.update(bytes(str(time.time()),encoding="utf-8"))
        random_str=obj.hexdigest()
        return random_str
    def __setitem__(self,key,value):
        #这里判断如果服务端没有随机数
        if not self.random_str:               #用户连接，首先服务端没有随机数，那么去客户端拿随机数
            random_str=self.handler.get_cookie("__session__") #去客户端中拿随机数
            if not  random_str:                           #如果客户端也没有随机数，那么服务端就自己创建随机数
                random_str=self.__genarate_random_str()  #创建随机数
                container[random_str]={}                 #清空随机数字典中的内容
            else:
                if random_str in container.keys():    #如果客户端有随机数，并且为真那么就直接登录成功
                    pass
                else:                                   #如果客户端到的随机数是伪造的，那么服务端就自己创建随机数
                    random_str=self.__genarate_random_str()
                    container[random_str]={}
            self.random_str=random_str   #最后把上面判断出来的随机数传递给类
        container[self.random_str][key]=value
        #这里是为写超时时间做准备
        self.handler.set_cookie("__session__",self.random_str)  #设置cookie给浏览器，这里可以设置超时时间


    def __getitem__(self,key):  #获取值
        random_str=self.handler.get_cookie("__session__")
        if not  random_str:#如果客户端没有随机字符串，就结束
            return None
        user_info_dict=container.get(random_str,None)#客户端有随机字符串，但是内容服务器不匹配，就退出
        if not user_info_dict:
            return None
        value=user_info_dict.get(key,None)   #前面如果都满足，有值就拿值，没有就为None
        return value