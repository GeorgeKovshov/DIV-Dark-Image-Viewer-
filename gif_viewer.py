import sys
import tkinter
from tkinter import *
from PIL import ImageTk, Image
import time
import os

""" developing the gif viewer here, later transferred to the main app"""

root = Tk()
root.title("Images")

Grid.rowconfigure(root,0, weight=1)
Grid.columnconfigure(root,0, weight=1)

frame = Frame(root, relief="flat", bd=50)
frame.grid(row=1, column=0, sticky=S)

bigger_than_window = False
stop_e = False

def canvas_reshape(height, width, canv_height, canv_width):
    if height <= canv_height and width <= canv_width:
        return height, width
    else:
        if height/width < 1:  # determening which dimension is the biggest one
            return min(height, canv_height), min(round(width * (canv_height / height)), canv_width)

        else:
            return min(round(height * (canv_width / width)), canv_height), min(width, canv_width)

def stop():
    """stops the gif"""
    global stop_e
    stop_e = not stop_e
    root.update()

zoom_value = 1
monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

def zoom():
    """resizes the image"""
    global zoom_value
    global gif_width
    global gif_height
    global monitor_width
    global monitor_height
    global canvas
    global bigger_than_window
    zoom_value *= 1.5
    gif_width = round(gif_width * zoom_value)
    gif_height = round(gif_height * zoom_value)

    size_of_canvas_new = (gif_height, gif_width)


    # if zoomed-in image gets bigger than monitor, function stops expanding window; the image within canvas always expands
    if size_of_canvas_new[0] > monitor_height - 100 or size_of_canvas_new[1] > monitor_width - 100:
        # print("image: ", size_of_image_new, " canvas old: ", size_of_canvas_new)
        size_of_canvas_new = canvas_reshape(size_of_canvas_new[0], size_of_canvas_new[1],
                                            monitor_height - 180, monitor_width - 180)
        # checkbox_Lock.select()
        # print("image: ", size_of_image_new, " canvas new: ", size_of_canvas_new)
        if not bigger_than_window:
            bigger_than_window = True
            gif_height = size_of_canvas_new[0]
            gif_width = size_of_canvas_new[1]
    canvas.config(height=size_of_canvas_new[0], width=size_of_canvas_new[1])

    root.update()

button_stop = Button(frame, text="stop", command=stop)
button_stop.grid(row=0, column=0)
button_zoom = Button(frame, text="zoom", command=zoom)
button_zoom.grid(row=0, column=2)
# opening the gif

#image = Image.open("2016_Grand_Rapids_tornado_outbreak_radar_loop.gif")
image = Image.open("KOXOBiN.gif")
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
canvas.grid(row=0, column=0, columnspan=3, sticky=N+W+E)

# initializing the index counter for frames
ind = 0



while ind <= frame_count and not stop_e:
    time.sleep(0.06 / zoom_value)  # the pause between frames
    #print(zoom_value)
    canvas.grid_forget()
    #canvas.configure(height=gif_height, width=gif_width)
    image_for_label = ImageTk.PhotoImage(image.resize((gif_width, gif_height)))  # loading the next image
    canvas.create_image(gif_width / 2, gif_height / 2, anchor=CENTER, image=image_for_label)
    canvas.grid(row=0, column=0, columnspan=3, sticky=E)

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