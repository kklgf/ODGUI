from Tensorflow.models.research.object_detection.utils import visualization_utils as vis_util
from typing import Tuple, Dict
import numpy as np
from PIL import Image


class Process:
    def __init__(self, config: Dict):
        self.config = config

    def add_detections_on_image(self, detections: Tuple, image: np.ndarray, category_index: Dict):
        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            *detections[0:3],
            category_index,
            min_score_thresh=self.config['threshold'],
            use_normalized_coordinates=True,
            line_thickness=2)
        return image

    def ss_image(self, image: np.ndarray, name: str, show=False, save=False):
        img = Image.fromarray(image, 'RGB')
        if save:
            img.save(self.config['loader']['save_path'] + "/boxes_" + name)
        if show:
            img.show()
