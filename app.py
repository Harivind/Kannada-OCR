from flask import Flask, render_template,flash, request, redirect, url_for,make_response,render_template
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from segment import segment_input
from segment_spaces import segmentspaces_input
import io 
from fastai.vision import *
from segment_lines import segment_line
from fpdf import FPDF 
import random
import json
# save FPDF() class into a  
# variable pdf 
pdf = FPDF() 
  
# Add a page 
pdf.add_page() 
  
# set style and size of font  
# that you want in the pdf 
pdf.add_font('kedage', '', 'kedage-b.ttf', uni=True) 
pdf.set_font('kedage', '', 14)
# pdf.write(8, u'Hindi: नमस्ते दुनिया')
# pdf.ln(20)
# create a cell 


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
        pdf = FPDF() 
        pdf.add_page() 
        pdf.add_font('kedage', '', 'kedage-b.ttf', uni=True) 
        pdf.set_font('kedage', '', 14)
        fileArr=[]
        predChars=[]
        if 'file' not in request.files:
            print("No file")
            return render_template('./index.html',result='false',uploaded='false',imagesrc="/static/assets/img/1%20CBkz7f_KjNh_wVuqLp-m0A.png")
        file = request.files['file']
        if file.filename == '':
            return render_template('./index.html',result='false',uploaded='false',imagesrc="/static/assets/img/1%20CBkz7f_KjNh_wVuqLp-m0A.png")
        if file:
            filename = secure_filename(file.filename)
            file.save("./static/Upload/{}".format(filename))
            file_nameoly=filename.split(".")[0]
            if os.path.exists('./static/{}.pdf'.format(file_nameoly)):
                os.remove('./static/{}.pdf'.format(file_nameoly))
            number_lines=segment_line("./static/Upload/{}".format(filename),file_nameoly)
            print("Number of lines: ",number_lines)
            content=''
            for line_num in range(1,number_lines+1):
                number_files=segmentspaces_input("./static/images/{}line{}.png".format(file_nameoly,line_num),file_nameoly,line_num)
                # s=''
                for i in range(1,number_files+1):

                    img = open_image('./static/images/{}line{}c{}.png'.format(file_nameoly,line_num,i))
                    print("opened  image: ",i)
                    #img with size 6X9 is a space
                    if img.size[0]==6 and img.size[1]==9:
                        # outputFile.write(' ')
                        content+=' '
                        print("Skipped: ",i)
                        continue
                    fileArr.append('./static/images/{}line{}c{}.png'.format(file_nameoly,line_num,i))
                    prediction = learn.predict(img)[0]
                    sampleNumber = int(prediction.obj[-3:])
                    try:
                        if sampleNumber<17:
                            # print(independentMatraUnicode[sampleNumber])
                            content+=independentMatraUnicode[sampleNumber]
                            predChars.append(independentMatraUnicode[sampleNumber])
                            # outputFile.write(independentMatraUnicode[sampleNumber])
                        else:
                            # print(charUnicode[sampleNumber//17]+matraUnicode[sampleNumber%17])
                            content+=charUnicode[sampleNumber//17]+matraUnicode[sampleNumber%17]
                            predChars.append(charUnicode[sampleNumber//17]+matraUnicode[sampleNumber%17])
                            # outputFile.write(charUnicode[sampleNumber//17]+matraUnicode[sampleNumber%17])
                    except:
                        # outputFile.write('')
                        content+='☐'
                        predChars.append('☐')
                        print('I: ',i)
                    print('CONTENT: ',content,'\nI: ',i)
                print('S: ',content)
                content+='\n'
            pdf.write(8,content)
            pdf.ln(20)
            # randnum = random.randint(0,1000)
            pdf.output('./static/Output/{}.pdf'.format(file_nameoly))#,randnum))

            # response = make_response(pdf.output(dest='S').encode('latin-1')) 
            # response.headers['Content-Type'] = 'application/pdf'
            
            # response.headers['Content-Disposition'] = 'attachment; filename=Results.pdf'
            # return response
            print(fileArr)
            filenames={'files':fileArr}
            chars={'chars':predChars}
            try:
                return render_template('./index.html',result='true',imagesrc="/static/Upload/{}".format(filename),
                                        data=content,openpdf='true',filename='{}'.format(file_nameoly),#,randnum),
                                        numfiles=filenames,numlines=number_lines,charspred=chars)
                
            except:
                return render_template('./index.html',result='true',imagesrc="/static/Upload/{}".format(filename))

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
if __name__ == '__main__':
   app.run(debug=True)