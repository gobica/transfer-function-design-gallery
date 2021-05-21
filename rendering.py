import helper
import vtk 
def setRenderer(reader,funcColor, funcOpacityScalar, funcOpacityGradient): 
     # set properties 
    propVolume = vtk.vtkVolumeProperty()
    propVolume.ShadeOff()
    propVolume.SetColor(funcColor)
    propVolume.SetScalarOpacity(funcOpacityScalar)
    propVolume.SetGradientOpacity(funcOpacityGradient)
    propVolume.SetInterpolationTypeToLinear()

    # set renderer
    mapperVolume = vtk.vtkGPUVolumeRayCastMapper()
    mapperVolume.SetInputConnection(reader.GetOutputPort())

    actorVolume = vtk.vtkVolume()
    actorVolume.SetMapper(mapperVolume)
    actorVolume.SetProperty(propVolume)

    renderer = helper.createRenderer()
    renderer.AddActor(actorVolume)
    return renderer