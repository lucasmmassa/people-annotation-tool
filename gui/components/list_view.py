import tkinter
from tkinter import filedialog


def add_file():
    list_box.insert(tkinter.END, filedialog.askopenfilename(title='Selecionar arquivo'))


def show_files():
    for file in list_box.get(0, tkinter.END):
        print(file)


window = tkinter.Tk()

list_box: tkinter.Listbox = tkinter.Listbox(window)
list_box.pack(side='top', fill=tkinter.X, expand=True)

add_file_button = tkinter.Button(window, text='Adicionar arquivo...', command=add_file)
add_file_button.pack(side='bottom')

show_files_button = tkinter.Button(window, text='Mostrar arquivos', command=show_files)
show_files_button.pack(side='bottom')

window.mainloop()
