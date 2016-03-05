#!/bin/env python

"""
This simple program does not under any licenses.
This is just an assignment and for educational purpose only.
Feel free to edit the code to suit yourself
"""

# import os for split path
import os
# import tkinter GUI lib
from tkinter import *
from tkinter import ttk # themed tk
from tkinter import filedialog # browse files
# import Pillow(PIL) image lib
from PIL import Image
from PIL import ImageFilter  # for Blur etc...
from PIL import ImageEnhance # for adjust brightness,contrast etc...
# for histogram
from PIL import ImageDraw

# create an "application" class for create a frame in the main window
class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) # create a frame in root window
        self.grid() # create grid 
        self.button_clicks = 0 # counter of button clicks, useless
        self.create_widget() # call create_wiget function to add elements

    def create_widget(self): # create all buttons,labels,textbox etc...
        # create lable and buttons
        self.instruction = Label(self) # create a label        
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
        self.qualbl["text"] = "image quality(1-100): "  # add text
        self.qualbl.grid(row=2,column=0,sticky=W) # positioning
        self.imgQuality = Entry(self) # create entry for input quality 1-100
        self.imgQuality.config(width=3) # adjust entry width
        self.imgQuality.insert(0, "90") # default value 90
        self.imgQuality.grid(row=2,column=1,sticky=W) # positioning
        
        # label + entry for adjust brighness
        self.brightnesslbl = Label(self) # create text label        
        self.brightnesslbl["text"] = "brightness(1-10): "  # add text
        self.brightnesslbl.grid(row=3,column=0,sticky=W) # positioning
        self.brightlvl = Entry(self) # create entry for input brighness 1-10
        self.brightlvl.config(width=3) # adjust entry width
        self.brightlvl.insert(0, "4") # default value 4
        self.brightlvl.grid(row=3,column=1,sticky=W) # positioning
        
        # label + entry for adjust contrast
        self.contrastlbl = Label(self) # create text label        
        self.contrastlbl["text"] = "contrast(1-10): "  # add text
        self.contrastlbl.grid(row=4,column=0,sticky=W) # positioning
        self.contrastlvl = Entry(self) # create entry for input contrast 1-10
        self.contrastlvl.config(width=3) # adjust entry width
        self.contrastlvl.insert(0, "4") # default value 4
        self.contrastlvl.grid(row=4,column=1,sticky=W) # positioning
        
        # label + entry for adjust sharpness
        self.sharpnesslbl = Label(self) # create text label        
        self.sharpnesslbl["text"] = "sharpness(1-10): "  # add text
        self.sharpnesslbl.grid(row=5,column=0,sticky=W) # positioning
        self.sharpnesslvl = Entry(self) # create entry for input contrast 1-10
        self.sharpnesslvl.config(width=3) # adjust entry width
        self.sharpnesslvl.insert(0, "4") # default value 4
        self.sharpnesslvl.grid(row=5,column=1,sticky=W) # positioning
        
        # label + entry for adjust colour
        self.colourlbl = Label(self) # create text label        
        self.colourlbl["text"] = "colour(1-10): "  # add text
        self.colourlbl.grid(row=6,column=0,sticky=W) # positioning
        self.colourlvl = Entry(self) # create entry for input contrast 1-10
        self.colourlvl.config(width=3) # adjust entry width
        self.colourlvl.insert(0, "4") # default value 4
        self.colourlvl.grid(row=6,column=1,sticky=W) # positioning

        # text box for display infomation
        self.text = Text(self, width=40, height=5, wrap=WORD) # add textbox area
        self.text.grid(row=7,column=0,columnspan=3,sticky=W) # positioning
   
        # entry for set the convert destination and "save in" button
        self.destination = Entry(self)
        self.destination.insert(0,os.getcwd())
        self.destination.grid(row=8,column=0,sticky=W)
        self.saveIn = Button(self, text="Save Path")
        self.saveIn["command"] = self.savePath
        self.saveIn.grid(row=8,column=1,sticky=W)

        # for histogram
        self.histogram_button = Button(self) # create a convert button
        self.histogram_button["text"] = "View Histogram" # text of button
        self.histogram_button["command"] = self.showHistogram # onclick, run convertJPG function
        self.histogram_button.grid(row=9,column=0,sticky=W) # positioning
        # create preview button, run preview func.        
        self.preview_button = Button(self) # create a convert button
        self.preview_button["text"] = "Preview" # text of button
        self.preview_button["command"] = self.previewIMG # onclick, run convertJPG function
        self.preview_button.grid(row=9,column=1,sticky=W) # positioning
        # create submit button, run convert func.
        self.submit_button = Button(self) # create a convert button
        self.submit_button["text"] = "Convert" # text of button
        self.submit_button["command"] = self.convertJPG # onclick, run convertJPG function
        self.submit_button.grid(row=10,column=1,sticky=W) # positioning
        # checkbox to greyscale
        self.greyscale = BooleanVar()
        Checkbutton(self, text="To Greyscale", variable = self.greyscale).grid(row=10,column=0,sticky=W)


    def selectIMG(self): # function for select target image
        self.imgName.configure(state="normal") # entry writable
        self.imgName.delete(0,END) # clear entry area   
        self.text.delete(0.0,END)  # clear info area
        path = filedialog.askopenfilenames( filetypes = # store multiple images as array to path
                [
                    ("image files", "*.png *.gif *.bmp"),
                    ("All files", "*.*")                              
                ] )

        self.selectedIMGs = {} # dict. store the image : size

        for img in path:
            oriSize = os.path.getsize(img) # size of target file
            self.selectedIMGs[img]=oriSize # add into the dictionary
            fileName = os.path.basename(img) # get the filename
            #print(fileName)
            self.imgName.configure(state="normal") # entry writable
            self.imgName.insert(END, fileName + ";")  # insert the image path
            self.imgName.configure(state="readonly") # disable entry
            self.text.insert(END,fileName+":"+str(round(oriSize/1000/1000,3))+"MB\n") #display selected size

        return self.selectedIMGs
        
    def savePath(self): # select the destination directory to save the images
        self.destination.delete(0,END)
        savePath = filedialog.askdirectory(initialdir=os.getcwd())
        self.destination.insert(0,savePath)

    def adjustment(self, imgDict): # do the adjsutment effects, brighness, contrast etc...
        self.preConvertIMGs = {} # store the images for preview / save in a list
        for path,size in imgDict.items(): 
            #print(path)
            image = Image.open(path) # open the actual image according to path
            if image.mode != 'RGBA' or image.mode != 'RGB': # check if image is not in RGM mode
                image = image.convert('RGB') # convert it to RGB for save as JPEG format later
            fileName = os.path.basename(path) # trim out the path, get filename
            imgname = fileName.split('.') # split the file by name + extention
            saveAs = imgname[0] + ".jpg" # new file name
			
            # get custom values
            bright = int(self.brightlvl.get()) / 4.0 # get the brightness value as factor
            contra = int(self.contrastlvl.get()) / 4.0   # get the contrast value as factor
            sharp = int(self.sharpnesslvl.get()) / 4.0   # get the sharpness value as factor
            colour = int(self.colourlvl.get()) / 4.0   # get the colour balance value as factor
            
            brightEnhancer = ImageEnhance.Brightness(image) # create brightness enhancer
            image = brightEnhancer.enhance(bright) # adjust brightness

            contraEnhancer = ImageEnhance.Contrast(image) # create contrast enhancer
            image = contraEnhancer.enhance(contra) # adjust contrast
            
            sharpEnhancer = ImageEnhance.Sharpness(image) # create sharpness enhancer
            image = sharpEnhancer.enhance(sharp)   # adjust sharpness
            
            colourEnhancer = ImageEnhance.Color(image) # create colour balance enhancer
            image = colourEnhancer.enhance(colour) # adjust colour balance
            
            if self.greyscale.get(): # if checked the greyscale box
                image = image.convert('L') # convert it to greyscale

            self.preConvertIMGs[saveAs]=image # key: file name that will be saved, 
                                              # value: the actual processed image object
        return self.preConvertIMGs

    def showHistogram(self): # this func. for show the histogram of that image (ref: http://tophattaylor.blogspot.hk/2009/05/python-rgb-histogram.html)
        self.adjustment(self.selectedIMGs) # get adjusted images
        histHeight = 120            # Height of the histogram
        histWidth = 256             # Width of the histogram
        multiplerValue = 1.5        # The multiplier value basically increases
                                    # the histogram height so that love values
                                    # are easier to see, this in effect chops off
                                    # the top of the histogram.
        showFstopLines = True       # True/False to hide outline
        fStopLines = 5
        
        # Colours to be used
        backgroundColor = (51,51,51)    # Background color
        lineColor = (102,102,102)       # Line color of fStop Markers 
        red = (255,60,60)               # Color for the red lines
        green = (51,204,51)             # Color for the green lines
        blue = (0,102,255)              # Color for the blue lines
        for img in self.preConvertIMGs.values():
            hist = img.histogram()
            histMax = max(hist)
            xScale = float(histWidth)/len(hist)                   # xScaling
            yScale = float((histHeight)*multiplerValue)/histMax   # yScaling 
            im = Image.new("RGBA", (histWidth, histHeight), backgroundColor)   
            draw = ImageDraw.Draw(im)
            # Draw Outline is required
            if showFstopLines:    
                xmarker = histWidth/fStopLines
                x =0
                for i in range(1,fStopLines+1):
                    draw.line((x, 0, x, histHeight), fill=lineColor)
                    x+=xmarker
                draw.line((histWidth-1, 0, histWidth-1, 200), fill=lineColor)
                draw.line((0, 0, 0, histHeight), fill=lineColor)
                
            # Draw the RGB histogram lines
            x=0; c=0;
            for i in hist:
                if int(i)==0: pass
                else:
                    color = red
                    if c>255: color = green
                    if c>511: color = blue
                    draw.line((x, histHeight, x, histHeight-(i*yScale)), fill=color)        
                if x>255: x=0
                else: x+=1
                c+=1
            
            # Now show the histogram   
            im.show()

    def previewIMG(self): # this func. show all processed images
        self.adjustment(self.selectedIMGs) # get adjusted images
        for image in self.preConvertIMGs.values():
            image.show() # preview the images

    def convertJPG(self): # function for convert to JPEG
        os.chdir(self.destination.get()) # change to the destination directory
        self.text.delete(0.0, END) # clear the textbox area
        self.adjustment(self.selectedIMGs) # adjust the image properties
        oriSize = list(self.selectedIMGs.values()) # get size of images as list
        i=0 # index of oriSize for calculate ratio
        qualvl = int(self.imgQuality.get()) # get the quality value
        for saveAs, image in self.preConvertIMGs.items():
            image.save(saveAs,'JPEG',quality=qualvl) # convert and save it

            self.text.insert(END, "selected image saved as " +  saveAs + "\n") # display info

            self.convertedSize = os.path.getsize(saveAs) # get size of new converted file
            compressRatio = round(oriSize[i] / self.convertedSize,3) # get compress ratio
            self.text.insert(END, "ratio: " + 
                    str(round(oriSize[i]/1000/1000,3)) + "/" + str(round(self.convertedSize/1000/1000,3)) + 
                    "=" + str(compressRatio) + "\n" ) # display result
            i = i+1 # increment oriSize index
    
# create main window
root = Tk()

# add title
root.title("jpeg converter")

# window size
root.geometry("380x320")

# create a frame in the main window
app = Application(root)

# main loop
root.mainloop()
