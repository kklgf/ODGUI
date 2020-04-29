import os, sys
from PIL import Image

script_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(script_path, "webImport/")


filelist = []
dirs = os.listdir(path)


def resize():
    for item in dirs:
        #if os.path.isfile(path+item):
        print(path+item)
        filelist.append(path+item)
        im = Image.open(path+item)
        f, e = os.path.splitext(path+item)
        imResize = im.resize((200,100), Image.ANTIALIAS)
        imResize.save(f+'.png', 'png', quality=80)


resize()




# FIRST TRY ERROR in for
# for root, subdirs, files in os.walk(path):
#     for f in files:
#         if f.endswith('jpg'):
#             filelist.append(f)
#
# for filepath in filelist:
#     print(filepath)