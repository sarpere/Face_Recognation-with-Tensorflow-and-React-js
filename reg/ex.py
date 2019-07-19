from face_detection import MTCNNFaceDetection
import time

from face_recognization import FaceNet
from recognization import Recognization
import utils

from PIL import Image



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

