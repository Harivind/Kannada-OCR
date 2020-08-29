import cv2
import numpy as np

def segment_line(PATH,filename):
    img=cv2.imread(PATH,0)
    COL_THRESH=100
    WHITE_THRESH=100
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    ret,thresh1 = cv2.threshold(blurred,127,255,cv2.THRESH_BINARY)
    mean_row=[]
    num_whites=[]
    for i in range(thresh1.shape[0]):
        mean_row.append(np.mean(thresh1[i]))
        white=np.unique(thresh1[i],return_counts=True)[1][0]
        num_whites.append(white)
    fin_list=[]
    for i in num_whites:
        if i>thresh1.shape[1]-WHITE_THRESH:
            fin_list.append(1)
        else:
            fin_list.append(0)
    content=[]
    flag=0
    for i in range(len(fin_list)):
        if fin_list[i]==0 and flag==0:
            start=i
            flag=1
        if fin_list[i]==1 and flag==1:
            finish=i
            flag=0
            content.append((start,finish))
    content=[i for i in content if i[1]-i[0]>COL_THRESH]

    color = [255, 255, 255]
    pad=100
    
    line=0
    for i in content:
        line+=1
        new_im = cv2.copyMakeBorder(img[i[0]:i[1]], pad, pad, 0, 0, cv2.BORDER_CONSTANT,value=color)
        cv2.imwrite('./static/images/{}line{}.png'.format(filename,line),new_im)
        
    return line