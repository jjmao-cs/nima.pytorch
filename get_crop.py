from PIL import Image
import os,sys,json,cv2,collections
import numpy as np

#imfile, box = sys.argv[1], sys.argv[2]



def adjust():

    img = cv2.imread('1.jpg')

    height, width, _ = img.shape

    b = -40
    c = -40
    print(height,width)
    out = np.zeros((height, width, 3), dtype = np.uint8)
    out[0:height,0:width] = apply_brightness_contrast(img, b, c)
    out[80:722,300:1020] = img[80:722,300:1020]

    cv2.imshow("out",out)
    cv2.waitKey(0)


def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
#https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv/50053219#50053219
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

    return buf


adjust()