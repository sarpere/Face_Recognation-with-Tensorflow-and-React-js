import os
from .utils import parse_params
import numpy as np

class Recognization:


    def __init__(self, detector, recognizer):
        self.detector = detector
        self.recognizer = recognizer


    def register(self, idx, dirname):
        print('idx: {}, name{}'.format(idx, dirname))
        results = []
        image_names = os.listdir(dirname)
        for image_name in image_names:
            result = self.detector(os.path.join(dirname, image_name))
            results.append(result)


        results = [np.concatenate(result, 0) for result in zip(*results)]
        self.recognizer.register(idx, results)

    def save(self,path):
        self.recognizer.save(path)
    
    def load(self,path):
        self.recognizer.load(path)

    def __call__(self, image):
        results = self.detector(image)
        return self.recognizer(results)


class FaceDetection:

    def __init__(self, params_path):
        self.params = parse_params(params_path)

    def __call__(self, image):
        raise NotImplementedError


class Recognizer:

    def __init__(self, params_path):
        self.params = parse_params(params_path)

    def register(self, idx, bboxs):
        raise NotImplementedError
    
    def save(self, path):
        raise NotImplementedError
    
    def load(self, path):
            raise NotImplementedError
        
    def __call__(self, bboxs):
        raise NotImplementedError

