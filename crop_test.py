from PIL import Image
from nima.inference.inference_model import InferenceModel
import sys

imfile, box = sys.argv[1], sys.argv[2]
box = eval(box)
print(box)

im = Image.open(imfile)
cim = im.crop(box)

model_pth = './tmp0911/emd_loss_epoch_7_train_0.1333131288342482_0.12994747442647445.pth'  
model = InferenceModel(path_to_model=model_pth)

ims = float(model.predict_from_pil_image(cim)['mean_score'])
print(ims)
