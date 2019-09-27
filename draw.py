'''
Using opt4.py ,an Genetic Algorithm (GA), to estimate 
the best contrast and brightness parameter for the input image. (judge by score)

Compare with all the possibility contrast and brightness combination to the input image,
output a 3D graph shows the whole combination score distributes ans where the GA score locates.

By. Jonathan J. Mao  (jjmao.cs@gmail.com)
'''

import cv2, sys, os, copy
import numpy as np
from itertools import product
from nima.inference.inference_model import InferenceModel
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import opt4 as opt


X = []
Y = []
Z = []

def adjust_img(img_pth,adjust_image):
    try:
        img = cv2.imread(img_pth)
    except:
        print("error")
        sys.exit(0)

    blist = list(range(-60,66,5)) # list of brightness values
    clist = list(range(-60,66,5)) # list of contrast values

    for b,c in product(blist,clist):
        #threads.append(threading.Thread(target=apply_brightness_contrast,args=(img,adjust_image,b,c)))
        #threads[i].start()
        #i += 1
        apply_brightness_contrast(img,adjust_image,b,c)


'''
Adjust image by RGB by pixel
https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv/50053219#50053219
'''
def apply_brightness_contrast(input_img,adjust_image, brightness = 0, contrast = 0):
    #test#
    height, width, _ = input_img.shape
    out = np.zeros((height, width, 3), dtype = np.uint8)
    #test#
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
    #test#
    out[0:height,0:width] = buf
    image = Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB))
    score = float(model.predict_from_pil_image(image)['mean_score'])
    X.append(brightness)
    Y.append(contrast)
    Z.append(score)
    #adjust_image.append([[brightness,contrast],score])
    #test#
    #return buf


def starts(args):
    model_pth = './tmp0911/emd_loss_epoch_7_train_0.1333131288342482_0.12994747442647445.pth'
    #model_pth = './tmp3/emd_loss_epoch_49_train_0.05391903784470127_0.12613263790013726.pth'
    global model
    model = InferenceModel(path_to_model=model_pth)
    img_pth = args
    adjust_image = []
    adjust_img(img_pth,adjust_image)

    opt_score = opt.starts(args)
    print(opt_score)

    #plot section
    x = np.array(X)
    y = np.array(Y)
    z = np.array(Z)

    plt3d = plt.figure().gca(projection='3d')
    plt3d.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5)
    plt.xlabel("brightness")
    plt.ylabel("contrast")

    plt3d.scatter(opt_score[0][0],opt_score[0][1],opt_score[1],color='red')

    plt.show()

    return 

starts(sys.argv[1])