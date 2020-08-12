#!/usr/bin/env python
# coding: utf-8

# In[13]:


import os
import shutil


# In[12]:


try:
    Dir = "./Img/Sample"
    NewDir = "./NewData/"
    os.mkdir(NewDir)
except:
    pass


# In[11]:


k = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 35, 52, 69, 103,
    120, 137, 154, 188, 205, 222, 239, 256, 273, 290, 307, 324, 341, 358, 375,
    392, 409, 426, 443, 460, 494, 511, 545, 562, 579, 596, 613
]


# In[17]:


count = 1
for i in k:
    try:
        dest = NewDir + str(count)
        count+=1
        os.mkdir(dest)
    except:
        pass
    if i < 18:
        folder = Dir + str(i).zfill(3) + "/"
        files = os.listdir(folder)
        for f in files:
            shutil.copy(folder + f, dest)
    else:
        for j in range(i-1, i+16 ):
            folder = Dir + str(j).zfill(3) + "/"
            files = os.listdir(folder)
            for f in files:
                shutil.copy(folder + f, dest)

