from typing import Dict
from utils import *
import os
import cv2


class Model:
    def __init__(self, config: Dict):
        self.config = config
        self.loader = self.config['loader']['loader']
        self.process = self.config['process']
        self.graph = None
        self.load_inference_graph()
        self.create_session()
        self.labels = self.loader.load_coco_labels()

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

    def predict_img(self, img_path: str):
        image = self.loader.get_image(img_path)
        detections = self.run_inference_one_image(image)
        img_boxes = self.process.add_detections_on_image(detections, image, self.labels)
        self.process.ss_image(image, path_leaf(img_path), self.config['show'], self.config['save'])
        return img_boxes

    def predict_video(self, video_path: str, video_out = "./results/video.avi", show=False, save=False):
        metadata = video_metadata(video_path)
        cap = cv2.VideoCapture(video_path)
        if (cap.isOpened() == False):
            print("Unable to read camera feed")

        frame_width = metadata['width']
        frame_height = metadata['height']
        codec = cv2.VideoWriter_fourcc(*metadata['codec_tag_string'])
        fps_str = metadata['avg_frame_rate'].split('/')
        fps = int(int(fps_str[0]) / int(fps_str[1]))
        out = cv2.VideoWriter(video_out, codec, fps, (frame_width, frame_height))

        while (True):
            ret, frame = cap.read()
            if ret == True:
                detections = self.run_inference_one_image(frame)
                img_boxes = self.process.add_detections_on_image(detections, frame, self.labels)
                # img = Image.fromarray(img_boxes, 'RGB')
                out.write(cv2.UMat(img_boxes))
            else:
               break
        cap.release()
        out.release()
        return video_out

    def predict_camera(self, video_out = "./results/camera.avi"):
        cap = cv2.VideoCapture(0)
        if (cap.isOpened() == False):
            print("Unable to read camera feed")

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        fps = 10
        out = cv2.VideoWriter(video_out, codec, fps, (frame_width, frame_height))

        while (True):
            ret, frame = cap.read()
            if ret == True:
                detections = self.run_inference_one_image(frame)
                img_boxes = self.process.add_detections_on_image(detections, frame, self.labels)
                # img = Image.fromarray(img_boxes, 'RGB')
                cv2.imshow('Camera detections', img_boxes)
                out.write(cv2.UMat(img_boxes))
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        return video_out
