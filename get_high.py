'''
A tool that can get the highest score image form the directory chosen.
Score calculate by the txt file AVA provided for made by user.

txt format : (Copy from AVA Dataset)

**************************************************************************
Content of AVA.txt
**************************************************************************

Column 1: Index

Column 2: Image ID 

Columns 3 - 12: Counts of aesthetics ratings on a scale of 1-10. Column 3 
has counts of ratings of 1 and column 12 has counts of ratings of 10.

Columns 13 - 14: Semantic tag IDs. There are 66 IDs ranging from 1 to 66.
The file tags.txt contains the textual tag corresponding to the numerical
id. Each image has between 0 and 2 tags. Images with less than 2 tags have
a "0" in place of the missing tag(s).

Column 15: Challenge ID. The file challenges.txt contains the name of 
the challenge corresponding to each ID.
**************************************************************************

By. Jonathan J. Mao  (jjmao.cs@gmail.com)
'''


import os
import numpy as np


AVA_Image_Dir = "ENTER_YOUR_PATH"
AVA_TXT_PATH = "ENTER_YOUR_PATH"


a = os.listdir(AVA_Image_Dir)


with open(AVA_TXT_PATH) as f:
    b = f.readlines()
    c = {}
    for i in b:
        c[i.split()[1]] = np.sum(np.array(i.split()[2:12],dtype=np.int) * np.array([1,2,3,4,5,6,7,8,9,10],dtype=np.int))/np.sum(np.array(i.split()[2:12],dtype=np.int))

    top = ""
    tscore = 0
    for i in a:
        if not i.endswith('.jpg'):
            break
        if i.split('.')[0] in c:
            if c[i.split('.')[0]] > tscore:
                tscore = c[i.split('.')[0]]
                top = i.split('.')[0]

    print(top,tscore)

    
