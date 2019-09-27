'''
USAGE:
    From terminal:
        python messure_opt4.py (YOUR_IMAGE_PATH) 
    From Other Files (Same dirctory):
        import messure_opt4
        opt4.starts(YOUR_IMAGE_PATH)

BE AWARE:
    1. The model pth is fixed in this file, moodify it if any changes
    (at around line no. 264)
    2. This file doesn't link to opt4.py, if previous modified, this needs it too.

By. Jonathan J. Mao (jjamo.cs@gmail.com)
'''

import cv2, sys, os, random, copy
import numpy as np
from nima.inference.inference_model import InferenceModel
from PIL import Image 
import timeit

def tobin(num):
    #return bin(int(abs(num)/10))[2:].zfill(4)  #for-80~80
    return bin(int(abs(num)/10))[2:].zfill(3)


def encoding(tuple_num):
    num1 = tuple_num[0]
    num2 = tuple_num[1]
    if num1 >= 0:
        num1 = '0' + tobin(num1)
    elif num1 < 0:
        num1 = '1' + tobin(num1)
    else:
        sys.exit(0) 
    if num2 >= 0:
        num2 = '0' + tobin(num2)
    elif num2 < 0:
        num2 = '1' + tobin(num2)
    else:
        sys.exit(0) 
    return num1, num2


def decoding(num1, num2):
    if num1[0] == '0':
        num1 = int(num1[1:],2)
    elif num1[0] != '0':
        num1 = -int(num1[1:],2)
    else:
        sys.exit(0) 
    if num2[0] == '0':
        num2 = int(num2[1:],2)
    elif num2[0] != '0':
        num2 = -int(num2[1:],2)
    else:
        sys.exit(0) 
    return num1*10, num2*10


'''
detect and convert
10bit encoded string to no minus zero string
'''
def encode_error_detect(string):
    newstring = ''
    b, c = decoding(string[:4],string[4:])
    '''
    brightness
    '''
    if string[:4] == '1000':
        newstring += '0000'
    elif b > 60:
        newstring += '0110'
    elif b < -60:
        newstring += '1110'
    else:
        newstring += string[:4]
    '''
    constract
    '''
    if string[4:] == '1000':
        newstring += '0000'
    elif c > 60:
        newstring += '0110'
    elif c < -60:
        newstring += '1110'
    else:
        newstring += string[4:]

    return newstring


def bcrandom(bclist,psize):
    while True:
        bclist.append((int(random.randint(-60,70)/10)*10,int(random.randint(-60,70)/10)*10))
        bclist = list(dict.fromkeys(bclist))
        if len(bclist) >= psize:
            break
    return bclist


'''
bc is tuple
images save modified
'''
def find_image(bc,images,input_img):
    if bc in images:
        return images[bc]
    else:
        images[bc] = apply_brightness_contrast(bc,input_img)
        return images[bc]


def apply_brightness_contrast(bc,input_img):
    height, width, _ = input_img.shape
    out = np.zeros((height, width, 3), dtype = np.uint8)
    brightness = bc[0]
    contrast = bc[1]

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    out[0:height,0:width] = buf
    return out


def genetic(model,input_img):
    psize = 20
    bclist = []

    '''
    default random b,c
    '''
    bclist = bcrandom(bclist,psize)
    top,sec = ['',0],['',0]
    current = {}
    images = {}
    epoch = 5

    '''
    genetic opt
    '''
    while epoch != 0:
        top[0] = ''
        top[1] = 0
        sec[0] = ''
        sec[1] = 0
        epoch -= 1
        #count score
        for j in bclist:
            img = find_image(j,images,input_img)
            img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
            current[j] = float(model.predict_from_pil_image(img)['mean_score'])
            if current[j] > top[1]:
                #print('01',end = '')
                sec = copy.deepcopy(top)
                top[0] = j
                top[1] = current[j]
            elif current[j] > sec[1]:
                #print('02',end = '')
                sec[0] = j
                sec[1] = current[j]
            #print(bclist)
            #print(top,sec)
        #print('================')
        #print('bclist')
        #print(bclist)
        #print(top,sec)
        #print('================')
        
        #next generation
        iter_bclist = iter(bclist)
        next_bclist = [top[0],sec[0]]

        try:
            for i in iter_bclist:
                j = next(iter_bclist)
                ib1, ic1 = encoding(i)
                ib2, ic2 = encoding(j)
                p1 = ib1 + ic1
                p2 = ib2 + ic2
                n = random.randint(2,7)
                for k in range(n):
                    t = random.randint(1,8)
                    np1 = p1[:t] + p2[t:]
                    np1 = encode_error_detect(np1)
                    t = random.randint(1,8)
                    np2 = p2[:t] + p1[t:]
                    np2 = encode_error_detect(np2)
                    '''
                    #delete the same with parents and siblings
                    if np1 != p1 and np1 != p2:
                        next_bclist.append(decoding(np1[:4],np1[4:]))
                    if np2 != p1 and np2 != p2 and np2 != np1:
                        next_bclist.append(decoding(np1[:4],np1[4:]))
                    '''
                    #''' no delete same with parents
                next_bclist.append(decoding(np1[:4],np1[4:]))
                next_bclist.append(decoding(np2[:4],np2[4:]))
                    #'''


            next_bclist = next_bclist[:-2]  #排除高分保留
            #print(len(next_bclist),next_bclist)
            next_bclist = bcrandom(next_bclist,psize)
        except StopIteration:
            next_bclist = next_bclist[:-2]
            next_bclist = bcrandom(next_bclist,psize)

        bclist = copy.deepcopy(next_bclist)
        #print(len(bclist),bclist)
    print('=================')
    print(top)
    final_img = Image.fromarray(cv2.cvtColor(find_image(top[0],images,input_img),cv2.COLOR_BGR2RGB))
    #final_img.show()
    
    return top[0], top[1], final_img


def starts(args):
    model_pth = './tmp3/emd_loss_epoch_49_train_0.05391903784470127_0.12613263790013726.pth'
    model = InferenceModel(path_to_model=model_pth)
    img_pth = args
    img = cv2.imread(img_pth)
    return  genetic(model,img)


if __name__ == "__main__":
    a = timeit.repeat('starts(sys.argv[1])','from __main__ import starts',repeat=10,number=1)
    print(a)
    print(sum(a)/float(len(a)))

    
    

