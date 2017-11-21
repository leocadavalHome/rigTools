import pymel.core as pm
import lcGeneric as gen
import pickle

def hookOnCurve(tangent = False):
    sel = pm.ls (sl=True)
    crv=sel[-1]
    sampleNPoC = pm.createNode ('nearestPointOnCurve')
    sampleGrpA  = pm.group (empty=True)
    crv.worldSpace[0] >> sampleNPoC.inputCurve
    sampleGrpA.translate >> sampleNPoC.inPosition
    
    for obj in sel[:-1]:
        wp= pm.xform (obj, t=True, ws=True, q=True)
        pm.xform (sampleGrpA, t=wp, ws=True)
        hookPoci = pm.createNode ('pointOnCurveInfo')
        crv.worldSpace[0] >> hookPoci.inputCurve
        hookPoci.position >> obj.translate
        hookPar = sampleNPoC.parameter.get()
        hookPoci.parameter.set(hookPar)
        if tangent: 
			pm.tangentConstraint (crv, obj, aimVector=(-1, 0, 0),upVector=(0,1, 0),worldUpType="vector",worldUpVector =(0, 0, 1))
    pm.delete (sampleNPoC, sampleGrpA)

def attachObj (obj, mesh, u, v, mode=1):
    foll = pm.createNode ('follicle')
    follDag = foll.firstParent()
    mesh.worldMatrix[0] >> foll.inputWorldMatrix
    if pm.objectType (mesh) == 'mesh':
        mesh.outMesh >> foll.inputMesh
    else:
        mesh.local >> foll.inputSurface
          
    foll.outTranslate >> follDag.translate
    foll.outRotate >> follDag.rotate
    follDag.translate.lock()
    follDag.rotate.lock()
    follDag.parameterU.set (u)
    follDag.parameterV.set (v)
    if mode==1:
        pm.parent (obj, follDag)
    elif mode==2:
        pm.parentConstraint (follDag, obj, mo=True)
    elif mode==3:
        pm.pointConstraint (follDag, obj, mo=True)
    elif mode==4:
        pm.parentConstraint (follDag, obj, mo=False)
    return follDag   

def hookOnMesh(mode = 3):         
    sel = pm.ls (sl=True)
    mesh = sel[-1]
    meshShape = pm.listRelatives (mesh, s=True)[0]
    if pm.objectType (mesh) == 'mesh':  
        cpom =pm.createNode ('closestPointOnMesh')
        sampleGrpA = pm.group (empty=True)
        meshShape.worldMesh >> cpom.inMesh
    else:
        cpom =pm.createNode ('closestPointOnSurface')
        sampleGrpA = pm.group (empty=True)
        meshShape.worldSpace[0] >> cpom.inputSurface
        
    sampleGrpA.translate >> cpom.inPosition
    pm.parent (sampleGrpA, mesh)
                    
    for obj in sel[:-1]: 
        print obj
        #objShape = obj.getShape()[0]
        pos = pm.xform (obj, q=True, ws=True, t=True)
        pm.xform (sampleGrpA, ws=True, t=pos)  
        closestU =cpom.parameterU.get()
        closestV = cpom.parameterV.get()
        print closestU
        print closestV  
        attachObj (obj, mesh, closestU, closestV, mode)
    pm.delete (cpom, sampleGrpA) 

#olho
def eyeLidJnts(eyeCenter,eyeUp, verts):
	#selecione os vertives da palpebra
	center = pm.PyNode (eyeCenter)
	centerPos = center.translate.get()
	for vert in verts:
	    pos = vert.getPosition(space='world')
	    pm.select (cl=True)
	    jntBase = pm.joint (p=centerPos)
	    jnt =  pm.joint (p=pos)
	    pm.joint( jntBase, e=True, zso=True, oj='xyz', sao='yup')
	    loc = pm.spaceLocator (p=[0,0,0], n=jnt.name()+'Aim_loc')
	    loc.translate.set(pos)
	    pm.aimConstraint ( loc, jntBase,aim=(1,0,0), u=(0,1,0),wut='objectrotation', wu=(0,1,0), wuo=eyeUp)
 
 
#eyesdir
def eyeDirRig():
	sel = pm.ls (sl=True)
	if not len(sel)==3:
	    print 'selecione joint da cabeca e as esferas do olho'
	else:
	    print sel
	    for obj in sel[1:3]:
	        cls = pm.cluster (obj)      
	        loc = pm.group(empty=True, n='eyeRot_grp')
	        pos = pm.xform  (cls, q=True, ws=True, rp=True)
	        pm.delete (cls)
	        loc.translate.set(pos)
	        loc1= loc.duplicate (n='eyeRotFk_grp')[0]
	        loc2= loc.duplicate (n='eyeRotAim_grp')[0]
	        loc3= loc.duplicate (n='eyeRotDeform_grp')[0]
	        loc.rotate >> loc3.rotate
	        loc.rotate >> loc3.rotate
	        pm.orientConstraint (loc1,loc2,loc)
	        #faz controles
	        cntrlFk = gen.createCntrl (loc1.name(),loc1.name(),.5, 'ponteiroReto', 1)
	        pm.orientConstraint (cntrlFk,loc1, mo=True)
	        cntrlAim = gen.createCntrl (loc2.name(),loc2.name(),.5, 'circuloZ', 1)
	        aim = pm.PyNode(cntrlAim)
	        aim.translate.set([0,0,2])
	        aim.rename ('eyeAimTgt')
	        pm.aimConstraint ( aim, loc2,aim=(0,0,1), u=(0,1,0),wut='objectrotation', wu=(1,0,0), wuo=sel[0])
	    aimList = pm.ls ('eyeAimTgt*', type='transform')
	    print aimList  
	    aimGrp = pm.group(empty=True, n='eyeAim_grp') 
	    tmp = pm.pointConstraint (aimList,aimGrp)
	    pm.delete (tmp)
	    
	    cntrlAimGrp = gen.createCntrl (aimGrp.name(),aimGrp.name(),1, 'circuloX', 1)
	    pm.parent (aimList, cntrlAimGrp)

#dummy cntrsls
def copyDrvCntrls():
	sel = pm.ls (sl=True)
	cntrlGrp = pm.group (empty=True, n='cntrls_grp')
	for  obj in sel:
	    grp = obj.listRelatives (p=True)[0]
	    print grp
	    grp2 = grp.duplicate()[0]
	    obj2 = grp2.listRelatives (c=True)[0]
	    print obj2   
	    nm=obj2.name()
	    off = obj2.duplicate (n=nm+'Offset')[0]
	    shp= off.getShape()
	    pm.delete (shp)
	    child=off.listRelatives (c=True)
	    pm.delete (child)
	    pm.parent (obj2, off)
	    pm.parent (grp2, cntrlGrp)
	    mlt = pm.createNode ('multiplyDivide')
	    print mlt
	    mlt.input2.set([-1,-1,-1])
	    obj2.translate >> mlt.input1
	    mlt.output >> off.translate
	    obj2.translate >> obj.translate
	    obj2.rotate >> obj.rotate
	    obj2.scale >> obj.scale

#dummy2
def copyDrvCntrlsNoOffset():
	sel = pm.ls (sl=True)
	cntrlGrp = pm.group (empty=True, n='cntrls_grp')
	for  obj in sel:
	    grp = obj.listRelatives (p=True)[0]
	    print grp
	    grp2 = grp.duplicate()[0]
	    obj2 = grp2.listRelatives (c=True)[0]
	    print obj2   
	    nm=obj2.name()
	    #off = obj2.duplicate (n=nm+'Offset')[0]
	    #shp= off.getShape()
	    #pm.delete (shp)
	    #child=off.listRelatives (c=True)
	    #pm.delete (child)
	    #pm.parent (obj2, off)
	    pm.parent (grp2, cntrlGrp)
	    #mlt = pm.createNode ('multiplyDivide')
	    #print mlt
	    #mlt.input2.set([-1,-1,-1])
	    #obj2.translate >> mlt.input1
	    #mlt.output >> off.translate
	    obj2.translate >> obj.translate
	    obj2.rotate >> obj.rotate

def saveCntrlsShape(filename= 'd:/cntrls.shp'):
	userSel = pm.ls (sl=True)
	sel=[x for x in userSel if '_cntrl' in x.name()]
	cntrlShapeDict={}
	
	
	for obj in sel:
	    print obj
	    if pm.nodeType (obj.getShape())=='nurbsCurve':
	        pointList=[]
	        for i in range (len (obj.cv)):
	            pointList.append (pm.pointPosition (obj.cv[i], l=True))
	            cntrlShapeDict[obj]=pointList
	with open(filename, 'wb') as f:
	    pickle.dump(cntrlShapeDict, f)    

def loadCntrlShape(filename= 'd:/cntrls.shp'):
	
	cntrlShapeDict={}
	print cntrlShapeDict  
	    
	    
	with open(filename, 'rb') as f:
	    cntrlShapeDict  = pickle.load(f)
	print cntrlShapeDict    
	for obj in cntrlShapeDict:
	    print obj
	    for i in range (len (obj.cv)):
	        pm.xform (obj.cv[i], t=cntrlShapeDict[obj][i])

def selectSkinJoints():
	sel = pm.ls (sl=True)
	if sel:
	    objShp = sel[0].getShape()
	    print objShp
	    setList = objShp.inputs(t='objectSet')
	    for st in setList:
	        x= st.inputs (t='skinCluster')
	        if not x==[]:
	            skinCls=x    
	    print skinCls 
	    if skinCls:
	        jnts = skinCls[0].inputs (t='joint')
	        pm.select (jnts)
	    else:
	        print 'ERRO: objeto nao tem skin'
	else:
	    print 'ERRO:nenhum objeto selecionado'	        

def mirrorSetDriven():
# Mirror contrl connections
	LCntrl = pm.ls (sl=True)[0]
	RCntrl = LCntrl.replace('L_','R_')
	
	crvList = LCntrl.outputs (t = 'animCurve')
	print crvList
	direct = LCntrl.outputs (t ='blendShape', p=True, c=True)
	print direct
	for crv in crvList:
	    print crv
	    plugIN = crv.outputs(t = 'transform', p=True)[0]
	    print plugIN
	    plugOUT = crv.inputs(t = 'blendShape', p=True)[0]
	    print plugOUT
	    newCrv = pm.duplicate (crv, n=crv.replace('L_', 'R_'))[0]
	    print newCrv
	    
	    pm.connectAttr (plugIN.replace('L_','R_'), newCrv+'.input')
	    pm.connectAttr (newCrv+'.output',plugOUT.replace('L_','R_'), f=True)
	
	if direct:    
	    for i in xrange(0,len(direct),2):
	        OUT = direct[i].replace('L_','R_')
	        IN = direct[i+1].replace('L_','R_')
	        
	        OUT >> IN	


def cpSetDriven(ns):
    #referencie o arqivo com os setDrivens a copiar
    #selecione controles q vao receber o setDriven
    
    sel = pm.ls (sl=True)
    for tgt in sel:
        source = pm.PyNode (ns+':'+tgt)
        curveList =  source.inputs(t='animCurve', c=True, p=True)
        blendList =  source.inputs(t='blendWeighted', c=True, p=True, scn=True)
        
        for crvPlug, crv in curveList:
            print crvPlug
            print crv
            newCurve = pm.duplicate (crv)[0]
            print newCurve    
            newCurve.attr(crv.longName()) >> tgt.attr (crvPlug.longName())    
            
            drivers = crv.node().inputs(scn=True, p=True)
            print drivers
            for drv in drivers:
                newDriver = pm.PyNode (drv.split(':')[-1])
                newDriver >> newCurve.input
        
        
        for bldPlug, bld in blendList:
            print bldPlug, bld
            newBlend = pm.duplicate (bld)[0]
            newBlend.attr(bld.longName()) >> tgt.attr(bldPlug.longName())
            
            curveList =  bld.node().inputs(t='animCurve', c=True, p=True, scn=True)
            print curveList
            for crvPlug, crv in curveList:
                print crvPlug
                print crv
                newCurve = pm.duplicate (crv)[0]
                print newCurve    
                newCurve.attr(crv.longName()) >> newBlend.attr(crvPlug.longName())    
                
                drivers = crv.node().inputs(scn=True, p=True)
                print drivers
                for drv in drivers:
                    newDriver = pm.PyNode (drv.split(':')[-1])
                    newDriver >> newCurve.input


#conecta e disconecta
def connect (blendNode):
	
	obj = pm.PyNode (blendNode)
	
	conn = obj.inputs (c=True, p=True)
	print conn
	
	for p, c in conn:
	    print p, c
	    if 'weight' in p.name() :
	        print c, p
	        c // p
	
	for p, c in conn:
	    if 'weight' in p.name() :
	        print c, p
	        c >> p
	
def slideOnMesh ():         
    sel = pm.ls (sl=True)
    obj= sel[0]
    mesh = sel[-1]
    meshShape = pm.listRelatives (mesh, s=True)[0]
    cpom =pm.createNode ('closestPointOnMesh')
    sampleGrpA = pm.group (empty=True)
    sampleGrpA.translate >> cpom.inPosition
    meshShape.worldMesh >> cpom.inMesh
    transf = pm.group (empty=True)
    pm.parentConstraint (mesh,transf , mo=False)
    pm.scaleConstraint (mesh,transf , mo=False)    
    pm.parent (sampleGrpA, transf)
               
    foll = pm.createNode ('follicle')
    follDag = foll.firstParent()
    
    mesh.worldMatrix[0] >> foll.inputWorldMatrix
    mesh.outMesh >> foll.inputMesh
    foll.outTranslate >> follDag.translate
    foll.outRotate >> follDag.rotate
    follDag.translate.lock()
    follDag.rotate.lock()
    cpom.parameterU >> follDag.parameterU
    cpom.parameterV >> follDag.parameterV
    
    pos = pm.xform (obj, q=True, ws=True, t=True)
    pm.xform (sampleGrpA, ws=True, t=pos)
    cntrl =  gen.doCntrl (sampleGrpA.name(),sampleGrpA.name(), 1, 'bola', 1)
    pm.parentConstraint (cntrl ,sampleGrpA, mo=True)