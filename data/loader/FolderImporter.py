import os, sys
from PIL import Image
from tkinter import filedialog


class FolderImporter:
    def __init__(self, in_path="webImport"):
        self.path = in_path + '/'
        self.filelist = []
        self.dirs = os.listdir(in_path)

    # script_path = os.path.dirname(os.path.realpath(__file__))
    # path = os.path.join(script_path, "webImport/")

    def collect_images(self):
        for item in self.dirs:
            print(self.path + item)
            self.filelist.append(self.path + item)

    def resize(self):
        for item in self.dirs:
            # if os.path.isfile(path+item):
            print(self.path + item)
            self.filelist.append(self.path + item)
            im = Image.open(self.path + item)
            f, e = os.path.splitext(self.path + item)
            imResize = im.resize((200, 100), Image.ANTIALIAS)
            imResize.save(f + '.png', 'png', quality=80)
