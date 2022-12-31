import sys
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import time
import os

root = Tk()
root.title("Images")

image = Image.open("KOXOBiN.gif.gif")
image_for_label = ImageTk.PhotoImage(image)


images = [PhotoImage(file='KOXOBiN.gif.gif', format = 'gif -index %i' %i) for i in range(image.n_frames)]

#label = Label(root, image=images[0])
ind = 0
while ind < image.n_frames:
    time.sleep(0.06)
    label = Label(root, image=images[ind])
    #label.grid(row=0, column=0)
    label.grid(row=0, column=0)
    ind += 1
    if ind == image.n_frames:
        ind = 0
    root.update()


root.mainloop()