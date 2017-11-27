import maya.api.OpenMaya as om
import pymel.core as pm

def intersectEdgePlane (planePoint,planeNormal, A, B):
    u=B-A
    w=(A-planePoint)*-1
    D=planeNormal * u
    N=planeNormal * w
    if abs (D)<0.001:
        if N==0:
            return None
        else:
            return None
    SI = N/D
    if (SI<0 or SI>1):
        return 0
    I=A + SI *u
    return I


sel = om.MSelectionList()
sel.add('locator1')
dag = sel.getDagPath(0)
planeTransform = om.MFnTransform(dag)
planePoint= om.MVector (planeTransform.translation(om.MSpace.kWorld)) 
planeNormal=om.MVector.kZaxisVector * planeTransform.transformation().asMatrix()
   
sel = om.MSelectionList()
sel.add('pSphereShape1')
dag = sel.getDagPath(0)

mesh = om.MFnMesh(dag)
edgeIt = om.MItMeshEdge(dag)
polygonIt = om.MItMeshPolygon(dag)

intesectList = {}
while not edgeIt.isDone():
    vtxA = mesh.getPoint(edgeIt.vertexId(0), om.MSpace.kWorld)
    vtxB = mesh.getPoint(edgeIt.vertexId(1), om.MSpace.kWorld)	
    A = om.MVector(vtxA)
    B = om.MVector(vtxB)
    
    result = intersectEdgePlane (planePoint,planeNormal, A, B)
    onBoudary = edgeIt.onBoundary()
   
    if result:
        intesectList[edgeIt.index()]=[result,onBoudary]
                    
    edgeIt.next()

print intesectList

for i in intesectList:
    loc = pm.spaceLocator()
    loc.localScaleX.set(0.05)
    loc.localScaleY.set(0.05)
    loc.localScaleZ.set(0.05)
 
    pm.xform (loc, t= intesectList[i][0], wd=True)   
    
allSortedEdges=[]   
sortedEdges=[]
edgeIt.reset()  
remainedEdges = intesectList.keys()
count = len (remainedEdges)
boundary = [x for x in remainedEdges if intesectList[x][1]==True]
if boundary:
    i=boundary[0]
    isClosed =False
else:
    i = remainedEdges[0]
    isClosed = True

while not count==0:
    sortedEdges.append(i)    
    remainedEdges.remove(i)
    edgeIt.setIndex(i)    
    connectedFaces = edgeIt.getConnectedFaces()
    nextEdge = []
    for f in connectedFaces:
        polygonIt.setIndex(f) 
        connectedEdges = polygonIt.getEdges()
        a = [x for x in connectedEdges if x in remainedEdges]
        if a:
            i = a[0]
            nextEdge.append(i)
            print nextEdge
            
    if nextEdge:
        i=nextEdge[0] 
        
        print sortedEdges
        print count
    else:
        print 'entrou'
        print remainedEdges
        print count
        allSortedEdges.append([sortedEdges,isClosed])
        
        if remainedEdges:
            boundary = [x for x in remainedEdges if intesectList[x][1]==True]
            if boundary:
                i=boundary[0]
                isClosed = False
            else:
                i = remainedEdges[0]
                isClosed = True
        sortedEdges=[]
        
    count -= 1
    
    
print allSortedEdges