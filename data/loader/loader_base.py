from typing import Dict
import cv2
from Tensorflow.models.research.object_detection.utils import label_map_util


class Loader:
    def __init__(self, config: Dict):
        self.config = config

    def get_image(self, source):
        image = cv2.imread(source)
        image = cv2.resize(image, self.config['loader']['image_size'])
        # cv2 get images as BGR, models assumes RGB
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return img_rgb

    # def _get_test_image(self):
    #     image = cv2.imread(self.config['loader']['img_path'])
    #     image = cv2.resize(image, self.config['loader']['image_size'])
    #     # cv2 get images as BGR, models assumes RGB
    #     img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     return img_rgb

    def load_coco_labels(self):
        label_map = label_map_util.load_labelmap(self.config['loader']['labels'])
        categories = label_map_util.convert_label_map_to_categories(
            label_map, max_num_classes=self.config['loader']['classes'], use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        return category_index
