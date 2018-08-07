#!/usr/bin/env Python
# coding=utf-8
# 打包数据为excl 或图片zip压缩包
import xlwt
import zipfile
import datetime
import os
import random
import string

#导出excl数据
#querys为sqlalchemy搜索得到的结果参数，path为存储excl的路径，
#filename为返回的文件名
def patch2excl(querys, path = 'tmp'):
    #querys结果dict化
    result_dict = [u.column_dict() for u in querys]
    
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('OBDInfo',cell_overwrite_ok=True)

    # 写上字段信息
    keys = list(result_dict[0].keys())
    for key in range(0,len(keys)):
        sheet.write(0,key,keys[key])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1,len(result_dict)+1):
        for col in range(0,len(keys)):
            sheet.write(row,col,u'%s'%list(result_dict[row-1].values())[col])
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'_'+ran_str+'.xls'
    workbook.save(os.path.join(path,filename))
    return filename

def patch2imgzip(querys, path = 'tmp'):
    #querys结果dict化
    result_dict = [u.column_dict() for u in querys]
    
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'_'+ran_str+'.zip'
    azip = zipfile.ZipFile(os.path.join(path,filename), 'w')
    for r in result_dict:
        if r['picture_path'] and os.path.isfile('static/'+r['picture_path']):
            azip.write('static/'+r['picture_path'],'原图/'+r['picture_path'].split("/")[-1], compress_type=zipfile.ZIP_DEFLATED)
        if r['confirmed_picture_path'] and os.path.isfile('static/'+r['confirmed_picture_path']):
            azip.write('static/'+r['confirmed_picture_path'],'验证图/'+r['confirmed_picture_path'].split("/")[-1], compress_type=zipfile.ZIP_DEFLATED)
    azip.close()
    return filename