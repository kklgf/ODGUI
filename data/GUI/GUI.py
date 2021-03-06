import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from data.loader.FolderImporter import *
from data.loader.WebPageImporter import *
from data.loader.loader_base import *
from functools import partial
from typing import Dict
from pathlib2 import Path
from tqdm import tqdm
from data.preprocessing.preprocess_base import Process
from model.model_base import Model
from data.loader.loader_base import Loader


class GUI:
    def __init__(self, config: Dict):
        self.config = config
        self.folderpath = []
        self.outpufolder = 'results'
        self.root = tk.Tk()
        self.filespaths_labels = []
        # canvas
        self.canvas = tk.Canvas(self.root, width=900, height=500, bg="#263D42")
        self.canvas.pack(fill="both", expand=True)

        # Frames
        # Import Frames
        self.import_frame = tk.Frame(self.root, bg="#182629")
        self.import_frame.place(relwidth=0.44, relheight=0.66, relx=0.04, rely=0.29)
        self.choose_frame = tk.Frame(self.root, bg="#182629")
        self.choose_frame.place(relwidth=0.44, relheight=0.20, relx=0.04, rely=0.07)
        self.radio_btn_frame = tk.Frame(self.choose_frame, bg="#182629")
        self.radio_btn_frame.place(relwidth=0.44, relheight=0.50, relx=0.5, rely=0.5)
        # Object detection frames
        self.object_detection_frame = tk.Frame(self.root, bg="#182629")
        self.object_detection_frame.place(relwidth=0.44, relheight=0.86, relx=0.52, rely=0.07)
        # treshold frame
        self.threshold_frame = tk.Frame(self.root, bg="#182629")
        self.threshold_frame.place(relwidth=0.30, relheight=0.2, relx=0.58, rely=0.5)
        # Input and boxes
        # threshold inputbox
        self.threshold_entry_label = tk.Label(self.threshold_frame, text="Set threshold", bg="#263D42", fg="#C4CBCC")
        self.threshold_entry_label.pack()
        self.threshold_entry = tk.Entry(self.threshold_frame)
        self.threshold_entry.pack()
        # set output
        outpufolder_label = tk.Label(self.threshold_frame,
                                     text="Current output folder:", bg="#263D42", fg="#C4CBCC")
        outpufolder_label.pack()
        self.current_output_folder_label = tk.Label(self.threshold_frame,
                                                    text="./results", bg="#263D42", fg="#C4CBCC")
        self.current_output_folder_label.pack()
        set_output_folder_button = tk.Button(self.threshold_frame, text="Choose result folder!",
                                             padx=10, pady=5, fg="#C4CBCC", bg="#263D42",
                                             command=self._set_output_folder)
        set_output_folder_button.pack()

        # combobox
        self.choose_import_label = tk.Label(self.choose_frame, text="Choose import method", bg="#263D42", fg="#C4CBCC")
        self.choose_import_label.pack()
        self.choose_import = ttk.Combobox(self.choose_frame, values=["Folder", "Camera", "Webpage", "Video"])
        self.choose_import.pack()
        self.choose_import.bind("<<ComboboxSelected>>", self._callbackFunc)
        # Radiobutton .jpg/.jpeg
        self.radio_btn_var = tk.StringVar(value='.jpg')

        # Buttons
        analyze_button = tk.Button(self.object_detection_frame, text="Analyze!",
                                   padx=10, pady=5, fg="#C4CBCC", bg="#263D42", command=self._analyze)
        analyze_button.pack()
        # Radiobutton neural network
        self.label_choose_network = tk.Label(self.object_detection_frame,
                                             text="Choose neural network", bg="#263D42", fg="#C4CBCC")
        self.label_choose_network.pack()
        self.radio_btn_network_var = tk.StringVar(value='ssd_mobilenet_v1_coco_2018_01_28')
        self.radio_btn_network_1 = tk.Radiobutton(self.object_detection_frame, text='MobileNet v1',
                                                  variable=self.radio_btn_network_var,
                                                  value='ssd_mobilenet_v1_coco_2018_01_28',
                                                  fg="#C4CBCC", bg="#263D42")
        self.radio_btn_network_1.pack()
        self.radio_btn_network_2 = tk.Radiobutton(self.object_detection_frame, text='MobileNet v2',
                                                  variable=self.radio_btn_network_var,
                                                  value='ssdlite_mobilenet_v2_coco_2018_05_09',
                                                  fg="#C4CBCC", bg="#263D42")
        self.radio_btn_network_2.pack()
        self.radio_btn_network_3 = tk.Radiobutton(self.object_detection_frame, text='MobileNet v3 (mobile)',
                                                  variable=self.radio_btn_network_var,
                                                  value='ssd_mobilenet_v3_small_coco_2020_01_14',
                                                  fg="#C4CBCC", bg="#263D42")
        self.radio_btn_network_3.pack()
        self.radio_btn_network_4 = tk.Radiobutton(self.object_detection_frame, text='resnet50 v1',
                                                  variable=self.radio_btn_network_var,
                                                  value='ssd_resnet50_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03',
                                                  fg="#C4CBCC", bg="#263D42")
        self.radio_btn_network_4.pack()

        # starter
        self.root.mainloop()

    def _analyze(self) -> None:
        """
        Sets config for neural network
        :return: None
        """
        self.config['loader']['save_path'] = self.outpufolder
        if self.threshold_entry.get():
            if float(self.threshold_entry.get()) > 1.0 or float(self.threshold_entry.get()) < 0.0:
                raise ValueError('Treshold value should be in range 0.0 and 1.0')
            self.config['threshold'] = float(self.threshold_entry.get())
        self.config['loader']['img_path'] = self.folderpath[0]
        self.config['loader']['extentions'] = self.radio_btn_var.get()
        self.config['model']['name'] = self.radio_btn_network_var.get()
        loader = Loader(self.config)
        self.config['loader']['loader'] = loader
        process = Process(self.config)
        self.config['process'] = process
        model = Model(self.config)
        self.config['model']['model'] = model

        if self.config['loader']['img_path'] == 0:
            model.predict_camera()
        else:
            dest = Path(self.config['loader']['save_path'])
            if not dest.exists():
                dest.mkdir()

            source = Path(self.config['loader']['img_path'])

            if source.is_dir():
                for img_path in tqdm(source.rglob('**/*')):
                    if img_path.suffix in self.config['loader']['extentions']:
                        model.predict_img(str(img_path))
            elif source.is_file():
                if source.suffix == '.avi':
                    model.predict_video(str(source))
                elif source.suffix in self.config['loader']['extentions']:
                    model.predict_img(str(source))

    def _callbackFunc(self, event: tk.Event) -> None:
        """
        callback for import method combobox
        :param event:
        :return:
        """
        el_number = self.choose_import.current()
        if el_number == 0:
            self._print_folder_import()
        elif el_number == 1:
            self._print_camera_import()
        elif el_number == 2:
            self._print_webpage_import()
        elif el_number == 3:
            self._print_video_import()

    def _choose_folders(self) -> None:
        """
        Shows popup window to choose folder to import
        and sets it as an active one
        :return:
        """
        self.folderpath = []
        foldername = filedialog.askdirectory(initialdir="/home/", title="Select one folder!")
        self.folderpath.append(foldername)
        for label in self.filespaths_labels:
            label.destroy()
        for filepath in self.folderpath:
            label = tk.Label(self.import_frame, text=filepath, fg="#C4CBCC", bg="#2A3538")
            label.pack()
            self.filespaths_labels.append(label)

    def _print_folder_import(self) -> None:
        """
        Prints folder import GUI
        """
        self._destroy_input_children()
        self._print_image_format_radiobutton(False)
        choosefiles_button = \
            tk.Button(self.import_frame, text="Choose folder", padx=10, pady=5, fg="#C4CBCC", bg="#263D42",
                      command=self._choose_folders)
        choosefiles_button.pack()

    def _update_folder_import_files(self) -> None:
        folder_importer = FolderImporter(in_path=self.folderpath[0])
        folder_importer.collect_images()

    def _print_camera_import(self) -> None:
        self.folderpath = [0]
        self._destroy_input_children()

    def _print_webpage_import(self) -> None:
        self._destroy_input_children()
        self._print_image_format_radiobutton(False)
        tk.Label(self.import_frame, text="Provide  (http://)", bg="#263D42", fg="#C4CBCC").pack()
        web_adress = tk.Entry(self.import_frame)
        web_adress.pack()
        webpage_button_action = partial(self._run_webpage_analyze, web_adress)
        webpage_button = \
            tk.Button(self.import_frame, text="Analyze webpage", padx=10, pady=5, fg="#C4CBCC", bg="#263D42",
                      command=webpage_button_action)
        webpage_button.pack()

    def _run_webpage_analyze(self, web_adress: tk.Entry) -> None:
        self.folderpath = []
        self.folderpath.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'loader/webImport'))
        web_pi = WebPageImporter(self)
        try:
            web_pi.read_website(web_adress.get())
        finally:
            self._analyze()

    def _set_output_folder(self) -> None:
        foldername = filedialog.askdirectory(initialdir="/home/", title="Select one folder!")
        self.outpufolder = foldername
        self.current_output_folder_label.config(text=foldername)

    def _print_image_format_radiobutton(self, video: bool) -> None:
        """
        :param video: if true prints video formats
        :return: None
        """
        for widget in self.radio_btn_frame.winfo_children():
            widget.destroy()
        radio_btn_jpg = tk.Radiobutton(self.radio_btn_frame, text='.jpg',
                                       variable=self.radio_btn_var, value='.jpg', fg="#C4CBCC", bg="#263D42")
        radio_btn_jpg.pack()
        radio_btn_jpeg = tk.Radiobutton(self.radio_btn_frame, text='.jpeg', variable=self.radio_btn_var,
                                        value='.jpeg', fg="#C4CBCC", bg="#263D42")
        radio_btn_jpeg.pack()
        if video:
            radio_btn_avi = tk.Radiobutton(self.radio_btn_frame, text='.avi', variable=self.radio_btn_var,
                                           value='.avi', fg="#C4CBCC", bg="#263D42")
            radio_btn_avi.pack()

    def _destroy_input_children(self) -> None:
        for widget in self.radio_btn_frame.winfo_children():
            widget.destroy()
        for widget in self.import_frame.winfo_children():
            widget.destroy()

    def _print_video_import(self) -> None:
        self._destroy_input_children()
        radio_btn_avi = tk.Radiobutton(self.radio_btn_frame, text='.avi', variable=self.radio_btn_var,
                                       value='.avi', fg="#C4CBCC", bg="#263D42")
        radio_btn_avi.pack()
        choosefiles_button = \
            tk.Button(self.import_frame, text="Choose video", padx=10, pady=5, fg="#C4CBCC", bg="#263D42",
                      command=self._choose_video)
        choosefiles_button.pack()

    def _choose_video(self) -> None:
        """
        shows window to choose video to import
        :return:
        """
        self.folderpath = []
        foldername = filedialog.askopenfilename(initialdir="/home/mateusz", title="Select video",
                                                filetypes=[("Movies", '.avi')])
        self.folderpath.append(foldername)
        for label in self.filespaths_labels:
            label.destroy()
        for filepath in self.folderpath:
            label = tk.Label(self.import_frame, text=filepath, fg="#C4CBCC", bg="#2A3538")
            label.pack()
            self.filespaths_labels.append(label)
