#!/usr/bin/env python
import os,shutil
import cv2

directory="d://docs//Kannada project//cropped images//dataset2_File410-509//Combine"
l= os.listdir(directory)
l.sort(key=lambda s: os.path.getmtime(os.path.join(directory, s)))

ds=input("Enter dataset no: ")
prev=""
for i in l:
    print(i)
    pres=i.split('_')[0]
    dest="d://docs//Kannada project//Kannada//Hnd//Img//Sample"
    if pres != prev:
        image = cv2.imread(directory+"//{}".format(i))
        image=cv2.resize(image,(image.shape[1]//2,image.shape[0]//2),interpolation=cv2.INTER_AREA)
        cv2.imshow("image", image) 
        key = cv2.waitKey(0) & 0xFF
        if key == ord("q"):
            break
        num=input("Enter number: ")
        no=num
        no=no.zfill(3)
        d=dest+'{}/{}{}'.format(no,ds,i)
        cv2.destroyAllWindows()
        shutil.copy(directory+"//{}".format(i),d)
        prev=pres
        count=1
        continue    
    if pres==prev:
        count+=1
        if count==5:
            no=int(no)+1
            if(no-int(num)==7):
                no+=1
            no=str(no).zfill(3)
            count=1
        d=dest+'{}/D{}{}'.format(no,ds,i)
        shutil.copy(directory+"//{}".format(i),d)       
cv2.destroyAllWindows()