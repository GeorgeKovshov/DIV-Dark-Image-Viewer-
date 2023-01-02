import sys
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import time
import os

root = Tk()
root.title("Images")

image = Image.open("2016_Grand_Rapids_tornado_outbreak_radar_loop.gif")
#image = Image.open("KOXOBiN.gif")
#image = Image.open("blow.gif")
#image = Image.open("giphy (1).gif")
image_start = image

canvas = tkinter.Canvas(root, height=image.height, width=image.width)
canvas.grid(row=0, column=0, columnspan=3)

image_for_label = ImageTk.PhotoImage(image)
print(image)
frame_count = image.n_frames

#images = [PhotoImage(file='blow.gif', format = 'gif -index %i' %i) for i in range(image.n_frames)]

label = Label(root, image=image_for_label)
ind = 0
ind2 = 0
print(image.n_frames)
while ind <= frame_count:
    time.sleep(0.06)
    label.grid_forget()
    print(ind)
    image_for_label = ImageTk.PhotoImage(image)
    label = Label(root, image=image_for_label)
    label.grid(row=0, column=0)


    if ind == frame_count:
        image.seek(0)
        ind = 0
    else:
        image.seek(ind)
        ind += 1

    root.update()



"""
while ind < image.n_frames:
    time.sleep(0.06)
    label = Label(root, image=images[ind])
    #label.grid(row=0, column=0)
    label.grid(row=0, column=0)
    ind += 1
    if ind == image.n_frames:
        ind = 0
        #ind2 += 1
    root.update()
"""

root.mainloop()