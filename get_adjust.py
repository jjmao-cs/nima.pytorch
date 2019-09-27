'''
A tool that can get the adjust image depends on the input given.

The output will pop up a window shows the image adjust with the parameter inputs.

By. Jonathan J. Mao (jjmao.cs@gmail.com)
'''

import cv2, sys, os, copy
import numpy as np
from itertools import product
from nima.inference.inference_model import InferenceModel
from PIL import Image


brightness = -20
contrast = 60

'''
Adjust image by RGB by pixel
https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv/50053219#50053219
'''
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
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
    out = np.zeros((height, width, 3), dtype = np.uint8)
    out[0:height,0:width] = buf
    cv2.namedWindow('My Image', cv2.WINDOW_NORMAL)
    cv2.imshow('My Image',out)
    cv2.waitKey(0)
    #adjust_image.append([[brightness,contrast],score])
    #test#



img = cv2.imread(sys.argv[1])
apply_brightness_contrast(img, brightness, contrast)
