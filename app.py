from flask import Flask, render_template,flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from segment import segment_input
from segment_spaces import segmentspaces_input
import io 
from fastai.vision import *

# ROOT_DIR="D:\\Projects\\OcrKannada\\Application\\"
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = ROOT_DIR+'static\\Upload'
app.secret_key = 'asrtarstaursdlarsn'
#unicode for each dependent vowel

learn = load_learner('./')

matraUnicode={
    0: '\u0ccd',
    1: '',
    2: '\u0cbe',
    3: '\u0cbf',
    4: '\u0cc0',
    5: '\u0cc1',
    6: '\u0cc2',
    7: '\u0cc3',
    8: '\u0cc4',
    9: '\u0cc6',
    10: '\u0cc7',
    11: '\u0cc8',
    12: '\u0cca',
    13: '\u0ccb',
    14: '\u0ccc',
    15: '\u0c82',
    16: '\u0c83',
}

#unicode for each independent vowel
independentMatraUnicode = {
    1 : '\u0C85',
    2 : '\u0C86',
    3 : '\u0C87',
    4 : '\u0C88',
    5 : '\u0C89',
    6 : '\u0C8A',
    7 : '\u0C8B',
    8 : '\u0C8C',
    9 : '\u0C8E',
    10 : '\u0C8F',
    11 : '\u0C90',
    12 : '\u0C92',
    13 : '\u0C93',
    14 : '\u0C94',
    15 : '\u0c85\u0c82',
    16 : '\u0c85\u0c83',
}

#unicode for each consonant
charUnicode={
    1 : '\u0C95',
    2 : '\u0C96',
    3 : '\u0C97',
    4 : '\u0C98',
    5 : '\u0C99',
    6 : '\u0C9a',
    7 : '\u0C9b',
    8 : '\u0C9c',
    9 : '\u0C9d',
    10 : '\u0C9e',
    11 : '\u0C9f',
    12 : '\u0Ca0',
    13 : '\u0Ca1',
    14 : '\u0Ca2',
    15 : '\u0Ca3',
    16 : '\u0Ca4',
    17 : '\u0Ca5',
    18 : '\u0Ca6',
    19 : '\u0Ca7',
    20 : '\u0Ca8',
    21 : '\u0Caa',
    22 : '\u0Cab',
    23 : '\u0Cac',
    24 : '\u0Cad',
    25 : '\u0Cae',
    26 : '\u0Caf',
    27 : '\u0Cb0',
    28 : '\u0Cb1',
    29 : '\u0Cb2',
    30 : '\u0Cb3',
    31 : '\u0Cb4',
    32 : '\u0Cb5',
    33 : '\u0Cb6',
    34 : '\u0Cb7',
    35 : '\u0Cb8',
    36 : '\u0Cb9',
}


@app.route('/',methods=['GET'])
def upload_file():
    if request.method=='GET':
        return render_template('./index.html',result='false',imagesrc="/static/assets/img/1%20CBkz7f_KjNh_wVuqLp-m0A.png")

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file")
            return render_template('./index.html',result='false',uploaded='false',imagesrc="/static/assets/img/1%20CBkz7f_KjNh_wVuqLp-m0A.png")
        file = request.files['file']
        if file.filename == '':
            return render_template('./index.html',result='false',uploaded='false',imagesrc="/static/assets/img/1%20CBkz7f_KjNh_wVuqLp-m0A.png")
        if file:
            # print("Hello")
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save("./static/Upload/{}".format(filename))
            # number_files=segment_input(os.path.join(app.config['UPLOAD_FOLDER'], filename),filename.split(".")[0])
            number_files=segmentspaces_input("./static/Upload/{}".format(filename),filename.split(".")[0])
            #<HARIS CODE>
            s=''
            # with open('./static/output.txt','w') as outputFile:
            # number_files=1
            for i in range(0,number_files):
                #checking if the file is an image
                # if i.find('png')<1 and i.find('jpg')<1:
                    # continue
                print(i)
                img = open_image('./images/{}c{}.png'.format(filename.split(".")[0],i+1))
                
                #img with size 6X9 is a space
                if img.size[0]==6 and img.size[1]==9:
                    # outputFile.write(' ')
                    s+=' '
                    print("Skipped: ",i+1)
                    continue
                
                prediction = learn.predict(img)[0]
                sampleNumber = int(prediction.obj[-3:])
                try:
                    if sampleNumber<17:
                        print(independentMatraUnicode[sampleNumber])
                        s+=independentMatraUnicode[sampleNumber]
                        # outputFile.write(independentMatraUnicode[sampleNumber])
                    else:
                        print(charUnicode[sampleNumber//17]+matraUnicode[sampleNumber%17])
                        s+=charUnicode[sampleNumber//17]+matraUnicode[sampleNumber%17]
                        # outputFile.write(charUnicode[sampleNumber//17]+matraUnicode[sampleNumber%17])
                except:
                    # outputFile.write('')
                    s+='?'
            print('S: ',s)
            try:
                return render_template('./index.html',result='true',imagesrc="/static/Upload/{}".format(filename),data=s)
            except:
                return render_template('./index.html',result='true',imagesrc="/static/Upload/{}".format(filename))

if __name__ == '__main__':
   app.run(debug=True)