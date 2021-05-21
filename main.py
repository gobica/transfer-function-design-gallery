import vtk
import matplotlib.pyplot as plt
import vtk
import numpy as np
import helper
from scipy import ndimage
from scipy.signal import find_peaks
import random
import tkinter as tk
from PIL import Image, ImageTk
import rendering
#varibales
import transferFunctions
import itertools

#read DICOM file with reader
PathDicom = "./models/Hip"
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(PathDicom)
reader.Update()

#call function to convert to numpy array
numpyDicomArray = helper.DICOMToNumpy(reader)
#calculate histogram
startRange = -1500
endRange = 3000
histogram, bin_edges = np.histogram(numpyDicomArray.flatten(), bins= 4500, range=(startRange, endRange))

#apply median filtering to smooth historam and remove artifacts
histogram_smoothed = ndimage.median_filter(histogram,10)


# find peaks  and valleys
peaks, valleys = helper.find_peaks_valleys(histogram_smoothed, startRange)
helper.plot_histogram(histogram_smoothed, bin_edges)

#####CALULCATE TRANSFER FUNCTIONS#####
transferFunctionElements = []
photo_images = []
root = tk.Tk()

#INICIALIZE COLORS AND OPACITY
numberOfMaterials = len(valleys)-1
#opacitiesMaterials = [0] * numberOfMaterials

c1 = [0.5, 0.1, 0.1]
c2 = [0.2, 0.6, 0.15]
c3 = [0.2, 0.2, 0.7]
c4 = [0.4, 0.4, 0.4]
c5 = [0.5, 0, 0.5]
c6 = [0.6, 0.6, 0]
c7 = [0, 0.5, 0.8]
c8 = [0, 0.7, 0.3]
allcolors =[c1, c2, c3, c4, c5, c6, c7]

# inicialize how many combinations of volume are
opacitiesMaterials = list(itertools.product([0,1],repeat=numberOfMaterials)) 
colors = allcolors [:numberOfMaterials]
opacitiesGradietMaterials = [1, 1, 1, 1, 1, 1]
numberOfimagesPerSlide = len(opacitiesMaterials)

colNumber = numberOfMaterials
rowNumber = numberOfMaterials
#(funcColor, funcOpacityScalar, funcOpacityGradient) inide array
###INICIALIZE FUNCTIONS

for i in range(numberOfimagesPerSlide):
    transferFunctionElements.append(transferFunctions.getNewTransferFunction(valleys, opacitiesMaterials[i], colors, opacitiesGradietMaterials, True))
    funcColor, funcOpacityScalar, funcOpacityGradient = transferFunctionElements[i]

    renderer =  rendering.setRenderer(reader,funcColor, funcOpacityScalar, funcOpacityGradient)
    image = helper.get_image(renderer, 150, 150)
    photo_image = ImageTk.PhotoImage(image) #for gallery
    photo_images.append(photo_image)

# display interactive gallery
canvas = tk.Canvas (root, width=800, height = 800)
canvas.pack()
canvas.grid(row=rowNumber+1,column=colNumber)
        
def startRender(reader,funcColor, funcOpacityScalar, funcOpacityGradient):
    renderer =  rendering.setRenderer(reader,funcColor, funcOpacityScalar, funcOpacityGradient)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.SetSize(900, 900)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renWin)
    interactor.Initialize()
    renWin.Render()
    interactor.Start()

def on_click(pickId):
    # new window
    funcColor, funcOpacityScalar, funcOpacityGradient = transferFunctionElements[pickId]

    #start rendering
    startRender(reader,funcColor, funcOpacityScalar, funcOpacityGradient)

    opacitiesMaterials = transferFunctions.getOpacatiesFromTransferFunction(valleys, funcOpacityScalar)
    opacitiesGradietMaterials = transferFunctions.getGradientOpacatiesFromTransferFunction (valleys,  funcOpacityGradient) 

    transferFunctionElements.clear()
    photo_images.clear()
    buttons.clear()

    #adjust opacity on each iteration
    for i in range(numberOfimagesPerSlide):
        for op in range(len(opacitiesMaterials)):
            adjustOpacity = random.uniform(-0.20, 0.20)
            if opacitiesMaterials[op] != 0:
                opacitiesMaterials[op]  = opacitiesMaterials[op]  + adjustOpacity
                if opacitiesMaterials[op]  > 1: 
                    opacitiesMaterials[op]  = 0.9
                if  opacitiesMaterials[op]  < 0: 
                    opacitiesMaterials[op]  = 0.1
        #for og in range(len(opacitiesGradietMaterials)):

        #adjust opacity gradient on each iteration

        transferFunctionElements.append(transferFunctions.getNewTransferFunction(valleys, opacitiesMaterials, colors, opacitiesGradietMaterials))
        funcColor, funcOpacityScalar, funcOpacityGradient = transferFunctionElements[i]

        renderer =  rendering.setRenderer(reader,funcColor, funcOpacityScalar, funcOpacityGradient)
        image = helper.get_image(renderer, 150, 150)

        photo_image = ImageTk.PhotoImage(image) #for gallery
        photo_images.append(photo_image)
    
    for i in range(numberOfimagesPerSlide):
        button = tk.Button(canvas, image = photo_images[i], command= lambda i=i: on_click(i))
        buttons.append(button)

    buttonsI=0
    for i in range(colNumber):
        for j in range(rowNumber):
            buttons[buttonsI].grid(row=j,column=i)
            buttonsI += 1
    

buttons = []
for i in range(numberOfimagesPerSlide):
    button = tk.Button(canvas, image = photo_images[i], command= lambda i=i: on_click(i))
    buttons.append(button)

buttonsI=0
for i in range(colNumber):
    for j in range(rowNumber):
        buttons[buttonsI].grid(row=j,column=i)
        buttonsI += 1


root.mainloop()