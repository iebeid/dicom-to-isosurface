import vtk
import vtk.util.numpy_support as VN

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
 
    def __init__(self,parent=None):
        self.AddObserver("MiddleButtonPressEvent",self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent",self.middleButtonReleaseEvent)
 
    def middleButtonPressEvent(self,obj,event):
        print("Middle Button pressed")
        print("selectionCallback")
        self.OnMiddleButtonDown()
        hsel = vtk.vtkHardwareSelector()
        hsel.SetFieldAssociation(vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS)
        # hsel.SetRenderer(ren1)
        x,y = self.GetRenderWindow().GetSize()
        # Create a small area around clicked point for selector area
        hsel.SetArea(0,0,x,y)
        res = hsel.Select()
        numNodes = res.GetNumberOfNodes()
        if (numNodes < 1):
               print("No visible cells")
        else:
               sel_node = res.GetNode(0)
               print('Visible cell IDs: ', VN.vtk_to_numpy(sel_node.GetSelectionList()).tolist())
        return
 
    def middleButtonReleaseEvent(self,obj,event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
        return

		
filename = "D:/Projects/UALR/Research/Projects/UAMSCTScans/Sources/Paraview/UAMS/Anonymous.stl"
 
reader = vtk.vtkSTLReader()
reader.SetFileName(filename)

smoother = vtk.vtkSmoothPolyDataFilter()
smoother.SetInputConnection(reader.GetOutputPort())
smoother.SetNumberOfIterations(50)

normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(smoother.GetOutputPort())
normals.FlipNormalsOn()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.49, 0.25)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(normals.GetOutputPort())
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInputConnection(outline.GetOutputPort())
 
actor2 = vtk.vtkActor()
actor2.SetMapper(mapper2)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
 
iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(MyInteractorStyle())
iren.SetRenderWindow(renWin)



ren.AddActor(actor)
ren.AddActor(actor2)
 


axesActor = vtk.vtkAnnotatedCubeActor();
axesActor.SetXPlusFaceText('X')
axesActor.SetXMinusFaceText('-X')
axesActor.SetYMinusFaceText('-Y')
axesActor.SetYPlusFaceText('Y')
axesActor.SetZMinusFaceText('-Z')
axesActor.SetZPlusFaceText('Z')
axesActor.GetTextEdgesProperty().SetColor(1,1,0)
axesActor.GetTextEdgesProperty().SetLineWidth(2)
axesActor.GetCubeProperty().SetColor(0,0,1)
axes = vtk.vtkOrientationMarkerWidget()
axes.SetOrientationMarker(axesActor)
axes.SetInteractor(iren)
axes.EnabledOn()
axes.InteractiveOn()
ren.ResetCamera()

balloonRep = vtk.vtkBalloonRepresentation()
balloonRep.SetBalloonLayoutToImageRight()
 
balloonWidget = vtk.vtkBalloonWidget()
balloonWidget.SetInteractor(iren)
balloonWidget.SetRepresentation(balloonRep)
balloonWidget.AddBalloon(actor,"This is a spine")
balloonWidget.EnabledOn()


 
iren.Initialize()
renWin.Render()
iren.Start()