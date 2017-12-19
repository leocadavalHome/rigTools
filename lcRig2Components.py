class CntrlCrv:
    """
        Cria uma curva de controle e conecta em um objeto 
        **IMPORTANTE Para acessar os objetos do shape de controle e do seu grupo devem ser utilzados os parametros da classe .cntrl e .cntrlGrp
        **A classe em si nao eh um transform
        
        Parametros: 
            name (string): nome do novo controle
            obj(objeto) : objeto que será controlado 
            connType(string): tipo de conexao (parent,parentConstraint,orientConstraint)
            icone (string): tipo do icone (cubo,bola,circuloX,circuloY,circuloZ)
            size (float): escala do controle
            color (R,G,B): cor
            rotateOrder (int): ordem de rotacao default zxy
    """  
    
    def __init__ (self,obj=None, connType=None, **kwargs):                

        #seta variaveis com os inputs
        self.name = kwargs.pop('name','cntrl')            
        self.cntrlledObj = obj
        self.icone = kwargs.pop('icone','cubo')
        self.connType = connType
        self.cntrlSize = kwargs.pop('size', 1 )
        self.color = kwargs.pop('color', None)
        self.rotateOrder = kwargs.pop('rotateOrder', 0) #default xyz
                                                
        self.cntrl= None
        self.cntrlGrp= None
        self.cnstr = None
        
    #constroi icone                            
        if self.icone== "cubo":
            crv = pm.curve (n=self.name+"_cntrl", d=1,p=[(-0.5,0.5,0.5), (-0.5,0.5,-0.5), (0.5,0.5,-0.5),(0.5,0.5,0.5),(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),(-0.5,0.5,0.5),(-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(-0.5,0.5,-0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(0.5,-0.5,0.5)],k=[0,1,2,3,4 ,5,6,7,8,9,10,11,12,13,14,15,16])
            crv.scaleX.set (self.cntrlSize)
            crv.scaleY.set (self.cntrlSize)
            crv.scaleZ.set (self.cntrlSize)
            pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False )
        elif self.icone=='bola':
            crv = pm.circle (n=self.name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv1 = pm.circle (c=(0,0,0),nr=(1,0,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv2 = pm.circle (c=(0,0,0),nr=(0,0,1),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            pm.parent ([crv1.getShape(),crv2.getShape()], crv, shape=True, r=True)
            pm.delete (crv1, crv2)
            crv.scaleX.set (self.cntrlSize)
            crv.scaleY.set (self.cntrlSize)
            crv.scaleZ.set (self.cntrlSize)
            pm.makeIdentity (crv,apply=True,t=1,r=1,s=1,n=0)
        elif self.icone=='circuloY':
            crv = pm.circle (n=self.name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv.scaleX.set (self.cntrlSize)
            crv.scaleY.set (self.cntrlSize)
            crv.scaleZ.set (self.cntrlSize)
            pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False )         
        elif self.icone=='circuloX':
            crv = pm.circle (n=self.name+"_cntrl" , c=(0,0,0),nr=(1,0,0),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv.scaleX.set (self.cntrlSize)
            crv.scaleY.set (self.cntrlSize)
            crv.scaleZ.set (self.cntrlSize)
            pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False ) 
        elif self.icone=='circuloZ':
            crv = pm.circle (n=self.name+"_cntrl" , c=(0,0,0),nr=(0,0,1),sw=360,r=0.5,d=3,ut=0,ch=0)[0]
            crv.scaleX.set (self.cntrlSize)
            crv.scaleY.set (self.cntrlSize)
            crv.scaleZ.set (self.cntrlSize)
            pm.makeIdentity( crv, a = True, t = True, r = True, s = True, n=False ) 
            
    #seta ordem de rotacao        
        crv.rotateOrder.set(self.rotateOrder)
        grp = pm.group (crv, n=self.name+"_grp")
        crv.rotateOrder.set(self.rotateOrder)
        pm.xform (grp, os=True, piv=[0,0,0])
        
    #cor
        if self.color:
            shList = crv.getShapes()
            for sh in shList:
                sh.overrideEnabled.set (1)
                sh.overrideRGBColors.set(1)
                sh.overrideColorRGB.set (self.color) 
        
    #faz a conexao
        if self.cntrlledObj:
            matrix =pm.xform (self.cntrlledObj, q=True,  ws=True ,m=True) 
        
            pm.xform (grp, ws=True,  m=matrix)
            
            if self.connType=='parent':
                self.cntrlledObj.setParent (crv)
            elif self.connType=='parentConstraint':
                self.cnstr = pm.parentConstraint (crv, self.cntrlledObj, mo=True)
            elif self.connType=='orientConstraint':
                self.cnstr = pm.orientConstraint (crv, self.cntrlledObj, mo=True)                  
        self.cntrl= crv
        self.cntrlGrp = grp
        
        
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
        
        self.ribbonDict['cntrlSetup']={'name':'cntrl','icone':'circuloX','size':0.6,'color':(0,0,1)}       
        self.ribbonDict['cntrlTangSetup']={'name':'cntrl','icone':'bola','size':0.3,'color':(0,1,1)}        
        self.ribbonDict['cntrlExtraSetup']={'name':'cntrlExtra','icone':'circuloX','size':0.2}        

           
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
                kwargs= self.ribbonDict['cntrlSetup']                               
                kwargs['name'] = kwargs['name']+str(i)           
                cntrl = CntrlCrv (anchor[1],**kwargs)
            else:
                kwargs= self.ribbonDict['cntrlTangSetup']                               
                kwargs['name'] = kwargs['name']+str(i) 
                cntrl = CntrlCrv (anchor[1],**kwargs)
                        
            #Nao pode fazer conexao na criacao do controle, pois tera conexao direta
            pm.xform (cntrl.cntrlGrp, t=pos, ws=True)
            
            #estrutura de buffers para conexao direta
            auxLocGrp = pm.group (em=True)
            auxLoc = pm.group (em=True, p=auxLocGrp) 
            pm.xform (auxLocGrp, t=pos, ws=True)
            loc = pm.PyNode (auxLoc)
            
            if i==1 or i==4:
                pm.xform (anchorGrp, s=(-1,1,1), r=True)
                pm.xform (cntrl.cntrlGrp, s=(-1,1,1), r=True)
                pm.xform (loc.getParent(), s=(-1,1,1), r=True)
            
            #Conexoes dos buffers cm os clusters e com os controles
            pm.parentConstraint (cntrl.cntrl, loc )                    
            loc.translate >> anchorDrn.translate
            loc.rotate >> anchorDrn.rotate
            cntrlList.append(cntrl)
            locList.append (loc)
        
        cntrlsSpace.addAttr ('cntrlsVis', at='double', dv=1, k=False, h=True)
        cntrlsSpace.addAttr ('extraCntrlsVis', at='double', dv=0, k=False, h=True)            
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
        
        #hierarquia                
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
            
            kwargs= self.ribbonDict['cntrlExtraSetup']                               
            kwargs['name'] = kwargs['name']+'A'+str(i) 
            cntrl1 = CntrlCrv (jnt1,'parentConstraint',**kwargs)         
            #node tree
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
            #expressao que le a rampa para setar valores da escala de cada joint quando fizer squash/stretch        
            expre1=expre1+"$color = `colorAtPoint -o RGB -u "+str ((i/(self.numJnts/2.0))-(1.0/self.numJnts))+" -v 0.5 "+ramp1.name()+" `;$output["+str (i)+"] = $color[0];"+blend1A.name()+".attributesBlender=$output["+str (i)+"];"            
            
            #cria estrutura pra superficie 2       
            pm.select (cl=True)
            jnt2 = pm.joint (p=(0,0,0))
            kwargs= self.ribbonDict['cntrlExtraSetup']                               
            kwargs['name'] = kwargs['name']+'B'+str(i)             
            cntrl2 = CntrlCrv (jnt2, 'parentConstraint',**kwargs)            
            #node tree    
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
            #expressao que le a rampa para setar valores da escala de cada joint quando fizer squash/stretch           
            expre2=expre2+"$color = `colorAtPoint -o RGB -u "+str ((i/(self.numJnts/2.0))-(1.0/self.numJnts))+" -v 0.5 "+ramp2.name()+" `;$output["+str (i)+"] = $color[0];"+blend2A.name()+".attributesBlender=$output["+str (i)+"];"           
            
            #prende joints nas supeficies com follicules
            foll1= self.attachObj (cntrl1.cntrlGrp, bendSurf1[0], (i/(self.numJnts/2.0))-(1.0/self.numJnts), 0.5, 4)
            foll2= self.attachObj (cntrl2.cntrlGrp, bendSurf2[0], (i/(self.numJnts/2.0))-(1.0/self.numJnts), 0.5, 4)
            
            pm.parent (cntrl1.cntrlGrp, cntrl2.cntrlGrp,extraCntrlsGrp)
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
        cntrlsSpace.cntrlsVis >> cntrlList[0].cntrlGrp.visibility
        cntrlsSpace.cntrlsVis >> cntrlList[3].cntrlGrp.visibility
        cntrlsSpace.cntrlsVis >> cntrlList[6].cntrlGrp.visibility
              
        #povoa ribbon Dict        
        self.ribbonDict['name']= 'bezierRibbon'
        self.ribbonDict['ribbonMoveAll']=cntrlsSpace
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

        pm.parent (ribbonEndCntrl.cntrlGrp, endGrp)
        pm.parent (ribbonMidCntrl.cntrlGrp, midGrp)
        pm.parent (ribbonStartCntrl.cntrlGrp, startGrp)
        pm.parent (startGrp,midGrp,endGrp,ribbonMoveAll)

        ##lembrar de implementar outras possibilidade de eixos. Hardcode de X
        ribbonEndCntrl.cntrlGrp.translate.set(0,0,0)
        ribbonEndCntrl.cntrlGrp.rotate.set(0,rotY,0)
        ribbonMidCntrl.cntrlGrp.translate.set(0,0,0)
        ribbonMidCntrl.cntrlGrp.rotate.set(0,rotY,0)
        ribbonStartCntrl.cntrlGrp.translate.set(0,0,0)
        ribbonStartCntrl.cntrlGrp.rotate.set(0,rotY,0)

        #sistema de controle das tangentes suaves ou duras
        mid1AimGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
        mid2AimGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
        mid1SpcSwithGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)
        mid2SpcSwithGrp = pm.group (em=True, p=ribbonMidCntrl.cntrl)

        pm.aimConstraint (limbJoint1, mid1AimGrp ,weight=1, aimVector=(-1, 0 ,0) , upVector=(0, 1, 0),worldUpVector=(0,1,0), worldUpType='objectrotation', worldUpObject=limbJoint1 )
        pm.aimConstraint (limbJoint3, mid2AimGrp ,weight=1, aimVector=(1, 0 ,0) , upVector=(0, 1, 0),worldUpVector=(0,1,0), worldUpType='objectrotation', worldUpObject=limbJoint1 )
        pm.parent (ribbonMid1TangCntrl.cntrlGrp,mid1SpcSwithGrp)
        pm.parent (ribbonMid2TangCntrl.cntrlGrp,mid2SpcSwithGrp)
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
        extra1.extractor.extractTwist >> ribbonStartCntrl.cntrl.twist        
        extractMulti = pm.createNode('multDoubleLinear')
        extra2.extractor.extractTwist >> extractMulti.input1
        extractMulti.input2.set(-1)
        extractMulti.output >> ribbonEndCntrl.cntrl.twist
        extra1.extractorGrp.visibility.set(0)
        extra2.extractorGrp.visibility.set(0)
        
