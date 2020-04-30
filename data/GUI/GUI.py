import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from FolderImporter import *
from webPageImporter import *
from CameraImport import *

class GUI:
    def __init__(self):
        self.folderpath = []
        self.filespaths = []
        self.root = tk.Tk()
        # canvas
        self.canvas = tk.Canvas(self.root, width=900, height=500, bg="#263D42")
        self.canvas.pack()
        #Frames
        self.import_frame = tk.Frame(self.root, bg="#182629")
        self.import_frame.place(relwidth=0.44, relheight=0.66, relx=0.04, rely=0.29)
        self.choose_frame = tk.Frame(self.root, bg="#182629")
        self.choose_frame.place(relwidth=0.44, relheight=0.20, relx=0.04, rely=0.07)
        self.object_detection_frame = tk.Frame(self.root, bg="#182629")
        self.object_detection_frame.place(relwidth=0.44, relheight=0.86, relx=0.52, rely=0.07)
        # combobox
        self.choose_import_label = tk.Label(self.choose_frame, text="Choose import method",  bg="#263D42", fg="#C4CBCC")
        self.choose_import_label.pack()
        self.choose_import = ttk.Combobox(self.choose_frame, values = ["Folder", "Camera", "Webpage"])
        self.choose_import.pack()
        self.choose_import.bind("<<ComboboxSelected>>", self.callbackFunc)
        #Buttons

        analyze_button = tk.Button(self.object_detection_frame, text="Analyze!",
                                   padx=10, pady=5, fg="#C4CBCC", bg="#263D42", command=self.analyze)
        analyze_button.pack()
        #starter
        self.root.mainloop()

    def choose_folders(self):
        foldername = filedialog.askdirectory(initialdir="/home/", title="Select one folder!")  # TODO filetypes
        self.folderpath.append(foldername)
        for filepath in self.folderpath:
            label = tk.Label(self.import_frame, text=filepath, fg="#C4CBCC", bg="#2A3538")
            label.pack()

    def analyze(self):
        folder_importer = FolderImporter(in_path=self.folderpath[0])
        folder_importer.collect_images()
        self.filespaths = folder_importer.filelist

    def callbackFunc(self, event):
        el_number = self.choose_import.current()
        if el_number == 0:
            self.print_folder_import()
        elif el_number == 1:
            self.print_camera_import()
        elif el_number == 2:
            self.print_webpage_import()

    def print_folder_import(self):
        for widget in self.import_frame.winfo_children():
            widget.destroy()
        choosefiles_button = \
            tk.Button(self.import_frame, text="Choose files", padx=10, pady=5, fg="#C4CBCC", bg="#263D42",
                      command=self.choose_folders)
        choosefiles_button.pack()

    def print_camera_import(self):
        for widget in self.import_frame.winfo_children():
            widget.destroy()
        camera_importer = CameraImporter()
        camera_button = tk.Button(self.import_frame, text="Import images from camera",
                                   padx=10, pady=5, fg="#C4CBCC", bg="#263D42", command=camera_importer.cature)
        camera_button.pack()

    def print_webpage_import(self):
        for widget in self.import_frame.winfo_children():
            widget.destroy()
        tk.Label(self.import_frame, text="Provide webpage", bg="#263D42", fg="#C4CBCC").pack()
        web_adress = tk.Entry(self.import_frame)
        web_adress.pack()
        web_pi = webPageImporter(web_adress, self)
        webpage_button = \
            tk.Button(self.import_frame, text="Analyze webpage", padx=10, pady=5, fg="#C4CBCC", bg="#263D42",
                      command=web_pi.read_website) #todo
        webpage_button.pack()


    def update_web_page_files(self):
        folder_importer = FolderImporter("webImport")
        folder_importer.collect_images()
        self.filespaths = folder_importer.filelist


    # def read_all_images():
    #     my_string = "'" + str(filelist[0]) + "'"
    #     imgs = []
    #     path = my_string;
    #     # valid_images = [".jpg", ".gif", ".png", ".tga"]
    #     for f in os.listdir(path):
    #         ext = os.path.splitext(f)[1]
    #         imgs.append(Image.open(os.path.join(path, f)))



