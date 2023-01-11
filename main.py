import sys
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import time
import os

root = Tk()
root.title("Images")
root.configure(background="#121212")
# root.configure(background="gray")
options_frame = Frame(root, relief="raised", bd=5)
settings_frame = Frame(root, relief="sunken", bd=1)
options_frame.grid(row=3, column=2)
settings_frame.grid(row=0, column=0, columnspan=4, sticky=W)
Grid.rowconfigure(root, 0, weight=0)
Grid.rowconfigure(root, 1, weight=1)
Grid.columnconfigure(root, 0, weight=1000)
Grid.columnconfigure(root, 1, weight=1)
Grid.columnconfigure(root, 2, weight=1)
Grid.columnconfigure(root, 3, weight=1)
Grid.columnconfigure(root, 4, weight=1)
Grid.columnconfigure(root, 5, weight=1000)
#Grid.columnconfigure(root,4, weight=1)


# storing the current image directory path
current_dir_path = os.getcwd()

# Creating a list of image file names
images=[]
for f in os.listdir('.'):
    if f.endswith('.jpg'):
        images.append(f)

# global current_image - use 'global' only in functions, not here
current_image = 0

# variable for window size lock
lock_on = BooleanVar()

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
    if height < (monitor_height - 400) and width < (monitor_width - 400):
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
            return canv_height, round(width * (canv_height / height))
        else:
            return round(height * (canv_width / width)), canv_width



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
    """
    if is_horizontal:
        canvas.move(canvas_image_to_move, zoom_hor_slider.get() - moving_shift_X, zoom_ver_slider.get() - moving_shift_Y)
        moving_shift_X = zoom_hor_slider.get()
    else:
        canvas.move(canvas_image_to_move, 0, )
        moving_shift_Y = zoom_ver_slider.get()
    """
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
    #if abs(moving_shift_Y - e.y) > 200 or moving_shift_Y == 0:
    #    moving_shift_Y = e.y - canvas.winfo_height() / 2 - 1
    #if abs(moving_shift_X - e.x) > 200 or moving_shift_X == 0:
    #    moving_shift_X = e.x - canvas.winfo_width() / 2 - 1
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
    """Testing version
    if -y_stop <= image_coordinates[1] + y_movement <= 0:
        if abs(y_movement) < 15:
            canvas.move(canvas_image_to_move, 0, y_movement)
        elif y_movement > 0:
            canvas.move(canvas_image_to_move, 0, 0)
        elif y_movement < 0:
            canvas.move(canvas_image_to_move, 0, -0)
    if -x_stop <= image_coordinates[0] + x_movement <= 0:
        if abs(x_movement) < 15:
            canvas.move(canvas_image_to_move, x_movement, 0)
        elif x_movement > 0:
            canvas.move(canvas_image_to_move, 0, 0)
        elif x_movement < 0:
            canvas.move(canvas_image_to_move, -0, 0)
    """
    """
    if abs(y_movement) and < 15 -y_stop <= image_coordinates[1] + y_movement <= 0:
        canvas.move(canvas_image_to_move, 0, y_movement)
    if abs(x_movement) and-x_stop <= image_coordinates[0] + x_movement <= 0:
        canvas.move(canvas_image_to_move, x_movement, 0)
    Working version"""
    # We only move the image if it's not getting out of bounds of canvas, moving shift !=0 here is the measure against jugged movement
    if -y_stop <= image_coordinates[1] + y_movement <= 0 and moving_shift_Y != 0:
        canvas.move(canvas_image_to_move, 0, y_movement)
        zoom_ver_slider.set(zoom_ver_slider.get() + y_movement)
    if -x_stop <= image_coordinates[0] + x_movement <= 0 and moving_shift_X != 0:
        canvas.move(canvas_image_to_move, x_movement, 0)
        zoom_hor_slider.set(zoom_hor_slider.get() + x_movement)

    #print("x: ", e.x, "y:", e.y, "moving X:", moving_shift_X, "moving Y:", moving_shift_Y)
    # storing the old coordinates for next iteration
    moving_shift_X = e.x
    moving_shift_Y = e.y
    #print(canvas.bbox(canvas_image_to_move))
    #canvas.move(canvas_image_to_move, e.x - actual_image.width()/2 - moving_shift_X, e.y - actual_image.height()/2 - moving_shift_Y)
    #print("x: ", e.x, "y:", e.y)
    #moving_shift_X = e.x - actual_image.width()/2
    #moving_shift_Y = e.y - actual_image.height()/2



def show_image(img_number):
    """function to show an image from the list with img_number index"""
    global images
    global canvas
    global lock_on
    global rotation
    global current_dir_path
    global actual_image #without storing image here, garbage collector takes the image away

    image_for_canvas_new = Image.open(current_dir_path + "/" + images[img_number])

    # rotating image if its rotated
    if rotation == 1:
        image_for_canvas_new = image_for_canvas_new.rotate(-90)
    elif rotation == -1:
        image_for_canvas_new = image_for_canvas_new.rotate(90)
    elif rotation == 2:
        image_for_canvas_new = image_for_canvas_new.rotate(180)

    # if the window is locked, fit the image in window
    # else fit it and window into the monitor
    if not lock_on.get():
        size_of_image_new = max_size_reshape(image_for_canvas_new.height, image_for_canvas_new.width)
        canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
        root.geometry("")
    else:
        size_of_image_new = lock_on_size_reshape(image_for_canvas_new.height, image_for_canvas_new.width,
                                                 canvas.winfo_height(), canvas.winfo_width())

    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new
    canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2, image=image1_new)
    canvas.grid(row=1, column=1, columnspan=3)







# Initializing canvas for images to be put into
canvas = tkinter.Canvas(root, height=1, width=1)
canvas.configure(background="#121212")
canvas_image_to_move = canvas.create_image(1, 1)
canvas.grid(row=1, column=1, columnspan=3)
# Loading the first image
if images:
    show_image(current_image)
#actual_image = ImageTk.PhotoImage()


# storing current image in this variable, so garbage collector wouldn't get it
actual_image



def next_image(img_number):
    """function that loads and puts the picture with 'img_number' from 'images' list on screen"""
    global images
    global current_image
    global canvas
    global rotation
    global actual_image
    global zoom_ver_slider
    global zoom_hor_slider

    # Calculating the next image number in list
    current_image += (img_number - current_image)

    # Resetting rotation
    rotation = 0

    # Removing the sliders if they are there
    zoom_ver_slider.grid_forget()
    zoom_hor_slider.grid_forget()

    # Showing the current image index
    label2 = Label(root, text=current_image)
    label2.grid(row=4, column=1)


    # Replacing the old image with a new one
    show_image(current_image)
    # Making the image viewer cycle through images
    next, previous = 0, 0
    length_of_image_list = len(images)
    if current_image + 2 > length_of_image_list:
        previous = current_image - 1
    elif current_image - 1 < 0:
        next = current_image + 1
        previous = length_of_image_list - 1
    else:
        next = current_image + 1
        previous = current_image - 1

    # Remapping the buttons to new images
    button_next = Button(options_frame, text="Next ->", command=lambda: next_image(next))
    button_next.grid(row=2, column=2)
    button_back = Button(options_frame, text="<- Back", command=lambda: next_image(previous))
    button_back.grid(row=2, column=0)



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

    size_of_image = (actual_image.height(), actual_image.width())
    # if zooming in then first part, if zooming out then second
    if is_zoom_in:
        image_for_canvas_new = Image.open(current_dir_path + "/" + images[current_image]).resize(
            (round(size_of_image[1] * 1.5), round(size_of_image[0] * 1.5)))
    else:
        image_for_canvas_new = Image.open(current_dir_path + "/" + images[current_image]).resize(
            (round(size_of_image[1] * 0.75), round(size_of_image[0] * 0.75)))


    # rotating image if its rotated
    if rotation == 1:
        image_for_canvas_new = image_for_canvas_new.rotate(-90)
    elif rotation == -1:
        image_for_canvas_new = image_for_canvas_new.rotate(90)
    elif rotation == 2:
        image_for_canvas_new = image_for_canvas_new.rotate(180)

    zoom_ver_slider.grid_forget()
    zoom_hor_slider.grid_forget()
    size_of_image_new = (image_for_canvas_new.height, image_for_canvas_new.width)
    size_of_canvas_new = size_of_image_new


    if not lock_on.get():
        # if zoomed-in image gets bigger than monitor, function stops expanding window; the image within canvas always expands
        if size_of_canvas_new[0] > monitor_height - 100 or size_of_canvas_new[1] > monitor_width - 100:
            #print("image: ", size_of_image_new, " canvas old: ", size_of_canvas_new)
            size_of_canvas_new = canvas_reshape(size_of_canvas_new[0], size_of_canvas_new[1],
                                                     monitor_height - 180, monitor_width - 180)
            moving_shift_X = 0
            moving_shift_Y = 0
            # we only put the sliders and activate the mouse movement function when image is zoomed-in
            canvas.bind("<B1-Motion>", moving_mouse)
            canvas.bind("<ButtonRelease-1>", mouse_release)
            zoom_ver_slider = Scale(root, from_=0, to=-size_of_image_new[0] + size_of_canvas_new[0],
                                    length=size_of_canvas_new[0], showvalue=0, command=moving_pictures)
            zoom_ver_slider.grid(row=1, column=4)
            zoom_hor_slider = Scale(root, from_=0, to=-size_of_image_new[1] + size_of_canvas_new[1],
                                    length=size_of_canvas_new[1], orient="horizontal", showvalue=0, command=moving_pictures)
            zoom_hor_slider.grid(row=2, column=1, columnspan=3)
        canvas.config(height=size_of_canvas_new[0], width=size_of_canvas_new[1])
    else:
        moving_shift_X = 0
        moving_shift_Y = 0
        # we only put the sliders and activate the mouse movement function when image is zoomed-in
        canvas.bind("<B1-Motion>", moving_mouse)
        canvas.bind("<ButtonRelease-1>", mouse_release)
        zoom_ver_slider = Scale(root, from_=0, to=-size_of_image_new[0] + size_of_canvas_new[0],
                                length=canvas.winfo_height(), showvalue=0, command=moving_pictures)
        zoom_ver_slider.grid(row=1, column=4)
        zoom_hor_slider = Scale(root, from_=0, to=-size_of_image_new[1] + size_of_canvas_new[1],
                                length=canvas.winfo_width(), orient="horizontal", showvalue=0, command=moving_pictures)
        zoom_hor_slider.grid(row=2, column=1, columnspan=3)

    print(size_of_image_new[0], " ", size_of_image_new[1])
    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new
    canvas_image_to_move = canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2, anchor=CENTER, image=image1_new)
    canvas.grid(row=1, column=1, columnspan=3)
    print(canvas.bbox(canvas_image_to_move))
    print(canvas.winfo_height(), " ",  canvas.winfo_width())
    #zoom_slider = Scale(root, from_=0, to=400, length=canvas.winfo_height())
    #zoom_slider.grid(row=0, column=3)



def open_image():
    """function that allows the user to choose a picture on their computer"""
    global images
    global current_image
    global current_dir_path

    # handling the error of not choosing a file
    try:
        filename = filedialog.askopenfilename(initialdir=current_dir_path, title="Choose an image",
                                                filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"),
                                                           ("webp files", "*.webp"), ("all files", "*.*")))
    except FileNotFoundError as err:
        print("Error", err)
        filename = ""

    print("filename "+ filename)
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
            if f.endswith(('.jpg', '.JPG', '.png', '.webp')):
                images.append(f)
                if f == filename_end:  # if current is the chosen image - we remember it as the one to show first
                    current_image = index_filename
                index_filename += 1

        # putting the image on screen
        show_image(current_image)

def show_gif():
    """function for playing a gif"""



#label = Label(root, text=)
#label.grid(row=3, column=0)


# Buttons when loading the program. If only one image in folder, the buttons are Disabled
amount_of_images = 2  #len(images)
if amount_of_images > 1:
    button_next = Button(options_frame, text="Next ->", command=lambda: next_image(1))
    button_next.grid(row=2, column=2)
    button_back = Button(options_frame, text="<- Back", command=lambda: next_image(len(images) - 1))
    button_back.grid(row=2, column=0)
else:
    button_next = Button(options_frame, text="Next ->", command=DISABLED)
    button_next.grid(row=2, column=2)
    button_back = Button(options_frame, text="<- Back", command=DISABLED)
    button_back.grid(row=2, column=0)

button_open = Button(options_frame, text="open image", command=open_image)
button_open.grid(row=2, column=1)





button_zoom = Button(options_frame, text="Zoom In", command=lambda: zoom(True))
button_zoom.grid(row=1, column=1)

button_zoom = Button(options_frame, text="Zoom Out", command=lambda: zoom(False))
button_zoom.grid(row=3, column=1)

button_rotate_right = Button(options_frame, text="Rotate right", command=lambda: rotate_image(True))
button_rotate_right.grid(row=1, column=0)

button_rotate_left = Button(options_frame, text="Rotate left", command=lambda: rotate_image(False))
button_rotate_left.grid(row=1, column=2)

checkbox_Lock = Checkbutton(settings_frame, text="Lock window size", variable=lock_on, onvalue=True, offvalue=False)
checkbox_Lock.deselect()
checkbox_Lock.grid(row=4, column=1)

zoom_hor_slider = Scale(root, from_=0, to=10, length=1, command=moving_pictures)
zoom_ver_slider = Scale(root, from_=0, to=10, length=1, command=moving_pictures)

print(monitor_height, monitor_width)


root.mainloop()