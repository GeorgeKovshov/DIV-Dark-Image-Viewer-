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


image = Image.open(images[current_image]).resize((400, 400))
image1 = ImageTk.PhotoImage(image)

image1_label = Label(image=image1)
image1_label.grid(row=0, column=0, columnspan=3)

# storing current image in this variable, so garbage collector wouldn't get it
actual_image = image1


image2 = Image.open(images[1]).resize((400, 400))
image22 = ImageTk.PhotoImage(image2)



#photoss = ImageTk.PhotoImage(images[0])
#w = Canvas(root)
#w.create_image(0, 0, 50, 50, image=photoss)


def next_image(img_number):
    """function that loads and puts the picture with 'img_number' from 'images' list on screen"""
    global images
    global current_image
    global image1_label
    global image22
    global actual_image

    # Calculating the next image number in list
    current_image += (img_number - current_image)

    # Showing the current image index
    label2 = Label(root, text=current_image)
    label2.grid(row=2, column=0)


    # Replacing the old image with a new one
    image1_label.grid_forget()
    image_new = Image.open(images[current_image]).resize((400, 400))
    image1_new = ImageTk.PhotoImage(image_new)
    actual_image = image1_new
    image1_label = Label(image=actual_image)


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
    image1_label.grid(row=0, column=0, columnspan=3)
    button_next.grid(row=1, column=2)
    button_back = Button(root, text="<- Back", command=lambda: next_image(previous))
    button_back.grid(row=1, column=0)


def zoom(self):
    global images
    global current_image
    global image1_label
    global actual_image

    zoom_value = zoom_slider.get()

    # Try to put this into a button, maybe changing image while sliding is too taxing for tkinder
    image1_label.grid_forget()
    image_new = Image.open(images[current_image]).resize((600, 600))#resize((400 + (round(zoom_value)), (400 + round(zoom_value))))
    image1_new = ImageTk.PhotoImage(image_new)
    actual_image = image1_new
    image1_label = Label(image=actual_image)

    label = Label(root, text=zoom_value)
    label.grid(row=3, column=2)



#label = Label(root, text=images)
#label.grid(row=2, column=0)


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

zoom_slider = Scale(root, from_=0, to=400, orient=HORIZONTAL, command=zoom)
zoom_slider.grid(row=2, column=2)


root.mainloop()