import tensorflow as tf
import numpy as np
import pdb
import os
from . import facenet
from .recognization import Recognizer

def compare(memory, embeddings):
    return np.sqrt(np.sum(np.square(memory - np.expand_dims(embeddings, 1)), axis=-1))

class Embedding:


    def __init__(self, model_path):
        self.sess = tf.Session()

        with self.sess.as_default():
            facenet.load_model(model_path)

        graph = tf.get_default_graph()
        self.images = graph.get_tensor_by_name('input:0')
        self.embeddings = graph.get_tensor_by_name('embeddings:0')
        self.mode = graph.get_tensor_by_name('phase_train:0')


    def __call__(self, faces):
        faces = facenet.prewhiten_multiple(faces)
        feed_dict = {self.images: faces, self.mode: False}
        return self.sess.run(self.embeddings, feed_dict=feed_dict)



class Metric:


    def __init__(self, threshold, unknown):
        self.threshold = threshold
        self.unknown = unknown

        self.embeddings_memory = None
        self.idx_memory = None



    def register(self, idx, embeddings):
        idx = np.full(embeddings.shape[0], idx, dtype=np.int32)

        if self.idx_memory is not None:
            self.idx_memory = np.hstack((self.idx_memory, idx))
            self.embeddings_memory = np.vstack((self.embeddings_memory, embeddings))
            return

        self.idx_memory = idx
        self.embeddings_memory = embeddings

    def __call__(self, embeddings):
        n = embeddings.shape[0]

        similarity = compare(self.embeddings_memory, embeddings)

        idxs = np.argmin(similarity, axis=1)
        values = similarity[np.arange(n), idxs]

        idxs = self.idx_memory[idxs]
        mask = values > self.threshold

        idxs[mask] = self.unknown
        return idxs
    
    def save(self, path):
        np.savez(path, self.idx_memory, self.embeddings_memory)
    
    def load(self, path):
        saved = np.load(path)
        self.idx_memory , self.embeddings_memory = [saved[filecols] for filecols in saved.files] 


class FaceNet(Recognizer):

    def __init__(self, params_path):
        super(FaceNet, self).__init__(params_path)

        self.embedding = Embedding(self.params.facenet_model_pb)
        self.metric = Metric(self.params.threshold, self.params.unknown)


    def register(self,idx, results):
        faces, bboxs = results
        embeddings = self.embedding(faces)
        self.metric.register(idx, embeddings)

    def save(self, path):
        self.metric.save(path)

    def load(self, path):
        self.metric.load(path)

    def __call__(self, results):
        faces, bboxs = results
        embeddings = self.embedding(faces)
        idx = self.metric(embeddings)
        return bboxs, idx
