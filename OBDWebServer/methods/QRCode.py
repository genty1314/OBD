from PIL import Image
import zbarlight
def QRCode(img_path):
     image = Image.open(img_path)
     image.load()
     codes = zbarlight.scan_codes('qrcode', image)
     res = {}
     if codes and len(codes[0].decode().split(';')) >3:
        temp = codes[0].decode().split(';')
        res = { 'code':temp[0].split('：')[-1],
                'name':temp[1].split('：')[-1],
                'address':temp[2].split('：')[-1],
                'GPS':temp[3]+';'+temp[4]
        }
     else:
        res = { 'code':'',
                'name':'',
                'address':'',
                'GPS':''
        }
     return res

if __name__ == '__main__':
     a = QRcode("IMG_20170823_155244.jpg")
     print(a['name'])

