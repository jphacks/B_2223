import easyocr
from tokenize import cookie_re
import cv2
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import glob
import os
import translators as ts
import textwrap
from goolabs import GoolabsAPI
import time

ocr_img_dir = "/content/ocr"

if not os.path.exists(ocr_img_dir):
    os.makedirs(ocr_img_dir)

d_files = glob.glob("divide/*.jpg")
d_files.sort()

print(len(d_files), "image files")

# 使うフォント，サイズ，描くテキストの設定
ttfontname = "/usr/share/fonts/opentype/ipafont-mincho/ipam.ttf"
fontsize = 13

# 画像サイズ，背景色，フォントの色を設定
canvasSize    = (400, 720)
backgroundRGB = (255, 255, 255)
textRGB       = (0, 0, 0)

reader = easyocr.Reader(['ja','en'],gpu = True)
x = 0

app_id = "72d3486152b29be7c3e51aaa255f53de6cebc31d1315fb97dbfe6697b3ee5a39"
api = GoolabsAPI(app_id)

for i, file in enumerate(d_files):

    #img = cv2.imread(file)
    result = reader.readtext(file)
    print(x)
    x+=1

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output = ""

    for t in result:
      if t[2] > 0.6:
        #認識した文字 日本語の改行は23文字
        output += "Recognize   : "
        if len(t[1])<24:
          output += t[1]
        else:
          #time.sleep(60)
          print(t[1]+" "+str(len(t[1]))+"文字")
          for i in range(2):
            time.sleep(60)
            print("60秒経過")
          count = 0
          morph_response = api.morph(sentence=t[1])
          for s in morph_response["word_list"][0]:
            count += len(s[0])
            if count > 23:
              output += "\n"
              output += "              "
              output += s[0]
              count = len(s[0])
            else:
              output += s[0]
        output += "\n"
        #文字が正確である確率
        output += "Accuracy    : "
        output += str(t[2])
        output += "\n"
        #文字の改行 英語の改行は30文字
        output += "Translation : "
        trans_str = ts.google(t[1])
        s_wrap_list = textwrap.wrap(trans_str, 30)
        for s in s_wrap_list:
          output += s
          output += "\n"
          output += "              "
        #output += textwrap.fill(trans_str, 30)
        output += "\n\n"

    # 文字を描く画像の作成
    img  = PIL.Image.new('RGB', canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(img)

    # 用意した画像に文字列を描く
    font = PIL.ImageFont.truetype(ttfontname, fontsize)
    textTopLeft = (0, 0)
    draw.text(textTopLeft, output, fill=textRGB, font=font)

    # 画像を保存する
    ocr_file = "ocr/{index:04d}.jpg".format(index=i)
    img.save(ocr_file)
