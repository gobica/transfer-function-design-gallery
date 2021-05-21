import matplotlib.pyplot as plt
from PIL import Image
import vtk
import numpy_support
import io
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths



#from PIL import Image
def get_image(renderer, width = 100, height = 100): 
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    #renWin.Render()
    renWin.SetSize(width,height)
    grabber = vtk.vtkWindowToImageFilter()
    grabber.SetInput( renWin )
    grabber.Update()  # this is cousing interactive window to open... gth
    writer = vtk.vtkPNGWriter()
    writer.SetInputConnection( grabber.GetOutputPort() )
    writer.SetFileName( "screenshot.png" )
    writer.SetWriteToMemory(1)
    writer.Write() # this is cousing interactive window to open... gth nessery!
      
    data = memoryview(writer.GetResult()).tobytes()
    img = Image.open(io.BytesIO(data))
    return img


#plot gray histogram 
def plot_histogram (histogram, bin_edges): 
    plt.figure()
    plt.title("Grayscale Histogram")
    plt.xlabel("HU")
    plt.ylabel("pixels")
    plt.xlim([- 1500 ,1500]) 
    plt.plot(bin_edges[0:-1], histogram) 
    plt.show()
    return

def find_peaks_valleys(histogram, startRange):
    
    peaks, indeces = find_peaks(histogram, prominence=500)
    results_full  = peak_widths(histogram, peaks)

    widths = results_full[0]
    left_ips_right_ips = results_full[2]
    peaks = peaks + startRange # get original indices of histogram
    peaksLen = len(peaks)
    valleys = []
    for i in range(peaksLen-1) : #-1
        #if i == 0:
          #  valleys.append  (peaks[i] - widths[i])  
        valleys.append ((peaks[i+1] + peaks[i]) / 2 )  # valley between 2 sucessive peaks
    valleys.append (peaks[peaksLen-1] +  widths[peaksLen-1]) 

    print("peaks", peaks)
    print("valleys", valleys)
    print("widnths", widths)
    print("leftipsrightups",left_ips_right_ips )
    return peaks, valleys


def createRenderer():
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0)

    camera = renderer.MakeCamera()
    camera.SetPosition(-256, -256, 512)
    camera.SetFocalPoint(0.0, 0.0, 255.0)
    camera.SetViewAngle(30.0)
    camera.SetViewUp(0.46, -0.80, -0.38)
    renderer.SetActiveCamera(camera)
    
    return renderer

def vtkImageToNumPy(image, pixelDims):
    pointData = image.GetPointData()
    arrayData = pointData.GetArray(0)
    ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
    ArrayDicom = ArrayDicom.reshape(pixelDims, order='F')
    
    return ArrayDicom

def DICOMToNumpy(reader):
    _extent = reader.GetDataExtent()
    ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]
    #ConstPixelSpacing = reader.GetPixelSpacing()
    imageData = reader.GetOutput()
    pointData = imageData.GetPointData()
    assert (pointData.GetNumberOfArrays()==1)
    arrayData = pointData.GetArray(0)

    ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
    ArrayDicom = ArrayDicom.reshape(ConstPixelDims, order='F')
    return ArrayDicom
