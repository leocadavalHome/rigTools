def composeMMatrix (vecX, vecY, vecZ, vecP ):
    list = [ vecX.x, vecX.y, vecX.z, 0, vecY.x, vecY.y, vecY.z, 0, vecZ.x, vecZ.y, vecZ.z, 0, vecP.x, vecP.y,vecP.z,1]
    m= om.MMatrix (list)
    return m

def makeJoint(name='joint', matrix=None, obj=None, connectToLast=False):
    if not connectToLast:
        pm.select (cl=True)            
    jnt= pm.joint(n=name)
    if obj:
        pm.xform (obj, m = m, q=True, ws=True)
        pm.xform (jnt, m = m, ws=True)
    if matrix:        
        pm.xform (jnt, m = m, ws=True) 
    pm.makeIdentity (jnt, apply=True, r=1, t=0, s=0, n=0, pn=0)
    return jnt

def cntrlCrv(name='cntrl', obj=None, connType=None, **kwargs):
        
    #    Parametros: 
    #        name (string): nome do novo controle
    #        obj(objeto) : objeto que será controlado 
    #        connType(string): tipo de conexao (parent,parentConstraint,orientConstraint)
    #        icone (string): tipo do icone (cubo,bola,circuloX,circuloY,circuloZ)
    #        size (float): escala do controle
    #        color (R,G,B): cor
    #        rotateOrder (int): ordem de rotacao default zxy

    #seta variaveis com os inputs            
    #name=name
    cntrlledObj = obj
    connType = connType
    icone = kwargs.pop('icone','cubo')
    cntrlSize = kwargs.pop('size', 1 )
    color = kwargs.pop('color', None)
    rotateOrder = kwargs.pop('rotateOrder', 0) #default xyz
    nameConventions = kwargs.pop('nameConventions', None) #default xyz                                      
    cntrl= None
    cntrlGrp= None
    cnstr = None
        
    #constroi icone                            
    if icone== "cubo":
        crv = pm.curve (n=name+"_cntrl", d=1,p=[(-0.5,0.5,0.5), (-0.5,0.5,-0.5), (0.5,0.5,-0.5),(0.5,0.5,0.5),(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),(-0.5,0.5,0.5),(-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(-0.5,0.5,-0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(0.5,-0.5,0.5)],k=[0,1,2,3,4 ,5,6,7,8,9,10,11,12,13,14,15,16])
        crv.scaleX.set (cntrlSize)
        crv.scaleY.set (cntrlSize)
        crv.scaleZ.set (cntrlSize)
        pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False )
    elif icone=='bola':
        crv = pm.circle (n=name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
        crv1 = pm.circle (c=(0,0,0),nr=(1,0,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
        crv2 = pm.circle (c=(0,0,0),nr=(0,0,1),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
        pm.parent ([crv1.getShape(),crv2.getShape()], crv, shape=True, r=True)
        pm.delete (crv1, crv2)
        crv.scaleX.set (cntrlSize)
        crv.scaleY.set (cntrlSize)
        crv.scaleZ.set (cntrlSize)
        pm.makeIdentity (crv,apply=True,t=1,r=1,s=1,n=0)
    elif icone=='circuloY':
        crv = pm.circle (n=name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
        crv.scaleX.set (cntrlSize)
        crv.scaleY.set (cntrlSize)
        crv.scaleZ.set (cntrlSize)
        pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False )         
    elif icone=='circuloX':
        crv = pm.circle (n=name+"_cntrl" , c=(0,0,0),nr=(1,0,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
        crv.scaleX.set (cntrlSize)
        crv.scaleY.set (cntrlSize)
        crv.scaleZ.set (cntrlSize)
        pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False ) 
    elif icone=='circuloZ':
        crv = pm.circle (n=name+"_cntrl" , c=(0,0,0),nr=(0,0,1),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
        crv.scaleX.set (cntrlSize)
        crv.scaleY.set (cntrlSize)
        crv.scaleZ.set (cntrlSize)
        pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False ) 
        
#seta ordem de rotacao        
    crv.rotateOrder.set(rotateOrder)
    grp = pm.group (crv, n=name+"_grp")
    crv.rotateOrder.set(rotateOrder)
    pm.xform (grp, os=True, piv=[0,0,0])
    
#cor
    if color:
        shList = crv.getShapes()
        for sh in shList:
            sh.overrideEnabled.set (1)
            sh.overrideRGBColors.set(1)
            sh.overrideColorRGB.set (color) 
    
#faz a conexao
    if cntrlledObj:
        matrix =pm.xform (cntrlledObj, q=True,  ws=True ,m=True) 
    
        pm.xform (grp, ws=True,  m=matrix)
        
        if connType=='parent':
            cntrlledObj.setParent (crv)
        elif connType=='parentConstraint':
            cnstr = pm.parentConstraint (crv, cntrlledObj, mo=True)
        elif connType=='orientConstraint':
            cnstr = pm.orientConstraint (crv, cntrlledObj, mo=True)                  
    
    return (crv)
        
        
class twistExtractor:
    """
        Cria uma estrutura para calcular o twist de um joint 
        Parametros: 
            twistJntIn: joint a ser calculado
    """  
    
    def __init__(self, twistJntIn, conn='parentConstraint' ):
        
        self.extractor = None
        self.axis= 'X' #hard coding X como eixo. Aparentemente so ele funciona
        self.extractorGrp = None
        
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
        matrix =pm.xform (twistJnt.getParent(),q=True, m=True, ws=True)
        pm.xform (extractorGrp, m=matrix , ws=True)
        
        if conn=='parentConstraint':
            pm.parentConstraint (twistJnt.getParent(),extractorGrp,  mo=False)
        elif  conn=='parent':
            pm.parent (extractorGrp,twistJnt.getParent())
        
        self.extractorGrp =  extractorGrp         
        #pm.scaleConstraint (twistJnt.getParent(),extractorGrp,  mo=True)
        
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
        extractorLoc.attr('rotate'+self.axis) >> multi.input1
        multi.output >> extractorLoc.extractTwist
        self.extractor = extractorLoc

class RibbonBezier:
    """
        Cria um ribbon bezier
        Parametros: 
            name:
            size:
            numJoints:
           
    """ 
    ##IMPLEMENTAR:
    #controle de twist fique liberado pra q o usuario de offset, principalmente no inicio
    #stretch/squash com distancia ja no ribbon
        
    def __init__( self, **kwargs ):
        
        self.ribbonDict = {}
                    
        self.ribbonDict['size']=kwargs.pop('size', 10)
        self.ribbonDict['name']=kwargs.pop('name','ribbonBezier')
        self.ribbonDict['numJnts']=kwargs.pop('numJnts',10)
            
        self.name = self.ribbonDict['name']
        self.size = self.ribbonDict['size']
        self.numJnts = self.ribbonDict['numJnts']
        
        self.ribbonDict['cntrlSetup']={'nameTempl':'cntrl','icone':'circuloX','size':0.6,'color':(0,0,1)}       
        self.ribbonDict['cntrlTangSetup']={'nameTempl':'cntrl','icone':'bola','size':0.3,'color':(0,1,1)}        
        self.ribbonDict['cntrlExtraSetup']={'nameTempl':'cntrlExtra','icone':'circuloX','size':0.2}        

           
    def doRig(self): 
        anchorList = []
        cntrlList =[]
        locList =[]
        
        if pm.objExists(self.name+'NoMove'):
            pm.delete (self.name+'NoMove')
        if pm.objExists(self.name+'MoveAll'):
            pm.delete (self.name+'MoveAll')
                           
        ###Estrutura que nao deve ter transformacao       
        noMoveSpace = pm.group (empty=True, n=self.name+'NoMove')
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
        wireDef[0].rotation.set(1) #seta rotacao pra acontecer
        baseWire = [x for x in wireDef[0].connections() if 'BaseWire' in x.name()]
        pm.group (baseWire, noMoveCrvJnt, noMoveBend1[0],noMoveBend2[0],  p=noMoveSpace)
        pm.parent (twist1[1],twist2[1], noMoveSpace) 
        
        ###Estrutura que pode ser movida
        cntrlsSpace = pm.group (empty=True, n=self.name+'MoveAll')
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
                                    
            if i==0 or i==3 or i==6:
                displaySetup= self.ribbonDict['cntrlSetup'].copy()                               
                cntrlName = displaySetup['nameTempl']+str(i)           
                cntrl = cntrlCrv (name=cntrlName, obj=anchor[1],**displaySetup)
            else:
                displaySetup= self.ribbonDict['cntrlTangSetup'].copy()                               
                cntrlName = displaySetup['nameTempl']+str(i) 
                cntrl = cntrlCrv (name=cntrlName, obj=anchor[1],**displaySetup)
                        
            #Nao pode fazer conexao na criacao do controle, pois tera conexao direta
            pm.xform (cntrl.getParent(), t=pos, ws=True)
            
            #estrutura de buffers para conexao direta
            auxLocGrp = pm.group (em=True)
            auxLoc = pm.group (em=True, p=auxLocGrp) 
            pm.xform (auxLocGrp, t=pos, ws=True)
            loc = pm.PyNode (auxLoc)
            
            if i==1 or i==4:
                pm.xform (anchorGrp, s=(-1,1,1), r=True)
                pm.xform (cntrl.getParent(), s=(-1,1,1), r=True)
                pm.xform (loc.getParent(), s=(-1,1,1), r=True)
            
            #Conexoes dos buffers cm os clusters e com os controles
            pm.parentConstraint (cntrl, loc )                    
            loc.translate >> anchorDrn.translate
            loc.rotate >> anchorDrn.rotate
            cntrlList.append(cntrl)
            locList.append (loc)
        
        cntrlsSpace.addAttr ('cntrlsVis', at='double', dv=1, k=False, h=True)
        cntrlsSpace.addAttr ('extraCntrlsVis', at='double', dv=0, k=False, h=True)            
        cntrlList[0].addAttr ('twist', at='double', dv=0, k=True)
        cntrlList[0].addAttr ('stretchDist', at='double', dv=0, k=True)
        cntrlList[0].addAttr ('autoVolumStregth', at='double', dv=0, k=True)
        cntrlList[3].addAttr ('twist', at='double', dv=0, k=True)
        cntrlList[3].addAttr ('autoVolume', at='double', dv=0, k=True)
        cntrlList[6].addAttr ('twist', at='double', dv=0, k=True)
        cntrlList[6].addAttr ('stretchDist', at='double', dv=0, k=True)
        cntrlList[6].addAttr ('autoVolumStregth', at='double', dv=0, k=True)
        
        cntrlList[0].twist >> twist1[0].endAngle
        cntrlList[3].twist >> twist1[0].startAngle
        cntrlList[3].twist >> twist2[0].endAngle
        cntrlList[6].twist >> twist2[0].startAngle 
        
        #hierarquia                
        pm.parent (anchorList[1].getParent(2), anchorList[0])       
        pm.parent (anchorList[5].getParent(2), anchorList[6]) 
        pm.parent (anchorList[2].getParent(2),anchorList[4].getParent(2), anchorList[3])
        pm.parent (cntrlList[1].getParent(), cntrlList[0])       
        pm.parent (cntrlList[5].getParent(), cntrlList[6]) 
        pm.parent (cntrlList[2].getParent(), cntrlList[4].getParent(), cntrlList[3]) 
        pm.parent (cntrlList[3].getParent(), cntrlList[0].getParent(), cntrlList[6].getParent(), cntrlsSpace)
        pm.parent (locList[1].getParent(), locList[0])       
        pm.parent (locList[5].getParent(), locList[6]) 
        pm.parent (locList[2].getParent(),locList[4].getParent(), locList[3]) 
        pm.parent (locList[3].getParent(), locList[0].getParent(),locList[6].getParent(), cntrlsSpace)
        pm.parent (anchorList[3].getParent(2), anchorList[0].getParent(2),anchorList[6].getParent(2), noMoveSpace)        
        
        #Skin joints do ribbon
        skinJntsGrp = pm.group (em=True)
        follGrp = pm.group (em=True)
        
        #cria ramps para controlar o perfil de squash e stretch       
        ramp1 = pm.createNode ('ramp')
        ramp1.attr('type').set(1)
        
        ramp2 = pm.createNode ('ramp')
        ramp2.attr('type').set(1)
        
        expre1 = "float $dummy = "+ramp1.name()+".outAlpha;float $output[];float $color[];"
        expre2 = "float $dummy = "+ramp2.name()+".outAlpha;float $output[];float $color[];"
        
        extraCntrlsGrp = pm.group (em=True,r=True, p=cntrlsSpace) 
        
        #loop pra fazer os colocar o numero escolhido de joints ao longo do ribbon.
        #cria tmb node tree pro squash/stretch
        #e controles extras 
          
        for i in range (1,(self.numJnts/2)+1):
            #cria estrutura pra superficie 1
            pm.select (cl=True)
            jnt1 = pm.joint (p=(0,0,0))
            
            displaySetup = self.ribbonDict['cntrlExtraSetup'].copy()                               
            cntrlName = displaySetup['nameTempl']+'A'+str(i) 
            cntrl1 = cntrlCrv (name = cntrlName, obj=jnt1, connType='parentConstraint',**displaySetup)   
                  
            #node tree
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
            blend1B.output >> cntrl1.getParent().scaleY
            blend1B.output >> cntrl1.getParent().scaleZ  
            #expressao que le a rampa para setar valores da escala de cada joint quando fizer squash/stretch        
            expre1=expre1+"$color = `colorAtPoint -o RGB -u "+str ((i/(self.numJnts/2.0))-(1.0/self.numJnts))+" -v 0.5 "+ramp1.name()+" `;$output["+str (i)+"] = $color[0];"+blend1A.name()+".attributesBlender=$output["+str (i)+"];"            
            
            #cria estrutura pra superficie 2       
            pm.select (cl=True)
            jnt2 = pm.joint (p=(0,0,0))
            
            displaySetup = self.ribbonDict['cntrlExtraSetup'].copy()                              
            cntrlName = displaySetup['nameTempl']+'B'+str(i)             
            cntrl2 = cntrlCrv (name=cntrlName , connType='parentConstraint',obj=jnt2, **displaySetup)  
                      
            #node tree    
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
            blend2B.output >> cntrl2.getParent().scaleY
            blend2B.output >> cntrl2.getParent().scaleZ
            #expressao que le a rampa para setar valores da escala de cada joint quando fizer squash/stretch           
            expre2=expre2+"$color = `colorAtPoint -o RGB -u "+str ((i/(self.numJnts/2.0))-(1.0/self.numJnts))+" -v 0.5 "+ramp2.name()+" `;$output["+str (i)+"] = $color[0];"+blend2A.name()+".attributesBlender=$output["+str (i)+"];"           
            
            #prende joints nas supeficies com follicules
            foll1= self.attachObj (cntrl1.getParent(), bendSurf1[0], (i/(self.numJnts/2.0))-(1.0/self.numJnts), 0.5, 4)
            foll2= self.attachObj (cntrl2.getParent(), bendSurf2[0], (i/(self.numJnts/2.0))-(1.0/self.numJnts), 0.5, 4)
            
            pm.parent (cntrl1.getParent(), cntrl2.getParent(),extraCntrlsGrp)
            pm.parent (jnt1, jnt2, skinJntsGrp)
            pm.parent (foll1, foll2,  follGrp)       
        
        #seta expressoes para so serem avaliadas por demanda             
        pm.expression (s=expre1, ae=False)
        pm.expression (s=expre2, ae=False)
        
        pm.parent (skinJntsGrp, cntrlsSpace)
        pm.parent (follGrp, noMoveSpace)
        
        #hideCntrls
        pm.toggle (bendSurf1[0], bendSurf2[0], g=True)
        #skinJntsGrp.visibility.set(0)
        cntrlsSpace.extraCntrlsVis >> extraCntrlsGrp.visibility
        cntrlsSpace.cntrlsVis >> cntrlList[0].getParent().visibility
        cntrlsSpace.cntrlsVis >> cntrlList[3].getParent().visibility
        cntrlsSpace.cntrlsVis >> cntrlList[6].getParent().visibility
              
        #povoa ribbon Dict        
        self.ribbonDict['name']= 'bezierRibbon'
        self.ribbonDict['ribbonMoveAll']= cntrlsSpace
        for i in range (0, 7):
            self.ribbonDict['cntrl'+str(i)] = cntrlList[i]
    
    #Metodo para colar objetos por follicules                    
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
    
    #Metodo para descobrir ponto mais proximo da superficie onde devem objeto deve ser colado      
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

    def connectToLimb(self,limbObject): 
        #seta as variaveis locais com valores dos dicionarios dos objetos                 
        ribbonMoveAll = self.ribbonDict['ribbonMoveAll']
        limbMoveAll = limbObject.limbDict['limbMoveAll']
        limbJoint1 = limbObject.limbDict['joint1']
        limbJoint2 = limbObject.limbDict['joint2']
        limbJoint3 = limbObject.limbDict['joint3']
        limbJoint4 = limbObject.limbDict['joint4']
        ribbonEndCntrl = self.ribbonDict['cntrl0']
        ribbonMidCntrl = self.ribbonDict['cntrl3']
        ribbonStartCntrl = self.ribbonDict['cntrl6']
        ribbonMid2TangCntrl = self.ribbonDict['cntrl4']
        ribbonMid1TangCntrl = self.ribbonDict['cntrl2']
        if limbObject.flipAxis:
            rotY=180
        else:
            rotY=0
        #grupos de conexao
        startGrp = pm.group (em=True)
        midGrp = pm.group (em=True)
        endGrp = pm.group (em=True)
 
        pm.parentConstraint (limbJoint1,endGrp,mo=False)
        pm.pointConstraint (limbJoint2,midGrp,mo=False)
        ori = pm.orientConstraint (limbJoint2,limbJoint1,midGrp,mo=False)
        ori.interpType.set (2)
        pm.parentConstraint (limbJoint3,startGrp,mo=False)
        
        #hierarquia
        pm.parent (ribbonMoveAll, limbJoint1)
        ribbonMoveAll.translate.set(0,0,0)
        ribbonMoveAll.rotate.set(0,rotY,0)
        pm.parent (ribbonMoveAll, limbMoveAll)
        pm.parentConstraint (limbJoint1, ribbonMoveAll, mo=True)

        pm.parent (ribbonEndCntrl.getParent(), endGrp)
        pm.parent (ribbonMidCntrl.getParent(), midGrp)
        pm.parent (ribbonStartCntrl.getParent(), startGrp)
        pm.parent (startGrp,midGrp,endGrp,ribbonMoveAll)

        ##lembrar de implementar outras possibilidade de eixos. Hardcode de X
        ribbonEndCntrl.getParent().translate.set(0,0,0)
        ribbonEndCntrl.getParent().rotate.set(0,rotY,0)
        ribbonMidCntrl.getParent().translate.set(0,0,0)
        ribbonMidCntrl.getParent().rotate.set(0,rotY,0)
        ribbonStartCntrl.getParent().translate.set(0,0,0)
        ribbonStartCntrl.getParent().rotate.set(0,rotY,0)

        #sistema de controle das tangentes suaves ou duras
        mid1AimGrp = pm.group (em=True, p=ribbonMidCntrl)
        mid2AimGrp = pm.group (em=True, p=ribbonMidCntrl)
        mid1SpcSwithGrp = pm.group (em=True, p=ribbonMidCntrl)
        mid2SpcSwithGrp = pm.group (em=True, p=ribbonMidCntrl)

        pm.aimConstraint (limbJoint1, mid1AimGrp ,weight=1, aimVector=(-1, 0 ,0) , upVector=(0, 1, 0),worldUpVector=(0,1,0), worldUpType='objectrotation', worldUpObject=limbJoint1 )
        pm.aimConstraint (limbJoint3, mid2AimGrp ,weight=1, aimVector=(1, 0 ,0) , upVector=(0, 1, 0),worldUpVector=(0,1,0), worldUpType='objectrotation', worldUpObject=limbJoint1 )
        pm.parent (ribbonMid1TangCntrl.getParent(),mid1SpcSwithGrp)
        pm.parent (ribbonMid2TangCntrl.getParent(),mid2SpcSwithGrp)
        #node tree
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
        
        #twist extractors
        extra1 =  twistExtractor (limbJoint4)
        extra2 =  twistExtractor (limbJoint1, None)        
        pm.parent (extra1.extractorGrp,extra2.extractorGrp, limbMoveAll )        
        pm.pointConstraint (limbJoint1, extra2.extractorGrp, mo=True)        
        extra1.extractor.extractTwist >> ribbonStartCntrl.twist        
        extractMulti = pm.createNode('multDoubleLinear')
        extra2.extractor.extractTwist >> extractMulti.input1
        extractMulti.input2.set(-1)
        extractMulti.output >> ribbonEndCntrl.twist
        extra1.extractorGrp.visibility.set(0)
        extra2.extractorGrp.visibility.set(0)
        
class RibbonStandard:
    """
        Cria um ribbon standard
        Parametros: 
            name:
            guide1
            
            numJoints:
           
    """ 
    ##IMPLEMENTAR:
    #controle de twist fique liberado pra q o usuario de offset, principalmente no inicio
    #stretch/squash com distancia ja no ribbon
        
    def __init__( self, **kwargs ):
               
        self.guide1 = kwargs.pop('guide1','locator1') 
        self.guide2 = kwargs.pop('guide2','locator2')
        self.guide3 = kwargs.pop('guide3','locator3')
        self.name = kwargs.pop('name','ribbon')
        self.sections= kwargs.pop('sections',5)
        self.upVector=kwargs.pop('upVector',(0,1,0))
        self.direction=kwargs.pop('direction',(1,0,0))
        self.createCtrls = kwargs.pop('createCtrls',0)
        self.ctrlNormal= kwargs.pop('ctrlNormal',(1,0,0))
        self.topCtrl = kwargs.pop('topCtrl','top')
        self.midCtrl = kwargs.pop('midCtrl','mid')
        self.lwrCtrl = kwargs.pop('lwrCtrl','lwr')
        self.visibility = kwargs.pop('visibility',0)
        
    def doRig( self ):    
        p1 = pm.xform(self.guide1,q=1,t=1)
        p2 = pm.xform(self.guide2,q=1,t=1)
        p3 = pm.xform(self.guide3,q=1,t=1)
        
        A=om.MVector(p1)
        B=om.MVector(p2)
        C=om.MVector(p3)
        
        AC=A-C
        nurbsLength=AC.length()
        
        #setup do nurbs plane e follicles
        nurbs = pm.nurbsPlane(w=nurbsLength/self.sections, lr=self.sections, v=self.sections)[0]
        nurbsShp = nurbs.getShape()
        pm.rebuildSurface(nurbs,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kc=0,su=1,du=1,dv=3,tol=0.01,fr=0,dir=0)
        
        pm.xform (nurbs, t=p1, ws=True)
        
        guide2Up = pm.duplicate(guide2,n=guide2 + '_up')[0]
        pm.delete(pm.pointConstraint(guide1, guide3, guide2Up))
        pm.xform(guide2Up,r=True,t =(self.direction[0],self.direction[1],self.direction[2]))
        pm.delete(pm.aimConstraint(self.guide3,nurbs,w=1,o=(0,0,0),aim=(0,1,0),u=(-1,0,0),wut='object',wuo=guide2Up))
        pm.delete(guide2Up)
        pm.delete(pm.pointConstraint(self.guide1,self.guide3,nurbs))
        
        grpFol = pm.group(em=1)
        grpScale = pm.group(em=1)
        vValue = 0
        vSections = 1.0 / self.sections 
        vOffset = vSections / 2
        id = 0
        
        #medindo o comprimento do nurbs para o squash stretch 
        arcLengthShp = pm.createNode('arcLengthDimension')
        arcLength = arcLengthShp.getParent()
        nurbsShp.worldSpace[0] >> arcLengthShp.nurbsGeometry
        arcLengthShp.vParamValue.set(1)
        arcLengthShp.uParamValue.set(0)
        arcLenValue = arcLengthShp.arcLengthInV.get() 
        autoManualList = []
        factorList = []
        on_offList = []
        skinJntsList = []
        
        for follicle in range(self.sections):
            id += 1	
            #criando nodes para o stretch squash
            normalizeTo0 = pm.createNode('plusMinusAverage',n=self.name + 'RbbnNormalize0' + `id` + '_pma')
            scaleAux = pm.createNode('multiplyDivide',n=self.name + 'RbbnScaleAux0' + `id` + '_md')
            factor = pm.createNode('multiplyDivide',n=self.name + 'RbbnFactor0' + `id` + '_md')
            on_off = pm.createNode('multiplyDivide',n=self.name + 'RbbnOnOff0' + `id` + '_md')
            autoManual = pm.createNode('plusMinusAverage',n=self.name + 'RbbnAutoManual0' + `id` + '_pma')
            autoReverse = pm.createNode('reverse',n=self.name + 'RbbnReverse0' + `id` + '_rev')
            
            #ajustando valores dos nodes de stretch squash
            normalizeTo0.operation.set (2)
            scaleAux.input2.set ((arcLenValue,arcLenValue,arcLenValue))
            
            			
            #conectando os nodes de stretch squash
            arcLength.arcLengthInV >> normalizeTo0.input3D[0].input3Dx
            arcLength.arcLengthInV >> normalizeTo0.input3D[0].input3Dy
            arcLength.arcLengthInV >> normalizeTo0.input3D[0].input3Dz
            
            scaleAux.output >> normalizeTo0.input3D[1]
            grpScale.scale >> scaleAux.input1
            normalizeTo0.output3D >> factor.input2
            factor.output >> on_off.input1		
            on_off.output >> autoReverse.input
            autoReverse.output >> autoManual.input3D[0]
            
            #criando nodes do rbbn
            folShp = pm.createNode('follicle')
            print folShp
            fol = folShp.getParent ()
            
            #escondendo os follicles
            if self.visibility == 0:
            	folShp.visibility.set(0)
            
            jnt = pm.joint(radius=nurbsLength*0.2)
            skinJntsList.append(jnt)
            
            #conectando e ajustando nodes do rbbn
            autoManual.output3Dx >> jnt.scaleX
            autoManual.output3Dz >> jnt.scaleZ
            nurbsShp.local >> folShp.inputSurface
            nurbsShp.worldMatrix[0] >> folShp.inputWorldMatrix
            folShp.outRotate >> fol.rotate
            folShp.outTranslate >> fol.translate
            folShp.parameterU.set(0.5)
            vValue += vSections 
            folShp.parameterV.set(vValue - vOffset)
            pm.parent(fol,grpFol)
            
            pm.scaleConstraint(grpScale,fol,mo=1)
            			
            			#listas para loops posteriores
            on_offList.append(on_off)
            factorList.append(factor)
            autoManualList.append(autoManual)
        		
        		#fk setup
        FKSIZE = (nurbsLength/2) / self.sections
        
        topPosLoc = pm.spaceLocator()
        topAimLoc = pm.spaceLocator()
        topAimLoc.setParent(topPosLoc)
        
        topToSkin = pm.joint(radius=nurbsLength*0.2,p=(0,0,0),)
        pm.joint(radius=nurbsLength*0.15,p=(0,-FKSIZE,0),)		
        topUpLoc = pm.spaceLocator()
        topUpLoc.setParent(topPosLoc)
        
        pm.move(FKSIZE*3*self.upVector[0],FKSIZE*3*self.upVector[1],FKSIZE*3*self.upVector[2],topUpLoc)
        pm.delete(pm.pointConstraint(self.guide3,topPosLoc))
        #pm.delete(pm.parentConstraint(guide3,topPosLoc))
        
        midPosLoc = pm.spaceLocator()
        midAimLoc = pm.spaceLocator()
        midAimLoc.setParent(midPosLoc)
        
        midOffLoc = pm.spaceLocator()
        midOffLoc.setParent(midAimLoc)
        
        midToSkin = pm.joint(radius=nurbsLength*0.2,p=(0,0,0))
        midUpLoc = pm.spaceLocator()
        midUpLoc.setParent(midPosLoc)
        
        pm.move(FKSIZE*3*self.upVector[0],FKSIZE*3*self.upVector[1],FKSIZE*3*self.upVector[2],midUpLoc)
        
        lwrPosLoc = pm.spaceLocator()
        lwrAimLoc = pm.spaceLocator()
        lwrAimLoc.setParent(lwrPosLoc)
        
        lwrToSkin = pm.joint(radius=nurbsLength*0.2,p=(0,0,0))
        pm.joint(radius=nurbsLength*0.15,p=(0,FKSIZE,0))
        
        lwrUpLoc =pm.spaceLocator() 
        lwrUpLoc.setParent(lwrPosLoc)
        
        pm.move(FKSIZE*3*self.upVector[0],FKSIZE*3*self.upVector[1],FKSIZE*3*self.upVector[2],lwrUpLoc)
        pm.delete(pm.pointConstraint(self.guide1,lwrPosLoc))
        
        topPosLocShp = topPosLoc.getShape()
        midPosLocShp = midPosLoc.getShape()
        lwrPosLocShp = lwrPosLoc.getShape()
        topAimLocShp = topAimLoc.getShape()
        midAimLocShp = midAimLoc.getShape()
        lwrAimLocShp = lwrAimLoc.getShape()
        topUpLocShp = topUpLoc.getShape()
        midUpLocShp = midUpLoc.getShape()
        lwrUpLocShp = lwrUpLoc.getShape()
        midOffLocShp = midOffLoc.getShape()
        	
        topPosLocShp.localScale.set((nurbsLength*0.2, nurbsLength*0.2, nurbsLength*0.2))
        topAimLocShp.localScale.set((nurbsLength*0.2, nurbsLength*0.2, nurbsLength*0.2))
        topUpLocShp.localScale.set((nurbsLength*0.05, nurbsLength*0.05, nurbsLength*0.05))
        midPosLocShp.localScale.set((nurbsLength*0.2, nurbsLength*0.2, nurbsLength*0.2))
        midAimLocShp.localScale.set((nurbsLength*0.2, nurbsLength*0.2, nurbsLength*0.2))
        midUpLocShp.localScale.set((nurbsLength*0.05, nurbsLength*0.05, nurbsLength*0.05))
        midOffLocShp.localScale.set((nurbsLength*0.2, nurbsLength*0.2, nurbsLength*0.2))
        lwrPosLocShp.localScale.set((nurbsLength*0.2, nurbsLength*0.2, nurbsLength*0.2))
        lwrAimLocShp.localScale.set((nurbsLength*0.2, nurbsLength*0.2, nurbsLength*0.2))
        lwrUpLocShp.localScale.set((nurbsLength*0.05, nurbsLength*0.05, nurbsLength*0.05))
        
        pm.parent(topPosLoc,midPosLoc,lwrPosLoc,grpScale)
        		
        #criando constraints para os locators do rbbn
        pm.aimConstraint(midToSkin,topAimLoc,aim=(0,-1,0),u=(1,0,0),wut='object',wuo=topUpLoc)
        pm.aimConstraint(midToSkin,lwrAimLoc,aim=(0,1,0),u=(1,0,0),wut='object',wuo=lwrUpLoc) 
        pm.aimConstraint(topPosLoc,midAimLoc,aim=(0,1,0),u=(1,0,0),wut='object',wuo=midUpLoc)
        
        pm.pointConstraint(topPosLoc,lwrPosLoc,midPosLoc)
        pm.pointConstraint(topUpLoc,lwrUpLoc,midUpLoc)
        		
        #skin setup
        #print nurbs, topToSkin, midToSkin, lwrToSkin 
        skin = pm.skinCluster(topToSkin,midToSkin,lwrToSkin,nurbs,tsb=1)
        print skin
        if self.sections == 3:
        	pm.skinPercent(skin,nurbs + '.cv[0:1][5]',tv=(topToSkin,1))
        	pm.skinPercent(skin,nurbs + '.cv[0:1][4]',tv=[(topToSkin,0.6),(midToSkin,0.4)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][3]',tv=[(topToSkin,0.2),(midToSkin,0.8)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][2]',tv=[(topToSkin,0.2),(midToSkin,0.8)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][1]',tv=[(topToSkin,0.6),(midToSkin,0.4)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][0]',tv=(topToSkin,1))
        	
        elif self.sections == 5:
        	pm.skinPercent(skin,nurbs + '.cv[0:1][7]',tv=(topToSkin,1))
        	pm.skinPercent(skin,nurbs + '.cv[0:1][6]',tv=[(topToSkin,0.80),(midToSkin,0.2)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][5]',tv=[(topToSkin,0.5),(midToSkin,0.5)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][4]',tv=[(topToSkin,0.25),(midToSkin,0.75)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][3]',tv=[(lwrToSkin,0.25),(midToSkin,0.75)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][2]',tv=[(lwrToSkin,0.5),(midToSkin,0.5)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][1]',tv=[(lwrToSkin,0.8),(midToSkin,0.2)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][0]',tv=(lwrToSkin,1))
        	
        elif self.sections == 7:
        	pm.skinPercent(skin,nurbs + '.cv[0:1][9]',tv=(topToSkin,1))
        	pm.skinPercent(skin,nurbs + '.cv[0:1][8]',tv=[(topToSkin,0.85),(midToSkin,0.15)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][7]',tv=[(topToSkin,0.6),(midToSkin,0.4)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][6]',tv=[(topToSkin,0.35),(midToSkin,0.65)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][5]',tv=[(topToSkin,0.25),(midToSkin,0.75)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][4]',tv=[(lwrToSkin,0.25),(midToSkin,0.75)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][3]',tv=[(lwrToSkin,0.35),(midToSkin,0.65)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][2]',tv=[(lwrToSkin,0.6),(midToSkin,0.4)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][1]',tv=[(lwrToSkin,0.85),(midToSkin,0.15)])
        	pm.skinPercent(skin,nurbs + '.cv[0:1][0]',tv=(lwrToSkin,1))
        else:
        	print "!!!There's skinning support for 3,5 and 7 sections only!!!"
        		
        						
        #posicionando o controle do meio
        pm.delete(pm.pointConstraint(self.guide2,midOffLoc))
        
        #criando controles
        if self.createCtrls == 0:
        	topCircle = pm.circle(r=nurbsLength*.2,nr=(self.ctrlNormal[0],self.ctrlNormal[1],self.ctrlNormal[2]))
        	topCtrlGrp = pm.group()
        	topCtrlGrp.setParent(grpScale)
        	pm.delete(pm.parentConstraint(self.guide3,topCtrlGrp,mo=0))
        	pm.parentConstraint(topCircle[0],topPosLoc)
        	
        	midCircle = pm.circle(r=nurbsLength*.2, nr=(self.ctrlNormal[0],self.ctrlNormal[1],self.ctrlNormal[2]))
        	midCtrlGrp = pm.group()
        	midCtrlGrp.setParent(midOffLoc)
        	pm.delete(pm.parentConstraint(midToSkin,midCtrlGrp))
        	midJointZerado = self.zeroOut(midToSkin, returnGrpName=1)[0]
        	pm.parent(midJointZerado,grpScale)
        	pm.parentConstraint(midCircle[0],midJointZerado,mo=1)
        	
        	lwrCircle = pm.circle(r=nurbsLength*.2,nr=(self.ctrlNormal[0],self.ctrlNormal[1],self.ctrlNormal[2]))
        	lwrCtrlGrp = pm.parent(pm.group(),grpScale)
        	pm.delete(pm.parentConstraint(self.guide1,lwrCtrlGrp,mo=0))
        	pm.parentConstraint(lwrCircle[0],lwrPosLoc)
        else:
        	midCircle = pm.circle(r=nurbsLength*.2, nr=(self.ctrlNormal[0],self.ctrlNormal[1],self.ctrlNormal[2]))
        	midCtrlGrp = pm.parent(pm.group(),midOffLoc)
        	pm.delete(pm.parentConstraint(midToSkin,midCtrlGrp))
        	midJointZerado = self.zeroOut(midToSkin, returnGrpName=1)[0]
        	pm.parent(midJointZerado,grpScale)
        	pm.parentConstraint(midCircle[0],midJointZerado, mo=1)
        		
        id = 0
        
        midCircle[0].addAttr('autoSS',k=1,dv=0.0,at='double', min=0, max=1)
        midCircleShp = midCircle[0].getShape()
        
        if self.createCtrls:
        	midCircleShp.v.set(0)
        
        for autoManualAuxNodes in autoManualList:
        	id += 1	
        	#criando e ajustando nodes para stretch squash
        	manualNormalize = pm.createNode('plusMinusAverage',n= self.name + 'RbbnManualNormalize0' + str(id) + '_pma')
        	manualFactor = pm.createNode('multiplyDivide',n=self.name + 'RbbnManualFactor0' + str(id) + '_md')
        	ratioScale = pm.createNode('multiplyDivide',n=self.name + 'RbbnRatioScale0' + str(id) + 'md')
        	zRatio = pm.createNode('multiplyDivide',n=self.name + 'RbbnSsManualZratio' + str(id) + '_md')
        	
        	manualFactor.output >> autoManualAuxNodes.input3D[1]
        	midCircle[0].scale >> manualNormalize.input3D[0]
        	manualNormalize.output3D >> manualFactor.input2
        	
        	manualNormalize.operation.set(2)
        	manualNormalize.input3D[1].input3D.set((1,1,1))
        	ratioScale.operation.set(2)
        	
        	#adicionando atributos de squash
        	midCircleShp.addAttr('manualFactorX0' + str(id),k=1,at = 'float', dv=1)
        	midCircleShp.addAttr('manualRatioZ0' + str(id),k=1,at = 'float')
        	midCircleShp.addAttr('autoFactorX0' + str(id),k=1,at = 'float')
        	midCircleShp.addAttr('autoRatioZ0' + str(id),k=1,at = 'float')
        	
        	#conectando os atributos acima
        	midCircleShp.attr ('manualRatioZ0'+str(id))>> zRatio.input1Z
        	midCircleShp.attr ('autoRatioZ0' + str(id))>> zRatio.input1X
        	
        	midCircle[0].autoSS >> on_offList[id-1].input2X #on_off
        	midCircle[0].autoSS >> on_offList[id-1].input2Z #on_off
        	midCircleShp.attr ('manualFactorX0' + str(id))>> manualFactor.input1X
        	midCircleShp.attr ('manualFactorX0' + str(id))>> zRatio.input2Z
        	ratioScale.outputX >> zRatio.input2X
        	zRatio.outputZ >> manualFactor.input1Z
        	ratioScale.outputX >> factorList[id-1].input1X #factor
        	zRatio.outputX >> factorList[id-1].input1Z #factor
        	grpScale.scale >> ratioScale.input2
        	midCircleShp.attr('autoFactorX0' + str(id)) >> ratioScale.input1X
        	
        	#ajustando os atributos
        	midCircleShp.attr('manualRatioZ0' + str(id)).set(1)
        	midCircleShp.attr('autoRatioZ0' + str(id)).set(1)
        		
        	#ajustando valores iniciais para os factores de squash
        
        if self.sections == 3:
        	midCircleShp.autoFactorX02.set(0.08)
        elif self.sections == 5:
        	midCircleShp.autoFactorX01.set(0.02)
        	midCircleShp.autoFactorX02.set(0.25)
        	midCircleShp.autoFactorX03.set(0.22)
        	midCircleShp.autoFactorX04.set(0.25)
        	midCircleShp.autoFactorX05.set(0.02)
        elif self.sections == 7:
        	midCircleShp.autoFactorX01.set(0)
        	midCircleShp.autoFactorX02.set(0.11)
        	midCircleShp.autoFactorX03.set(0.1)
        	midCircleShp.autoFactorX04.set(0.16)
        	midCircleShp.autoFactorX05.set(0.1)
        	midCircleShp.autoFactorX06.set(0.11)
        	midCircleShp.autoFactorX07.set(0)
        			
        	#toggles displays
        if self.visibility == 0:	
        	pm.toggle(nurbs,g=1,te=1)
        	pm.toggle(arcLength,te=1)
        	arcLength.visibility.set(0)	
        	topPosLoc.visibility.set(0)
        	midPosLocShp = midPosLoc.getShape()
        	midPosLocShp.visibility.set(0)
        	midAimLocShp = midAimLoc.getShape()
        	midAimLocShp.visibility.set(0)
        	midOffLocShp = midOffLoc.getShape()
        	midOffLocShp.visibility.set(0)
        	lwrPosLoc.visibility.set(0)	
        	midUpLoc.visibility.set(0)
        	grpScale.visibility.set(0)
        	grpFol.visibility.set(0)
        	
        #agrupando tudo
        finalRbbnGrp = pm.group(em=1)
        pm.parent(nurbs,grpFol,grpScale,arcLength,finalRbbnGrp)
        
    def zeroOut(self, objeto=None, supressScale=0, returnGrpName=0):
	"""ZeroOut Static Function
	-agrupa o objeto em questão e passa seus valores para o grupo
	-Inputs: (string) nome do node a levar zeroOut
		 (boolean=0) nao mexer na escala durante o processo
		 (boolean=0) retorna o nome do grupo criado?
	"""
	#se nao for passado um nome, usar selecao atual
	if objeto == None:
		objetos = pm.ls(sl=1)
	else:
		objetos = [objeto]
	
	returnList = []
	#loop para multiplas selecoes
	for objeto in objetos:
		grp = pm.group(n=objeto+"_grp", em=1)
		pm.delete(pm.parentConstraint(objeto, grp))
		#vai que da algum problema...
		if not supressScale:
			pm.delete(pm.scaleConstraint(objeto, grp))
		
		pm.parent(objeto, grp)
		if returnGrpName:
			returnList.append(grp)
	
	if returnGrpName:
		return returnList