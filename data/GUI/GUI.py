# from PIL import Image
import os
import os.path
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()

canvas = tk.Canvas(root, width=900, height=500, bg="#263D42")
# canvas.create_line(root, relx=0.48)
canvas.pack()


import_frame = tk.Frame(root, bg="#182629")
import_frame.place(relwidth = 0.44, relheight = 0.86, relx=0.04, rely=0.07)

object_detection_frame = tk.Frame(root, bg="#182629")
object_detection_frame.place(relwidth=0.44, relheight= 0.86, relx = 0.52, rely = 0.07)

filelist = []

def choose_files():
    filename = filedialog.askopenfilename(initialdir = "/", title="Select one folder!")  # TODO filetypes
    filelist.append(filename)
    for filepath in filelist:
        label = tk.Label(import_frame, text=filepath, fg="#C4CBCC", bg="#2A3538")
        label.pack()


def analyze():
    raise NotImplementedError()


# def read_all_images():
#     my_string = "'" + str(filelist[0]) + "'"
#     imgs = []
#     path = my_string;
#     # valid_images = [".jpg", ".gif", ".png", ".tga"]
#     for f in os.listdir(path):
#         ext = os.path.splitext(f)[1]
#         imgs.append(Image.open(os.path.join(path, f)))



analyze_folder_butotn =  tk.Button(object_detection_frame, text = "Analyze!",
                           padx = 10, pady = 5, fg = "#C4CBCC", bg = "#263D42")
analyze_folder_butotn.pack()


choosefiles_button = \
    tk.Button(import_frame, text="Choose files", padx =10, pady = 5, fg="#C4CBCC", bg="#263D42", command = choose_files)
choosefiles_button.pack()

analyze_button = tk.Button(object_detection_frame, text = "Analyze!",
                           padx=10, pady=5, fg="#C4CBCC", bg="#263D42", command = analyze)
analyze_button.pack()

root.mainloop()

