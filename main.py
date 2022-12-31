import sys
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os

root = Tk()
root.title("Images")
# root.configure(background="gray")

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
    if direction:
        rotation += 1
        if rotation > 2:
            rotation = -1
    else:
        rotation -= 1
        if rotation < -1:
            rotation = 2
    show_image(current_image)



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
    else:
        size_of_image_new = lock_on_size_reshape(image_for_canvas_new.height, image_for_canvas_new.width,
                                                 canvas.winfo_height(), canvas.winfo_width())

    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new
    canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2, anchor=CENTER, image=image1_new)
    canvas.grid(row=0, column=0, columnspan=3)





# Initializing canvas for images to be put into
canvas = tkinter.Canvas(root, height=1, width=1)
canvas.grid(row=0, column=0, columnspan=3)
# Loading the first image
if images:
    show_image(current_image)
#actual_image = ImageTk.PhotoImage()


# storing current image in this variable, so garbage collector wouldn't get it
# actual_image = image1



def next_image(img_number):
    """function that loads and puts the picture with 'img_number' from 'images' list on screen"""
    global images
    global current_image
    global canvas
    global rotation
    global actual_image

    # Calculating the next image number in list
    current_image += (img_number - current_image)

    # Resetting rotation
    rotation = 0

    # Showing the current image index
    label2 = Label(root, text=current_image)
    label2.grid(row=2, column=0)


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
    button_next = Button(root, text="Next ->", command=lambda: next_image(next))
    button_next.grid(row=1, column=2)
    button_back = Button(root, text="<- Back", command=lambda: next_image(previous))
    button_back.grid(row=1, column=0)



def zoom(var):
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

    size_of_image = (actual_image.height(), actual_image.width())
    # if zooming in then first part, if zooming out then second
    if var == 1:
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

    size_of_image_new = (image_for_canvas_new.height, image_for_canvas_new.width)
    size_of_canvas_new = size_of_image_new
    if not lock_on.get():
        # if zoomed-in image gets bigger than monitor, function stops expanding window; the image within canvas always expands
        if size_of_canvas_new[0] > monitor_height - 100 or size_of_canvas_new[1] > monitor_width - 100:
            #print("image: ", size_of_image_new, " canvas old: ", size_of_canvas_new)
            size_of_canvas_new = canvas_reshape(size_of_canvas_new[0], size_of_canvas_new[1],
                                                     monitor_height - 180, monitor_width - 180)
            #checkbox_Lock.select()
            #print("image: ", size_of_image_new, " canvas new: ", size_of_canvas_new)
        canvas.config(height=size_of_canvas_new[0], width=size_of_canvas_new[1])
    print(size_of_image_new[0]/size_of_image_new[1])
    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new
    canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2, anchor=CENTER, image=image1_new)
    canvas.grid(row=0, column=0, columnspan=3)
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
                                                filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
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
            if f.endswith('.jpg'):
                images.append(f)
                if f == filename_end:  # if current is the chosen image - we remember it as the one to show first
                    current_image = index_filename
                index_filename += 1

        # putting the image on screen
        show_image(current_image)


#label = Label(root, text=)
#label.grid(row=3, column=0)


# Buttons when loading the program. If only one image in folder, the buttons are Disabled
amount_of_images = 2  #len(images)
if amount_of_images > 1:
    button_next = Button(root, text="Next ->", command=lambda: next_image(1))
    button_next.grid(row=1, column=2)
    button_back = Button(root, text="<- Back", command=lambda: next_image(len(images) - 1))
    button_back.grid(row=1, column=0)
else:
    button_next = Button(root, text="Next ->", command=DISABLED)
    button_next.grid(row=1, column=2)
    button_back = Button(root, text="<- Back", command=DISABLED)
    button_back.grid(row=1, column=0)

button_open = Button(root, text="open image", command=open_image)
button_open.grid(row=1, column=1)





button_zoom = Button(root, text="Zoom In", command=lambda: zoom(1))
button_zoom.grid(row=2, column=2)

button_zoom = Button(root, text="Zoom Out", command=lambda: zoom(0))
button_zoom.grid(row=2, column=0)

button_zoom = Button(root, text="Rotate right", command=lambda: rotate_image(True))
button_zoom.grid(row=3, column=2)

button_zoom = Button(root, text="Rotate left", command=lambda: rotate_image(False))
button_zoom.grid(row=3, column=0)

checkbox_Lock = Checkbutton(root, text="Lock window size", variable=lock_on, onvalue=True, offvalue=False)
checkbox_Lock.deselect()
checkbox_Lock.grid(row=3, column=1)

print(monitor_height, monitor_width)


root.mainloop()