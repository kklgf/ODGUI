from typing import Dict
import cv2
from Tensorflow.models.research.object_detection.utils import label_map_util

class Loader:
    def __init__(self, config: Dict):
        self.config = config

    def _get_test_image(self):
        image = cv2.imread(self.config['IMAGE_PATH'])
        image = cv2.resize(image, self.config['IMAGE_SIZE'])
        # cv2 get images as BGR, models assumes RGB
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return img_rgb

    def _load_coco_labels(self):
        label_map = label_map_util.load_labelmap(self.config['PATH_TO_LABELS'])
        categories = label_map_util.convert_label_map_to_categories(
            label_map, max_num_classes=self.config['NUM_CLASSES'], use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        return category_index