import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from copy import deepcopy
import cv2

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt

sys.path.append("..")
sys.path.append("./Tensorflow/models/research")
from Tensorflow.models.research.object_detection.utils import ops as utils_ops

from model.model_base import Model
from data.loader.loader_base import Loader
from data.preprocessing.preprocess_base import Process

config = {
    'MODEL_NAME': 'ssd_mobilenet_v1_coco_2018_01_28',
    # 'MODEL_FILE': MODEL_NAME + '.tar.gz',
    'LOKAL_FROZEN': 'frozen_models/',
    'DOWNLOAD_BASE': 'http://dmnbnm,≥≤nbvn mownload.tensorflow.org/models/object_detection/',
    # 'PATH_TO_CKPT': MODEL_NAME + '/frozen_inference_graph.pb',
    'PATH_TO_LABELS': os.path.join('Tensorflow/models/research/object_detection/data/', 'mscoco_label_map.pbtxt'),
    'NUM_CLASSES': 90,
    'IMAGE_SIZE': (1200, 900),
    'IMAGE_PATH': os.path.join(os.getcwd(), "test_images", "image3.jpg")
}

model = Model(config)
loader = Loader(config)
process = Process(config)

model.load_inference_graph()
model.create_session()

image = loader._get_test_image()
labels = loader._load_coco_labels()
detections = model.run_inference_one_image(image)

image = process.add_detections_on_image(detections, image, labels)
process.show_image(image, save=True)
