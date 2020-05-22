import sys
import yaml

if __name__ == "__main__":
    sys.path.append("..")
    sys.path.append("./Tensorflow/models/research")
    from data.GUI.GUI import *

    with open(r'config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    config['loader']['image_size'] = (config['loader']['default_size']['x'], config['loader']['default_size']['y'])

    ########
    # GUI idzie tutaj i zbiera dane w config
    # nadpisuje standardowe wartości wczytane z config.yml
    ########
    gui = GUI(config)

# photos_files_paths = gui.filespaths
#
# loader = Loader(config)
# config['loader']['loader'] = loader
# process = Process(config)
# config['process'] = process
# model = Model(config)
# config['model']['model'] = model
#
# dest = Path(config['loader']['save_path'])
# if not dest.exists():
#     dest.mkdir()
#
# source = Path(config['loader']['img_path'])
#
# if source.is_dir():
#     for img_path in tqdm(source.rglob('**/*')):
#         if img_path.suffix in config['loader']['extentions']:
#             detections = model.predict_img(str(img_path))
# elif source.is_file():
#     if source.suffix == '.avi':
#         model.predict_video(str(source))
#     elif source.suffix in config['loader']['extentions']:
#         model.predict_img(str(source))