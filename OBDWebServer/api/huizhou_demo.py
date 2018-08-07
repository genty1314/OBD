import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from shutil import copyfile
import skimage.io as io
from skimage import data_dir
import model as modellib

import os
import cv2
import json
import base64 #新加
import coco
import skimage
import visualize
from PIL import Image
import zbarlight
#from utils.image import resize, transform

config=coco.CocoConfig()
class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
inference_config = InferenceConfig()
ROOT_DIR = os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, "logs")


class cocobox(object):
    def __init__(self,input_json_path):
        input_data=json.load(open(input_json_path,'r'))
        self.num_class=4
        self.classes=['bg','box','p','u']

        #添加内容开始
        #从json中提取出图片并保存
        img = input_data["imgFile"][0]["body"].split("\'")[-2]
        img = base64.b64decode(img)
        #存储图片文件，路径请修改到您指定的路径，当前情况是保存在python运行目录
        file = open(input_data["imgFile"][0]["filename"],'wb') 
        file.write(img)
        file.close()
        #结束
        
        self.port_direction=input_data["port_direction"]
        self.zero_port_pos=input_data["zero_port_pos"]
        self.port_sort=input_data["port_sort"]
        self.imgFile=input_data["imgFile"][0]["filename"] #此处对应的是上面file存储的文件位置，请做对应路径的修改
        self.portnum=9

    def detect(self):
        model = modellib.MaskRCNN(mode="inference",config=inference_config,model_dir=MODEL_DIR)
        model_path = model.find_last()[1]
        assert model_path != "", "Provide path to trained weights"
        model.load_weights(model_path, by_name=True)

        response = {}

        #次时的imgFile即为对应目录,故暂时直接使用
        img_path= self.imgFile #'./' + self.imgFile['filename'] 
        #结束
        assert os.path.exists(img_path)
        image = skimage.io.imread(img_path)
        results = model.detect([image], verbose=1)
        r = results[0]
        class_ids=r['class_ids']

        flag=False
        if len(class_ids)==0:
            response['status']=-1
        else:
            response['status']=0
            flag=True
        try:
            resultim,location_info=visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], self.classes, r['scores'])
            boxinfo=location_info["box"]
            portsinfo=location_info["ports"]
            u_info=location_info["u_info"]
            boxinfo[1]=u_info[1]-1
            boxinfo[3]=u_info[0]+1
            height=boxinfo[3]-boxinfo[1]
            step=height/self.portnum
            ports_occupy=[0]*self.portnum
            for port in portsinfo:
                (x,y)=port
                index=int((y-boxinfo[1])/step)
                ports_occupy[index]=1
            response["ports_occupy"]=ports_occupy

            #路径稍做修改
            # save_dir='.'+img_path.split('.')[-2]+'_result.jpg'
            save_dir=img_path.split('.')[-2]+'_result.jpg'
            #结束
            
            a=cv2.imwrite(save_dir,resultim)
            #QRCode
            if flag:
                image = Image.open(img_path)
                image.load()
                codes = zbarlight.scan_codes('qrcode', image)
                if codes is not None:
                    response['status']=1
                    QRCode={}
                    QRCode["code"]=codes
                    QRCode["name"]=""
                    QRCode["address"]=""
                    QRCode["GPS"]=""
                    response["QRCode"]=QRCode
            
            #此处的imgFile因保存如下内容
            if(os.path.exists(os.path.join(save_dir))):
                body = open(os.path.join(save_dir),'rb').read()
                bodybase64 = str(base64.b64encode(body))
                response["imgFile"] = [{"filename":save_dir,
                                       "content_type": "img/"+save_dir.split(".")[-1],
                                       "body":bodybase64 }]
            else:
                response["imgFile"] = []
            #结束
            
            # response["imgFile"]=self.imgFile
            
            #output_data.json
            with open("./output_data.json","w",encoding='utf-8') as json_file:
                    json.dump(response,json_file,ensure_ascii=False)
            print("./output_data.json")
            #结束
            
            # print (response)
        except:
            print ("The input picture is not standardized.")


if __name__ == '__main__':
    cocoboximage=cocobox("./input_data.json")
    cocoboximage.detect()
