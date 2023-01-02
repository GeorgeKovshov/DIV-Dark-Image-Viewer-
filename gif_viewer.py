import sys
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import time
import os

""" developing the gif viewer here, later transferred to the main app"""

root = Tk()
root.title("Images")


stop_e = 0

def stop():
    """stops the gif"""
    global stop_e
    stop_e = 1

zoom_value = 1

def zoom():
    """resizes the image"""
    global zoom_value
    global gif_width
    global gif_height
    zoom_value = 2
    gif_width *= zoom_value
    gif_height *= zoom_value
    root.update()

button_stop = Button(root, text="stop", command=stop)
button_stop.grid(row=1, column=0)
button_zoom = Button(root, text="zoom", command=zoom)
button_zoom.grid(row=1, column=2)
# opening the gif

#image = Image.open("2016_Grand_Rapids_tornado_outbreak_radar_loop.gif")
#image = Image.open("KOXOBiN.gif")
image = Image.open("blow.gif")
#image = Image.open("giphy (1).gif")
# storing the image height and width, so there'd be no function call for image.height/width
gif_height = image.height
gif_width = image.width
# initializing the canvas
canvas = tkinter.Canvas(root, height=gif_height, width=gif_width)
# loading the first frame
image_for_label = ImageTk.PhotoImage(image.resize((gif_width, gif_height)))
# storing the amount of frames in gif
frame_count = image.n_frames

# images = [PhotoImage(file='blow.gif', format = 'gif -index %i' %i) for i in range(image.n_frames)]



canvas.create_image(gif_width / 2, gif_height / 2, anchor=CENTER, image=image_for_label)
canvas.grid(row=0, column=0, columnspan=3)

# initializing the index counter for frames
ind = 0



while ind <= frame_count and stop_e == 0:
    #time.sleep(0.06)  # the pause between frames
    canvas.grid_forget()
    canvas = tkinter.Canvas(root, height=gif_height, width=gif_width)
    image_for_label = ImageTk.PhotoImage(image.resize((gif_width, gif_height)))  # loading the next image
    canvas.create_image(gif_width / 2, gif_height / 2, anchor=CENTER, image=image_for_label)
    canvas.grid(row=0, column=0, columnspan=3)

    # making the gif loop:
    if ind == frame_count:
        image.seek(0)
        ind = 0
    else:
        image.seek(ind)
        ind += 1

    root.update()




#stop_e = 1


root.mainloop()