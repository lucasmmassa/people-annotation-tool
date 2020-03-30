import tkinter
from tkinter import filedialog
from tkinter import ttk

import cv2
import numpy
from PIL import Image, ImageTk


class Display(ttk.Frame):

    def __init__(self, master, label='Display', width=640, height=480, first_frame=None, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self.video_writer = None
        self.recording = False

        self.create_widgets(label, width, height)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label.grid(row=0, column=0, sticky='w')
        self.canvas.grid(row=1, column=0, sticky='nsew', columnspan=3)
        self.buttons.grid(row=0, column=1, sticky='e')
        self.snapshot_button.pack(side='left')
        self.record_button.pack(side='left')

        if first_frame is not None:
            self.update(image=first_frame)
        else:
            self.update(image=numpy.zeros((width, height, 3)).astype(numpy.uint8))

    def create_widgets(self, label, width, height):
        self.label = ttk.Label(self, text=label, font=('Arial', 12, 'bold'))
        self.canvas = tkinter.Canvas(self, width=width, height=height)

        self.buttons = ttk.Frame(self)
        self.snapshot_button = ttk.Button(self.buttons, text='Capturar imagem', command=self.snapshot)
        self.record_button = ttk.Button(self.buttons, text='Gravar vídeo', command=self.record)

    def update(self, flag=cv2.COLOR_BGR2RGB, **kwargs):
        if 'image' in kwargs:
            image = kwargs['image']
            image = cv2.resize(image, (self.winfo_width(), self.winfo_height()))

            if 'raw' in kwargs:
                self.image = Image.fromarray(image)
            else:
                self.image = Image.fromarray(cv2.cvtColor(image, flag))

            self.photo_image = ImageTk.PhotoImage(master=self.canvas, image=self.image)
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tkinter.NW)
            if self.recording:
                self.video_writer.write(image)

    def snapshot(self):
        filename = filedialog.asksaveasfilename(title='Salvar captura', defaultextension='.png')
        if not filename == '':
            self.image.save(filename, format='png')

    def record(self):
        filename = filedialog.asksaveasfilename()
        if not filename == '':
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(filename + '.avi', fourcc, 20, (self.winfo_width(), self.winfo_height()))
            self.recording = not self.recording

        if not self.recording:
            self.video_writer.release()

    def set_label(self, label):
        self.label['text'] = label
