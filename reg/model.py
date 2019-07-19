from .face_detection import MTCNNFaceDetection
from .face_recognization import FaceNet
from .recognization import Recognization
import numpy as np
import os


def build_model(detection_params_path, recognation_param_path):
    detector = MTCNNFaceDetection(detection_params_path)
    recognizer = FaceNet(recognation_param_path)
    return Recognization(detector,recognizer)


def init_model(model, people, base_dir, embedings_path):
    print(people)
    exists = os.path.exists(embedings_path)
    if exists:
        model.load(embedings_path) 
        with np.load(embedings_path) as data:
            for i in range(0,len(people)):
                personidx ,personName = people[i]
                idxs = data['arr_0']
                newPerson=[]
                if personidx not in idxs: 
                    newPerson.append((personidx,personName))
            if newPerson:
                for idx, dirname in newPerson:
                    model.register(idx, os.path.join(base_dir, dirname))
                    model.save(embedings_path)
        return

    for idx, dirname in people:
        model.register(idx, os.path.join(base_dir, dirname))
    model.save(embedings_path)