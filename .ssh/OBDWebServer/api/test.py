import os
import json
import base64

input_data=json.load(open("./input_data.json",'r'))
print(input_data["imgFile"][0]["filename"])
img = input_data["imgFile"][0]["body"].split("\'")[-2]
img = base64.b64decode(img)

#存储图片文件，路径请修改到您指定的路径
file = open(input_data["imgFile"][0]["filename"],'wb') 
file.write(img)
file.close()
