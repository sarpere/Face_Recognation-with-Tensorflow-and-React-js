from PIL import Image
import numpy as np 
import io
import os

def load_image(image):
    f = io.BytesIO(image)
    f.seek(0)
    return np.expand_dims(np.array(Image.open(f).convert(mode='RGB')), axis=0)
def save_image(path,imagePath,image):
   f = io.BytesIO(image)
   f.seek(0)
   image = Image.open(f).convert(mode='RGB')
   
   if not os.path.isdir(path):
      os.mkdir(path)
   image.save(path+"/"+imagePath+".jpeg","JPEG")