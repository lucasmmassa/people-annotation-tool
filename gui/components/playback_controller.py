import datetime
import tkinter
from tkinter import ttk


class PlaybackController(tkinter.Frame):

    def __init__(self, master, capture, **kw):
        super(tkinter.Frame, self).__init__(master, 'text', **kw)

        self.capture = capture
        self.slider_grabbed = False

        self.create_widgets()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.slider.grid(row=0, column=0, columnspan=3, sticky='we')

        self.current_time.grid(row=1, column=0, sticky='w')
        self.play_button.grid(row=1, column=1)
        self.duration.grid(row=1, column=2, sticky='e')

    def create_widgets(self):
        self.slider = tkinter.Scale(self, orient='horizontal', from_=0, to=self.capture.frame_count)

        self.slider.bind('<ButtonPress-1>', lambda val: self.on_slider_grabbed(val))
        self.slider.bind('<ButtonRelease-1>', lambda val: self.on_slider_released(val))
        self.slider['showvalue'] = 0

        self.play_button = ttk.Button(self, text='|>', command=lambda: self.capture.play())
        self.current_time = ttk.Label(self, text=datetime.timedelta(seconds=self.capture.get_current_seconds()))
        self.duration = ttk.Label(self, text=datetime.timedelta(seconds=self.capture.get_total_seconds()))

    def update(self):
        if not self.slider_grabbed:
            self.slider.set(self.capture.get_position())
        self.current_time['text'] = datetime.timedelta(seconds=self.capture.get_current_seconds())

    def on_slider_grabbed(self, event):
        print('Grabbed')

        self.slider_grabbed = True

    def on_slider_released(self, event):
        print('Released')

        self.event_generate('<<Slider Changed>>')

        self.slider_grabbed = False
        self.capture.set_position(self.slider.get())

