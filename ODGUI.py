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
from data.GUI.GUI import *

with open(r'config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
config['loader']['image_size'] = (config['loader']['default_size']['x'], config['loader']['default_size']['y'])

########
# GUI idzie tutaj i zbiera dane w config
# nadpisuje standardowe wartości wczytane z config.yml
########
gui = GUI(config)
photos_files_paths = gui.filespaths




loader = Loader(config)
config['loader']['loader'] = loader
process = Process(config)
config['process'] = process
model = Model(config)
config['model']['model'] = model

dest = Path(config['loader']['save_path'])
if not dest.exists():
    dest.mkdir()

source = Path(config['loader']['img_path'])

if source.is_dir():
    for img_path in tqdm(source.rglob('**/*')):
        if img_path.suffix in config['loader']['extentions']:
            detections = model.predict_img(str(img_path))
elif source.is_file():
    if source.suffix == '.avi':
        model.predict_video(str(source))
    elif source.suffix in config['loader']['extentions']:
        model.predict_img(str(source))

# image = loader._get_test_image()
# detections = model.run_inference_one_image(image)
#
# image = process.add_detections_on_image(detections, image, labels)
# process.ss_image(image, save=True)
