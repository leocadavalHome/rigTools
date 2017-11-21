import pymel.core as pm
import lcRigToolbox as tbox
import lcGeneric as gen

class FlexBezier:
    def __init__(self):
        
        #grupos de espaco local
        noMoveSpace = pm.group (empty=True, n='noMove')
        pm.xform (noMoveSpace , t=(-5,0,0) )
        cntrlsSpace = pm.group (empty=True, n='local')
        pm.xform (cntrlsSpace , t=(-5,0,0))
        
        #cria superficies no move e local        
        noMoveBend1 = pm.nurbsPlane ( p=(-2.5,0,0), ax=(0,1,0), w=5, lr = .1 , d = 3, u =5, v =1)
        noMoveBend2 = pm.nurbsPlane ( p=(2.5,0,0), ax=(0,1,0), w=5, lr = .1 , d = 3, u =5, v =1)
        bendSurf1 = pm.nurbsPlane ( p=(-2.5,0,0), ax=(0,1,0), w=5, lr = .1 , d = 3, u =5, v =1)
        bendSurf2 = pm.nurbsPlane ( p=(2.5,0,0), ax=(0,1,0), w=5, lr = .1 , d = 3, u =5, v =1)
        
        #Deformer Bezier
        #cria curvas bezier de deformacao
        noMoveCrvJnt = pm.curve ( bezier=True, d=3, p=[(-5,0,0),(-4,0,0),(-1,0,0),(0,0,0),(1,0,0),(4,0,0),(5,0,0)], k=[0,0,0,1,1,1,2,2,2])        


        #noMoveCrvUp = pm.curve ( bezier=True, d=3, p=[(-5,1,0),(-4,1,0),(-1,1,0),(0,1,0),(1,1,0),(4,1,0),(5,1,0)], k=[0,0,0,1,1,1,2,2,2])
                
        #joints e up vectors para deformar a superficie noMove
        #jntList = []
        #locList = []
        #for i in range (-5,6):
        #    pm.select (cl=True)
        #    jnt = pm.joint (p=(i,0,0))
        #    loc = pm.spaceLocator (p=(0,0,0))
        #    pm.xform (loc, t=(i,1,0))
        #    jntList.append (jnt)
        #    locList.append (loc)
        
        #jntGrp = pm.group (jntList)
        #locGrp =pm.group (locList) 
        pm.group (noMoveCrvJnt, noMoveBend1,noMoveBend2,  p=noMoveSpace) 
        pm.parent ( bendSurf1, bendSurf2, cntrlsSpace )       
        #self.hookJntsOnCurve ( jntList, locList, noMoveCrvJnt, noMoveCrvUp)
        
        
        #Deformers das superficies noMove
        #twist das superficies noMove
        twist1 = pm.nonLinear(noMoveBend1[0],  type='twist')
        twist2 = pm.nonLinear(noMoveBend2[0],  type='twist')
        twist1[1].rotateZ.set(90)
        twist2[1].rotateZ.set(90)
        pm.parent (twist1[1],twist2[1], noMoveSpace)
        wireDef = pm.wire (noMoveBend1, noMoveBend2, w=noMoveCrvJnt, dds=[(0, 50)])
        #pm.wire( wireDef, edit=True, en=1, dds=[(0, 50)] )
        
        #skin das superficies noMove
        #pm.skinCluster (jntList, noMoveBend1[0])
        #pm.skinCluster (jntList, noMoveBend2[0])
        
        #blendShape transferindo as deformações para a superficie move
        blend1 = pm.blendShape (noMoveBend1[0], bendSurf1[0])
        blend2 = pm.blendShape (noMoveBend2[0], bendSurf2[0])
        pm.blendShape (blend1, e=True, w=[(0, 1)])
        pm.blendShape (blend2, e=True, w=[(0, 1)])
        
        #controles da Bezier   
        anchorList = []
        cntrlList =[]
        for i in range (0, 7):
            anchor = pm.cluster (noMoveCrvJnt.name()+'.cv['+str(i)+']')
            anchorGrp = pm.group (em=True)
            anchorDrn = pm.group (em=True, p=anchorGrp)
            pm.parent (anchorDrn, anchorGrp)
            pos = pm.xform (anchor, q=True, ws=True, rp=True)
  
            pm.xform (anchorGrp, t=pos, ws=True)
            pm.parent (anchor, anchorDrn)            
            #pm.sets (anchor[0].name()+'Set', add = noMoveCrvUp.name()+'.cv['+str(i)+']')
            cntrlName =gen.createCntrl (anchor[1].name() ,anchor[1].name() ,1, 'cubo', 1)
            cntrl = pm.PyNode (cntrlName)
            if i==1 or i==4:
                pm.xform (anchorGrp, s=(-1,1,1))
                pm.xform (cntrl.getParent(), s=(-1,1,1))
            cntrl.translate >> anchorDrn.translate
            cntrl.rotate >> anchorDrn.rotate
            anchorList.append (anchor[1])
            cntrlList.append(cntrl)

        pm.addAttr (cntrlList[0], ln='twist', at='double', dv=0, k=True)
        pm.addAttr (cntrlList[0], ln='stretchDist', at='double', dv=0, k=True)
        pm.addAttr (cntrlList[0], ln='autoVolumStregth', at='double', dv=0, k=True)
        pm.addAttr (cntrlList[3], ln='twist', at='double', dv=0, k=True)
        pm.addAttr (cntrlList[3], ln='autoVolume', at='double', dv=0, k=True)
        pm.addAttr (cntrlList[6], ln='twist', at='double', dv=0, k=True)
        pm.addAttr (cntrlList[6], ln='stretchDist', at='double', dv=0, k=True)
        pm.addAttr (cntrlList[6], ln='autoVolumStregth', at='double', dv=0, k=True)
        
        cntrlList[0].twist >> twist1[0].endAngle
        cntrlList[3].twist >> twist1[0].startAngle
        cntrlList[3].twist >> twist2[0].endAngle
        cntrlList[6].twist >> twist2[0].startAngle       
                  
        pm.parent (anchorList[1].getParent(2), anchorList[0])       
        pm.parent (anchorList[5].getParent(2), anchorList[6]) 
        pm.parent (anchorList[2].getParent(2),anchorList[4].getParent(2), anchorList[3])
        pm.parent (cntrlList[1].getParent(), cntrlList[0])       
        pm.parent (cntrlList[5].getParent(), cntrlList[6]) 
        pm.parent (cntrlList[2].getParent(),cntrlList[4].getParent(), cntrlList[3]) 
        pm.parent (cntrlList[3].getParent(), cntrlList[0].getParent(),cntrlList[6].getParent(), cntrlsSpace)
        pm.parent (anchorList[3].getParent(2), anchorList[0].getParent(2),anchorList[6].getParent(2), noMoveSpace)        

        #Skin joints do ribbon
        skinJntsGrp = pm.group (em=True)
        follGrp = pm.group (em=True)
        
        #cria rampss        
        ramp1 = pm.createNode ('ramp')
        ramp1.attr('type').set(1)
        
        ramp2 = pm.createNode ('ramp')
        ramp2.attr('type').set(1)
        
        expre1 = "float $dummy = "+ramp1.name()+".outAlpha;float $output[];float $color[];"
        expre2 = "float $dummy = "+ramp2.name()+".outAlpha;float $output[];float $color[];"
        numJnts = 8
            
        for i in range (1,(numJnts/2)+1):
            pm.select (cl=True)
            jnt1 = pm.joint (p=(0,0,0))
            cntrlName1= gen.createCntrl (jnt1.name() ,jnt1.name() ,1, 'circuloX', 1)
            cntrl1 = pm.PyNode (cntrlName1)
            pm.parentConstraint ( cntrl1,jnt1, mo=True)
            
            blend1A = pm.createNode ('blendTwoAttr')
            blend1B = pm.createNode ('blendTwoAttr')
            gammaCorr1 = pm.createNode ('gammaCorrect')
            cntrlList[0].attr ('autoVolumStregth') >> gammaCorr1.gammaX
            cntrlList[0].attr ('stretchDist') >> gammaCorr1.value.valueX
            blend1A.input[0].set (1)
            gammaCorr1.outValueX >> blend1A.input[1]
            blend1B.input[0].set(1)
            blend1A.output >> blend1B.input[1];
            cntrlList[3].attr('autoVolume') >> blend1B.attributesBlender
            ##blend1B.output >> cntrl1.getParent().scaleX
            blend1B.output >> cntrl1.getParent().scaleY
            blend1B.output >> cntrl1.getParent().scaleZ
            
            expre1=expre1+"$color = `colorAtPoint -o RGB -u "+str ((i/(numJnts/2.0))-(1.0/numJnts))+" -v 0.5 "+ramp1.name()+" `;$output["+str (i)+"] = $color[0];"+blend1A.name()+".attributesBlender=$output["+str (i)+"];"
            
            pm.select (cl=True)
            jnt2 = pm.joint (p=(0,0,0))            
            cntrlName2= gen.createCntrl (jnt2.name() ,jnt2.name() ,1, 'circuloX', 1)
            cntrl2 = pm.PyNode (cntrlName2)
            pm.parentConstraint ( cntrl2,jnt2, mo=True)


            blend2A = pm.createNode ('blendTwoAttr')
            blend2B = pm.createNode ('blendTwoAttr')
            gammaCorr2 = pm.createNode ('gammaCorrect')
            cntrlList[6].attr ('autoVolumStregth') >> gammaCorr2.gammaX
            cntrlList[6].attr ('stretchDist') >> gammaCorr2.value.valueX
            blend2A.input[0].set (1)
            gammaCorr2.outValueX >> blend2A.input[1]
            blend2B.input[0].set(1)
            blend2A.output >> blend2B.input[1];
            cntrlList[3].attr('autoVolume') >> blend2B.attributesBlender
            ##blend1B.output >> cntrl1.getParent().scaleX
            blend2B.output >> cntrl2.getParent().scaleY
            blend2B.output >> cntrl2.getParent().scaleZ
            
            expre2=expre2+"$color = `colorAtPoint -o RGB -u "+str ((i/(numJnts/2.0))-(1.0/numJnts))+" -v 0.5 "+ramp2.name()+" `;$output["+str (i)+"] = $color[0];"+blend2A.name()+".attributesBlender=$output["+str (i)+"];"
            
            foll1= self.attachObj (cntrl1.getParent(), bendSurf1[0], (i/(numJnts/2.0))-(1.0/numJnts), 0.5, 4)
            foll2= self.attachObj (cntrl2.getParent(), bendSurf2[0], (i/(numJnts/2.0))-(1.0/numJnts), 0.5, 4)

            pm.parent (jnt1, jnt2, skinJntsGrp)
            pm.parent (foll1, foll2,  follGrp)       
             
        pm.expression (s=expre1, ae=False)
        pm.expression (s=expre2, ae=False)
        
        pm.parent (skinJntsGrp, cntrlsSpace)
        pm.parent (follGrp, noMoveSpace)
                      
        
    def attachObj (self, obj, mesh, u, v, mode=1):
        foll = pm.createNode ('follicle')
        follDag = foll.firstParent()
        print foll, follDag
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
         
    def hookJntsOnCurve(self, jntList, upList, jntCrv, upCrv):
        jntNPoC = pm.createNode ('nearestPointOnCurve')
        jntGrpA  = pm.group (empty=True)
        jntCrv.worldSpace[0] >> jntNPoC.inputCurve
        
        jntGrpA.translate >> jntNPoC.inPosition
    
        upNPoC = pm.createNode ('nearestPointOnCurve')
        upGrpA  = pm.group (empty=True)
        upCrv.worldSpace[0] >> upNPoC.inputCurve
        upGrpA.translate >> upNPoC.inPosition
        
        for jnt, up in zip(jntList, upList):
            wp= pm.xform (jnt, t=True, ws=True, q=True)
            pm.xform (jntGrpA, t=wp, ws=True)
            hookPoci = pm.createNode ('pointOnCurveInfo')
            jntCrv.worldSpace[0] >> hookPoci.inputCurve
            hookPoci.position >> jnt.translate
            hookPar = jntNPoC.parameter.get()
            hookPoci.parameter.set(hookPar)
            pm.tangentConstraint (jntCrv, jnt, aimVector=(-1, 0, 0),upVector=(0,1, 0),worldUpType="object",worldUpObject =up )
    
            wp= pm.xform (up, t=True, ws=True, q=True)
            pm.xform (upGrpA, t=wp, ws=True)
            hookPoci = pm.createNode ('pointOnCurveInfo')
            upCrv.worldSpace[0] >> hookPoci.inputCurve
            hookPoci.position >> up.translate
            hookPar = upNPoC.parameter.get()
            hookPoci.parameter.set(hookPar)
    
        pm.delete (upNPoC, upGrpA , jntNPoC, jntGrpA)


x = FlexBezier()


