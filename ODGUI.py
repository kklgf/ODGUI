import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from copy import deepcopy
import cv2
from pathlib2 import Path
from tqdm import tqdm

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
import yaml

sys.path.append("..")
sys.path.append("./Tensorflow/models/research")
from Tensorflow.models.research.object_detection.utils import ops as utils_ops
from model.model_base import Model
from data.loader.loader_base import Loader
from data.preprocessing.preprocess_base import Process

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

########
# GUI idzie tutaj i zbiera dane w config
# nadpisuje standardowe wartości wczytane z config.yml
########


model = Model(config)
loader = Loader(config)
config['loader']['loader'] = loader
process = Process(config)

dest = Path(config['loader']['results'])
if not dest.exists():
    dest.mkdir()

source = Path(config['loader']['img_path'])
######################### WORK IN PROGRESS
# if source.is_dir():
#     for img_path in tqdm(source.rglob('**/*')):
#         if img_path.suffix in config['loader']['extentions']:
#             predict_img(str(img_path), model, args.output)
# elif source.is_file():
#     if source.suffix == '.avi':
#         predict_video(str(source), model, args.output)
#     elif source.suffix in VALID_FORMATS:
#         predict_img(str(source), model, args.output)
######################### WORK IN PROGRESS END

model.load_inference_graph()
model.create_session()

image = loader._get_test_image()
labels = loader._load_coco_labels()
detections = model.run_inference_one_image(image)

image = process.add_detections_on_image(detections, image, labels)
process.show_image(image, save=True)
