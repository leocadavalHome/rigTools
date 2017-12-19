import pymel.core as pm
import maya.api.OpenMaya as om
import lcRigToolbox as tbox
import lcGeneric as gen

class Limb():
    """
        Cria um Limb
        Parametros: 
            name (string): nome do novo limb            
            ikCntrl (string): nome
            startCntrl (string): nome
            midCntrl (string): nome
            endCntrl (string): nome
            poleCntrl (string): nome
            flipAxis (boolean): se o eixo eh flipado ao longo do bone
            handJoint (boolean): se exite joint da mao
            axis (string:'X','Y' ou 'Z'): eixo ao longo do bone
                 
    """  
    ## IMPLEMENTAR:
    #  setagem de parametros e formatacao de nomes 
    #  grupos de spaceSwitch acima dos controles
 
    #self.twoJoints=False RETIREI CODIGO DE ARTICULACAO DE DOIS JOINTS. PRECISA FAZER IMPLEMENTACAO COMPLETA 
                 
    def __init__ (self, **kwargs):

        self.limbDict={'name':'limb',
                       'ikCntrl':None,
                       'startCntrl':None,
                       'midCntrl':None,
                       'endCntrl':None,
                       'poleCntrl':None,
                       'flipAxis':False,
                       'handJoint':True,
                       'axis':'X',
                       'moveAll1Cntrl':None} #valores default

        self.limbDict.update(kwargs) # atualiza com o q foi entrado

        self.name = self.limbDict['name']
        self.flipAxis = self.limbDict['flipAxis']
        self.axis = self.limbDict['axis']
        self.handJoint = self.limbDict['handJoint']
                    
        ##setups visuais dos controles
        self.limbDict['moveAll1CntrlSetup']={'name':self.name+'moveAll1', 'icone':'circulo'+self.axis,'size':1.5,'color':(1,1,0) }    
        self.limbDict['ikCntrlSetup'] = {'name':self.name+'Ik', 'icone':'cubo','size':0.75,'color':(1,0,0) }    
        self.limbDict['startCntrlSetup'] = {'name':self.name+'Start', 'icone':'cubo','size':0.5,'color':(0,1,0) }
        self.limbDict['midCntrlSetup'] = {'name':self.name+'Mid', 'icone':'cubo', 'size':0.5, 'color':(0,1,0)}
        self.limbDict['endCntrlSetup'] = {'name':self.name+'End', 'icone':'cubo', 'size':0.5, 'color':(0,1,0)}
        self.limbDict['poleVecCntrlSetup'] = {'name':self.name+'PoleVec', 'icone':'bola', 'size':0.4, 'color':(1,0,0)}
        self.limbDict['nodeTree'] = {}
        self.limbDict['nameConventions'] = None
        ##e implementar no codigo padroes de nome 
        
    def doRig(self):
            
        #apagar todos os node ao reconstruir                      
        if pm.objExists(self.name+'MoveAll'):
            pm.delete (self.name+'MoveAll')
            
        #Cria o grupo moveAll
        limbMoveAll = pm.group(empty=True, n=self.name+'MoveAll')
        limbMoveAll.addAttr('ikfk', at='float',min=0, max=1,dv=1, k=1)

        ## cria guia se não existir  
        locPos = [(0,0,0), (3,0,-1), (6,0,0), (7,0,0)]
        
        if self.handJoint:
            n=5
        else:
            n=4
            
        for i in range (1,n):
            if not pm.objExists (self.name+'Guide'+str(i)):
                loc = pm.spaceLocator (n=self.name+'Guide'+str(i), p=(0,0,0))
                pm.xform (loc, t=locPos[i-1], ws=True)
            else:
                locPos[i-1]= pm.xform (self.name+'Guide'+str(i), q=True, t=True, ws=True)
        
        #define pontos do guide como vetores usando api para faciitar os calculos
        p1 = locPos[0]
        p2 = locPos[1]
        p3 = locPos[2]
        
        A= om.MVector(p1)
        B= om.MVector(p2)
        C= om.MVector(p3)
        
        if self.handJoint:
            p4=locPos[3]
            D=om.MVector(p4)
        
        #Calculando a normal do plano definido pelo guide
        #invertendo inverte a direcao do eixo ao longo do vetor        
        if self.flipAxis:
            AB = A-B
            BC = B-C
            CD = C-D
        else:
            AB = B-A
            BC = C-B
            CD = D-C
            
        n = BC^AB
        nNormal = n.normal()
                
        #cria joint1
        #criando a matriz do joint conforme a orientacao setada
        x = nNormal ^ AB.normal()
        t = x.normal() ^ nNormal        
        if self.axis=='Y':
            list = [ nNormal.x, nNormal.y, nNormal.z, 0, t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, A.x, A.y,A.z,1]
        elif self.axis=='Z':
            list = [ x.x, x.y, x.z, 0,nNormal.x, nNormal.y, nNormal.z, 0,t.x, t.y, t.z, 0, A.x, A.y,A.z,1]
        else:
            list = [ t.x, t.y, t.z, 0,nNormal.x, nNormal.y, nNormal.z, 0, x.x*-1, x.y*-1, x.z*-1, 0, A.x, A.y,A.z,1]
                 
        m= om.MMatrix (list)
        pm.select(cl=True)
        j1 = pm.joint()
        pm.xform (j1, m = m, ws=True) 
        pm.makeIdentity (j1, apply=True, r=1, t=0, s=0, n=0, pn=0)
        
        #cria joint2
        #criando a matriz do joint conforme a orientacao setada
        x = nNormal ^ BC.normal()
        t = x.normal() ^ nNormal
        if self.axis=='Y':
            list = [ nNormal.x, nNormal.y, nNormal.z,0,t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, B.x, B.y, B.z,1]
        elif self.axis =='Z':
            list = [ x.x, x.y, x.z, 0,nNormal.x, nNormal.y, nNormal.z, 0,t.x, t.y, t.z, 0, B.x, B.y, B.z,1]
        else:   
            list = [ t.x, t.y, t.z, 0, nNormal.x, nNormal.y, nNormal.z, 0 , x.x*-1, x.y*-1, x.z*-1, 0, B.x, B.y, B.z,1]  
               
        m= om.MMatrix (list)
        pm.select(cl=True)
        j2= pm.joint()
        pm.xform (j2, m = m, ws=True) 
        pm.makeIdentity (j2, apply=True, r=1, t=0, s=0, n=0, pn=0)
        
        #cria joint3
        #aqui so translada o joint, usa a mesma orientacao
        pm.select(cl=True)
        j3=pm.joint()
        pm.xform (j3, m = m, ws=True) 
        pm.xform (j3, t= C, ws=True)
        pm.makeIdentity (j3, apply=True, r=1, t=0, s=0, n=0, pn=0)
        
        #hierarquia
        pm.parent (j2, j1)
        pm.parent (j3, j2)
        j1.setParent (limbMoveAll)
        
        ##joint4(hand) se estiver setado nas opcoes      
        if self.handJoint:
            #joint4
            #criando a matriz do joint conforme a orientacao setada            
            if self.flipAxis:
                if nNormal.y < 0:
                    nNormal=om.MVector((0,-1,0))
                else:
                    nNormal=om.MVector((0,1,0))
                        
            x = nNormal ^ CD.normal()
            t = x.normal() ^ nNormal
            if self.axis=='Y':
                list = [ nNormal.x, nNormal.y, nNormal.z, 0, t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, C.x, C.y,C.z,1]
            elif self.axis=='Z':
                list = [ x.x, x.y, x.z, 0,nNormal.x, nNormal.y, nNormal.z, 0,t.x, t.y, t.z, 0, C.x, C.y,C.z,1]
            else:
                list = [ t.x, t.y, t.z, 0,nNormal.x, nNormal.y, nNormal.z, 0, x.x*-1, x.y*-1, x.z*-1, 0, C.x, C.y,C.z,1]
          
            m= om.MMatrix (list)
            pm.select(cl=True)
            j4= pm.joint()
            pm.xform (j4, m = m, ws=True) 
            pm.makeIdentity (j4, apply=True, r=1, t=0, s=0, n=0, pn=0) 
            
            #cria joint5 e so move
            pm.select(cl=True)
            j5=pm.joint()
            pm.xform (j5, m = m, ws=True) 
            pm.xform (j5, t=D, ws=True)
            pm.makeIdentity (j5, apply=True, r=1, t=0, s=0, n=0, pn=0)        
            
            #hierarquia        
            pm.parent (j4, j3)
            pm.parent (j5, j4)            
                
        ##Estrutura FK
        if self.axis=='Y'  or self.axis=='Z' or self.axis=='X':
            axisName=self.axis
        else:
            axisName='X'
        
        kwargs=self.limbDict['moveAll1CntrlSetup']
        moveAll1Cntrl = CntrlCrv(j1, **kwargs)
        
        kwargs=self.limbDict['endCntrlSetup']            
        endCntrl = CntrlCrv (j1,'parentConstraint', **kwargs )
        endCntrl.cntrl.addAttr('manualStretch', at='float',min=.1,dv=1, k=1)
        
        kwargs=self.limbDict['midCntrlSetup'] 
        midCntrl = CntrlCrv (j2,'orientConstraint',**kwargs)
        midCntrl.cntrl.addAttr('manualStretch', at='float',min=.1,dv=1, k=1)
        
        pm.pointConstraint (j2, midCntrl.cntrlGrp, mo=True)
        
        ##Estrutura IK
        ikH = pm.ikHandle (sj=j1, ee=j3, sol="ikRPsolver")
        kwargs=self.limbDict['ikCntrlSetup']
        ikCntrl = CntrlCrv(ikH[0],'parent',**kwargs)
        
        ikCntrl.cntrl.addAttr ('pin', at='float',min=0, max=1,dv=0, k=1)
        ikCntrl.cntrl.addAttr ('bias', at='float',min=-0.9, max=0.9, k=1)
        ikCntrl.cntrl.addAttr ('autoStretch', at='float',min=0, max=1,dv=1, k=1)
        ikCntrl.cntrl.addAttr ('manualStretch', at='float',dv=1, k=1)
        ikCntrl.cntrl.addAttr ('twist', at='float',dv=0, k=1)        
            
        #pole vector
        kwargs=self.limbDict['poleVecCntrlSetup']
        poleVec = CntrlCrv(j2,**kwargs)
        
        #calcula a direcao q deve ficar o polevector
        BA=B-A
        CA=C-A
        U=BA*CA.normal()
        dist=CA.length()
        V=U/dist*dist
        T=A+V*CA.normal()
        D=B-T
        Pole=(D.normal()*1.2)+B
        
        #test=pm.spaceLocator (p=(0,0,0)) # locator de teste de onde calculou o ponto mais proximo
        #pm.xform (test, t=T)
        
        pm.xform (poleVec.cntrlGrp , t=Pole) 
        pm.xform (poleVec.cntrlGrp , ro=(0,0,0)) 
        pm.poleVectorConstraint (poleVec.cntrl, ikH[0])
        pm.parent (midCntrl.cntrlGrp, endCntrl.cntrl)
        pm.parent (endCntrl.cntrlGrp, moveAll1Cntrl.cntrl)
        pm.parent (moveAll1Cntrl.cntrlGrp, poleVec.cntrlGrp, ikCntrl.cntrlGrp, limbMoveAll)

        #handCntrls se houver
        if self.handJoint:
            kwargs=self.limbDict['startCntrlSetup']
            startCntrl = CntrlCrv (j4,**kwargs)
            buf=pm.group (em=True)
            matrix=pm.xform (j4, q=True, ws=True, m=True)
            pm.xform (buf, m=matrix, ws=True)
            pm.parent (buf,ikCntrl.cntrl)
            handCnst = pm.orientConstraint (buf,startCntrl.cntrl, j4, mo=False)
            pm.pointConstraint (j3,startCntrl.cntrlGrp, mo=True)
            pm.parent (startCntrl.cntrlGrp, midCntrl.cntrl)
        
        #display
        ikH[0].visibility.set(0)
               
        #grupos de stretch
        startGrp = pm.group (empty=True)
        endGrp=pm.group (empty=True)
        pm.parent (endGrp,ikCntrl.cntrl,r=True)
        pm.xform (startGrp , t=p1, ws=True)
        pm.parent (startGrp,endCntrl.cntrl)
        
        ##NODE TREE#######               
        #Pin
        p5 = pm.xform (poleVec.cntrlGrp, q=True, t=True, ws=True)
        E=om.MVector (p5)
        
        AE = A - E
        CE = E - C
        distMax=AB.length()+BC.length() #distancia somada dos bones    
        pinScaleJnt1 = AE.length()/AB.length()
        pinScaleJnt2 = CE.length()/BC.length()
               
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
        
        poleVec.cntrl.worldMatrix[0]  >> pinDist1.inMatrix2
        poleVec.cntrl.worldMatrix[0]  >> pinDist2.inMatrix2
        
        limbMoveAll.scaleX >> pinMultiScale1.input1
        limbMoveAll.scaleX >> pinMultiScale2.input1
        
        pinMultiScale1.input2.set (AE.length())
        pinMultiScale2.input2.set (CE.length())
        
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
               
        weightAttr = midCntrl.cnstr.target.connections(p=True, t='orientConstraint') ##Descobre o parametro de peso do constraint        
        ikfkReverse.outputX >> weightAttr[0]
        
        if self.handJoint:
            handTargetAttrs = handCnst.target.connections(p=True, t='orientConstraint')
            ikfkReverse.outputX >> handTargetAttrs [1]
            limbMoveAll.ikfk >> handTargetAttrs [0]
        
        limbMoveAll.ikfk >> ikH[0].ikBlend      
        ikfkBlend1.output >> j1.attr('scale'+axisName) 
        ikfkBlend2.output >> j2.attr('scale'+axisName)
        
        
        ##ikfk visibility
        ikCntrlVisCond = pm.createNode ('condition',n='ikVisCond')
        fkCntrlVisCond = pm.createNode ('condition',n='fkVisCond')
        limbMoveAll.ikfk >> ikCntrlVisCond.ft
        ikCntrlVisCond.secondTerm.set (0)
        ikCntrlVisCond.operation.set (1)
        ikCntrlVisCond.colorIfTrueR.set (1)
        ikCntrlVisCond.colorIfFalseR.set (0)
        limbMoveAll.ikfk >> fkCntrlVisCond.ft
        fkCntrlVisCond.secondTerm.set (1)
        fkCntrlVisCond.operation.set (1)
        fkCntrlVisCond.colorIfTrueR.set (1)
        fkCntrlVisCond.colorIfFalseR.set (0)
        
        ikCntrlVisCond.outColor.outColorR >> ikCntrl.cntrlGrp.visibility
        ikCntrlVisCond.outColor.outColorR >> poleVec.cntrlGrp.visibility
        fkCntrlVisCond.outColor.outColorR >> endCntrl.cntrlGrp.visibility
                       
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
        if j4:
            self.limbDict['joint4'] = j4
        self.limbDict['limbMoveAll'] = limbMoveAll
        
        ##implementar aqui as setagens padrao
        self.limbDict['ikCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['midCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['endCntrlSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['poleVecSetup'] = {'name':None, 'icone':None, 'cntrlSize':None, 'rotOrder':None}
        self.limbDict['nodeTree']={}
        self.limbDict['nameConventions']=None





