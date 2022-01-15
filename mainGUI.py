from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from skimage.metrics import structural_similarity as ssim
import imutils
import cv2


#place an image on the grid
def display_logo(url, row, column):
    img = Image.open(url)
    img = img.resize((int(img.size[0]/1.5),int(img.size[1]/1.5)))
    img = ImageTk.PhotoImage(img)
    img_label = Label(image=img, bg="white")
    img_label.image = img
    img_label.grid(column=column, row=row, rowspan=4, sticky=NW, padx=20, pady=40)


def display_image(path):
    img = Image.open(path)
    img = img.resize((400,400))
    show_img = ImageTk.PhotoImage(img)
    show_img_label = Label( image=show_img)
    show_img_label.configure(image=show_img)
    show_img_label.image = show_img
    return show_img_label



#initiallize a Tkinter r_gui object
r_gui = Tk()
r_gui.geometry('+%d+%d'%(350,10)) #place GUI at x=350, y=10


#open an image file
def open_image():
    global img_file1
    browse_text.set("Opening...")
    img_file1 = askopenfile( filetypes=[( 'Only PNG and JPG', '*.png;*.jpg')])
    if img_file1:
        print("Image Opened", img_file1.name)  
        path = img_file1.name
        img1 = display_image(path)
        img1.grid(row=7, column=0, rowspan=3)
        browse_text.set("Image Selected")
    else:
        browse_text.set("Browse")


#open an image2 file
def open_image2():
    global img_file2
    browse_text2.set("Opening...")
    img_file2 = askopenfile( filetypes=[( 'Only PNG and JPG', '*.png;*.jpg')])
    if img_file2:
        print("Image Opened", img_file2.name)  
        path = img_file2.name   
        img2 = display_image(path)
        img2.grid(row=7, column=2, rowspan=3)
        browse_text2.set("Image Selected")
    else:
        browse_text2.set("Browse")

#compare the two images
def compare_images():
    path1 = img_file1.name
    path2 = img_file2.name
    image_one = cv2.imread(path1)
    image_two = cv2.imread(path2)

    gray1 = cv2.cvtColor(image_one, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image_two, cv2.COLOR_BGR2GRAY)

    (score, diff) = ssim(gray1, gray2, full=True)
    diff=(diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    thresh = cv2.threshold(diff, 0, 128, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    no_of_differences = 0
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        rect_area = w*h
        if rect_area > 10:
            no_of_differences += 1
            cv2.rectangle(image_one, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(image_two, (x, y), (x + w, y + h), (0, 0, 255), 2)

    print("nod : ",no_of_differences)

    # show the output images
    cv2.imwrite("Original.png", image_one)
    cv2.imwrite("Modified.png", image_two)
    img1 = display_image("Original.png")
    img1.grid(row=7, column=0, rowspan=3)
    img2 = display_image("Modified.png")
    img2.grid(row=7, column=2, rowspan=3)
    nofdiff = Label(r_gui, text="Number of Differences : {}".format(no_of_differences), font=("Roboto", 15), fg="white", bg="#a16200")
    nofdiff.grid(row=8, column=1, padx=20)



#header area - logo & browse button
header = Frame(r_gui, width=1200, height=200, bg="white")
header.grid(columnspan=3, rowspan=4, row=0)

#main content area - text and image extraction
main_content = Frame(r_gui, width=1200, height=600, bg="#a16200")
main_content.grid(columnspan=6, rowspan=4, row=7)




#BEGIN INITIAL APP COMPONENTS
display_logo('logo.png', 0, 0)

#instructions
instructions = Label(r_gui, text="Select 1st Image File", font=("Ubuntu", 10), bg="white")
instructions.grid(column=2, row=0, sticky=SE, padx=75, pady=5)
instructions2 = Label(r_gui, text="Select 2nd Image File", font=("Ubuntu", 10), bg="white")
instructions2.grid(column=2, row=2, sticky=SE, padx=75, pady=5)

#browse button
browse_text = StringVar()
browse_text2 = StringVar()
browse_btn = Button(r_gui, textvariable=browse_text,command=open_image, font=("Raleway",12), bg="#02ac00", fg="white", height=1, width=15)
browse_btn2 = Button(r_gui, textvariable=browse_text2,command=open_image2, font=("Raleway",12), bg="#02ac00", fg="white", height=1, width=15)
browse_text.set("Browse")
browse_text2.set("Browse")
browse_btn.grid(column=2, row=1, sticky=NE, padx=50)
browse_btn2.grid(column=2, row=3,sticky=NE, padx=50)


#main button
main_button_text = StringVar()
main_button_text.set("Spot It!")
main_button = Button(r_gui, textvariable=main_button_text,command=compare_images, font=("Ubuntu",12), bg="#02ac00", fg="white", height=1, width=30)
main_button.grid(column=1, row=7, padx=20)











r_gui.mainloop()