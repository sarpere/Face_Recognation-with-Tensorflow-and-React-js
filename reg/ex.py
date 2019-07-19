from face_detection import MTCNNFaceDetection
import time

from face_recognization import FaceNet
from recognization import Recognization
import utils

from PIL import Image


# idx_to_name = {  
#                  3: 'Sarper Ekinci',
#                  2: 'hediye',
#                  1: 'Kaan',
#                 -1: 'Unknown',
# }
# r.register(2, 'database/Hediye_Parlar')
# r.register(3, 'database/sarper_ekinci')

# image_path = img
# bboxs, idx = r(image_path)
# names = [idx_to_name[i] for i in idx]
# image = Image.open(image_path)
# utils.draw(image, bboxs, names)
# image.save('deneme.jpg')
def setInitials(data,img):
    detection_params_path = 'detection_params.json'
    recognization_params_path = 'recognization_params.json'


    detection = MTCNNFaceDetection(detection_params_path)
    recognizer = FaceNet(recognization_params_path)




    r = Recognization(detection, recognizer)
    for d in data:
        r.register(d['id'], 'database/'+d['FileId'])
    image = img
    result = r(image)
    return result

