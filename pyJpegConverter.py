#!/bin/env python

# import os for split path
import os
# import tkinter GUI lib
from tkinter import *
from tkinter import ttk # themed tk
from tkinter import filedialog # browse files
# import Pillow(PIL) image lib
from PIL import Image
from PIL import ImageFilter

# create an "application" class for create a frame in the main window
class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) # create a frame in root window
        self.grid() # create grid 
        self.button_clicks = 0 # counter of button clicks, useless
        self.create_widget() # call create_wiget function to add elements

    def create_widget(self):
        # create lable and buttons
        self.instruction = Label(self) # create a label
        self.instruction.pack()
        self.instruction["text"] = "select an image to be converted in jpeg format: " # add text in label
        self.instruction.grid(row=0, column=0, columnspan=2, sticky=W) # add label into the grid and positioning

        # entry for display the selected image path
        self.imgName = Entry(self) # create a text display area
        self.imgName.config(state='readonly') # make it non-editable
        self.imgName.grid(row=1,column=0,sticky=W) # add entry into grid and positioning

        # create browse button
        self.browseIMG = Button(self) # add "browse" button
        self.browseIMG["text"] = "browse" # text
        self.browseIMG["command"] = self.selectIMG # onclick, call function selectIMG
        self.browseIMG.grid(row=1,column=1,sticky=W); # add next to display entry

        # label + entry for define the convert quality
        self.qualbl = Label(self) # create text label
        self.qualbl.pack
        self.qualbl["text"] = "image quality(1-100): "  # add text
        self.qualbl.grid(row=2,column=0,sticky=W) # positioning
        self.imgQuality = Entry(self) # create entry for input quality 1-100
        self.imgQuality.config(width=3) # adjust entry width
        self.imgQuality.insert(0, "90") # default value 90
        self.imgQuality.grid(row=2,column=1,sticky=W) # positioning

        # create submit button, run convert func.
        self.submit_button = Button(self) # create a convert button
        self.submit_button["text"] = "Convert" # text of button
        self.submit_button["command"] = self.convertJPG # onclick, run convertJPG function
        self.submit_button.grid(row=4,column=1,sticky=W) # positioning

        # text box for display infomation
        self.text = Text(self, width=40, height=5, wrap=WORD) # add textbox area
        self.text.grid(row=3,column=0,columnspan=2,sticky=W) # positioning

    def convertJPG(self): # function for convert to JPEG
        self.text.delete(0.0, END) # clear the textbox area
        for path,size in self.selectedIMGs.items():
            #print(size)
            image = Image.open(path)
            if image.mode != 'RGBA' or image.mode != 'RGB': # check if image is not in RGM mode
                image = image.convert('RGB') # convert it to RGB for save as JPEG format later
            fileName = os.path.basename(path) # trim out the path, get filename
            print(fileName)
            imgname = fileName.split('.') # split the file by name + extention
            print(imgname)
            saveAs = imgname[0] + ".jpg" # new file name

            qualvl = int(self.imgQuality.get()) # get the quality value

            image.save(saveAs,'JPEG',quality=qualvl) # convert and save it

            self.text.insert(END, "selected image saved as " +  saveAs + "\n") # display info

            self.convertedSize = os.path.getsize(saveAs) # get size of new converted file
            compressRatio = round(size / self.convertedSize,3) # get compress ratio
            self.text.insert(END, "ratio: " + 
                    str(size) + "/" + str(self.convertedSize) + 
                    "=" + str(compressRatio) + "\n" ) # display result
    
    def selectIMG(self): # function for select target image
        self.imgName.delete(0,END) # clear entry area        
        path = filedialog.askopenfilenames( filetypes = 
                [
                    ("image files", "*.png *.gif *.bmp"),
                    ("All files", "*.*")                              
                ] )

        self.selectedIMGs = {}

        for img in path:
            oriSize = os.path.getsize(img) # size of target file
            self.selectedIMGs[img]=oriSize # add into the dictionary
            fileName = os.path.basename(img) # get the filename
            #print(fileName)
            self.imgName.configure(state="normal") # entry writable
            self.imgName.insert(END, fileName + ";")  # insert the image path
            self.imgName.configure(state="readonly") # disable entry
            self.text.insert(END,fileName+":"+str(oriSize)+"bytes\n") #display selected size

        return self.selectedIMGs

# create main window
root = Tk()

# add title
root.title("jpeg converter")

# window size
root.geometry("300x200")

# create a frame in the main window
app = Application(root)

# main loop
root.mainloop()
