'''
An old approach compare to opt4.py
Do not use this anymore

By. Jonathan J. Mao (jjmao.cs@gmail.com)
'''


import os,sys,json,cv2,collections
import numpy as np
from nima.inference.inference_model import InferenceModel

def mynima(args):
    
    '''
    測試pth是否存在
    '''  
    #print(args[1])
    try:
        print(args[1])
        os.stat(args[1])
        pth = args[1]
    except:
        print('file dir error')
        print('end process')
        return
        #pth = './image/image'
        #print('Using "./image/image"(training set) as default img pth.')


    if not pth.endswith('/'):
        pth += '/'

    pics = []
    pths = []
    for i in os.listdir(pth):
        if i.endswith('.jpeg') or i.endswith('.jpg'):
            pics.append(i)
            pths.append(pth+i)
    for i in pths:
        adjust(i)

    for i in os.listdir(pth):
        if i.endswith('.jpeg') or i.endswith('.jpg'):
            pics.append(i)
            pths.append(pth+i)

    pics = list(set(pics))
    pths = list(set(pths))
    print(str(len(pics)) + ' pictures found!')

    #os.popen('python nima/cli.py get-image-score --path_to_model_weight ./tmp/emd_loss_epoch_49_train_0.03547421253612805_0.08993149643023331.pth --path_to_image '+pths[0])
    model_str = './tmp/emd_loss_epoch_49_train_0.03547421253612805_0.08993149643023331.pth'
    model = InferenceModel(path_to_model=model_str)
    #result = model.predict_from_file(pths[10])
    #print(result)

    score = {}
    highest_score = 0
    highest_pic = ''
    for i in range(int(len(pths))):
        r = model.predict_from_file(pths[i])
        score[pics[i]] = r['mean_score']
        #print('',end='>> ',flush=True)
        if int(r['mean_score']) > highest_score:
            highest_score = int(r['mean_score'])
            highest_pic = pics[i]

    print(str(highest_score)+' '+highest_pic+'finish')	
    sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)
    sorted_score = collections.OrderedDict(sorted_score)

    final = {}
    final['results']=[]
    for i in sorted_score:
        final['results'].append({'name':i, 'score':sorted_score.get(i)})
    #print(sorted_score)
    #print(score)

    try:
        outfile = open(args[2],'w')
        print('saving test json at '+args[2])

    except:
        print('output_location not found')
        print('saving test json at "./test_data/data.json"')
        outfile = open('./test_data/data.json','w+')
    finally:
        #data = json.dumps(sorted_score)
        json.dump(final,outfile)
        #json.dump(score,outfile)        
        outfile.close


def adjust(img_pth):
    try:
        img = cv2.imread(img_pth)
    except:
        print("image path error at adjust")
        return
    height, width, _ = img.shape
    #dir = os.path.dirname(img_pth)
    frontname = os.path.splitext(img_pth)[0]
    filetype = os.path.splitext(img_pth)[-1]

    blist = [20, 40, 60, -20, -40, -60,  0,  0,  0,   0,   0,   0] # list of brightness values
    clist = [ 0,  0,  0,   0,   0,   0, 20, 40, 60, -20, -40, -60] # list of contrast values   

    
    for i, b in enumerate(blist):
        out = np.zeros((height, width, 3), dtype = np.uint8)
        c = clist[i]
        #print('b, c:  ', b,', ',c)
        #row = s*int(i/3)
        #col = s*(i%3)
        #print('row, col:   ', row, ', ', col)

        out[0:height,0:width] = apply_brightness_contrast(img, b, c)
        cv2.imwrite(frontname +'_B_'+ str(b)+ '_C_'+str(c)+ filetype,out)
        #print(type(frontname))
        print('writing new img : '+frontname +'_B:_'+ str(b)+ '_C:_'+str(c)+ filetype)
    pass

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


# mynima input_dir output.json 
mynima(sys.argv)