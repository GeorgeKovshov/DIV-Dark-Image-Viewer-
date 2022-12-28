import tkinter
from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
root.title("Images")


#Creating a list of image file names
images=[]
for f in os.listdir('.'):
    if f.endswith('.jpg'):
        images.append(f)

#global current_image - use 'global' only in functions, not here
current_image = 0

# Getting the monitor screen height and width

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()


def max_size_reshape(height, width):
    """function to check the image size and reshape it to fit into the monitor"""
    if height < (monitor_height - 400) and width < (monitor_width - 400):
        return height, width
    else:
        return max_size_reshape(height//2, width//2)


"""
# Loading the first image

image = Image.open(images[current_image]).resize((400, 400))
image1 = ImageTk.PhotoImage(image)

image1_label = Label(image=image1)
image1_label.grid(row=0, column=0, columnspan=3)
"""

# Initializing canvas for images to be put into
canvas = tkinter.Canvas(root, height=1, width=1)
canvas.grid(row=0, column=0, columnspan=3)

# Loading the first image
image_for_canvas = Image.open(images[current_image])
size_of_image = max_size_reshape(image_for_canvas.height, image_for_canvas.width)
canvas.config(height=size_of_image[0], width=size_of_image[1])
image1 = ImageTk.PhotoImage(image_for_canvas.resize((size_of_image[1], size_of_image[0])))
image = canvas.create_image(size_of_image[1]/2, size_of_image[0]/2, anchor=CENTER, image=image1)


# storing current image in this variable, so garbage collector wouldn't get it
actual_image = image1






#photoss = ImageTk.PhotoImage(images[0])
#w = Canvas(root)
#w.create_image(0, 0, 50, 50, image=photoss)


def next_image(img_number):
    """function that loads and puts the picture with 'img_number' from 'images' list on screen"""
    global images
    global current_image
    global canvas
    global actual_image

    # Calculating the next image number in list
    current_image += (img_number - current_image)

    # Showing the current image index
    label2 = Label(root, text=current_image)
    label2.grid(row=2, column=0)


    # Replacing the old image with a new one
    """
    image1_label.grid_forget()
    image_new = Image.open(images[current_image]).resize((400, 400))
    image1_new = ImageTk.PhotoImage(image_new)
    actual_image = image1_new
    image1_label = Label(image=actual_image)
    """
    image_for_canvas_new = Image.open(images[current_image])
    size_of_image_new = max_size_reshape(image_for_canvas_new.height, image_for_canvas_new.width)
    canvas.config(height=size_of_image_new[0], width=size_of_image_new[1])
    image1_new = ImageTk.PhotoImage(image_for_canvas_new.resize((size_of_image_new[1], size_of_image_new[0])))
    actual_image = image1_new
    image_new = canvas.create_image(size_of_image_new[1] / 2, size_of_image_new[0] / 2, anchor=CENTER, image=image1_new)
    canvas.grid(row=0, column=0, columnspan=3)

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
    """function that resizes an image based on the slider value"""
    global images
    global current_image
    global image1_label
    global actual_image


    size_of_image = (actual_image.height(), actual_image.width())

    image1_label.grid_forget()
    if var == 1:
        image_new = Image.open(images[current_image]).resize((round(size_of_image[0] * 1.5), round((size_of_image[1] * 1.5))))
    else:
        image_new = Image.open(images[current_image]).resize((round(size_of_image[0] * 0.75), round((size_of_image[1] * 0.75))))
    image1_new = ImageTk.PhotoImage(image_new)
    actual_image = image1_new
    image1_label = Label(image=actual_image)
    image1_label.grid(row=0, column=0, columnspan=3)

    label = Label(root, text=size_of_image)
    label.grid(row=3, column=0)




#label = Label(root, text=str(root.winfo_screenwidth()) + " " + str(root.winfo_screenheight()))
#label.grid(row=3, column=0)

#label = Label(root, text=)
#label.grid(row=3, column=0)


# Buttons when loading the program. If only one image in folder, the buttons are Disabled
amount_of_images = len(images)
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

button_delete = Button(root, text="hide image")
button_delete.grid(row=1, column=1)


zoom_slider = Scale(root, from_=0, to=400, orient=HORIZONTAL)
zoom_slider.grid(row=2, column=1)


button_zoom = Button(root, text="Zoom In", command=lambda: zoom(1))
button_zoom.grid(row=2, column=2)

button_zoom = Button(root, text="Zoom Out", command=lambda: zoom(0))
button_zoom.grid(row=2, column=0)


root.mainloop()