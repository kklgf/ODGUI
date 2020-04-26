from typing import Dict
from utils import *
import os


class Model:
    def __init__(self, config: Dict):
        self.config = config
        self.graph = None

    def load_inference_graph(self):
        path = os.path.join(os.getcwd(),
                            self.config['model']['path'],
                            self.config['model']['name'],
                            self.config['model']['file'])
        self.graph = get_frozen_graph(path)

    def create_session(self):
        input_names = ['image_tensor']

        # Create session and load graph
        self.tf_config = tf.ConfigProto()
        self.tf_config.gpu_options.allow_growth = True
        self.tf_sess = tf.Session(config=self.tf_config)
        tf.import_graph_def(self.graph, name='')

        self.tf_input = self.tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
        self.tf_scores = self.tf_sess.graph.get_tensor_by_name('detection_scores:0')
        self.tf_boxes = self.tf_sess.graph.get_tensor_by_name('detection_boxes:0')
        self.tf_classes = self.tf_sess.graph.get_tensor_by_name('detection_classes:0')
        self.tf_num_detections = self.tf_sess.graph.get_tensor_by_name('num_detections:0')

    def run_inference_one_image(self, image):
        scores, boxes, classes, num_detections = self.tf_sess.run(
            [self.tf_scores, self.tf_boxes, self.tf_classes, self.tf_num_detections],
            feed_dict={self.tf_input: image[None, ...]})
        return boxes[0], classes[0].astype(int), scores[0], int(num_detections[0])  # index by 0 to remove batch dimension
