import tensorflow as tf
import numpy as np
import os

from scipy import misc
from . import detect_face


class FaceDetector:

    def __init__(self, minsize, threshold, factor, bbox_size, margin, model_dirname):


        self.minsize = minsize
        self.threshold = threshold
        self.factor = factor
        self.bbox_size = (bbox_size, bbox_size)
        self.margin = margin

        self._load_graph(model_dirname)

    def _load_graph(self, model_dirname):
        self.sess = tf.Session()
        with self.sess.as_default():
            self.model = detect_face.create_mtcnn(self.sess, model_dirname)


    def __call__(self, image):
        bboxs, _ = detect_face.detect_face(image, self.minsize, *self.model, self.threshold, self.factor)

        img_size = np.asarray(image.shape)[0:2]
        aligned_faces, aligned_bboxs = [], []
        for i in range(len(bboxs)):
            det = np.squeeze(bboxs[i, 0:4])
            bb  = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0]-self.margin/2, 0)
            bb[1] = np.maximum(det[1]-self.margin/2, 0)
            bb[2] = np.minimum(det[2]+self.margin/2, img_size[1])
            bb[3] = np.minimum(det[3]+self.margin/2, img_size[0])
            cropped = image[bb[1]:bb[3],bb[0]:bb[2],:]
            aligned = misc.imresize(cropped, self.bbox_size, interp='bilinear')
            aligned_faces.append(aligned)
            aligned_bboxs.append(bb)
        return aligned_faces, aligned_bboxs
