from typing import Tuple, Any
from PIL.Image import Image
from utils import *
import os
import cv2


class Model:
    def __init__(self, config: Dict):
        self.config = config
        self.loader = self.config['loader']['loader']
        self.process = self.config['process']
        self.graph = None
        self._load_inference_graph()
        self._create_session()
        self.labels = self.loader.load_coco_labels()

    def _load_inference_graph(self) -> None:
        path = os.path.join(os.getcwd(),
                            self.config['model']['path'],
                            self.config['model']['name'],
                            self.config['model']['file'])
        self.graph = get_frozen_graph(path)

    def _create_session(self) -> None:
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

    def _run_inference_one_image(self, image: Image) -> Tuple[Any, Any, Any, int]:
        """
        @param image: image on which you want to detect objects
        @return: detections in format: boxes[], classes[], scores[], number of detections
        """
        scores, boxes, classes, num_detections = self.tf_sess.run(
            [self.tf_scores, self.tf_boxes, self.tf_classes, self.tf_num_detections],
            feed_dict={self.tf_input: image[None, ...]})
        # index by 0 to remove batch dimension
        return boxes[0], classes[0].astype(int), scores[0], int(num_detections[0])

    def predict_img(self, img_path: str):
        """
        @param img_path: path to image which you want predict
        """
        image = self.loader.get_image(img_path)
        detections = self._run_inference_one_image(image)
        # img_boxes = self.process.add_detections_on_image(detections, image, self.labels)
        self.process.add_detections_on_image(detections, image, self.labels)
        self.process.ss_image(image, path_leaf(img_path), self.config['show'], self.config['save'])

    def predict_video(self, video_path: str):
        """
        @param video_path: path to video to predict BB
        """
        metadata = video_metadata(video_path)
        cap = cv2.VideoCapture(video_path)
        if (cap.isOpened() == False):
            print("Unable to read camera feed")

        frame_width = metadata['width']
        frame_height = metadata['height']
        codec = cv2.VideoWriter_fourcc(*metadata['codec_tag_string'])
        fps_str = metadata['avg_frame_rate'].split('/')
        fps = int(int(fps_str[0]) / int(fps_str[1]))
        out = cv2.VideoWriter(self.config['loader']['save_path'], codec, fps, (frame_width, frame_height))

        while (True):
            ret, frame = cap.read()
            if ret == True:
                detections = self._run_inference_one_image(frame)
                self.process.add_detections_on_image(detections, frame, self.labels)
                out.write(cv2.UMat(frame))
            else:
               break
        cap.release()
        out.release()

    def predict_camera(self):
        """
        Open webcam stream, process it and show in real time in window
        """
        cap = cv2.VideoCapture(0)
        if (cap.isOpened() == False):
            print("Unable to read camera feed")

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        fps = 10
        out = cv2.VideoWriter(self.config['loader']['save_path'], codec, fps, (frame_width, frame_height))

        while (True):
            ret, frame = cap.read()
            if ret == True:
                detections = self._run_inference_one_image(frame)
                self.process.add_detections_on_image(detections, frame, self.labels)
                cv2.imshow('Camera detections', frame)
                out.write(cv2.UMat(frame))
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
