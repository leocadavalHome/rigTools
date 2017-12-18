x = Limb({'name':'teste','flipAxis':False, 'axis':'X'})
x.doRig()

p1=pm.xform (x.limbDict['joint1'], q=True, t=True, ws=True)
p2=pm.xform (x.limbDict['joint2'], q=True, t=True, ws=True)
p3=pm.xform (x.limbDict['joint3'], q=True, t=True, ws=True)

A=om.MVector (p1)
B=om.MVector (p2)
C=om.MVector (p3)

AB= A-B
BC= B-C
L=AB.length()+BC.length()

rb = RibbonBezier('ribbonBezier', L, numJnts=10)
rb.doRig()

ribbonMoveAll = rb.ribbonDict['ribbonMoveAll']
limbMoveAll = x.limbDict['limbMoveAll']
limbJoint1 = x.limbDict['joint1']
limbJoint2 = x.limbDict['joint2']
limbJoint3 = x.limbDict['joint3']
limbJoint4 = x.limbDict['joint4']
ribbonEndCntrl = rb.ribbonDict['cntrl0']
ribbonMidCntrl = rb.ribbonDict['cntrl3']
ribbonStartCntrl = rb.ribbonDict['cntrl6']
ribbonMid2TangCntrl = rb.ribbonDict['cntrl4']
ribbonMid1TangCntrl = rb.ribbonDict['cntrl2']
startGrp = pm.group (em=True)
midGrp = pm.group (em=True)
endGrp = pm.group (em=True)
print limbJoint4  
pm.parentConstraint (limbJoint1,endGrp,mo=False)
pm.pointConstraint (limbJoint2,midGrp,mo=False)
ori = pm.orientConstraint (limbJoint2,limbJoint1,midGrp,mo=False)
ori.interpType.set (2)
pm.parentConstraint (limbJoint3,startGrp,mo=False)


pm.parent (ribbonMoveAll, limbJoint1)
ribbonMoveAll.translate.set(0,0,0)
ribbonMoveAll.rotate.set(0,0,0)
pm.parent (ribbonMoveAll, limbMoveAll)
pm.parentConstraint (limbJoint1, ribbonMoveAll, mo=True)

pm.parent (ribbonEndCntrl.cntrlGrp, endGrp)
pm.parent (ribbonMidCntrl.cntrlGrp, midGrp)
pm.parent (ribbonStartCntrl.cntrlGrp, startGrp)
pm.parent (startGrp,midGrp,endGrp,ribbonMoveAll)

##lembrar de implementar outras possibilidade de eixos. Hardcode de X
ribbonEndCntrl.cntrlGrp.translate.set(0,0,0)
ribbonEndCntrl.cntrlGrp.rotate.set(0,0,0)
ribbonMidCntrl.cntrlGrp.translate.set(0,0,0)
ribbonMidCntrl.cntrlGrp.rotate.set(0,0,0)
ribbonStartCntrl.cntrlGrp.translate.set(0,0,0)
ribbonStartCntrl.cntrlGrp.rotate.set(0,0,0)

mid1AimGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
mid2AimGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
mid1SpcSwithGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
mid2SpcSwithGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)

pm.aimConstraint (limbJoint1, mid1AimGrp ,weight=1, aimVector=(-1, 0 ,0) , upVector=(0, 1, 0),worldUpVector=(0,1,0), worldUpType='objectrotation', worldUpObject=limbJoint1 )
pm.aimConstraint (limbJoint3, mid2AimGrp ,weight=1, aimVector=(1, 0 ,0) , upVector=(0, 1, 0),worldUpVector=(0,1,0), worldUpType='objectrotation', worldUpObject=limbJoint1 )
pm.parent (ribbonMid1TangCntrl.cntrlGrp,mid1SpcSwithGrp)
pm.parent (ribbonMid2TangCntrl.cntrlGrp,mid2SpcSwithGrp)

aimBlend1 = pm.createNode('blendTwoAttr')
aimBlend2 = pm.createNode('blendTwoAttr')
ribbonMoveAll.addAttr ('softTang1', at='float', dv=0, max=1, min=0,k=1)
ribbonMoveAll.addAttr ('softTang2', at='float', dv=0, max=1, min=0,k=1)
aimBlend1.input[0].set(0)
mid1AimGrp.rotateY >> aimBlend1.input[1]
aimBlend2.input[0].set(0)
mid2AimGrp.rotateY >> aimBlend2.input[1]
ribbonMoveAll.softTang1 >> aimBlend1.attributesBlender
ribbonMoveAll.softTang2 >> aimBlend2.attributesBlender
aimBlend1.output >> mid1SpcSwithGrp.rotateY
aimBlend2.output >> mid2SpcSwithGrp.rotateY
        
extra1 =  twistExtractor (x.limbDict['joint4'])
extra2 =  twistExtractor (x.limbDict['joint1'])
extra1.extractor.extractTwist >> ribbonStartCntrl.cntrl.twist
extra2.extractor.extractTwist >> ribbonEndCntrl.cntrl.twist
