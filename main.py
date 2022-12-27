from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
root.title("Images")

images=[]

for f in os.listdir('.'):
    if f.endswith('.jpg'):
        images.append(f)

#global current_image - use 'global' only in functions, not here
current_image = 0


image = Image.open(images[0]).resize((400, 400))
image1 = ImageTk.PhotoImage(image)
actual_image = image1
image1_label = Label(image=image1)
image1_label.grid(row=0, column=0, columnspan=3)

image2 = Image.open(images[1]).resize((400, 400))
image22 = ImageTk.PhotoImage(image2)



#photoss = ImageTk.PhotoImage(images[0])

#w = Canvas(root)
#w.create_image(0, 0, 50, 50, image=photoss)


def next_image(img_number):
    global images
    global current_image
    global image1_label
    global image22
    global actual_image
    #current_image += 1
    #label2 = Label(root, text=current_image)
    #label2.grid(row=0, column=0)


    #root.forget(image1_label)
    image1_label.grid_forget()
    image_new = Image.open(images[img_number-1]).resize((400, 400))
    image1_new = ImageTk.PhotoImage(image_new)
    actual_image = image1_new
    image1_label = Label(image=actual_image)

    button_next = Button(root, text="Next ->", command=lambda: next_image(img_number + 1))
    image1_label.grid(row=0, column=0, columnspan=3)
    button_next.grid(row=1, column=1)




#label = Label(root, text=images)
#label.grid(row=2, column=0)



button_next = Button(root, text="Next ->", command=lambda: next_image(2))
button_next.grid(row=1, column=1)

button_delete = Button(root, text="hide image")
button_delete.grid(row=1, column=2)


root.mainloop()