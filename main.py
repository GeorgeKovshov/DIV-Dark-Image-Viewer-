import sys
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
import time
import os
import viewer_style
import custom_titlebar




root = ThemedTk()

root.minsize(562, 151)


root.overrideredirect(True) # turns off title bar, geometry



root.title("Simple Image Viewer")







style = ttk.Style(root)
style.theme_use("clam")
viewer_style.my_style(style)

style.configure(root, focuscolor="")
root.configure(background="#121212")

# root.configure(background="gray")

#options_frame = Frame(root, relief="raised", bd=5, background="#363636")
#settings_frame = Frame(root, relief="sunken", bd=1, background="#363636")

options_frame = ttk.Frame(root, relief="raised", padding=[10, 10, 10, 10])
settings_frame = ttk.Frame(root, relief="sunken", padding=[10, 10, 10, 10])
closing_frame = ttk.Frame(root, relief="sunken", padding=[15, 10, 10, 10])

options_frame.grid(row=3, column=1, columnspan= 2)#, sticky="e")
settings_frame.grid(row=0, column=0, columnspan=3, sticky="nw")
closing_frame.grid(row=0, column = 1, columnspan=3, sticky="ne")
# bind title bar motion to the move window function


# put a close button on the title bar
close_button = ttk.Button(closing_frame, text='X', width=3, command=root.destroy)
close_button.grid(row=0, column=1, padx=5, ipady=3)


Grid.rowconfigure(root, 0, weight=0)
Grid.rowconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 2, weight=1)
Grid.rowconfigure(root, 3, weight=0)
#Grid.rowconfigure(root, 4, weight=0)
#Grid.rowconfigure(root, 5, weight=0)


Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)
Grid.columnconfigure(root, 2, weight=1)
Grid.columnconfigure(root, 3, weight=1)


# storing the current image directory path
current_dir_path = os.getcwd()

# Creating a list of image file names
images=[]
for f in os.listdir('.'):
    if f.endswith(('.jpg', '.JPG', '.jpeg', '.png', '.gif')):
        images.append(f)






# global current_image - use 'global' only in functions, not here
current_image = 0

# variable for window size lock
lock_on = BooleanVar()

# variable to fix an off-centering of newly locked images
previous_lock_on = BooleanVar()

# variable for whether the controls menu is hidden
hide_on = BooleanVar()

# variable for whether the zoomed image is bigger than window
zoom_on = BooleanVar()
zoom_value = 1

# variable for whether the app is fullscreen'd
fullscreen_on = False


# variable for rotation
rotation = 0

# Getting the monitor screen height and width
monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

# The coordinates of zoomed image point we look at
moving_shift_X = 0
moving_shift_Y = 0


def locking():
    """changing the lock_on value based on checkbox alteration"""
    global lock_on
    lock_on = not lock_on

def max_size_reshape(height, width):
    """function to check the image size and reshape it to fit into the monitor,
     returns new height and width"""
    if height < (monitor_height - 200) and width < (monitor_width - 400):
        return height, width
    else:
        return max_size_reshape(height//2, width//2)



def lock_on_size_reshape(height, width, canv_height, canv_width):
    """function to fit image inside of window and canvas,
     returns new height and width"""
    if height <= canv_height and width <= canv_width:
        return height, width
    else:
        if height - canv_height > width - canv_width:  # Calculating which dimension is out of bounds (if both then which is the bigger one)
            return lock_on_size_reshape(canv_height, round(width * (canv_height / height)), canv_height, canv_width)
        else:
            return lock_on_size_reshape(round(height * (canv_width / width)), canv_width, canv_height, canv_width)




def canvas_reshape(height, width, canv_height, canv_width):
    if height <= canv_height and width <= canv_width:
        return height, width
    else:
        if height/width < 1:  # determening which dimension is the biggest one
            print(1)
            return min(height, canv_height), min(round(width * (canv_height / height)), canv_width)

        else:
            print(2)
            return min(round(height * (canv_width / width)), canv_height), min(width, canv_width)

def rotate_image(direction):
    """function that changes the rotation value depending on the button pressed"""
    global rotation
    global current_image
    # 0 - original image, 1 - rotated right, -1 - rotated left, 2 - upside down image
    if direction:
        rotation += 1
        if rotation > 2:
            rotation = -1
    else:
        rotation -= 1
        if rotation < -1:
            rotation = 2
    show_image(current_image)


def moving_pictures(var):
    """moving zoomed-in image with the sliders"""
    global canvas
    global canvas_image_to_move
    global moving_shift_X
    global moving_shift_Y
    print("zoom_hor_slider.get():", zoom_hor_slider.get(), " moving_shift_X: ", moving_shift_X)
    # if moving parameters are at zero, we get the first bunch to compare the second against
    if moving_shift_X == 0 and moving_shift_Y == 0:
        moving_shift_X = zoom_hor_slider.get()
        moving_shift_Y = zoom_ver_slider.get()
    else:
        canvas.move(canvas_image_to_move, zoom_hor_slider.get() - moving_shift_X, zoom_ver_slider.get() - moving_shift_Y)
    moving_shift_X = zoom_hor_slider.get()
    moving_shift_Y = zoom_ver_slider.get()


def mouse_release(e):
    """function that resets the moving parameters when mouse button is released"""
    global canvas
    global moving_shift_Y
    global moving_shift_X
    global zoom_hor_slider
    global zoom_ver_slider
    canvas.config(cursor="arrow")
    # resetting the parameters to avoid jugged jumps while moving
    moving_shift_X = 0
    moving_shift_Y = 0
    #after mouse movement, we turn the sliders back on
    zoom_hor_slider.config(command=moving_pictures)
    zoom_ver_slider.config(command=moving_pictures)
    print("release")

def empty_dunction(e):
    """function that does nothing"""
    return

def moving_mouse(e):
    """moving zoomed-in image with the mouse"""
    #e.x
    #e.y
    global canvas
    global canvas_image_to_move
    global moving_shift_X
    global moving_shift_Y
    global zoom_ver_slider
    global zoom_hor_slider
    image_coordinates = canvas.bbox(canvas_image_to_move)
    canvas.config(cursor="fleur")
    x_movement = e.x - moving_shift_X  # calculating horizontal movement value
    y_movement = e.y - moving_shift_Y  # calculating vertical movement value
    # calculating the coordinates of the image boundaries in relation to canvas
    y_stop = abs(image_coordinates[1]) + abs(image_coordinates[3]) - canvas.winfo_height()
    x_stop = abs(image_coordinates[0]) + abs(image_coordinates[2]) - canvas.winfo_width()
    # while moving the picture with the mouse, the slider will not move the image
    zoom_ver_slider.config(to=-y_stop, command=empty_dunction)
    zoom_hor_slider.config(to=-x_stop, command=empty_dunction)

    # We only move the image if it's not getting out of bounds of canvas, moving shift !=0 here is the measure against jugged movement
    if -y_stop <= image_coordinates[1] + y_movement <= 0 and moving_shift_Y != 0:
        canvas.move(canvas_image_to_move, 0, y_movement)
        zoom_ver_slider.set(zoom_ver_slider.get() + y_movement)
    if -x_stop <= image_coordinates[0] + x_movement <= 0 and moving_shift_X != 0:
        canvas.move(canvas_image_to_move, x_movement, 0)
        zoom_hor_slider.set(zoom_hor_slider.get() + x_movement)

    # storing the old coordinates for next iteration
    moving_shift_X = e.x
    moving_shift_Y = e.y


def show_image(img_number):
    """function to show an image from the list with img_number index"""
    global images
    global canvas
    global lock_on
    global previous_lock_on
    global rotation
    global current_dir_path
    global actual_image #without storing image here, garbage collector takes the image away
    global options_frame
    global actual_image_height
    global actual_image_width
    global zoom_value
    global fullscreen_on
    global hide_on


    image_for_canvas_new = Image.open(current_dir_path + "/" + images[img_number])
    actual_image_height = image_for_canvas_new.height
    actual_image_width = image_for_canvas_new.width

    # rotating image if its rotated
    if rotation == 1:
        actual_image_height = image_for_canvas_new.width
        actual_image_width = image_for_canvas_new.height
        image_for_canvas_new = image_for_canvas_new.rotate(-90, expand=True)

    elif rotation == -1:
        actual_image_height = image_for_canvas_new.width
        actual_image_width = image_for_canvas_new.height
        image_for_canvas_new = image_for_canvas_new.rotate(90, expand=True)
    elif rotation == 2:
        image_for_canvas_new = image_for_canvas_new.rotate(180)


    # if the window is locked, fit the image in window
    # else fit it and window into the monitor
    if not lock_on.get():
        #size_of_image_new = max_size_reshape(actual_image_height, actual_image_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
        size_of_image_new = max_size_reshape(round(actual_image_height * zoom_value), round(actual_image_width * zoom_value))#image_for_canvas_new.height, image_for_canvas_new.width)
        #x = size_of_image_new[1]
        #y = size_of_image_new[0]
        canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
        if not fullscreen_on:
            if options_frame.winfo_height()>1 and not hide_on.get():  # loading the first image
                root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + options_frame.winfo_height() + 58}")
            elif hide_on.get():  # loading images when hide on
                root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + 58}")
            else:  # loading images when not hide on
                root.geometry("")

    else:
        y = root.winfo_height()
        x = root.winfo_width()
        if fullscreen_on:
            y = root.winfo_screenheight()
            x = root.winfo_screenwidth()
            canvas.config(height=y, width=x)
        elif hide_on.get():
            y -= 69
            canvas.config(height=root.winfo_height() - 69, width=root.winfo_width())  # height=root.winfo_height() - 152
        else:
            y -= options_frame.winfo_height() + 58
            canvas.config(height=root.winfo_height() - options_frame.winfo_height() - 58, width=root.winfo_width())

        size_of_image_new = lock_on_size_reshape(round(actual_image_height * zoom_value),
                                                 round(actual_image_width * zoom_value),
                                                 y, x)

    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new

    if not lock_on.get():
        canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2, image=actual_image)
    else:
        #canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2, image=image1_new)
        canvas.create_image(x/2, y/2, anchor=CENTER, image=image1_new)
    canvas.grid(row=1, column=1, sticky="se")  # columnspan=4)

image_is_animation = False
bigger_than_window = False
stop_e = False
old_stop_e = False
gif_index = 0
gif_height = 0
gif_width = 0

def stop():
    """stops the gif"""
    global stop_e
    global current_image
    stop_e = not stop_e
    show_gif(current_image)

def stop_full():
    """stops the gif"""
    global stop_e
    global old_stop_e
    old_stop_e = stop_e
    stop_e = True
    show_gif(current_image)
    #root.update()

def resume_stop_full():
    "restores old stop value"
    global stop_e
    global old_stop_e
    stop_e = old_stop_e
    show_gif(current_image)


def zoom_gif3(is_zoom_in):
    global current_dir_path
    global images
    global canvas
    global options_frame
    global actual_image_width
    global actual_image_height
    global actual_image
    global button_stop
    global stop_e
    global zoom_ver_slider
    global zoom_hor_slider
    global zoom_value
    global gif_index
    global gif_width
    global gif_height
    global moving_shift_X
    global moving_shift_Y
    global zoom_on
    global bigger_than_window

    canvas.grid_forget()
    if is_zoom_in:
        zoom_value = zoom_value * 1.5
        gif_width = round(gif_width * 1.5)
        gif_height = round(gif_height * 1.5)
    else:
        zoom_value = zoom_value * 0.75
        gif_width = round(gif_width * 0.75)
        gif_height = round(gif_height * 0.75)
    # if the window is locked, fit the image in window
    # else fit it and window into the monitor

    """
    size_of_image_new = (image_for_canvas_new.height, image_for_canvas_new.width) - that's gif_width and gif_height
    size_of_canvas_new = size_of_image_new
    """
    size_of_canvas_new = (gif_height, gif_width)

    if not lock_on.get():
        # if zoomed-in image gets bigger than monitor, function stops expanding window; the image within canvas always expands
        if size_of_canvas_new[0] > monitor_height - 100 or size_of_canvas_new[1] > monitor_width - 100:
            #size_of_canvas_new = canvas_reshape(size_of_canvas_new[0], size_of_canvas_new[1],
            #                                         monitor_height - 180, monitor_width - 180)
            bigger_than_window = True
            moving_shift_X = 0
            moving_shift_Y = 0
            zoom_on.set(True)
            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)

            zoom_ver_slider = ttk.Scale(root, from_=0, to=-gif_height + canvas.winfo_height(),
                                        length=canvas.winfo_height(), orient="vertical")
            zoom_hor_slider = ttk.Scale(root, from_=0, to=-gif_width + canvas.winfo_width(),
                                        length=canvas.winfo_width(), orient="horizontal")

            zoom_ver_slider.grid(row=1, column=2, sticky=SW, rowspan=1)

            zoom_hor_slider.grid(row=2, column=1, sticky=NE)
            """
            moving_shift_X = 0
            moving_shift_Y = 0
            zoom_on.set(True)
            bigger_than_window = True

            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)
            zoom_ver_slider = ttk.Scale(root, from_=0, to=-gif_height + size_of_canvas_new[0],
                                    length=size_of_canvas_new[0], orient="vertical")
            zoom_ver_slider.grid(row=1, column=2, rowspan=1, sticky=SW)
            zoom_hor_slider = ttk.Scale(root, from_=0, to=-gif_width + size_of_canvas_new[1],
                                    length=size_of_canvas_new[1], orient="horizontal") #showvalue=0
            zoom_hor_slider.grid(row=2, column=1, sticky=NE)
            """
        else:
            canvas.config(height=size_of_canvas_new[0], width=size_of_canvas_new[1])
    else:
        if canvas.winfo_width() < gif_width or canvas.winfo_height()< gif_height:
            moving_shift_X = 0
            moving_shift_Y = 0
            zoom_on.set(True)
            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)

            zoom_ver_slider = ttk.Scale(root, from_=0, to=-gif_height + canvas.winfo_height(),
                                        length=canvas.winfo_height(), orient="vertical")
            zoom_hor_slider = ttk.Scale(root, from_=0, to=-gif_width + canvas.winfo_width(),
                                        length=canvas.winfo_width(), orient="horizontal")

            zoom_ver_slider.grid(row=1, column=2,sticky=SW, rowspan=1)

            zoom_hor_slider.grid(row=2, column=1, sticky=NE)

            #placing the default sliders positions in the middle
            #zoom_hor_slider.set(zoom_hor_slider.cget("to")/2)
            #zoom_ver_slider.set(zoom_ver_slider.cget("to")/2)



    if not lock_on.get() and not bigger_than_window:
        # size_of_image_new = max_size_reshape(actual_image_height, actual_image_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
        size_of_image_new = max_size_reshape(gif_height,
                                             gif_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
        canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
        # x = size_of_image_new[1]
        # y = size_of_image_new[0]
        if not fullscreen_on:
            if options_frame.winfo_height() > 1 and not hide_on.get():  # loading the first image
                root.geometry(
                    f"{size_of_image_new[1]}x{size_of_image_new[0] + 136 + 58}")  # + options_frame.winfo_height() + 58}")
            elif hide_on.get():  # loading images when hide on
                root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + 58}")
            else:  # loading images when not hide on
                root.geometry("")
    canvas.grid(row=1, column=1)


def zoom_gif2(is_zoomed_in):
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


def old_show_gif(img_number):
    """function for playing a gif"""
    global current_dir_path
    global images
    global canvas
    global options_frame
    global actual_image_width
    global actual_image_height
    global actual_image
    global button_stop
    global stop_e
    global zoom_ver_slider
    global zoom_hor_slider
    global gif_index
    global gif_width
    global gif_height

    image = Image.open(current_dir_path + "/" + images[img_number])

    # image = Image.open("2016_Grand_Rapids_tornado_outbreak_radar_loop.gif")
    #image = Image.open("KOXOBiN.gif")
    # image = Image.open("giphy (1).gif")
    # storing the image height and width, so there'd be no function call for image.height/width
    actual_image_height = image.height
    actual_image_width = image.width
    gif_height = round(image.height)
    gif_width = round(image.width)
    """
    rotated_image = image

    # rotating image if its rotated
    if rotation == 1:
        actual_image_height = image.width
        actual_image_width = image.height
        #image = image.rotate(-90, expand=True)
        rotated_image = image.rotate(-90, expand=True)
    elif rotation == -1:
        actual_image_height = image.width
        actual_image_width = image.height
        #image = image.rotate(90, expand=True)
        rotated_image = image.rotate(90, expand=True)
    elif rotation == 2:
        #image = image.rotate(180)
        rotated_image = image.rotate(180)

    # if the window is locked, fit the image in window
    # else fit it and window into the monitor
    if not lock_on.get():
        # size_of_image_new = max_size_reshape(actual_image_height, actual_image_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
        size_of_image_new = max_size_reshape(round(actual_image_height * zoom_value), round(
            actual_image_width * zoom_value))  # image_for_canvas_new.height, image_for_canvas_new.width)
        # x = size_of_image_new[1]
        # y = size_of_image_new[0]
        canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
        if not fullscreen_on:
            if options_frame.winfo_height() > 1 and not hide_on.get():  # loading the first image
                root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + options_frame.winfo_height() + 58}")
            elif hide_on.get():  # loading images when hide on
                root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + 58}")
            else:  # loading images when not hide on
                root.geometry("")
    else:
        y = root.winfo_height()
        x = root.winfo_width()
        if fullscreen_on:
            y = root.winfo_screenheight()
            x = root.winfo_screenwidth()
            canvas.config(height=y, width=x)
        elif hide_on.get():
            y -= 69
            canvas.config(height=root.winfo_height() - 69, width=root.winfo_width())  # height=root.winfo_height() - 152
        else:
            y -= options_frame.winfo_height() + 58
            canvas.config(height=root.winfo_height() - options_frame.winfo_height() - 58, width=root.winfo_width())

        size_of_image_new = lock_on_size_reshape(round(actual_image_height * zoom_value),
                                                 round(actual_image_width * zoom_value),
                                                 y, x)
    """

    # initialize stop button
    button_stop.grid(row=4, column=1, pady=5)
    # storing the amount of frames in gif
    frame_count = image.n_frames
    """
    if gif_index == 0:
        # initializing the canvas
        #canvas.configure(height=actual_image_height, width=actual_image_width)
        image_for_label = ImageTk.PhotoImage(image.resize((round(size_of_image_new[1]*zoom_value),
                                                            (round(size_of_image_new[0]*zoom_value)))))

        canvas.create_image(actual_image_width / 2, actual_image_height / 2, anchor=CENTER, image=image_for_label)
        canvas.grid(row=1, column=1, sticky="se")

    """

    while gif_index <= frame_count and not stop_e:
        time.sleep(0.06 / zoom_value)  # the pause between frames
        # print(zoom_value)
        canvas.grid_forget()

        # making the gif loop:
        if gif_index == frame_count:
            image.seek(0)
            gif_index = 0
        else:
            image.seek(gif_index)
        #canvas.configure(height=gif_height, width=gif_width)
        rotated_image = image
        if rotation == 1:
            actual_image_height = image.width
            actual_image_width = image.height
            #image = image.rotate(-90, expand=True)
            rotated_image = image.rotate(-90, expand=True)
        elif rotation == -1:
            actual_image_height = image.width
            actual_image_width = image.height
            #image = image.rotate(90, expand=True)
            rotated_image = image.rotate(90, expand=True)
        elif rotation == 2:
            #image = image.rotate(180)
            rotated_image = image.rotate(180)
        #size_of_image_new = max_size_reshape(round(actual_image_height * zoom_value),
                                             #round(actual_image_width * zoom_value))
        #image_for_label = ImageTk.PhotoImage(rotated_image.resize((round(size_of_image_new[1]*zoom_value), round(size_of_image_new[0]*zoom_value))))  # loading the next image

        # if the window is locked, fit the image in window
        # else fit it and window into the monitor
        if not lock_on.get():
            # size_of_image_new = max_size_reshape(actual_image_height, actual_image_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
            size_of_image_new = max_size_reshape(round(actual_image_height),
                                                 round(actual_image_width))  # image_for_canvas_new.height, image_for_canvas_new.width)
            # x = size_of_image_new[1]
            # y = size_of_image_new[0]
            canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
            if not fullscreen_on:
                if options_frame.winfo_height() > 1 and not hide_on.get():  # loading the first image
                    root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + options_frame.winfo_height() + 58}")
                elif hide_on.get():  # loading images when hide on
                    root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + 58}")
                else:  # loading images when not hide on
                    root.geometry("")
        else:
            y = root.winfo_height()
            x = root.winfo_width()
            if fullscreen_on:
                y = root.winfo_screenheight()
                x = root.winfo_screenwidth()
                canvas.config(height=y, width=x)
            elif hide_on.get():
                y -= 69
                canvas.config(height=root.winfo_height() - 69,
                              width=root.winfo_width())  # height=root.winfo_height() - 152
            else:
                y -= options_frame.winfo_height() + 58
                canvas.config(height=root.winfo_height() - options_frame.winfo_height() - 58, width=root.winfo_width())

            size_of_image_new = lock_on_size_reshape(round(actual_image_height),
                                                     round(actual_image_width),
                                                     y, x)
        image_for_label = ImageTk.PhotoImage(rotated_image.resize((round(size_of_image_new[1]),
                                                                 round(size_of_image_new[0]))))  # loading the next image

        actual_image = image_for_label
        if zoom_ver_slider.winfo_ismapped():
            slide_y = zoom_ver_slider.get()
        else:
            slide_y = 0
        if zoom_hor_slider.winfo_ismapped():
            slide_x = zoom_hor_slider.get()
        else:
            slide_x = 0
        if not lock_on:
            canvas.create_image(round(size_of_image_new[1]) / 2 + slide_x, round(size_of_image_new[0]) / 2 + slide_y, anchor=CENTER, image=image_for_label)
        else:
            canvas.create_image(round(canvas.winfo_width()) / 2 + slide_x, round(canvas.winfo_height()) / 2 + slide_y,
                                anchor=CENTER, image=image_for_label)
        canvas.grid(row=1, column=1, sticky="se")

        gif_index += 1
        root.update()

def show_gif2(img_number):
    global current_dir_path
    global images
    global canvas
    global options_frame
    global actual_image_width
    global actual_image_height
    global actual_image
    global button_stop
    global stop_e
    global zoom_ver_slider
    global zoom_hor_slider
    global gif_index
    global gif_width
    global gif_height

    image = Image.open(current_dir_path + "/" + images[img_number])
    # image = Image.open("giphy (1).gif")
    # storing the image height and width, so there'd be no function call for image.height/width
    gif_height = image.height
    gif_width = image.width
    canvas = tkinter.Canvas(root, height=gif_height, width=gif_width)
    # loading the first frame
    image_for_label = ImageTk.PhotoImage(image.resize((gif_width, gif_height)))
    # storing the amount of frames in gif
    frame_count = image.n_frames

    while gif_index <= frame_count and not stop_e:
        time.sleep(0.06 / zoom_value)  # the pause between frames
        # print(zoom_value)
        canvas.grid_forget()
        # canvas.configure(height=gif_height, width=gif_width)
        image_for_label = ImageTk.PhotoImage(image.resize((gif_width, gif_height)))  # loading the next image
        canvas.create_image(gif_width / 2, gif_height / 2, anchor=CENTER, image=image_for_label)
        canvas.grid(row=0, column=0, columnspan=3, sticky=E)

        # making the gif loop:
        if gif_index == frame_count:
            image.seek(0)
            gif_index = 0
        else:
            image.seek(gif_index)
            gif_index += 1

        root.update()


def show_gif(img_number):
    """function for playing a gif"""
    global current_dir_path
    global images
    global canvas
    global options_frame
    global actual_image_width
    global actual_image_height
    global actual_image
    global button_stop
    global button_zoom_in2
    global stop_e
    global zoom_ver_slider
    global zoom_hor_slider
    global zoom_value
    global gif_index
    global gif_width
    global gif_height

    image = Image.open(current_dir_path + "/" + images[img_number])
    canvas.grid_forget()
    # image = Image.open("2016_Grand_Rapids_tornado_outbreak_radar_loop.gif")
    #image = Image.open("KOXOBiN.gif")
    # image = Image.open("giphy (1).gif")
    # storing the image height and width, so there'd be no function call for image.height/width
    actual_image_height = image.height
    actual_image_width = image.width
    gif_height = round(image.height)
    gif_width = round(image.width)

    rotated_image = image
    if zoom_value==1:
        print(zoom_value)
        # rotating image if its rotated
        if rotation == 1:
            actual_image_height = image.width
            actual_image_width = image.height
            #image = image.rotate(-90, expand=True)
            rotated_image = image.rotate(-90, expand=True)
        elif rotation == -1:
            actual_image_height = image.width
            actual_image_width = image.height
            #image = image.rotate(90, expand=True)
            rotated_image = image.rotate(90, expand=True)
        elif rotation == 2:
            #image = image.rotate(180)
            rotated_image = image.rotate(180)

        # if the window is locked, fit the image in window
        # else fit it and window into the monitor
        if not lock_on.get():
            # size_of_image_new = max_size_reshape(actual_image_height, actual_image_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
            size_of_image_new = max_size_reshape(actual_image_height,
                                                 actual_image_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
            # x = size_of_image_new[1]
            # y = size_of_image_new[0]
            canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
            if not fullscreen_on:
                if options_frame.winfo_height() > 1 and not hide_on.get():  # loading the first image
                    root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + 136 + 58}") #+ options_frame.winfo_height() + 58}")
                elif hide_on.get():  # loading images when hide on
                    root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + 58}")
                else:  # loading images when not hide on
                    root.geometry("")
        else:
            y = root.winfo_height()
            x = root.winfo_width()
            if fullscreen_on:
                y = root.winfo_screenheight()
                x = root.winfo_screenwidth()
                canvas.config(height=y, width=x)
            elif hide_on.get():
                y -= 69
                canvas.config(height=root.winfo_height() - 69, width=root.winfo_width())  # height=root.winfo_height() - 152
            else:
                y -= 136 + 58 #options_frame.winfo_height() + 58
                canvas.config(height=root.winfo_height() - 136 - 58, width=root.winfo_width())
                print(options_frame.winfo_height())

            size_of_image_new = lock_on_size_reshape(round(actual_image_height),
                                                     round(actual_image_width),
                                                     y, x)
        image_for_label = ImageTk.PhotoImage(rotated_image.resize((size_of_image_new[1],
                                                        size_of_image_new[0])))
        actual_image = image_for_label

        if not lock_on.get():

            canvas.create_image(size_of_image_new[1]/2, size_of_image_new[0]/2,
                                anchor=CENTER, image=image_for_label)
        else:
            #canvas.create_image(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
            canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2,
                                anchor=CENTER, image=image_for_label)

        canvas.grid(row=1, column=1, sticky="se")
        gif_height = size_of_image_new[0]
        gif_width = size_of_image_new[1]


    # initialize stop button
    button_stop.grid(row=3, column=1, pady=5)
    button_zoom_in2.grid(row=3, column=2)
    # storing the amount of frames in gif
    frame_count = image.n_frames
    """
    if gif_index == 0:
        # initializing the canvas
        #canvas.configure(height=actual_image_height, width=actual_image_width)
        image_for_label = ImageTk.PhotoImage(image.resize((round(size_of_image_new[1]*zoom_value),
                                                            (round(size_of_image_new[0]*zoom_value)))))

        canvas.create_image(actual_image_width / 2, actual_image_height / 2, anchor=CENTER, image=image_for_label)
        canvas.grid(row=1, column=1, sticky="se")

    """

    while gif_index <= frame_count and not stop_e:
        time.sleep(0.06 / zoom_value)  # the pause between frames
        # print(zoom_value)
        canvas.grid_forget()

        # making the gif loop:
        if gif_index == frame_count:
            image.seek(0)
            gif_index = 0
        else:
            image.seek(gif_index)
        #canvas.configure(height=gif_height, width=gif_width)
        rotated_image = image
        if rotation == 1:
            actual_image_height = image.width
            actual_image_width = image.height
            #image = image.rotate(-90, expand=True)
            rotated_image = image.rotate(-90, expand=True)
        elif rotation == -1:
            actual_image_height = image.width
            actual_image_width = image.height
            #image = image.rotate(90, expand=True)
            rotated_image = image.rotate(90, expand=True)
        elif rotation == 2:
            #image = image.rotate(180)
            rotated_image = image.rotate(180)
        #size_of_image_new = max_size_reshape(round(actual_image_height * zoom_value),
                                             #round(actual_image_width * zoom_value))
        #image_for_label = ImageTk.PhotoImage(rotated_image.resize((round(size_of_image_new[1]*zoom_value), round(size_of_image_new[0]*zoom_value))))  # loading the next image
        """
        # if the window is locked, fit the image in window
        # else fit it and window into the monitor
        if not lock_on.get():
            # size_of_image_new = max_size_reshape(actual_image_height, actual_image_width)  # image_for_canvas_new.height, image_for_canvas_new.width)
            size_of_image_new = max_size_reshape(round(actual_image_height),
                                                 round(actual_image_width))  # image_for_canvas_new.height, image_for_canvas_new.width)
            # x = size_of_image_new[1]
            # y = size_of_image_new[0]
            #canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
            
            if not fullscreen_on:
                if options_frame.winfo_height() > 1 and not hide_on.get():  # loading the first image
                    root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + options_frame.winfo_height() + 58}")
                elif hide_on.get():  # loading images when hide on
                    root.geometry(f"{size_of_image_new[1]}x{size_of_image_new[0] + 58}")
                else:  # loading images when not hide on
                    root.geometry("")
            
        else:
            y = root.winfo_height()
            x = root.winfo_width()
            if fullscreen_on:
                y = root.winfo_screenheight()
                x = root.winfo_screenwidth()
                #canvas.config(height=y, width=x)
            elif hide_on.get():
                y -= 69
                #canvas.config(height=root.winfo_height() - 69,
                #              width=root.winfo_width())  # height=root.winfo_height() - 152
            else:
                y -= options_frame.winfo_height() + 58
                #canvas.config(height=root.winfo_height() - options_frame.winfo_height() - 58, width=root.winfo_width())

            size_of_image_new = lock_on_size_reshape(round(actual_image_height),
                                                     round(actual_image_width),
                                                     y, x)
        """

        image_for_label = ImageTk.PhotoImage(
            rotated_image.resize((gif_width,  # round(size_of_image_new[1]),
                                  gif_height)))  # round(size_of_image_new[0]))))  # loading the next image
        """
        Weebly-woobly
        image_for_label = ImageTk.PhotoImage(rotated_image.resize((actual_image.height(),#round(size_of_image_new[1]),
                                                                 actual_image.width())))#round(size_of_image_new[0]))))  # loading the next image
        """
        actual_image = image_for_label
        if zoom_ver_slider.winfo_ismapped():
            slide_y = zoom_ver_slider.get()
        else:
            slide_y = 0
        if zoom_hor_slider.winfo_ismapped():
            slide_x = zoom_hor_slider.get()
        else:
            slide_x = 0


        if not lock_on.get():
            canvas.create_image(gif_width / 2 + slide_x, gif_height / 2 + slide_y, anchor=CENTER, image=image_for_label)
        else:
            canvas.create_image(gif_width / 2 + slide_x, gif_height / 2 + slide_y,
            #canvas.create_image(round(canvas.winfo_width()) / 2 + slide_x, round(canvas.winfo_height()) / 2 + slide_y,
                                anchor=CENTER, image=image_for_label)
        canvas.grid(row=1, column=1, sticky="se")

        gif_index += 1
        root.update()


# Initializing canvas for images to be put into
canvas = tkinter.Canvas(root, height=1, width=1)
#canvas.configure(background="#121212", highlightbackground="#D9DDDC", highlightthickness=0)
canvas.configure(background="#222222", highlightbackground="#D9DDDC", highlightthickness=0)
canvas_image_to_move = canvas.create_image(1, 1)

# Loading the first image
if images:
    show_image(current_image)

actual_image

actual_image_height
actual_image_width




def cycling_calculation():
    "function that returns the next and previous image index from images list (cycles through them)"
    global images
    next_ind, previous_ind = 0, 0
    length_of_image_list = len(images)
    if current_image + 2 > length_of_image_list:
        previous_ind = current_image - 1
    elif current_image - 1 < 0:
        next_ind = current_image + 1
        previous_ind = length_of_image_list - 1
    else:
        next_ind = current_image + 1
        previous_ind = current_image - 1
    return next_ind, previous_ind


def next_image(img_number):
    """function that loads and puts the picture with 'img_number' from 'images' list on screen"""
    global images
    global current_image
    global canvas
    global rotation
    global actual_image
    global zoom_ver_slider
    global zoom_hor_slider
    global zoom_on
    global zoom_value
    global stop_e
    global button_stop
    global gif_index
    global image_is_animation
    global bigger_than_window
    # Calculating the next image number in list


    #Image.close(current_dir_path + "/" + images[img_number])

    current_image += (img_number - current_image)

    # Resetting rotation
    rotation = 0

    # Removing the sliders if they are there
    zoom_ver_slider.grid_forget()
    zoom_hor_slider.grid_forget()
    # resetting zoom for new image
    zoom_on.set(False)
    zoom_value = 1

    bigger_than_window = False

    # Resetting stop
    stop_e = True
    if button_stop.winfo_ismapped():
        button_stop.grid_forget()
    gif_index = 0

    # Making the image viewer cycle through images
    next_ind, previous_ind = cycling_calculation()

    # Remapping the buttons to new images
    button_next = ttk.Button(options_frame, text="Next ->", command=lambda: next_image(next_ind))
    button_next.grid(row=2, column=2)
    button_back = ttk.Button(options_frame, text="<- Back", command=lambda: next_image(previous_ind))
    button_back.grid(row=2, column=0)
    root.bind("<Right>", lambda event: next_image(next_ind))
    root.bind("<Left>", lambda event: next_image(previous_ind))

    # Replacing the old image with a new one
    if images[current_image].endswith(".gif"):
        image_is_animation = True
        stop_e = False
        show_gif(current_image)
    elif images[current_image].endswith(".webp"):
        try:
            image_is_animation = True
            stop_e = False
            show_gif(current_image)
        except:
            show_image(current_image)
    else:
        image_is_animation = False
        show_image(current_image)




def zoom(is_zoom_in):
    """function that resizes an image based on button pressed"""
    global images
    global current_image
    global canvas
    global actual_image
    global lock_on
    global monitor_width
    global monitor_height
    global checkbox_Lock
    global current_dir_path
    global zoom_ver_slider
    global zoom_hor_slider
    global moving_shift_X
    global moving_shift_Y
    global canvas_image_to_move
    global zoom_on
    global zoom_value

    # assigning image dimensions according to rotation
    if rotation == 1 or rotation == -1:
        size_of_image = (actual_image.width(), actual_image.height())
    else:
        size_of_image = (actual_image.height(), actual_image.width())

    # if zooming in then first part, if zooming out then second
    if is_zoom_in:
        image_for_canvas_new = Image.open(current_dir_path + "/" + images[current_image]).resize(
            (round(size_of_image[1] * 1.5), round(size_of_image[0] * 1.5)))
        zoom_value = zoom_value * 1.5
    else:
        image_for_canvas_new = Image.open(current_dir_path + "/" + images[current_image]).resize(
            (round(size_of_image[1] * 0.75), round(size_of_image[0] * 0.75)))
        zoom_value = zoom_value * 0.75


    # rotating image if its rotated
    if rotation == 1:
        image_for_canvas_new = image_for_canvas_new.rotate(-90, expand=True)
        #size_of_image_new = (image_for_canvas_new.width, image_for_canvas_new.height)
    elif rotation == -1:
        image_for_canvas_new = image_for_canvas_new.rotate(90, expand=True)
        #size_of_image_new = (image_for_canvas_new.width, image_for_canvas_new.height)
    elif rotation == 2:
        image_for_canvas_new = image_for_canvas_new.rotate(180)


    zoom_ver_slider.grid_forget()
    zoom_hor_slider.grid_forget()
    zoom_on.set(False)
    size_of_image_new = (image_for_canvas_new.height, image_for_canvas_new.width)
    size_of_canvas_new = size_of_image_new


    if not lock_on.get():
        # if zoomed-in image gets bigger than monitor, function stops expanding window; the image within canvas always expands
        if size_of_canvas_new[0] > monitor_height - 100 or size_of_canvas_new[1] > monitor_width - 100:
            size_of_canvas_new = canvas_reshape(size_of_canvas_new[0], size_of_canvas_new[1],
                                                     monitor_height - 180, monitor_width - 180)
            moving_shift_X = 0
            moving_shift_Y = 0
            zoom_on.set(True)
            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)
            zoom_ver_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[0] + size_of_canvas_new[0],
                                    length=size_of_canvas_new[0], orient="vertical", command=moving_pictures)
            zoom_ver_slider.grid(row=1, column=2, rowspan=1, sticky=SW)
            zoom_hor_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[1] + size_of_canvas_new[1],
                                    length=size_of_canvas_new[1], orient="horizontal", command=moving_pictures) #showvalue=0
            zoom_hor_slider.grid(row=2, column=1, sticky=NE)

        canvas.config(height=size_of_canvas_new[0], width=size_of_canvas_new[1])
    else:
        if canvas.winfo_width() < size_of_image_new[1] or canvas.winfo_height()< size_of_image_new[0]:
            moving_shift_X = 0
            moving_shift_Y = 0
            zoom_on.set(True)
            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)

            zoom_ver_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[0] + canvas.winfo_height(),
                                        length=canvas.winfo_height(), orient="vertical", command=moving_pictures)
            zoom_hor_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[1] + canvas.winfo_width(),
                                        length=canvas.winfo_width(), orient="horizontal", command=moving_pictures)

            zoom_ver_slider.grid(row=1, column=2,sticky=SW, rowspan=1)

            zoom_hor_slider.grid(row=2, column=1, sticky=NE)

            #placing the default sliders positions in the middle
            zoom_hor_slider.set(zoom_hor_slider.cget("to")/2)
            zoom_ver_slider.set(zoom_ver_slider.cget("to")/2)

    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new
    if not lock_on.get():
        canvas_image_to_move = canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2,
                                                   anchor=CENTER, image=image1_new)
        root.geometry("")
    else:
        canvas_image_to_move = canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2,
                                                   anchor=CENTER, image=image1_new)

    canvas.grid(row=1, column=1)


def zoom_gif(is_zoom_in):
    """function that resizes an image based on button pressed"""
    global images
    global current_image
    global canvas
    global actual_image
    global lock_on
    global monitor_width
    global monitor_height
    global checkbox_Lock
    global current_dir_path
    global zoom_ver_slider
    global zoom_hor_slider
    global moving_shift_X
    global moving_shift_Y
    global canvas_image_to_move
    global zoom_on
    global zoom_value

    # assigning image dimensions according to rotation
    if rotation == 1 or rotation == -1:
        size_of_image = (actual_image.width(), actual_image.height())
    else:
        size_of_image = (actual_image.height(), actual_image.width())

    # if zooming in then first part, if zooming out then second
    if is_zoom_in:
        image_for_canvas_new = Image.open(current_dir_path + "/" + images[current_image]).resize(
            (round(size_of_image[1] * 1.5), round(size_of_image[0] * 1.5)))
        zoom_value = zoom_value * 1.5
    else:
        image_for_canvas_new = Image.open(current_dir_path + "/" + images[current_image]).resize(
            (round(size_of_image[1] * 0.75), round(size_of_image[0] * 0.75)))
        zoom_value = zoom_value * 0.75


    # rotating image if its rotated
    if rotation == 1:
        image_for_canvas_new = image_for_canvas_new.rotate(-90, expand=True)
        #size_of_image_new = (image_for_canvas_new.width, image_for_canvas_new.height)
    elif rotation == -1:
        image_for_canvas_new = image_for_canvas_new.rotate(90, expand=True)
        #size_of_image_new = (image_for_canvas_new.width, image_for_canvas_new.height)
    elif rotation == 2:
        image_for_canvas_new = image_for_canvas_new.rotate(180)


    zoom_ver_slider.grid_forget()
    zoom_hor_slider.grid_forget()
    zoom_on.set(False)
    size_of_image_new = (image_for_canvas_new.height, image_for_canvas_new.width)
    size_of_canvas_new = size_of_image_new


    if not lock_on.get():
        # if zoomed-in image gets bigger than monitor, function stops expanding window; the image within canvas always expands
        if size_of_canvas_new[0] > monitor_height - 100 or size_of_canvas_new[1] > monitor_width - 100:
            size_of_canvas_new = canvas_reshape(size_of_canvas_new[0], size_of_canvas_new[1],
                                                     monitor_height - 180, monitor_width - 180)
            moving_shift_X = 0
            moving_shift_Y = 0
            zoom_on.set(True)
            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)
            zoom_ver_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[0] + size_of_canvas_new[0],
                                    length=size_of_canvas_new[0], orient="vertical", command=moving_pictures)
            zoom_ver_slider.grid(row=1, column=2, rowspan=1, sticky=SW)
            zoom_hor_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[1] + size_of_canvas_new[1],
                                    length=size_of_canvas_new[1], orient="horizontal", command=moving_pictures) #showvalue=0
            zoom_hor_slider.grid(row=2, column=1, sticky=NE)

        canvas.config(height=size_of_canvas_new[0], width=size_of_canvas_new[1])
    else:
        if canvas.winfo_width() < size_of_image_new[1] or canvas.winfo_height()< size_of_image_new[0]:
            moving_shift_X = 0
            moving_shift_Y = 0
            zoom_on.set(True)
            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)

            zoom_ver_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[0] + canvas.winfo_height(),
                                        length=canvas.winfo_height(), orient="vertical", command=moving_pictures)
            zoom_hor_slider = ttk.Scale(root, from_=0, to=-size_of_image_new[1] + canvas.winfo_width(),
                                        length=canvas.winfo_width(), orient="horizontal", command=moving_pictures)

            zoom_ver_slider.grid(row=1, column=2,sticky=SW, rowspan=1)

            zoom_hor_slider.grid(row=2, column=1, sticky=NE)

            #placing the default sliders positions in the middle
            #zoom_hor_slider.set(zoom_hor_slider.cget("to")/2)
            #zoom_ver_slider.set(zoom_ver_slider.cget("to")/2)

    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new
    if not lock_on.get():
        canvas_image_to_move = canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2,
                                                   anchor=CENTER, image=image1_new)
        root.geometry("")
    else:
        canvas_image_to_move = canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2,
                                                   anchor=CENTER, image=image1_new)

    canvas.grid(row=1, column=1)


def open_image():
    """function that allows the user to choose a picture on their computer"""
    global images
    global current_image
    global current_dir_path
    global zoom_on

    # handling the error of not choosing a file
    try:
        filename = filedialog.askopenfilename(initialdir=current_dir_path, title="Choose an image",
                                                filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"),
                                                           ("jpg files", "*.jpg"), ("png files", "*.png"),
                                                           ("webp files", "*.webp"), ("all files", "*.*")))
    except FileNotFoundError as err:
        print("Error", err)
        filename = ""

    # only doing the rest if a filename was chosen
    if filename != "":

        # storing the directory location
        current_dir_path = os.path.dirname(filename)

        # emptying the image file names list
        images.clear()

        # index_counter and name of file to store the index of chosen image within the created images list
        index_filename = 0
        filename_end = os.path.basename(filename)

        # filling the images list with filenames
        for f in os.listdir(current_dir_path):
            if f.endswith(('.jpg', '.JPG', '.jpeg', '.png', '.webp')):
                images.append(f)
                if f == filename_end:  # if current is the chosen image - we remember it as the one to show first
                    current_image = index_filename
                index_filename += 1

        #loading_files(filename)
        # putting the image on screen
        show_image(current_image)
        next_ind, previous_ind = cycling_calculation()
        # Remapping the buttons to new images
        button_next = ttk.Button(options_frame, text="Next ->", command=lambda: next_image(next_ind))
        button_next.grid(row=2, column=2)
        button_back = ttk.Button(options_frame, text="<- Back", command=lambda: next_image(previous_ind))
        button_back.grid(row=2, column=0)
        root.bind("<Right>", lambda event: next_image(next_ind))
        root.bind("<Left>", lambda event: next_image(previous_ind))

        zoom_on.set(False)





def hide_menu():
    "function that minimizes the controls/options menu"
    global options_frame
    global hide_settings_button
    global hide_on
    global fullscreen_on
    global root

    if options_frame.winfo_ismapped():
        options_frame.grid_forget()
        hide_settings_button.configure(text="Min. Menu")
        if not fullscreen_on:
            root.geometry(f"{root.winfo_width()}x{root.winfo_height() - options_frame.winfo_height() + 12}")
        hide_on.set(True)
    else:
        options_frame.grid(row=3, column=1, columnspan= 2)
        hide_settings_button.configure(text="Std. Menu")
        if not fullscreen_on:
            root.geometry(f"{root.winfo_width()}x{root.winfo_height() + options_frame.winfo_height() - 12}")
        hide_on.set(False)


def fullscreen():
    "function that enters fullscreen mode"
    global fullscreen_on
    global old_position
    global hide_on
    global closing_frame
    global settings_frame
    global resize_widget
    global lock_on
    global monitor_width
    global monitor_height
    global zoom_hor_slider
    global zoom_ver_slider
    global canvas


    if fullscreen_on:  # Turning fullscreen off
        fullscreen_on = False
        root.unbind("<Escape>")
        settings_frame.grid(row=0, column=0, columnspan=3, sticky="nw")
        closing_frame.grid(row=0, column=1, columnspan=3, sticky="ne")
        resize_widget.grid(row=3, column=1, columnspan=3, ipadx=3, ipady=3, padx=2, pady=2, sticky="se")
        lock_on.set(False)
        zoom_hor_slider.grid_forget()
        zoom_ver_slider.grid_forget()

    else:  # Turning fullscreen on
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        fullscreen_on = True
        root.bind("<Escape>", lambda event: fullscreen())
        closing_frame.grid_forget()
        settings_frame.grid_forget()
        resize_widget.grid_forget()
        lock_on.set(True)
        zoom_hor_slider.grid_forget()
        zoom_ver_slider.grid_forget()

    if fullscreen_on and not hide_on.get():
        hide_menu()
    elif not fullscreen_on:
        hide_menu()

    show_image(current_image)

def resizing_press(event):
    "function that hides the buttons and replaces them with an image when the window is being resized (when the mouse is clicked)"
    global minimize_button
    global button_zoom_in
    global button_zoom_out
    global button_rotate_left
    global button_rotate_right
    global button_next
    global button_back
    global resizing_image
    global resizing_image2
    global options_frame
    global closing_frame
    global close_button
    global button_stop
    global label
    global label2
    global image_is_animation

    #pausing the animation
    if image_is_animation:
        stop_full()
        button_stop.destroy()

    #restoring the image label to put in place of the buttons (to improve perfomance)
    label = Label(options_frame, image=resizing_image, borderwidth=0)
    label2 = Label(closing_frame, image=resizing_image2, borderwidth=0)

    #deleting the buttons to improve perfomance and putting a label there
    button_zoom_in.destroy()
    button_zoom_out.destroy()
    button_rotate_right.destroy()
    button_rotate_left.destroy()
    button_next.destroy()
    button_back.destroy()
    close_button.destroy()
    minimize_button.destroy()
    label.grid(row=0, column=0, columnspan=3, rowspan=3)
    label2.grid(row=0, column=0, columnspan=2)

    # restoring the original options_frame size
    options_frame.config(padding = [3, 3, 3, 3])
    closing_frame.config(padding=[3, 3, 3, 3])
    checkbox_Lock.state(["selected"])
    lock_on.set(True)

    #depending on whether zoomed-in or not, the resize is different
    if zoom_on.get():
        resize_widget.bind("<B1-Motion>", resize_window_with_zoom)
    else:
        resize_widget.bind("<B1-Motion>", resize_window_no_zoom)

def resizing_release(event):
    "function that puts the buttons back (when the mouse is released)"
    global minimize_button
    global button_zoom_in
    global button_zoom_out
    global button_rotate_left
    global button_rotate_right
    global button_next
    global button_back
    global resizing_image
    global options_frame
    global closing_frame
    global close_button
    global button_stop
    global label
    global label2
    global root
    global lock_on
    global hide_on

    #resuming the animation, if it was not paused
    if image_is_animation:
        resume_stop_full()



    # deleting the label with image
    label.destroy()
    label2.destroy()
    # removing the options frame just in case
    options_frame.destroy()
    closing_frame.destroy()
    # restoring all the frames and buttons
    options_frame = ttk.Frame(root, relief="raised", padding=[10, 10, 10, 10])
    if not hide_on.get():
        options_frame.grid(row=3, column=1, sticky=S, columnspan= 2)
    closing_frame = ttk.Frame(root, relief="sunken", padding=[15, 10, 10, 10])
    closing_frame.grid(row=0, column=1, columnspan=3, sticky="ne")

    button_zoom_in = ttk.Button(options_frame, text="Zoom In", command=lambda: zoom(True))
    button_zoom_out = ttk.Button(options_frame, text="Zoom Out", command=lambda: zoom(False))
    button_rotate_right = ttk.Button(options_frame, text="Rotate right", command=lambda: rotate_image(True))
    button_rotate_left = ttk.Button(options_frame, text="Rotate left", command=lambda: rotate_image(False))
    button_zoom_in.grid(row=1, column=1, padx=5, pady=5)
    button_zoom_out.grid(row=2, column=1, padx=5)
    button_rotate_right.grid(row=1, column=2)
    button_rotate_left.grid(row=1, column=0, padx=5)
    close_button = ttk.Button(closing_frame, text='X', width=3, command=root.destroy)
    close_button.grid(row=0, column=1, padx=5, ipady=3)
    minimize_button = ttk.Button(closing_frame, text=' _ ', width=3,
                                 command=lambda a=root: custom_titlebar.minimize_me(root))
    minimize_button.grid(row=0, column=0, ipady=3)
    button_stop = ttk.Button(options_frame, text="Stop", command=stop)

    if image_is_animation:
        button_stop.grid(row=4, column=1)

    # using a function to determine which is the next and previous image
    next_ind, previous_ind = cycling_calculation()

    button_next = ttk.Button(options_frame, text="Next ->", command=lambda: next_image(next_ind))
    button_next.grid(row=2, column=2, padx=5)
    button_back = ttk.Button(options_frame, text="<- Back", command=lambda: next_image(previous_ind))
    button_back.grid(row=2, column=0, padx=5)




def resize_window_with_zoom(event):
    "Function for resizing the whole window (when the image was zoomed-in)"
    global options_frame
    global resizing_image
    global root
    global label
    global label2
    global canvas
    global zoom_ver_slider
    global zoom_hor_slider
    global hide_ong
    global zoom_on
    global actual_image
    global actual_image_height
    global actual_image_width
    global canvas_image_to_move

    #calculating the new window size
    ywin = root.winfo_y()
    difference_y = (event.y_root - ywin)
    xwin = root.winfo_x()
    difference_x = (event.x_root - xwin)

    if difference_x>563 and difference_y>147:
        try:
            image_coordinates = canvas.bbox(canvas_image_to_move)
            root.geometry(f"{difference_x}x{difference_y}")

            #calculations for when the zoomed image is smaller than the window
            if actual_image.width() <= canvas.winfo_width() or actual_image.height() <= canvas.winfo_height():
                canvas.coords(canvas_image_to_move, actual_image.width()/2, actual_image.height()/2)

            # resizing canvas and moving image along its Y axis
            if canvas.winfo_height() < actual_image.height():
                # y is the required movement value
                y = root.winfo_height() - zoom_hor_slider.winfo_height() - 158 - canvas.winfo_height()

                canvas.config(height=root.winfo_height() - zoom_hor_slider.winfo_height() - 158)

                zoom_ver_slider.grid(row=1, column=2, sticky=SW, rowspan=1)
                zoom_ver_slider.config(length=canvas.winfo_height())

                y_stop = abs(image_coordinates[1]) + abs(image_coordinates[3]) - canvas.winfo_height()
                if -y_stop <= image_coordinates[1] + y <= 0:
                    canvas.move(canvas_image_to_move, 0, y)
            else:
                # removing the slider if image becomes full-size
                zoom_ver_slider.grid_forget()

            # resizing canvas and moving image along its X axis
            if canvas.winfo_width() < actual_image.width():
                # x is the required movement value
                x = root.winfo_width() - zoom_ver_slider.winfo_width() - canvas.winfo_width()
                canvas.config(width=min((root.winfo_width() - zoom_ver_slider.winfo_width(), actual_image.width())))

                zoom_hor_slider.grid(row=2, column=1, sticky=NE)
                zoom_hor_slider.config(length=canvas.winfo_width())

                x_stop = abs(image_coordinates[0]) + abs(image_coordinates[2]) - canvas.winfo_width()

                if -x_stop <= image_coordinates[0] + x <= 0:

                    canvas.move(canvas_image_to_move, x, 0)

            else:
                zoom_hor_slider.grid_forget()

            if not hide_on.get():
                # only putting the options on screen if the user didn't hide them
                options_frame.grid(row=3, column=1, sticky=S, columnspan= 2)
                label = Label(options_frame, image=resizing_image, borderwidth=0)
                label.grid_forget()
                label.grid(row=0, column=0, columnspan=3, rowspan=3)

            label2 = Label(closing_frame, image=resizing_image2, borderwidth=0)
            label2.grid_forget()
            label2.grid(row=0, column=0, columnspan=2)
        except:
            pass


def resize_window_no_zoom(event):
    "Function for resizing the whole window (when the image is not zoomed-in)"
    global options_frame
    global resizing_image
    global root
    global label
    global label2
    global canvas
    global hide_on
    global zoom_on
    global actual_image
    global actual_image_height
    global actual_image_width

    #calculating the new window size
    ywin = root.winfo_y()
    difference_y = (event.y_root - ywin)
    xwin = root.winfo_x()
    difference_x = (event.x_root - xwin)

    if difference_x>563 and difference_y>147:
        try:
            root.geometry(f"{difference_x}x{difference_y}")
            show_image(current_image)

            if not hide_on.get():
                options_frame.grid(row=3, column=1, sticky=S, columnspan= 2)

                label = Label(options_frame, image=resizing_image, borderwidth=0)
                label.grid_forget()
                label.grid(row=0, column=0, columnspan=3, rowspan=3)

            label2 = Label(closing_frame, image=resizing_image2, borderwidth=0)
            label2.grid_forget()
            label2.grid(row=0, column=0, columnspan=2)
        except:
            pass


# Buttons when loading the program. If only one image in folder, the buttons are Disabled
amount_of_images = 2  #len(images)
if amount_of_images > 1:
    button_next = ttk.Button(options_frame, text="Next ->", command=lambda: next_image(1))
    button_next.grid(row=2, column=2, padx=5)
    button_back = ttk.Button(options_frame, text="<- Back", command=lambda: next_image(len(images) - 1))
    button_back.grid(row=2, column=0, padx=5)
else:
    button_next = ttk.Button(options_frame, text="Next ->", command=DISABLED)
    button_next.grid(row=2, column=2,padx=5)
    button_back = ttk.Button(options_frame, text="<- Back", command=DISABLED)
    button_back.grid(row=2, column=0, padx=5)

button_open = ttk.Button(settings_frame, text=" Open", width=5, command=open_image)
button_open.grid(row=0, column=0, ipady=3, padx=5)

root.bind("<Right>", lambda event: next_image(1))
root.bind("<Left>", lambda event: next_image(len(images) - 1))


button_zoom_in2 = ttk.Button(options_frame, text="Zoom In2", command=lambda: zoom_gif3(True))
button_zoom_in = ttk.Button(options_frame, text="Zoom In", command=lambda: zoom(True))
button_zoom_in.grid(row=1, column=1, padx=5, pady=5)
#button_zoom_in2.grid(row=3, column=2)

button_zoom_out = ttk.Button(options_frame, text="Zoom Out", command=lambda: zoom(False))
button_zoom_out.grid(row=2, column=1, padx=5)

button_rotate_right = ttk.Button(options_frame, text="Rotate right", command=lambda: rotate_image(True))
button_rotate_right.grid(row=1, column=2)

button_rotate_left = ttk.Button(options_frame, text="Rotate left", command=lambda: rotate_image(False))
button_rotate_left.grid(row=1, column=0, padx=5)

# checkbox that locks the window size
checkbox_frame = ttk.Frame(settings_frame, borderwidth=5, relief="sunken", style="check.TFrame")
checkbox_frame.grid(row=0, column=1,)
checkbox_Lock = ttk.Checkbutton(checkbox_frame, text=" Lock window", variable=lock_on, onvalue=True, offvalue=False)
checkbox_Lock.grid(row=0, column=1, ipadx=2, ipady=3)
checkbox_Lock.bind('<Enter>', lambda event, a = 'check': viewer_style.change_style(event, a, style))
checkbox_Lock.bind('<Leave>', lambda event, a = 'check': viewer_style.change_style_back(event, a, style))

img_unticked_box = ImageTk.PhotoImage(Image.open("uncheck2.png"))
img_ticked_box = ImageTk.PhotoImage(Image.open("check2.png"))
viewer_style.change_checkbutton(style, img_ticked_box, img_unticked_box)


zoom_hor_slider = ttk.Scale(root, from_=0, to=10, length=1, command=moving_pictures)
zoom_ver_slider = ttk.Scale(root, from_=0, to=10, length=1, command=moving_pictures)

root.bind("<Up>", lambda event: zoom(True))
root.bind("<Down>", lambda event: zoom(False))



button_stop = ttk.Button(options_frame, text="Stop", command=stop)
#button_stop.grid(row=1, column=4)

expand_button = ttk.Button(settings_frame, text=' Fullscreen ', width=9, command=fullscreen)#command=lambda a=root: custom_titlebar.maximize_me(a))
minimize_button = ttk.Button(closing_frame, text=' _ ', width=3, command=lambda a=root: custom_titlebar.minimize_me(root))

hide_settings_button = ttk.Button(settings_frame, text=' Std. Menu ', width=9, command=hide_menu)
hide_settings_button.grid(row=0, column=4, ipady=3)

expand_button.grid(row=0, column=3, ipady=3, padx=5)
minimize_button.grid(row=0, column=0, ipady=3)

settings_frame.bind('<Button-1>',lambda event, a=root, b=settings_frame: custom_titlebar.get_pos(event, a, b))  # so you can drag the window from the title bar
closing_frame.bind('<Button-1>',lambda event, a=root, b=closing_frame: custom_titlebar.get_pos(event, a, b))  # so you can drag the window from the title bar

root.bind("<FocusIn>", lambda event, a=root: custom_titlebar.deminimize(event, a))  # to view the window by clicking on the window icon on the taskbar
root.after(10, lambda: custom_titlebar.set_appwindow(root))  # to see the icon on the task bar

#button_next.configure(command=)


print(monitor_height, monitor_width)


resize_widget = ttk.Frame(root, cursor='sizing')

# loading the images of menus instead of them to improve perfomance during resizing the window
resizing_image = ImageTk.PhotoImage(Image.open("menu.png"))
resizing_image2 = ImageTk.PhotoImage(Image.open("close_menu.png"))
label = Label(options_frame, image=resizing_image, borderwidth=0)
label2 = Label(closing_frame, image=resizing_image2, borderwidth=0)


resize_widget.bind("<Button-1>", resizing_press)
resize_widget.bind("<ButtonRelease-1>", resizing_release)

resize_widget.grid(row=3, column=1, columnspan=3, ipadx=3, ipady=3, padx=2, pady=2, sticky="se")


zoom_ver_slider.bind("<Button-1>", stop_full)
zoom_hor_slider.bind("<Button-1>", stop_full)



root.mainloop()