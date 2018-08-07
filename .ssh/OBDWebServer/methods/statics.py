#!/usr/bin/env Python
# coding=utf-8

#web服务默认配置参数

#数据库连接设置
# ?charset=utf8 防止中文乱码
# mysql         数据库类型
# root:root     数据库用户名:数据库密码
# localhost     数据库地址
# 3306          数据库端口
DATABASE_CONNCT_SEETING = "mysql://root:root@localhost:3306/OBD?charset=utf8"

#网站后台名称
WEBSIDE_NAME = "OBD智能识别系统后台"


FRONT_WEBSIDE_NAME = "OBD智能识别系统"

DEFAULT_PROFILE_PHOTO = "images/default_profile_photo.png"