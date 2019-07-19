from .mtcnn_face_detector import detector
from .recognization import FaceDetection

from .utils import imread
import numpy as np

import os


class MTCNNFaceDetection(FaceDetection):

    def __init__(self, params_path):
        super(MTCNNFaceDetection, self).__init__(params_path)

        params = self.params
        self.detector = detector.FaceDetector(params.minsize, params.threshold, params.factor,
                params.bbox_size, params.margin, params.model_dirname)

    def __call__(self, image):
        image = imread(image)
        aligned_faces, bboxs = self.detector(image)
        return np.asarray(aligned_faces), np.asarray(bboxs)
