import vtk
import random
from itertools import combinations



#Colors: 
c1 = [0.8, 0, 0]
c2 = [0, 0.8, 0]
c3 = [0, 0, 0.8]
c4 = [0.8, 0.8, 0.8]
c5 = [0.5, 0, 0.5]
c6 = [0.6, 0.6, 0]
c7 = [0, 0.5, 0.8]
c8 = [0, 0.7, 0.3]
colors= [c1, c2, c3, c4, c5, c6, c7, c8]
gradientOpacityX = [-2500, -800, - 0, 1500, 2000]


def getNewTransferFunction (valleys,opacitiesMaterials, colors, opacitiesGradietMaterials, first = False): 
    # COLOR FUNCTION 
    funcColor = vtk.vtkColorTransferFunction()
    for i in range(len(valleys) - 1):    
        #rColor = random.choice(colors)
        funcColor.AddRGBSegment(valleys[i] + 1, colors[i][0], colors[i][1], colors[i][2], valleys[i+1], colors[i][0], colors[i][1], colors[i][2] )
        
    # OPACITY FUNCTION
    funcOpacityScalar = vtk.vtkPiecewiseFunction()
   

    for i in range(len(valleys) - 1):
        funcOpacityScalar.AddSegment(valleys[i] + 1, opacitiesMaterials[i], valleys[i+1], opacitiesMaterials[i])
    
    funcOpacityScalar.ClampingOff () # set vlaues to 0 if not in segment
    # OPACITY GRADIENT FUNCTION 

    funcOpacityGradient = vtk.vtkPiecewiseFunction()
    if first == False:
        for i in range(len(gradientOpacityX)):
            funcOpacityGradient.AddPoint(gradientOpacityX[i], opacitiesGradietMaterials[i] + random.uniform(-0.1, 0.1))
        
    return (funcColor, funcOpacityScalar, funcOpacityGradient)



def getOpacatiesFromTransferFunction (valleys,  funcOpacityScalar, ): 
    selectedOpacities = []

    index_opacity = 0
    index_opacity += 1
    for i in range(len(valleys)-1):
        selectedOpacities.append(funcOpacityScalar.GetValue(valleys[i] + 2))
    return selectedOpacities

def getGradientOpacatiesFromTransferFunction (valleys,  funcOpacityGradient): 
    selectedGradientOpacities = []
    
    for i in gradientOpacityX:
        selectedGradientOpacities.append(funcOpacityGradient.GetValue(i))
    return selectedGradientOpacities