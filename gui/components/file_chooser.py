import tkinter
from tkinter import filedialog
from tkinter import ttk


class FileChooser(tkinter.Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.browse_button = ttk.Button(self, text='Procurar', command=self.browse)
        self.path_entry = ttk.Entry(self)

        self.browse_button.pack(side=tkinter.RIGHT)
        self.path_entry.pack(expand=True, side=tkinter.LEFT, fill=tkinter.X)

    def browse(self):
        filename = filedialog.askopenfilename()

        if not filename == '':
            self.path_entry.delete(0, len(self.path_entry.get()))
            self.path_entry.insert(0, filename)

    def get_path(self):
        return self.path_entry.get()
