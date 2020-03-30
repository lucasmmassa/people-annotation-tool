import csv
from tkinter import *
from tkinter import filedialog
import glob

import cv2
import gui

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX

class FrameLabeler:
    def __init__(self):
        self.root = Tk()
        self.display = gui.Display(self.root, 'Annotation tool')
        self.root.focus_set()
        self.source_directory_path = filedialog.askdirectory()
        self.csv_file_path = filedialog.asksaveasfilename()
        self.csv_data = [['filename', 'counting']]
        self.filename_list = self.create_files_list()
        self.label = ['0' for i in range(len(self.filename_list))]
        self.index = 0
        self.counter = 0
        self.display.grid(row=0, column=0)
        self.exit = False
        self.framesList = Listbox(self.root)

        for fname in self.filename_list:
            self.framesList.insert(END, fname)

        self.framesList.grid(row=0, column=1, rowspan=2, sticky=NSEW)

        buttonFrame = Frame(self.root)
        Button(buttonFrame, text='Proximo', command=self.next).pack(side=LEFT)
        Button(buttonFrame, text='Anterior', command=self.previous).pack(side=LEFT)
        Button(buttonFrame, text='Incrementar', command=self.increment_counter).pack(side=LEFT)
        Button(buttonFrame, text='Decrementar', command=self.decrement_counter).pack(side=LEFT)
        Button(buttonFrame, text='Salvar', command=self.finish).pack(side=LEFT)
        buttonFrame.grid(row=1, column=0, columnspan=2)

    def increment_index(self):
        self.index += 1

    def finish(self):
        self.exit = True

    def decrement_index(self):
        self.index -= 1

    def increment_counter(self):
        self.counter += 1

    def decrement_counter(self):
        self.counter -= 1

    def update_label(self):
        self.label[self.index] = str(self.counter)

    def create_files_list(self):
        pngs = []
        '''
        for root, dirs, files in sorted(os.walk(self.source_directory_path)):
            for file in files:
                if file.endswith('.png'):
                    pngs.append(file)
        pngs.sort(key=lambda x: (x.split('/')[-1][:-4]))
        '''
        for file in sorted(glob.glob(self.source_directory_path + '/*.png')):
            pngs.append(file)
        return pngs

    def save_csv_dataframe(self):
        with open(self.csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.csv_data)
        csv_file.close()

    def show_frame(self, frame, index, count):
        text = 'Count: ' + str(count) + ' (' + str(index) + ')'
        frame_with_text = cv2.resize(frame.copy(), (800, 450))
        cv2.putText(frame_with_text, text, (10, 350), FONT, 1, BLACK, 3, cv2.LINE_AA)
        cv2.putText(frame_with_text, text, (10, 350), FONT, 1, WHITE, 2, cv2.LINE_AA)

        self.display.update(image=frame_with_text)

    def previous(self):
        # print('a')
        if self.index != 0:
            self.decrement_index()
            self.csv_data.pop()

    def next(self):
        if self.index != (len(self.filename_list) - 1):
            self.update_label()
            self.csv_data.append([self.filename_list[self.index], self.label[self.index]])
            self.increment_index()

    def process_frames(self):
        current_frame = cv2.imread(self.filename_list[self.index])
        self.show_frame(current_frame, self.index, self.label[self.index])
        self.update_label()
        # print('a')

        if not self.exit:
            self.root.after(1, self.process_frames)


def keyEvent(event):
    print(event)
    annotationTool.keyEvent(event.char)


annotationTool = FrameLabeler()
annotationTool.root.bind('<Button-1>', lambda event: annotationTool.root.focus_set())
annotationTool.root.bind('<Key>', keyEvent)
annotationTool.process_frames()
annotationTool.root.mainloop()
annotationTool.save_csv_dataframe()
