import pymel.core as pm
import maya.api.OpenMaya as om
import lcRigToolbox as tbox
import lcGeneric as gen

class RibbonBezier:
    def __init__(self,name='ribbonBezier', size=10, numJnts=10):
       
        self.ribbonDict = {}
        self.size = size
        self.numJnts = numJnts
        self.ribbonDict['size']=size
        self.ribbonDict['name']=name
        self.ribbonDict['numJnts']=numJnts
   
    def doRig(self): 
        anchorList = []
        cntrlList =[]
        locList =[]
               
        ###Estrutura No Move        
        noMoveSpace = pm.group (empty=True, n='noMove')
        noMoveSpace.visibility.set(0)
        noMoveSpace.translate.set(self.size*-0.5,0,0)    
        noMoveBend1 = pm.nurbsPlane ( p=(self.size*-0.25,0,0), ax=(0,0,1), w=self.size*0.5, lr = .1 , d = 3, u =5, v =1)        
        noMoveBend2 = pm.nurbsPlane ( p=(self.size*0.25,0,0), ax=(0,0,1), w=self.size*0.5, lr = .1 , d = 3, u =5, v =1)
        noMoveCrvJnt = pm.curve ( bezier=True, d=3, p=[(self.size*-0.5,0,0),(self.size*-0.4,0,0),(self.size*-0.1,0,0),(0,0,0),(self.size*0.1,0,0),(self.size*0.4,0,0),(self.size*0.5,0,0)], k=[0,0,0,1,1,1,2,2,2])        
        
        #Deformers das superficies noMove
        twist1 = pm.nonLinear(noMoveBend1[0],  type='twist')         #twist das superficies noMove
        twist2 = pm.nonLinear(noMoveBend2[0],  type='twist')
        twist1[1].rotateZ.set(90)
        twist2[1].rotateZ.set(90)
        wireDef = pm.wire (noMoveBend1[0], noMoveBend2[0], w=noMoveCrvJnt, dds=[(0, 50)]) #Wire das superficies noMove
        wireDef[0].rotation.set(0)
        baseWire = [x for x in wireDef[0].connections() if 'BaseWire' in x.name()]
        pm.group (baseWire, noMoveCrvJnt, noMoveBend1[0],noMoveBend2[0],  p=noMoveSpace)
        pm.parent (twist1[1],twist2[1], noMoveSpace) 
        
        ###Estrutura Move
        cntrlsSpace = pm.group (empty=True, n='local')
        cntrlsSpace.translate.set(self.size*-0.5,0,0)
        bendSurf1 = pm.nurbsPlane ( p=(self.size*-0.25,0,0), ax=(0,0,1), w=self.size*0.5, lr = .1 , d = 3, u =5, v =1)
        bendSurf2 = pm.nurbsPlane ( p=(self.size*0.25,0,0), ax=(0,0,1), w=self.size*0.5, lr = .1 , d = 3, u =5, v =1)   
        #blendShape transferindo as deformações para a superficie move
        blend1 = pm.blendShape (noMoveBend1[0], bendSurf1[0])
        blend2 = pm.blendShape (noMoveBend2[0], bendSurf2[0])
        pm.blendShape (blend1, e=True, w=[(0, 1)])
        pm.blendShape (blend2, e=True, w=[(0, 1)])
        pm.parent (bendSurf1[0], bendSurf2[0], cntrlsSpace ) 
        
        ##Cntrls                
        for i in range (0, 7):
            anchor = pm.cluster (noMoveCrvJnt.name()+'.cv['+str(i)+']')
            clsHandle = anchor [1]
            anchorGrp = pm.group (em=True, n='clusterGrp'+str (i))
            anchorDrn = pm.group (em=True, n='clusterDrn'+str (i),p=anchorGrp)
            pos = pm.xform (anchor, q=True, ws=True, rp=True)  
            pm.xform (anchorGrp, t=pos, ws=True)
            pm.parent (anchor[1], anchorDrn)   
            anchorList.append (anchor[1])
                                    
            #cntrlName =gen.createCntrl (anchor[1].name(),anchor[1].name() ,1, 'cubo', 1) ###    TROCAR AQUI PELA CLASSE CNTRL 
            if i==0 or i==3 or i==6:
                cntrl = CntrlCrv ('cntrl'+str(i+1), anchor[1], 'cubo',None, 0.5, (0,0,1))
            else:
                cntrl = CntrlCrv ('cntrl'+str(i+1), anchor[1], 'cubo',None, 0.3, (0,1,1))        
            # nao da para fazer contraint direto pela classe, pois precisamos da posicao do pivot do cluster
            pm.xform (cntrl.cntrlGrp, t=pos, ws=True)
            #pm.parentConstraint (cntrl.cntrl, anchor[1], mo=True)
            
            auxLocGrp = pm.group (em=True)
            auxLoc = pm.group (em=True, p=auxLocGrp) 
            pm.xform (auxLocGrp, t=pos, ws=True)
            loc = pm.PyNode (auxLoc)
            
            if i==1 or i==4:
                pm.xform (anchorGrp, s=(-1,1,1), r=True)
                pm.xform (cntrl.cntrlGrp, s=(-1,1,1), r=True)
                pm.xform (loc.getParent(), s=(-1,1,1), r=True)
            
            pm.parentConstraint (cntrl.cntrl, loc )                    
            loc.translate >> anchorDrn.translate
            loc.rotate >> anchorDrn.rotate
            cntrlList.append(cntrl)
            locList.append (loc)
                    
        cntrlList[0].cntrl.addAttr ('twist', at='double', dv=0, k=True)
        cntrlList[0].cntrl.addAttr ('stretchDist', at='double', dv=0, k=True)
        cntrlList[0].cntrl.addAttr ('autoVolumStregth', at='double', dv=0, k=True)
        cntrlList[3].cntrl.addAttr ('twist', at='double', dv=0, k=True)
        cntrlList[3].cntrl.addAttr ('autoVolume', at='double', dv=0, k=True)
        cntrlList[6].cntrl.addAttr ('twist', at='double', dv=0, k=True)
        cntrlList[6].cntrl.addAttr ('stretchDist', at='double', dv=0, k=True)
        cntrlList[6].cntrl.addAttr ('autoVolumStregth', at='double', dv=0, k=True)
        
        cntrlList[0].cntrl.twist >> twist1[0].endAngle
        cntrlList[3].cntrl.twist >> twist1[0].startAngle
        cntrlList[3].cntrl.twist >> twist2[0].endAngle
        cntrlList[6].cntrl.twist >> twist2[0].startAngle                 
        pm.parent (anchorList[1].getParent(2), anchorList[0])       
        pm.parent (anchorList[5].getParent(2), anchorList[6]) 
        pm.parent (anchorList[2].getParent(2),anchorList[4].getParent(2), anchorList[3])
        pm.parent (cntrlList[1].cntrlGrp, cntrlList[0].cntrl)       
        pm.parent (cntrlList[5].cntrlGrp, cntrlList[6].cntrl) 
        pm.parent (cntrlList[2].cntrlGrp, cntrlList[4].cntrlGrp, cntrlList[3].cntrl) 
        pm.parent (cntrlList[3].cntrlGrp, cntrlList[0].cntrlGrp, cntrlList[6].cntrlGrp, cntrlsSpace)
        pm.parent (locList[1].getParent(), locList[0])       
        pm.parent (locList[5].getParent(), locList[6]) 
        pm.parent (locList[2].getParent(),locList[4].getParent(), locList[3]) 
        pm.parent (locList[3].getParent(), locList[0].getParent(),locList[6].getParent(), cntrlsSpace)
        pm.parent (anchorList[3].getParent(2), anchorList[0].getParent(2),anchorList[6].getParent(2), noMoveSpace)        
        
        #Skin joints do ribbon
        skinJntsGrp = pm.group (em=True)
        follGrp = pm.group (em=True)
        
        #cria ramps        
        ramp1 = pm.createNode ('ramp')
        ramp1.attr('type').set(1)
        
        ramp2 = pm.createNode ('ramp')
        ramp2.attr('type').set(1)
        
        expre1 = "float $dummy = "+ramp1.name()+".outAlpha;float $output[];float $color[];"
        expre2 = "float $dummy = "+ramp2.name()+".outAlpha;float $output[];float $color[];"
        
        extraCntrlsGrp = pm.group (em=True,r=True, p=cntrlsSpace) 
           
        for i in range (1,(self.numJnts/2)+1):
            pm.select (cl=True)
            jnt1 = pm.joint (p=(0,0,0)) 
            cntrl1 = CntrlCrv ('cntrlExtraA'+str(i), jnt1, 'cubo','parentConstraint',0.2)         
        
            blend1A = pm.createNode ('blendTwoAttr')
            blend1B = pm.createNode ('blendTwoAttr')
            gammaCorr1 = pm.createNode ('gammaCorrect')    
            cntrlList[0].cntrl.attr ('autoVolumStregth') >> gammaCorr1.gammaX
            cntrlList[0].cntrl.attr ('stretchDist') >> gammaCorr1.value.valueX
            blend1A.input[0].set (1)
            gammaCorr1.outValueX >> blend1A.input[1]
            blend1B.input[0].set(1)
            blend1A.output >> blend1B.input[1];
            cntrlList[3].cntrl.attr('autoVolume') >> blend1B.attributesBlender
            blend1B.output >> cntrl1.cntrlGrp.scaleY
            blend1B.output >> cntrl1.cntrlGrp.scaleZ          
            expre1=expre1+"$color = `colorAtPoint -o RGB -u "+str ((i/(self.numJnts/2.0))-(1.0/self.numJnts))+" -v 0.5 "+ramp1.name()+" `;$output["+str (i)+"] = $color[0];"+blend1A.name()+".attributesBlender=$output["+str (i)+"];"            
        
            pm.select (cl=True)
            jnt2 = pm.joint (p=(0,0,0))            
            cntrl2 = CntrlCrv ('cntrlExtraB'+str(i), jnt2, 'cubo','parentConstraint',0.2)            
                
            blend2A = pm.createNode ('blendTwoAttr')
            blend2B = pm.createNode ('blendTwoAttr')
            gammaCorr2 = pm.createNode ('gammaCorrect')
            cntrlList[6].cntrl.attr ('autoVolumStregth') >> gammaCorr2.gammaX
            cntrlList[6].cntrl.attr ('stretchDist') >> gammaCorr2.value.valueX
            blend2A.input[0].set (1)
            gammaCorr2.outValueX >> blend2A.input[1]
            blend2B.input[0].set(1)
            blend2A.output >> blend2B.input[1];
            cntrlList[3].cntrl.attr('autoVolume') >> blend2B.attributesBlender
            blend2B.output >> cntrl2.cntrlGrp.scaleY
            blend2B.output >> cntrl2.cntrlGrp.scaleZ            
            expre2=expre2+"$color = `colorAtPoint -o RGB -u "+str ((i/(self.numJnts/2.0))-(1.0/self.numJnts))+" -v 0.5 "+ramp2.name()+" `;$output["+str (i)+"] = $color[0];"+blend2A.name()+".attributesBlender=$output["+str (i)+"];"           
        
            foll1= self.attachObj (cntrl1.cntrlGrp, bendSurf1[0], (i/(self.numJnts/2.0))-(1.0/self.numJnts), 0.5, 4)
            foll2= self.attachObj (cntrl2.cntrlGrp, bendSurf2[0], (i/(self.numJnts/2.0))-(1.0/self.numJnts), 0.5, 4)
            
            pm.parent (cntrl1.cntrlGrp, cntrl2.cntrlGrp,extraCntrlsGrp)
            pm.parent (jnt1, jnt2, skinJntsGrp)
            pm.parent (foll1, foll2,  follGrp)       
                     
        pm.expression (s=expre1, ae=False)
        pm.expression (s=expre2, ae=False)
        
        pm.parent (skinJntsGrp, cntrlsSpace)
        pm.parent (follGrp, noMoveSpace)
        
        #povoa ribbon Dict        
        self.ribbonDict['name']= 'bezierRibbon'
        self.ribbonDict['ribbonMoveAll']=cntrlsSpace
        for i in range (0, 7):
            self.ribbonDict['cntrl'+str(i)] = cntrlList[i]
                        
    def attachObj (self, obj, mesh, u, v, mode=1):
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

class CntrlCrv():
    """
        Cria uma curva de controle e conecta em um objeto 
        Parametros: 
            name (string): nome do novo controle
            obj(objeto) : objeto que será controlado 
            type(string): tipo de conexao 
                                    parent - parenteia o objeto ao controle
                                    contraint
                                    conexao direta
            icone (string): tipo do icone
                                cubo
            cntrlself.size (float): escala do controle
            rotateOrder (int): ordem de rotacao default zxy
    """  
    def __init__ (self, name, obj = None, icone='cubo', type = None, cntrlSize=1, color=(0,0,0), rotateOrder=2):                

    #seta variaveis com os inputs
        self.name = name
        self.rotateOrder = rotateOrder # seta rotation order. Por default: zxy
        self.cntrlSize = cntrlSize     
        self.cntrlledObj = obj
        self.cntrl= None
        self.cntrlGrp= None
        self.cnstr = None
        self.color = color
    #constroi icone                            
        if icone== "cubo":
            crv = pm.curve (n=name+"_cntrl", d=1,p=[(-0.5,0.5,0.5), (-0.5,0.5,-0.5), (0.5,0.5,-0.5),(0.5,0.5,0.5),(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),(-0.5,0.5,0.5),(-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(-0.5,0.5,-0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(0.5,-0.5,0.5)],k=[0,1,2,3,4 ,5,6,7,8,9,10,11,12,13,14,15,16])
            crv.scaleX.set (self.cntrlSize)
            crv.scaleY.set (self.cntrlSize)
            crv.scaleZ.set (self.cntrlSize)
            pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False )
        elif icone=='bola':
            crv = pm.circle (n=name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv1 = pm.circle (c=(0,0,0),nr=(1,0,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv2 = pm.circle (c=(0,0,0),nr=(0,0,1),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            pm.makeIdentity ([crv,crv1,crv2],apply=True,t=1,r=1,s=1,n=0)
            pm.parent ([crv1.getShape(),crv2.getShape()], crv, shape=True, r=True)
            pm.delete (crv1, crv2)
        elif icone=='circuloY':
            crv = pm.circle (n=name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv.scaleX.set (self.cntrlSize)
            crv.scaleY.set (self.cntrlSize)
            crv.scaleZ.set (self.cntrlSize)
            pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False )         

    #seta ordem de rotacao        
        crv.rotateOrder.set(self.rotateOrder)
        grp = pm.group (crv, n=name+"_grp")
        crv.rotateOrder.set(self.rotateOrder)
        pm.xform (grp, os=True, piv=[0,0,0])
        
    #cor
        crv.getShape().overrideEnabled.set (1)
        crv.getShape().overrideRGBColors.set(1)
        crv.getShape().overrideColorRGB.set (self.color) 
        
    #faz a conexao
        if self.cntrlledObj:
            matrix =pm.xform (self.cntrlledObj, q=True,  ws=True ,m=True) 
        
            pm.xform (grp, ws=True,  m=matrix)
            #pm.xform (grp, ws=True,  s=[self.cntrlSize,self.cntrlSize,self.cntrlSize])
            
            if type=='parent':
                obj.setParent (crv)
            elif type=='parentConstraint':
                cnstr = pm.parentConstraint (crv, obj, mo=True)
                self.cnstr = cnstr
            elif type=='orientConstraint':
                cnstr = pm.orientConstraint (crv, obj, mo=True)
                self.cnstr = cnstr                  
        self.cntrl= crv
        self.cntrlGrp = grp

class Limb():
    """
        Cria um Limb
        Parametros: 
            name (string): nome do novo limb
            
        Name
        IkCntrl
        EndCntrl ### AGORA CHAMA START, MUDAR PARA ENDCNTRL
        MidCntrl
        PoleCntrl
        
        guideDict
            guide1
            guide2
            guide3
        
                  
    """        

        
    def __init__ (self, limbDict=None):
                
        
        self.limbDict = {}
        self.twoJoints=False
        self.limbDict['ikCntrl'] = None
        self.limbDict['midCntrl'] = None
        self.limbDict['endCntrl'] = None
        self.limbDict['poleVec'] = None
        self.limbDict['joint1'] = None
        self.limbDict['joint2'] = None
        self.limbDict['joint3'] = None
        self.limbDict['limbMoveAll'] = None
        
        ##implementar aqui as setagens padrao
        self.limbDict['ikCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['midCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['endCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['poleVecSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['nodeTree']={}
        self.limbDict['nameConventions']=None
        ##FAZER AS SETAGENS PADRAO SE NAO VIEREM NO DICIONARIO

    def doRig(self):                        
        ## cria guia se não existir  
        locPos = [(0,0,0), (3,0,-1), (6,0,0)]
        for i in range (1,4):
            if not pm.objExists ('locator'+str(i)):
                loc = pm.spaceLocator (n='locator'+str(i), p=(0,0,0))
                pm.xform (loc, t=locPos[i-1], ws=True)
            else:
                locPos[i-1]= pm.xform ('locator'+str(i), q=True, t=True, ws=True)
        
        p1 = locPos[0]
        p2 = locPos[1]
        p3 = locPos[2]
        
        A= om.MVector(p1)
        B= om.MVector(p2)
        C= om.MVector(p3)
        
        #Calculando a normal do plano definido pelo guide
        #invertendo inverte a direcao do eixo ao longo do vetor
        AB = A-B
        BC = B-C
        
        #AB = B-A
        #BC = C-B
        
        n = BC^AB
        nNormal = n.normal()
        
        
        #duplos joint de cotovelo

        if self.twoJoints:
            AC=C-A
        
            p2a =B-AC.normal()*.5
            p2b =B+AC.normal()*.5
            
            loc2a = pm.spaceLocator (p=(0,0,0))
            pm.xform (loc2a, t=p2a, ws=True)
            loc2b = pm.spaceLocator (p=(0,0,0))
            pm.xform (loc2b, t=p2b, ws=True)
            
            B1= om.MVector (p2a)
            B2= om.MVector (p2b)
            
            AB1=A-B1
            B1B2 = B1-B2
            B2C = B2-C
            
            x = nNormal ^ AB1.normal()
            t = x.normal() ^ nNormal
            list = [ nNormal.x, nNormal.y, nNormal.z, 0, t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, A.x, A.y,A.z,1]
            m= om.MMatrix (list)
            pm.select(cl=True)
            j1 = pm.joint()
            pm.xform (j1, m = m, ws=True) 
            pm.makeIdentity (j1, apply=True, r=1, t=0, s=0, n=0, pn=0)
            
            x = nNormal ^ B1B2.normal()
            t = x.normal() ^ nNormal
            list = [ nNormal.x, nNormal.y, nNormal.z, 0, t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, B1.x, B1.y,B1.z,1]
            m= om.MMatrix (list)
            pm.select(cl=True)
            j2a = pm.joint()
            pm.xform (j2a, m = m, ws=True) 
            pm.makeIdentity (j2a, apply=True, r=1, t=0, s=0, n=0, pn=0)
            
            x = nNormal ^ B2C.normal()
            t = x.normal() ^ nNormal
            list = [ nNormal.x, nNormal.y, nNormal.z, 0, t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, B2.x, B2.y,B2.z,1]
            m= om.MMatrix (list)
            pm.select(cl=True)
            j2 = pm.joint()
            pm.xform (j2, m = m, ws=True) 
            pm.makeIdentity (j2, apply=True, r=1, t=0, s=0, n=0, pn=0)
            
            pm.select(cl=True)
            j3=pm.joint()
            pm.xform (j3, m = m, ws=True) 
            pm.xform (j3, t= C, ws=True)
            pm.makeIdentity (j3, apply=True, r=1, t=0, s=0, n=0, pn=0)
            
            pm.parent (j2a, j1)
            pm.parent (j2,j2a)
            pm.parent (j3, j2)
        else:
            x = nNormal ^ AB.normal()
            t = x.normal() ^ nNormal
            list = [ nNormal.x, nNormal.y, nNormal.z, 0, t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, A.x, A.y,A.z,1]
            m= om.MMatrix (list)
            
            pm.select(cl=True)
            j1 = pm.joint()
            pm.xform (j1, m = m, ws=True) 
            pm.makeIdentity (j1, apply=True, r=1, t=0, s=0, n=0, pn=0)
            
            x = nNormal ^ BC.normal()
            t = x.normal() ^ nNormal
            
            list = [ nNormal.x, nNormal.y, nNormal.z,0,t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, B.x, B.y, B.z,1]
            
            m= om.MMatrix (list)
            pm.select(cl=True)
            j2= pm.joint()
            pm.xform (j2, m = m, ws=True) 
            pm.makeIdentity (j2, apply=True, r=1, t=0, s=0, n=0, pn=0)
            
            pm.select(cl=True)
            j3=pm.joint()
            pm.xform (j3, m = m, ws=True) 
            pm.xform (j3, t= C, ws=True)
            pm.makeIdentity (j3, apply=True, r=1, t=0, s=0, n=0, pn=0)
            
            pm.parent (j2, j1)
            pm.parent (j3, j2)
        
        limbMoveAll = pm.group(empty=True)
        limbMoveAll.addAttr('ikfk', at='float',min=0, max=1,dv=1, k=1)
        
        j1.setParent (limbMoveAll)
        
        ###########################
        
        ##Estrutura FK
        endCntrl = CntrlCrv ('endCntrl', j1, 'circuloY', 'parentConstraint')
        endCntrl.cntrl.addAttr('manualStretch', at='float',min=.1,dv=1, k=1)
        
        midCntrl = CntrlCrv ('midCntrl', j2, 'circuloY', 'orientConstraint')
        midCntrl.cntrl.addAttr('manualStretch', at='float',min=.1,dv=1, k=1)
        
        pm.pointConstraint (j2, midCntrl.cntrlGrp, mo=True)
        
        ##Estrutura IK
        ikH = pm.ikHandle (sj=j1, ee=j3, sol="ikRPsolver")
        ikCntrl = CntrlCrv('teste',ikH[0],'cubo','parent')
        ikCntrl.cntrl.addAttr ('pin', at='float',min=0, max=1,dv=0, k=1)
        ikCntrl.cntrl.addAttr ('bias', at='float',min=-0.9, max=0.9, k=1)
        ikCntrl.cntrl.addAttr ('autoStretch', at='float',min=0, max=1,dv=1, k=1)
        ikCntrl.cntrl.addAttr ('manualStretch', at='float',dv=1, k=1)
        ikCntrl.cntrl.addAttr ('twist', at='float',dv=0, k=1)
        
        #pole vector
        poleVec = CntrlCrv('test5',j2,'bola')
        pm.xform (poleVec.cntrlGrp , t=(0,0,-2), r=True) 
        pm.xform (poleVec.cntrlGrp , ro=(0,0,0)) 
        pm.poleVectorConstraint (poleVec.cntrl, ikH[0])
        pm.parent (midCntrl.cntrlGrp, endCntrl.cntrl)
        pm.parent (endCntrl.cntrlGrp, poleVec.cntrlGrp, ikCntrl.cntrlGrp, limbMoveAll)
        
        #grupos de stretch
        startGrp = pm.group (empty=True)
        endGrp=pm.group (empty=True)
        pm.parent (endGrp,ikCntrl.cntrl,r=True)
        pm.xform (startGrp , t=p1, ws=True)
        pm.parent (startGrp,endCntrl.cntrl)
        
        ##NODE TREE#######               
        #Pin
        p4 = pm.xform (poleVec.cntrlGrp, q=True, t=True, ws=True)
        D=om.MVector (p4)
        
        if self.twoJoints:
            D1 = D-AC.normal()*.5
            D2 = D+AC.normal()*.5
            
            AD = A - D1
            CD = D2 - C
            
            distMax=AB1.length()+B2C.length() #distancia somada dos bones    
            pinScaleJnt1 = AD.length()/AB1.length()
            pinScaleJnt2 = CD.length()/B2C.length()
            pinLoc1 = pm.spaceLocator (p=(0,0,0))
            pm.xform (pinLoc1, t=D1, ws=True)
            pinLoc2 = pm.spaceLocator (p=(0,0,0))
            pm.xform (pinLoc2, t=D2, ws=True)
            pm.parent (pinLoc1, pinLoc2, poleVec.cntrl)            
        else:
            AD = A - D
            CD = D - C
            distMax=AB.length()+BC.length() #distancia somada dos bones    
            pinScaleJnt1 = AD.length()/AB.length()
            pinScaleJnt2 = CD.length()/BC.length()
        
        
        pinDist1 = pm.createNode ('distanceBetween',n='pinDist1') #distance do pole vector a ponta do joint1
        pinDist2 = pm.createNode ('distanceBetween',n='pinDist2') #distance do pole vector a ponta do joint2
        pinNorm1 = pm.createNode ('multiplyDivide',n='pinNorm1')  #normalizador distancia1 para escala
        pinNorm2 = pm.createNode ('multiplyDivide',n='pinNorm2')  #normalizador distancia2 para escala
        pinMultiScale1 = pm.createNode ('multDoubleLinear',n='pinMultiScale1') #multiplicador da distancia inicial pela escala Global
        pinMultiScale2 = pm.createNode ('multDoubleLinear',n='pinMultiScale2') #multiplicador da distancia inicial pela escala Global
        pinMultiOffset1 = pm.createNode ('multDoubleLinear',n='pinMultiOffset1') #multiplicador escala para chegar ao pole vec pela escala Global
        pinMultiOffset2 = pm.createNode ('multDoubleLinear',n='pinMultiOffset2') #multiplicador escala para chegar ao pole vec pela escala Global
        pinMulti1 = pm.createNode ('multDoubleLinear',n='pinMulti1') #multiplicador do normalizador
        pinMulti2 = pm.createNode ('multDoubleLinear',n='pinMulti2') #multiplicador do normalizador
               
        startGrp.worldMatrix[0] >> pinDist1.inMatrix1
        endGrp.worldMatrix[0] >> pinDist2.inMatrix1
        
        if self.twoJoints:
            pinLoc1.worldMatrix[0]  >> pinDist1.inMatrix2
            pinLoc2.worldMatrix[0]  >> pinDist2.inMatrix2
        else:
            poleVec.cntrl.worldMatrix[0]  >> pinDist1.inMatrix2
            poleVec.cntrl.worldMatrix[0]  >> pinDist2.inMatrix2
        
        limbMoveAll.scaleX >> pinMultiScale1.input1
        limbMoveAll.scaleX >> pinMultiScale2.input1
        
        pinMultiScale1.input2.set (AD.length())
        pinMultiScale2.input2.set (CD.length())
        
        pinMultiOffset1.input2.set (pinScaleJnt1)
        pinMultiOffset2.input2.set (pinScaleJnt2)
        pinMultiOffset1.input1.set (1)
        pinMultiOffset2.input1.set (1)
        
        pinDist1.distance >> pinNorm1.input1X
        pinDist2.distance >> pinNorm2.input1X
        pinMultiScale1.output >> pinNorm1.input2X
        pinMultiScale2.output >> pinNorm2.input2X
        pinNorm1.operation.set(2)
        pinNorm2.operation.set(2)
        
        pinNorm1.outputX >> pinMulti1.input1
        pinNorm2.outputX >> pinMulti2.input1
        pinMultiOffset1.output >> pinMulti1.input2
        pinMultiOffset2.output >> pinMulti2.input2
         
        ##Stretch
        stretchDist = pm.createNode ('distanceBetween',n='stretchDist') #distance
        stretchNorm = pm.createNode ('multiplyDivide',n='stretchNorm')  #normalizador
        stretchMultiScale = pm.createNode ('multDoubleLinear',n='stretchMultiScale') #mutiplica valor maximo pela escala do moveAll
        stretchCond = pm.createNode ('condition',n='stretchCond') # condicao so estica se for maior q distancia maxima
        stretchAdd2jointsDist = pm.createNode ('addDoubleLinear',n='stretchAdd2jointDist') # condicao so estica se for maior q distancia maxima
        
        ##Manual Stretch
        stretchManualStretch1 = pm.createNode ('multDoubleLinear',n='stretchManualStretch1') #mutiplica valor maximo pela escala do moveAll
        stretchManualStretch2 = pm.createNode ('multDoubleLinear',n='stretchManualStretch2') #mutiplica valor maximo pela escala do moveAll
        stretchManualStretch3 = pm.createNode ('multDoubleLinear',n='stretchManualStretch3') #mutiplica valor maximo pela escala do moveAll
        
        startGrp.worldMatrix[0] >> stretchDist.inMatrix1
        endGrp.worldMatrix[0] >> stretchDist.inMatrix2
        
        limbMoveAll.scaleX >> stretchMultiScale.input1
        stretchMultiScale.input2.set (distMax)
        stretchMultiScale.output >> stretchManualStretch1.input2
        stretchManualStretch1.output >> stretchNorm.input2X
        stretchNorm.operation.set(2)
        
        if self.twoJoints:
            stretchAdd2jointsDist = pm.createNode ('addDoubleLinear',n='stretchAdd2jointDist') # condicao so estica se for maior q distancia maxima
            stretchDist.distance >> stretchAdd2jointsDist.input1
            stretchAdd2jointsDist.output >> stretchNorm.input1X
            stretchAdd2jointsDist.input2.set (-1*B1B2.length())
        else:
            stretchDist.distance >>  stretchNorm.input1X    
        
        stretchNorm.outputX >> stretchCond.colorIfTrue.colorIfTrueR
        stretchNorm.outputX >> stretchCond.firstTerm
        stretchCond.operation.set (2)
        stretchCond.secondTerm.set (1)
        stretchCond.colorIfFalseR.set (1)
        

        
        ##AutoStretch switch
        autoStretchSwitch = pm.createNode ('blendTwoAttr',n='autoStretchSwitch') 
        stretchCond.outColor.outColorR >> autoStretchSwitch.input[1]
        autoStretchSwitch.input[0].set(1)
        
        ##Bias
        biasAdd1 =  pm.createNode ('plusMinusAverage',n='biasAdd1')
        biasAdd2 =  pm.createNode ('plusMinusAverage',n='biasAdd2')
        biasMulti1 = pm.createNode ('multDoubleLinear',n='biasMult1') 
        biasMulti2  = pm.createNode ('multDoubleLinear',n='biasMult2')
        
        biasAdd1.input1D[1].set(1)
        biasAdd1.operation.set(1)
        biasAdd1.output1D >> biasMulti1.input1
        autoStretchSwitch.output >> biasMulti1.input2
        biasMulti1.output >> stretchManualStretch2.input2
        biasAdd2.input1D[0].set(1)
        biasAdd2.operation.set(2)
        biasAdd2.output1D >> biasMulti2.input1
        autoStretchSwitch.output >> biasMulti2.input2
        biasMulti2.output >> stretchManualStretch3.input2
        
        ##Twist offset
        twistBlend1 = pm.createNode ('blendTwoAttr', n='twistBlend')
        twistBlend1.input[0].set(1)
        twistBlend1.output >> ikH[0].twist
        
        ##Blend stretch e pin
        stretchPinBlend1 = pm.createNode ('blendTwoAttr',n='stretchPinBlend1') 
        stretchPinBlend2 = pm.createNode ('blendTwoAttr',n='stretchPinBlend2')
        stretchManualStretch2.output >> stretchPinBlend1.input[0]
        stretchManualStretch3.output >> stretchPinBlend2.input[0]
        pinMulti1.output >> stretchPinBlend1.input[1]
        pinMulti2.output >> stretchPinBlend2.input[1]
        
        ##Blend ikfk
        ikfkBlend1 = pm.createNode ('blendTwoAttr',n='ikfkBlend1')
        ikfkBlend2 = pm.createNode ('blendTwoAttr',n='ikfkBlend2')
        ikfkReverse = pm.createNode ('reverse',n='ikfkReverse')
        stretchPinBlend1.output >> ikfkBlend1.input[0]
        stretchPinBlend2.output >> ikfkBlend2.input[0]
        
        
        endCntrl.cntrl.manualStretch >> ikfkBlend1.input[1] ##AQUI PRECISA MULTIPLICAR PELA ESCALA GLOBAL
        midCntrl.cntrl.manualStretch >> ikfkBlend2.input[1]
       
        limbMoveAll.ikfk >> ikfkReverse.inputX
        ikfkReverse.outputX >> ikfkBlend1.attributesBlender
        ikfkReverse.outputX >> ikfkBlend2.attributesBlender
               
        list = midCntrl.cnstr.connections(p=True, d=False, s=True) ##Descobre o parametro de peso do constraint
        weightAttr = [x for x in list if 'W0' in x.name()][0]
        ikfkReverse.outputX >> weightAttr
        
        limbMoveAll.ikfk >> ikH[0].ikBlend      
        ikfkBlend1.output >> j1.scaleY 
        ikfkBlend2.output >> j2.scaleY
        
        ##Atributos e conexoes do controle ik
        ikCntrl.cntrl.bias >> biasAdd2.input1D[1]
        ikCntrl.cntrl.bias >> biasAdd1.input1D[0]
        ikCntrl.cntrl.pin >> stretchPinBlend1.attributesBlender
        ikCntrl.cntrl.pin >> stretchPinBlend2.attributesBlender
        ikCntrl.cntrl.manualStretch >> stretchManualStretch1.input1
        ikCntrl.cntrl.manualStretch >> stretchManualStretch2.input1
        ikCntrl.cntrl.manualStretch >> stretchManualStretch3.input1
        ikCntrl.cntrl.autoStretch >> autoStretchSwitch.attributesBlender
        ikCntrl.cntrl.pin >> twistBlend1.attributesBlender
        ikCntrl.cntrl.twist >> twistBlend1.input[0]


        ###Dicionario do Limb
        self.limbDict['ikCntrl'] = ikCntrl
        self.limbDict['midCntrl'] = midCntrl
        self.limbDict['endCntrl'] = endCntrl
        self.limbDict['poleVec'] = poleVec
        self.limbDict['joint1'] = j1
        self.limbDict['joint2'] = j2
        self.limbDict['joint3'] = j3
        self.limbDict['limbMoveAll'] = limbMoveAll
        
        ##implementar aqui as setagens padrao
        self.limbDict['ikCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['midCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['endCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['poleVecSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['nodeTree']={}
        self.limbDict['nameConventions']=None
        
###############################
## bezier
 import pymel.core as pm

class twistExtractor:
    def __init__(self, twistJntIn, axis='Y'):
        
        self.extractor = None
        
        #Error Handling
        try:
            twistJnt=pm.PyNode(twistJntIn)
        except:
            print "ERROR:The Node Doesn't Exist:", twistJntIn
            return

        try:
            twistJnt.getParent()
        except:
            print "ERROR:The Node Has No Parent:", twistJntIn
            return
            
        try:
            twistJnt.childAtIndex(0)
        except:
            print "ERROR:The Node Has No Child:", twistJntIn
            return
        
        if twistJnt.nodeType() != 'joint':
            print "ERROR:The Node Is Not A Joint:", twistJntIn
            return    
        
        if twistJnt.childAtIndex(0).nodeType() != 'joint':
            print "ERROR:The Node Child Is Not A Joint:", twistJnt.childAtIndex(0)
            return 
                    
        #cria grupo base e parenteia no pai do joint fonte do twist
        extractorGrp = pm.group (empty = True)
        pm.parentConstraint (twistJnt.getParent(),extractorGrp,  mo=False)
        pm.scaleConstraint (twistJnt.getParent(),extractorGrp,  mo=True)
        
        #duplica o joint fonte do twist e seu filho
        extractorStart = pm.duplicate (twistJnt, po=True)[0]
        pm.makeIdentity (extractorStart, a=True, r=True)
        extractorEnd = pm.duplicate (twistJnt.childAtIndex(0), po=True)[0]
        pm.parent (extractorEnd, extractorStart)
        pm.parent (extractorStart, extractorGrp)
        
        #cria o locator que calcula o twist. Cria OrientConstraint
        extractorLoc = pm.spaceLocator ()
        pm.parent (extractorLoc,  extractorStart, r=True)
        ori = pm.orientConstraint (twistJnt, extractorStart, extractorLoc, mo=False) 
        ori.interpType.set (0)
        
        #cria ik handle com polevector zerado e parenteia no joint fonte (noRoll)
        extractorIkh = pm.ikHandle( sj=extractorStart, ee=extractorEnd, sol='ikRPsolver')[0]
        extractorIkh.poleVector.set(0,0,0)        
        pm.parentConstraint (twistJnt, extractorIkh, mo=True)
        pm.parent (extractorIkh, extractorGrp )
        
        # multiplica por 2 o valor de rot do locator
        pm.addAttr (extractorLoc, ln='extractTwist', at='double', k=1)
        multi = pm.createNode ('multDoubleLinear')
        multi.input2.set(2)
        extractorLoc.attr('rotate'+axis) >> multi.input1
        multi.output >> extractorLoc.extractTwist
        self.extractor = extractorLoc



x = Limb()
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
ribbonEndCntrl = rb.ribbonDict['cntrl0']
ribbonMidCntrl = rb.ribbonDict['cntrl3']
ribbonStartCntrl = rb.ribbonDict['cntrl6']
ribbonMid1TangCntrl = rb.ribbonDict['cntrl4']
ribbonMid2TangCntrl = rb.ribbonDict['cntrl2']
startGrp = pm.group (em=True)
midGrp = pm.group (em=True)
endGrp = pm.group (em=True)

pm.parentConstraint (limbJoint1,endGrp,mo=False)
pm.pointConstraint (limbJoint2,midGrp,mo=False)
pm.orientConstraint (limbJoint2,limbJoint1,midGrp,mo=False)
pm.parentConstraint (limbJoint3,startGrp,mo=False)

pm.parent (ribbonEndCntrl.cntrlGrp, endGrp)
pm.parent (ribbonMidCntrl.cntrlGrp, midGrp)
pm.parent (ribbonStartCntrl.cntrlGrp, startGrp)
pm.parent (startGrp,midGrp,endGrp,ribbonMoveAll)
pm.parent (ribbonMoveAll, limbMoveAll)

##lembrar de implementar outras possibilidade de eixos
ribbonMoveAll.translate.set(0,0,0)
ribbonMoveAll.rotate.set(0,0,0)
ribbonEndCntrl.cntrlGrp.translate.set(0,0,0)
ribbonEndCntrl.cntrlGrp.rotate.set(0,0,-90)
ribbonMidCntrl.cntrlGrp.translate.set(0,0,0)
ribbonMidCntrl.cntrlGrp.rotate.set(0,0,-90)
ribbonStartCntrl.cntrlGrp.translate.set(0,0,0)
ribbonStartCntrl.cntrlGrp.rotate.set(0,0,-90)

mid1Tang1Grp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
mid1Tang2Grp = pm.group (em=True, p=limbJoint2)
mid2Tang1Grp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
mid2Tang2Grp = pm.group (em=True, p=limbJoint1)

mid1Tang1Grp.translate.set(L*0.1,0,0)
mid1Tang2Grp.translate.set(0,L*-0.1,0)
#mid1Tang2Grp.setParent (ribbonMidCntrl.cntrl)

mid2Tang1Grp.translate.set(L*-0.1,0,0)
mid2Tang2Grp.translate.set(0,-1*(AB.length()-(L*0.1)),0)
#mid2Tang2Grp.setParent (ribbonMidCntrl.cntrl)

pm.parentConstraint (mid1Tang1Grp, mid1Tang2Grp, ribbonMid1TangCntrl.cntrlGrp)
pm.parentConstraint (mid2Tang1Grp, mid2Tang2Grp, ribbonMid2TangCntrl.cntrlGrp)
        
extra =  twistExtractor ('joint14')