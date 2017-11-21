import maya.cmds as cmds
import lcGeneric as gen
import lcFlex as flex
import pickle
import os.path
reload (flex)
reload (gen)
###########################################################################################
#
#Limb
#
###########################################################################################
class Limb:   
    def  __init__(self, name='Limb', nameList=[], guidePos=[], guideDict={}, cntrlList=[]):
       self.name=name
       self.skinJoints=[]
       if not nameList:
           self.nameList = ['LimbA','LimbB','LimbC']
       else:
           self.nameList = nameList
          
       if not guideDict:
           self.guideDict = {self.nameList[0]:[[0,0,0],[90,0,0]],
                             self.nameList[1]: [[4,0,-0.1],[90,0,0]], 
                             self.nameList[2]:[[8, 0, 0],[90,0,0]]}
       else:
           self.guideDict = guideDict
           
       if not guidePos:
           self.guidePos = [[2,23,0], [0,0,0]]
       else:
           self.guidePos = guidePos
             
       if not cntrlList:
           self.cntrlList = ['cubo', 'cubo', 'cubo']
       else:
           self.cntrlList = cntrlList
           
       self.eixo=1
    
    def saveGuide(self, filename):
        currentGuideDict={}
        for name in self.nameList:
            wt=cmds.xform (self.name+'_loc_'+name, wd=True, q=True, t=True)
            wr=cmds.xform (self.name+'_loc_'+name, wd=True, q=True, ro=True)
            ws=cmds.xform (self.name+'_loc_'+name,  q=True, s=True)
            currentGuideDict[name]=[wt, wr, ws]
        
        wt=cmds.xform (self.name+'_guide', wd=True, q=True, t=True)
        wr=cmds.xform (self.name+'_guide', wd=True, q=True, ro=True)
        ws=cmds.xform (self.name+'_guide', q=True,r=True, s=True)
        currentGuidePos=[wt, wr, ws]
        
        saveGuideDict={'nameList':self.nameList, 'guideDict':currentGuideDict, 'guidePos':currentGuidePos, 'cntrlList':self.cntrlList, 'eixo':self.eixo}
        with open(filename, 'wb') as f:
            pickle.dump(saveGuideDict, f)
        
    def loadGuide(self, filename):
        with open(filename, 'rb') as f:
            loadGuide = pickle.load(f)
        self.nameList=loadGuide['nameList']
        self.guideDict=loadGuide['guideDict']
        self.guidePos=loadGuide['guidePos']
        self.cntrlList=loadGuide['cntrlList']
        self.eixo=loadGuide['eixo']
        self.doGuide()
        
        
    def doGuide(self):
        if cmds.objExists (self.name+'_guide'):
		    cmds.delete (self.name+'_guide', hi='below')
		
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        
        guideGlobal = cmds.circle (n=self.name+'_guide', r=1.5, ch=True, o=True, nr=[1,0,0])[0]
        lineGrp= cmds.group (n=self.name+'Lines', empty=True)
        cmds.parent (lineGrp, guideGlobal)
        if len (self.guidePos)==3:
				print 'tem escala guidePos'
				print 
				cmds.xform (guideGlobal, s=self.guidePos[2])        
        prev=''
        for guide in  self.nameList:
            loc = gen.doLocator (self.name+'_loc_'+guide,self.guideDict[guide][0],self.guideDict[guide][1])
            if len (self.guideDict[guide])==3:
				print 'tem escala'
				cmds.xform (loc, s=self.guideDict[guide][2]) 
            cmds.parent (loc, guideGlobal)
            if prev:
                line= gen.doLine (self.name+'_loc_'+prev, self.name+'_loc_'+ guide)
                cmds.parent (line,lineGrp)
            prev = guide
       
        upCrv = cmds.curve (n=self.name+'_'+self.nameList[0]+'Up_crv',d=1,p=[(-0.427371,0,0.433891),(-0.450045,0,2.935303),(-0.849086,0,2.943396),(-0.0173168,0,3.780935),(0.837273,0,2.960979),(0.438157,0,2.93212),(0.427371,0,0.410865)], k=[0,1,2,3,4 ,5,6])
        cmds.parent (upCrv,self.name+'_loc_'+self.nameList[0])
        cmds.setAttr (upCrv+'.translateX', 0)
        cmds.setAttr (upCrv+'.translateY', 0)
        cmds.setAttr (upCrv+'.translateZ', 0)
        cmds.setAttr (upCrv+'.rotateX', 90)
        cmds.setAttr (upCrv+'.rotateY', 0)
        cmds.setAttr (upCrv+'.rotateZ', 0)
        
        aux = cmds.spaceLocator (p=(0, 0, 0), n=self.name+'AuxUpvec')
        cmds.setAttr (aux[0]+'.visibility', 0)
        cmds.parent (aux, upCrv)
        cmds.move (0,0,-4, aux)
        
        cmds.aimConstraint (self.name+'_loc_'+self.nameList[1], self.name+'_loc_'+self.nameList[0], n=self.name+'_loc_'+self.nameList[0]+'_aimConstraint', offset=(0, 0,0) ,weight=1, aimVector=(1, 0 ,0) ,upVector=(0, 1, 0), worldUpType='object', worldUpObject=self.name+'_loc_'+self.nameList[2])
        cmds.aimConstraint (self.name+'_loc_'+self.nameList[2], self.name+'_loc_'+self.nameList[1], n=self.name+'_loc_'+self.nameList[1]+'_aimConstraint', offset=(0, 0,0) ,weight=1, aimVector=(1, 0 ,0) ,upVector=(0, 1, 0), worldUpType='object', worldUpObject=self.name+'_loc_'+self.nameList[0])
        
        cmds.move (self.guidePos[0][0], self.guidePos[0][1], self.guidePos[0][2], guideGlobal ,rpr =True)
        cmds.rotate (self.guidePos[1][0], self.guidePos[1][1], self.guidePos[1][2], guideGlobal)

        cmds.select (cl=True)
        if sele:
            cmds.select (sele)
        
        self.guideGlobal = guideGlobal

    def doMirrorGuide(self, eixo, local=False):
        source= self.guideGlobal
           
        if eixo=='-X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX+180)
            cmds.setAttr (self.name+'_loc_'+self.nameList[0]+'_aimConstraint.aimVectorX', -1)
            cmds.setAttr (self.name+'_loc_'+self.nameList[0]+'_aimConstraint.upVectorY', -1)
            cmds.setAttr (self.name+'_loc_'+self.nameList[1]+'_aimConstraint.aimVectorX', -1)
            cmds.setAttr (self.name+'_loc_'+self.nameList[1]+'_aimConstraint.upVectorY', -1)
            cmds.setAttr (self.name+'_'+self.nameList[0]+'Up_crv.scaleZ', -1)
            self.eixo = -1             

        elif eixo=='+X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX-180)
            cmds.setAttr (self.name+'_loc_'+self.nameList[0]+'_aimConstraint.aimVectorX', 1)
            cmds.setAttr (self.name+'_loc_'+self.nameList[0]+'_aimConstraint.upVectorY', 1)
            cmds.setAttr (self.name+'_loc_'+self.nameList[1]+'_aimConstraint.aimVectorX', 1)
            cmds.setAttr (self.name+'_loc_'+self.nameList[1]+'_aimConstraint.upVectorY', 1)
            cmds.setAttr (self.name+'_'+self.nameList[0]+'Up_crv.scaleZ', 1)
            self.eixo = 1
                        
        if not local:
            posicaoX= cmds.getAttr (source+'.translateX')
            cmds.setAttr (source+'.translateX', posicaoX*-1)
        
        rotacaoY= cmds.getAttr (source+'.rotateY')
        cmds.setAttr (source+'.rotateY', rotacaoY*-1)    
        rotacaoZ= cmds.getAttr (source+'.rotateZ')
        cmds.setAttr (source+'.rotateZ', rotacaoZ*-1) 
        
        childList  = cmds.listRelatives (source, allDescendents=True, fullPath=True, type='transform')          
        for child in childList:
            posicaoX = cmds.getAttr(child+'.translateX')
            cmds.setAttr(child+'.translateX', posicaoX*-1)
            posicaoY = cmds.getAttr (child+".translateY")
            cmds.setAttr (child+".translateY", posicaoY*-1)
            posicaoZ = cmds.getAttr (child+".translateZ")
            cmds.setAttr (child+".translateZ",posicaoZ*-1)

        if eixo=='-X':
            cmds.setAttr (self.name+'AuxUpvec.translateZ', 4)                 
        if eixo=='+X':
            cmds.setAttr (self.name+'AuxUpvec.translateZ', 4)
                              
    def doSkeleton(self,prefix='',drawStyle=0):
        allJoints=[]
        if cmds.objExists (self.name+'_'+prefix+self.nameList[0]+'_jnt'):
            cmds.delete (self.name+'_'+prefix+self.nameList[0]+'_jnt', hi='below')
        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        
        for jntName in self.nameList:           
            jnt=gen.doJoint (self.name+'_'+prefix+jntName+'_jnt',self.name+'_loc_'+jntName )
            allJoints.append(jnt)
            cmds.setAttr (self.name+'_'+prefix+jntName+'_jnt.drawStyle', drawStyle)
            gen.alignObjs (self.name+'_loc_'+jntName, self.name+'_'+prefix+jntName+'_jnt', False)

        cmds.select (cl=True)
        if sele:
            cmds.select (sele)
        return allJoints

    def doCntrlFK(self, doStretch=True):
        if cmds.objExists (self.name+'_fkGrp'):
		    cmds.delete (self.name+'_fkGrp', hi='below')
		    
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)
            
        self.doSkeleton('fk', 2)
        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        
        prev =''
        for i in range (len(self.nameList)):     
            gen.createCntrl (self.name+'_'+'fk'+self.nameList[i],self.name+'_'+'fk'+self.nameList[i]+'_jnt',1, self.cntrlList[i], 1)           
            if prev:
                cmds.parent (self.name+'_'+'fk'+self.nameList[i]+'_grp', self.name+'_'+'fk'+prev+'_cntrl')
            prev = self.nameList[i]
            cmds.parentConstraint (self.name+'_'+'fk'+self.nameList[i]+'_cntrl', self.name+'_'+'fk'+self.nameList[i]+'_jnt', mo=False)
        
        fkGrp = cmds.group (self.name+'_'+'fk'+self.nameList[0]+'_grp', self.name+'_'+'fk'+self.nameList[0]+'_jnt', n=self.name+'_fkGrp')
        cmds.select (cl=True)
        
        if doStretch:
            if cmds.objExists(self.name+'fkDist1'):
            	cmds.delete(self.name+'fkDist1')
            if cmds.objExists(self.name+'fkDist2'):
            	cmds.delete(self.name+'fkDist2')
            if cmds.objExists(self.name+'fkMult1'):
            	cmds.delete(self.name+'fkMult1')			
            if cmds.objExists(self.name+'fkMult2'):
            	cmds.delete(self.name+'fkMult2')
            
            distFK1 = cmds.createNode ('distanceBetween', n=self.name+'fkDist1')
            distFK2 = cmds.createNode ('distanceBetween', n=self.name+'fkDist2')
            multiFK1 = cmds.createNode ('multiplyDivide', n=self.name+'fkMult1')
            multiFK2 = cmds.createNode ('multiplyDivide', n=self.name+'fkMult2')
            
            cmds.connectAttr (self.name+'_'+'fk'+self.nameList[0]+'_jnt.worldMatrix[0]', distFK1+'.inMatrix1', force=True)
            cmds.connectAttr (self.name+'_'+'fk'+self.nameList[1]+'_jnt.worldMatrix[0]', distFK1+'.inMatrix2', force=True)
            cmds.connectAttr (distFK1+'.distance',multiFK1+'.input1X', force=True)
            cmds.setAttr (multiFK1+'.input2X', cmds.getAttr (distFK1+'.distance'))
            cmds.setAttr (multiFK1+'.operation', 2)
            
            cmds.connectAttr (self.name+'_'+'fk'+self.nameList[1]+'_jnt.worldMatrix[0]', distFK2+'.inMatrix1', force=True)
            cmds.connectAttr (self.name+'_'+'fk'+self.nameList[2]+'_jnt.worldMatrix[0]', distFK2+'.inMatrix2', force=True)
            cmds.connectAttr (distFK2+'.distance',multiFK2+'.input1X', force=True)
            cmds.setAttr (multiFK2+'.input2X', cmds.getAttr (distFK2+'.distance'))
            cmds.setAttr (multiFK2+'.operation', 2)
            
        if sele:
            cmds.select (sele)
                
        self.fkGrp = fkGrp
           
    def doCntrlIK(self, doStretch=True):
        if cmds.objExists (self.name+'_'+self.nameList[1]+'Upvec_grp'):
            cmds.delete (self.name+'_'+self.nameList[1]+'Upvec_grp', hi='below')
        if cmds.objExists (self.name+'_ikGrp'):
            cmds.delete (self.name+'_ikGrp', hi='below')
        if cmds.objExists (self.name+'_'+'ik'+self.nameList[2]+'_grp'):
            cmds.delete (self.name+'_'+'ik'+self.nameList[2]+'_grp', hi='below')
            		
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)
                       
        self.doSkeleton('ik', 2)
        
        elbowJnt=self.name+'_'+'ik'+self.nameList[1]+'_jnt'
        wristJnt = self.name+'_'+'ik'+self.nameList[2]+'_jnt'
        shoulderJnt = self.name+'_'+'ik'+self.nameList[0]+'_jnt'
        
        upvec = cmds.curve (n=self.name+'_'+self.nameList[1]+'Upvec_cntrl', d=1, p=[(0,0,-0.471058),(-0.471058,0,0.471058),(0.471058,0,0.471058),(0,0,-0.471058)],k=[0,1,2,3])
        upVecGrp = cmds.group (upvec, n=self.name+'_'+self.nameList[1]+'Upvec_grp')
        cmds.setAttr (upvec+'.scaleX', 1)
        cmds.setAttr (upvec+'.scaleY', 1)
        cmds.setAttr (upvec+'.scaleZ', 1)
        gen.alignObjs (elbowJnt, upVecGrp, True, True, False)
        
        
        auxGuide = cmds.xform (self.name+'AuxUpvec', q=True, t=True, ws=True)
        upGuide = cmds.xform (self.name+'_'+self.nameList[0]+'Up_crv', q=True, t=True, ws=True)
        dir=upGuide[2] - auxGuide[2]
        print dir
        if dir>0:
            cmds.move (0,0,-6, upVecGrp, r=True)
        if dir<0:
            cmds.move (0,0,6, upVecGrp, r=True)
            
        tempCnst = cmds.aimConstraint (elbowJnt, upvec, n='ElbowCns', offset=(0, 0,0) ,weight=1, aimVector=(0, 0 ,-1) ,upVector=(0, 1, 0), worldUpType='vector', worldUpVector= (0,1,0))
        cmds.delete (tempCnst)
        cmds.makeIdentity (upvec,apply=True,t=1,r=1,s=1,n=0)        
        
        wristCntrl = gen.createCntrl (self.name+'_'+'ik'+self.nameList[2],wristJnt ,1.2, "cubo", 1)
        ikWristHandle = cmds.ikHandle( ee=wristJnt , sj=shoulderJnt , sol='ikRPsolver' ,n=self.name+'_'+self.nameList[2]+'IkHandle')[0]
        cmds.setAttr (ikWristHandle+'.visibility', 0)
        cmds.parentConstraint (wristCntrl, ikWristHandle)
        cmds.poleVectorConstraint (upvec  ,ikWristHandle, w=1)
        cmds.orientConstraint (wristCntrl,wristJnt)
              
        cmds.group ( self.name+'_'+'ik'+self.nameList[0]+'_jnt', ikWristHandle,  n=self.name+'_ikGrp')
        
        if doStretch:
			cmds.group (empty=True, n=self.name+'DistAux')
			gen.alignObjs (self.name+'_'+'ik'+self.nameList[0]+'_jnt', self.name+'DistAux', True, True, False)
			cmds.parent (self.name+'DistAux', self.name+'_ikGrp')
            
			if cmds.objExists(self.name+'ikDist1'):
				cmds.delete(self.name+'ikDist1')            
			if cmds.objExists(self.name+'ikMult1'):
				cmds.delete(self.name+'ikMult1') 
			
			
			distIK1 = cmds.createNode ('distanceBetween', n=self.name+'ikDist1')
			multiIK1 = cmds.createNode ('multiplyDivide', n=self.name+'ikMult1')
			cmds.addAttr (wristCntrl, ln='stretchMulti', at='double',k=True)
			cmds.addAttr (wristCntrl, ln='stretchBias', at='double', k=True)
            
			if cmds.objExists(self.name+'ikcond1'):
				cmds.delete(self.name+'ikcond1')            
			condIK1 = cmds.createNode ('condition', n=self.name+'ikcond1')
			
			cmds.connectAttr (self.name+'DistAux.worldMatrix[0]', distIK1+'.inMatrix1', force=True)
			cmds.connectAttr (wristCntrl+'.worldMatrix[0]', distIK1+'.inMatrix2', force=True)
			cmds.connectAttr (distIK1+'.distance',multiIK1+'.input1X', force=True)
			
			multi2 = cmds.createNode ('multiplyDivide', n=self.name+'ikMultScl')
			multi3 =cmds.createNode ('multiplyDivide', n=self.name+'ikMultGlbScl')
			cond2 = cmds.createNode ('condition', n=self.name+'ikGlbSclCond')
			cmds.setAttr (multi3+'.input1X', 1)
			cmds.setAttr (multi3+'.input2X', cmds.getAttr (distIK1+'.distance'))
			cmds.connectAttr (multi3+'.output.outputX' ,multi2+'.input2X', force=True) 
					  
			cmds.connectAttr (wristCntrl+'.stretchMulti',cond2+'.firstTerm', force=True)
			cmds.connectAttr (wristCntrl+'.stretchMulti',cond2+'.colorIfTrue.colorIfTrueR', force=True)
			cmds.setAttr (cond2+'.operation', 1)
			cmds.connectAttr (cond2+'.outColor.outColorR',multi2+'.input1.input1X', force=True)
				   
			cmds.connectAttr (multi2+'.output.outputX',multiIK1+'.input2X', force=True)
			cmds.setAttr (multiIK1+'.operation', 2)            
			
			cmds.connectAttr (multiIK1+'.outputX',condIK1+'.firstTerm', force=True)
			cmds.connectAttr (multiIK1+'.outputX',condIK1+'.colorIfTrueR', force=True)
			cmds.setAttr (condIK1+'.operation', 3)
			cmds.setAttr (condIK1+'.secondTerm', 1)
            #cmds.connectAttr (self.name+'ikcond1.outColorR', self.name+'_'+'ik'+self.nameList[0]+'_jnt.scaleX', force=True)
            #cmds.connectAttr (self.name+'ikcond1.outColorR', self.name+'_'+'ik'+self.nameList[1]+'_jnt.scaleX', force=True)
            
            
            
            ##stretch cntrls
			av01 = cmds.createNode ('plusMinusAverage', n=self.name+'ik'+self.nameList[0]+'StretchAdd')
			av02 = cmds.createNode ('plusMinusAverage', n=self.name+'ik'+self.nameList[1]+'StretchAdd')
			multi01 = cmds.createNode ('multDoubleLinear', n=self.name+'ik'+self.nameList[1]+'Stretch01Multi')
			multi02 = cmds.createNode ('multDoubleLinear', n=self.name+'ik'+self.nameList[1]+'Stretch02Multi')
			multi03 = cmds.createNode ('multDoubleLinear', n=self.name+'ik'+self.nameList[1]+'Stretch03Multi')
			cond02 = cmds.createNode ('condition', n=self.name+'ikcond2')
			
			cmds.connectAttr (wristCntrl+'.stretchMulti', multi01+'.input1')
			cmds.connectAttr (condIK1+'.outColor.outColorR', multi01+'.input2')
			
			cmds.connectAttr (wristCntrl+'.stretchBias', av01 +'.input1D[0]')
			cmds.setAttr (av01+'.input1D[1]', 1)
			cmds.setAttr (av01+'.operation', 1)
			
			cmds.setAttr (av02+'.input1D[0]', 1)
			cmds.setAttr (av02+'.operation', 2)
			cmds.connectAttr (wristCntrl+'.stretchBias', av02 +'.input1D[1]')
			
			cmds.connectAttr (multi01+'.output', multi02+'.input1')
			cmds.connectAttr (multi01+'.output', multi03+'.input1')
			cmds.connectAttr (av01+'.output1D', multi02+'.input2')
			cmds.connectAttr (av02+'.output1D', multi03+'.input2')            
			
			cmds.connectAttr (wristCntrl+'.stretchMulti', cond02+'.firstTerm')
			cmds.setAttr (cond02+'.secondTerm', 0)
			cmds.setAttr (cond02+'.colorIfTrueR', 1)
			cmds.setAttr (cond02+'.colorIfTrueG', 1)
			cmds.setAttr (cond02+'.operation', 0)
			
			cmds.connectAttr (multi02+'.output', cond02+'.colorIfFalseR')
			cmds.connectAttr (multi03+'.output', cond02+'.colorIfFalseG')
			
			cmds.connectAttr (cond02+'.outColor.outColorR', self.name+'_'+'ik'+self.nameList[0]+'_jnt.scaleX', force=True)
			cmds.connectAttr (cond02+'.outColor.outColorG', self.name+'_'+'ik'+self.nameList[1]+'_jnt.scaleX', force=True)
				
			self.ikGrp = self.name+'_ikGrp'
        
    def doSkinJoints(self, doFlex=False, doStretch=True):
        self.skinJoints = self.doSkeleton('skin')
        multiFK1 =self.name+'fkMult1'
        if 1:
			cmds.select (self.name+'_'+'skin'+self.nameList[1]+'_jnt')
			jnt=gen.doJoint (self.name+'_'+'skin_auxFoldCenter_jnt',self.name+'_loc_'+self.nameList[1])
			jnt1=gen.doJoint (self.name+'_'+'skin_auxFoldIN_jnt',self.name+'_loc_'+self.nameList[1])
			cmds.move (0,0.5,0, jnt1, r=True, os=True)
			cmds.select (jnt)
			jnt2=gen.doJoint (self.name+'_'+'skin_auxFoldOUT_jnt',self.name+'_loc_'+self.nameList[1])
			cmds.move(0, -0.5,0, jnt2, r=True, os=True)
			
        if cmds.objExists (self.name+'_IKFK_Switch'):
            grp=self.name+'_IKFK_Switch' 
        else:
            grp=cmds.group (empty=True, n=self.name+'_IKFK_Switch')
        
        attrList = cmds.listAttr (grp, v=True, k=True)
        for attr in attrList:
            cmds.setAttr (grp+'.'+attr, k=0)
        
        cmds.addAttr (grp, ln='tp', dt='string', k=False)
        cmds.setAttr (grp+'.tp', 'limb',type='string')
          
        cmds.addAttr (grp, ln='IKFK', at='double', k=True, min=0, max=1, dv=1)
        node=cmds.createNode ('reverse', n=self.name+'_IKFKrev')
        cmds.connectAttr (grp+'.IKFK', node+'.input.inputX')
        
        cmds.addAttr (grp, ln='ikCntrl', at='bool', k=False)
        cmds.addAttr (grp, ln='fkCntrl', at='bool', k=False)
        cmds.connectAttr (grp+'.fkCntrl', self.name+'_'+'fk'+self.nameList[0]+'_grp.visibility')
        cmds.connectAttr (grp+'.ikCntrl', self.name+'_'+'ik'+self.nameList[-1]+'_grp.visibility')
        cmds.connectAttr (grp+'.ikCntrl', self.name+'_'+self.nameList[1]+'Upvec_grp.visibility')
        
        ikCond=cmds.createNode ('condition', n=self.name+'_ikVizCond')
        cmds.connectAttr (grp+'.IKFK', ikCond+'.firstTerm')
        cmds.setAttr (ikCond+'.secondTerm', 0)
        cmds.setAttr (ikCond+'.colorIfTrueR', 1)
        cmds.setAttr (ikCond+'.colorIfFalseR', 0)
        cmds.setAttr (ikCond+'.operation', 2)
        cmds.connectAttr (ikCond+'.outColor.outColorR', grp+'.ikCntrl')
        
        fkCond=cmds.createNode ('condition', n=self.name+'_fkVizCond')
        cmds.connectAttr (grp+'.IKFK', fkCond+'.firstTerm')
        cmds.setAttr (fkCond+'.secondTerm', 1)
        cmds.setAttr (fkCond+'.colorIfTrueR', 1)
        cmds.setAttr (fkCond+'.colorIfFalseR', 0)
        cmds.setAttr (fkCond+'.operation', 4)
        cmds.connectAttr (fkCond+'.outColor.outColorR', grp+'.fkCntrl')
        
        cmds.addAttr (grp, ln='ik0', at='message')
        cmds.connectAttr (self.name+'_'+'ik'+self.nameList[-1]+'_cntrl.message',grp+'.ik0')
        cmds.addAttr (grp, ln='ikUp', at='message')
        cmds.connectAttr (self.name+'_'+self.nameList[1]+'Upvec_cntrl.message',grp+'.ikUp')
        cmds.addAttr (grp, ln='to', at='message', k=False)
        
        for i in range (len(self.nameList)):
            fkCnst=None
            ikCnst=None
            if cmds.objExists (self.name+'_'+'fk'+self.nameList[i]+'_jnt'):
                fkCnst = cmds.parentConstraint (self.name+'_'+'fk'+self.nameList[i]+'_jnt', self.name+'_'+'skin'+self.nameList[i]+'_jnt', mo=False)[0]
                
                cmds.addAttr (grp, ln='fkJnt'+str (i), at='message')
                cmds.connectAttr (self.name+'_'+'fk'+self.nameList[i]+'_jnt.message',grp+'.fkJnt'+str(i))
                
                cmds.addAttr (grp, ln='fk'+str(i), at='message')
                cmds.connectAttr (self.name+'_'+'fk'+self.nameList[i]+'_cntrl.message', grp+'.fk'+str(i))
                
            if cmds.objExists (self.name+'_'+'ik'+self.nameList[i]+'_jnt'):
                ikCnst = cmds.parentConstraint (self.name+'_'+'ik'+self.nameList[i]+'_jnt', self.name+'_'+'skin'+self.nameList[i]+'_jnt', mo=False)[0]
                
                cmds.addAttr (grp, ln='ikJnt'+str (i), at='message')
                cmds.connectAttr (self.name+'_'+'ik'+self.nameList[i]+'_jnt.message',grp+'.ikJnt'+str(i))
            
            if fkCnst and ikCnst:
                cmds.connectAttr (grp+'.IKFK', ikCnst+'.'+self.name+'_'+'ik'+self.nameList[i]+'_jntW1') 
                cmds.connectAttr (node+'.output.outputX',fkCnst+'.'+self.name+'_'+'fk'+self.nameList[i]+'_jntW0')
		
		cond02 = self.name+'ikcond2'
			
        if doFlex:
			
			cmds.addAttr (grp, ln='ribbonViz', at='bool', k=True)
			
			width1= cmds.getAttr (self.name+'_'+'skin'+self.nameList[1]+'_jnt.translateX')
			flexBraco1 = flex.RibbonLimb(self.name+'_'+self.nameList[0],abs (width1))
			cmds.parent (flexBraco1.cntrlGrp, self.name+'_'+'skin'+self.nameList[0]+'_jnt', relative = True)
			cmds.rotate (-90*self.eixo,0,0, flexBraco1.cntrlGrp)
			gen.alignObjs (self.name+'_'+'skin'+self.nameList[1]+'_jnt', flexBraco1.aux1 ,True, True, False)
			cmds.setAttr (flexBraco1.aux1+'.rotateX', 0)
			gen.alignObjs (self.name+'_'+'skin'+self.nameList[0]+'_jnt', flexBraco1.aux2 ,True, True, False)
			cmds.setAttr (flexBraco1.aux2+'.rotateX', 0)
					  
			width2= cmds.getAttr (self.name+'_'+'skin'+self.nameList[2]+'_jnt.translateX')
			flexBraco2 = flex.RibbonLimb(self.name+'_'+self.nameList[1],abs (width2))
			cmds.parent (flexBraco2.cntrlGrp, self.name+'_'+'skin'+self.nameList[1]+'_jnt', relative = True)
			cmds.rotate (-90*self.eixo,0,0, flexBraco2.cntrlGrp)
			gen.alignObjs (self.name+'_'+'skin'+self.nameList[2]+'_jnt', flexBraco2.aux1 ,True, True, False)
			cmds.setAttr (flexBraco2.aux1+'.rotateX', 0) 
			gen.alignObjs (self.name+'_'+'skin'+self.nameList[1]+'_jnt', flexBraco2.aux2 ,True, True, False)           
			cmds.setAttr (flexBraco2.aux2+'.rotateX', 0)  
			
			gen.alignObjs (self.name+'_'+'skin'+self.nameList[1]+'_jnt', flexBraco1.extr ,True, False, False)
			gen.alignObjs (self.name+'_'+'skin'+self.nameList[2]+'_jnt', flexBraco2.extr ,True, False, False)
			if self.eixo==-1:
				cmds.rotate (0,180,0,flexBraco1.midJnt)
				cmds.rotate (0,180,0,flexBraco2.midJnt)
				
			ribbon1 = gen.createCntrl (self.name+'_'+self.nameList[1]+'RibbonEnd',flexBraco1.aux1,0.3, "circuloX", 1)                  
			ribbon2 = gen.createCntrl (self.name+'_'+self.nameList[0]+'RibbonMid',flexBraco1.aux3,0.3, "circuloX", 1)
			ribbon3 = gen.createCntrl (self.name+'_'+self.nameList[1]+'RibbonMid',flexBraco2.aux3,0.3, "circuloX", 1)
			
			cmds.parent (self.name+'_'+self.nameList[1]+'RibbonEnd_grp', self.name+'_'+'skin'+self.nameList[1]+'_jnt')
			cmds.rotate (0,0,0, self.name+'_'+self.nameList[1]+'RibbonEnd_grp')
			cmds.parent (self.name+'_'+self.nameList[0]+'RibbonMid_grp', self.name+'_'+'skin'+self.nameList[0]+'_jnt')
			cmds.rotate (0,0,0, self.name+'_'+self.nameList[0]+'RibbonMid_grp')
			cmds.pointConstraint (self.name+'_'+'skin'+self.nameList[0]+'_jnt', self.name+'_'+self.nameList[1]+'RibbonEnd_cntrl', self.name+'_'+self.nameList[0]+'RibbonMid_grp')
			
			cmds.parent (self.name+'_'+self.nameList[1]+'RibbonMid_grp', self.name+'_'+'skin'+self.nameList[1]+'_jnt')
			cmds.rotate (0,0,0, self.name+'_'+self.nameList[1]+'RibbonMid_grp')
			cmds.pointConstraint (self.name+'_'+self.nameList[1]+'RibbonEnd_cntrl', self.name+'_'+'skin'+self.nameList[2]+'_jnt', self.name+'_'+self.nameList[1]+'RibbonMid_grp')
			
			cmds.parentConstraint (self.name+'_'+'skin'+self.nameList[2]+'_jnt', flexBraco2.aux1, mo=True)
			cmds.parentConstraint (ribbon1, flexBraco1.aux1, mo=True)
			cmds.parentConstraint (ribbon1, flexBraco2.aux2, mo=True)
			cmds.parentConstraint (ribbon2, flexBraco1.aux3, mo=True)                       
			cmds.parentConstraint (ribbon3, flexBraco2.aux3, mo=True)
			
			cmds.connectAttr (grp+'.ribbonViz', self.name+'_'+self.nameList[1]+'RibbonEnd_grp.visibility') 
			cmds.connectAttr (grp+'.ribbonViz', self.name+'_'+self.nameList[0]+'RibbonMid_grp.visibility') 
			cmds.connectAttr (grp+'.ribbonViz', self.name+'_'+self.nameList[1]+'RibbonMid_grp.visibility')
			x = self.skinJoints[-1]
			y = self.skinJoints[0]
			self.skinJoints=flexBraco2.skinJoints+flexBraco1.skinJoints
			self.skinJoints.append (x)
			#self.skinJoints.append (y)
			
			cmds.parent (jnt, self.name+'_'+self.nameList[0]+'4_jnt')
			cmds.parentConstraint (self.name+'_'+self.nameList[1]+'0_jnt', self.name+'_'+self.nameList[0]+'4_jnt', jnt, mo=True)
			self.skinJoints=self.skinJoints+[jnt1,jnt2]
        else:
			cmds.expression (s=jnt+'.rotateX ='+ self.name+'_skin'+self.nameList[1]+'_jnt.rotateZ/-2', o=jnt, ae=True, uc="all")
			    
        if doStretch:			
            multiSkn1 = cmds.createNode ('multDoubleLinear', n=self.name+'skinMult1') 
            multiSkn2 = cmds.createNode ('multDoubleLinear', n=self.name+'skinMult2')   
            multiSkn3 = cmds.createNode ('multDoubleLinear', n=self.name+'skinMult3')            
            addSkn1 = cmds.createNode ('addDoubleLinear', n=self.name+'skinAdd1') 
            addSkn2 = cmds.createNode ('addDoubleLinear', n=self.name+'skinAdd2')
            
            cmds.connectAttr (cond02+'.outColorR',multiSkn1+'.input1')
            cmds.connectAttr (self.name+'_IKFK_Switch.IKFK',multiSkn1+'.input2') 
            
            cmds.connectAttr (multiFK1+'.outputX',multiSkn2+'.input1')
            cmds.connectAttr (node+'.outputX',multiSkn2+'.input2')
            
            cmds.connectAttr (self.name+'fkMult2.outputX',multiSkn3+'.input1')
            cmds.connectAttr (node+'.outputX',multiSkn3+'.input2')
            
            cmds.connectAttr (multiSkn1+'.output',addSkn1+'.input1')
            cmds.connectAttr (multiSkn2+'.output',addSkn1+'.input2')
            
            cmds.connectAttr (multiSkn1+'.output',addSkn2+'.input1')
            cmds.connectAttr (multiSkn3+'.output',addSkn2+'.input2')
            
            #cmds.connectAttr (self.name+'skinAdd1.output', self.name+'_'+'skin'+self.nameList[0]+'_jnt.scaleX')
            #cmds.connectAttr (self.name+'skinAdd2.output', self.name+'_'+'skin'+self.nameList[1]+'_jnt.scaleX')
                    
        self.skinJntStart = self.name+'_'+'skin'+self.nameList[0]+'_jnt'        
        self.skinJntEnd =  self.name+'_'+'skin'+self.nameList[2]+'_jnt'
        
                                          
###########################################################################################
#
#FINGER
#
###########################################################################################
class Finger:
    def __init__ (self,name, divNum=5, divNames=[], guidePos=[], guideDict={}, falange=True):
        self.name = name
        self.divNum = divNum
        self.falange = falange
        
        if not guidePos:
            self.guidePos=[[0,0,0],[0,0,0]]
        else:
            self.guidePos = guidePos
            
        if not divNames:
            self.divNames=[]
            for i in range(divNum):
                self.divNames.append('Div'+str(i))
        elif len(divNames)<divNum:
            print 'entre numero certo de nomes'
            sys.exit()
        else:
            self.divNames=divNames
            
        if not guideDict:
            self.guideDict={}
            for i in range(divNum):
                self.guideDict[self.name+self.divNames[i]]=[[1,0,0],[0,0,0]]
            self.guideDict[self.name+self.divNames[0]]=[[0,0,0],[0,0,0]]
        else:
            self.guideDict=guideDict       
        
        self.eixo=1

    def saveGuide(self, filename):
        currentGuideDict={}
        for i in range (self.divNum):
            wt=cmds.xform (self.name+self.divNames[i]+'_loc', wd=True, q=True, t=True)
            wr=cmds.xform (self.name+self.divNames[i]+'_loc', wd=True, q=True, ro=True)
            #ws=cmds.xform (self.name+self.divNames[i]+'_loc', r = True, q=True, s=True)
            currentGuideDict[self.name+self.divNames[i]]=[wt, wr]
        
        wt=cmds.xform (self.name+'_guide', wd=True, q=True, t=True)
        wr=cmds.xform (self.name+'_guide', wd=True, q=True, ro=True)
        ws=cmds.xform (self.name+'_guide', q=True, r=True, s=True)
        currentGuidePos=[wt, wr,ws]
       
        saveGuideDict={'divNum':self.divNum, 'divNames':self.divNames, 'guideDict':currentGuideDict, 'guidePos':currentGuidePos, 'falange':self.falange}
        with open(filename, 'wb') as f:
            pickle.dump(saveGuideDict, f)
        
    def loadGuide(self, filename):
        with open(filename, 'rb') as f:
            loadGuide = pickle.load(f)
        self.divNum=loadGuide['divNum']
        print self.divNum
        self.divNames=loadGuide['divNames']
        print self.divNames       
        self.guideDict=loadGuide['guideDict']
        print self.guideDict
        self.guidePos=loadGuide['guidePos']
        print self.guidePos
        self.falange=loadGuide['falange']
        print self.falange
        self.doGuide()
                          
    def doGuide (self):
        if cmds.objExists (self.name+'_guide'):
		    cmds.delete (self.name+'_guide', hi='below')
		    
        guideGlobal = cmds.circle (n=self.name+'_guide', r=0.5, ch=True, o=True, nr=[1,0,0])[0]
        
        if len (self.guidePos)==3:
				cmds.xform (guideGlobal, s=self.guidePos[2])
				       
        prev=guideGlobal
        for i in range (self.divNum):
            loc=gen.doLocator (self.name+self.divNames[i]+'_loc', [0,0,0],[0,0,0], 0.2)
            cmds.parent (loc,prev)
            cmds.xform (loc, t=self.guideDict[self.name+self.divNames[i]][0])
            cmds.xform (loc, ro=self.guideDict[self.name+self.divNames[i]][1])

            prev=loc
        
        cmds.xform (guideGlobal, t=self.guidePos[0], ro=self.guidePos[1])

        self.guideGlobal = guideGlobal
        
    def doSkeleton(self, prefix='', drawStyle=0):
        allJoints=[]
        if cmds.objExists (self.name+'_'+prefix+self.divNames[0]+'_jnt'):
		    cmds.delete (self.name+'_'+prefix+self.divNames[0]+'_jnt', hi='below')
		    
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        for i in range (self.divNum):
            jnt = gen.doJoint (self.name+'_'+prefix+self.divNames[i]+'_jnt',self.name+self.divNames[i]+'_loc' )
            allJoints.append(jnt)
            gen.alignObjs (self.name+self.divNames[i]+'_loc', self.name+'_'+prefix+self.divNames[i]+'_jnt', False)
        cmds.select (cl=True)
        if sele:
            cmds.select (sele)
        return allJoints

    def doMirrorGuide(self, eixo, local=False):
        source= self.guideGlobal
           
        if eixo=='-X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX+180)
            self.eixo = -1          
        elif eixo=='+X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX-180)
            self.eixo = 1             
        if not local:
            posicaoX= cmds.getAttr (source+'.translateX')
            cmds.setAttr (source+'.translateX', posicaoX*-1)
        
        rotacaoY= cmds.getAttr (source+'.rotateY')
        cmds.setAttr (source+'.rotateY', rotacaoY*-1)    
        rotacaoZ= cmds.getAttr (source+'.rotateZ')
        cmds.setAttr (source+'.rotateZ', rotacaoZ*-1) 
        
        childList  = cmds.listRelatives (source, allDescendents=True, fullPath=True, type='transform')          
        for child in childList:
            posicaoX = cmds.getAttr(child+'.translateX')
            cmds.setAttr(child+'.translateX', posicaoX*-1)
            posicaoY = cmds.getAttr (child+".translateY")
            cmds.setAttr (child+".translateY", posicaoY*-1)
            posicaoZ = cmds.getAttr (child+".translateZ")
            cmds.setAttr (child+".translateZ",posicaoZ*-1)
       
    def doCntrlFK(self):
        if cmds.objExists (self.name+'_grp'):
            cmds.delete (self.name+'_grp', hi='below')
        
        cmds.setAttr(self.name+'_guide.visibility',False)    
        
        if self.falange:
            cntrl = gen.createCntrl (self.name,self.name+'_'+self.divNames[0]+'_jnt',1, 'ponteiroReto', 1)
            cmds.parentConstraint (cntrl, self.name+'_'+self.divNames[0]+'_jnt')
            
            cntrlFal = gen.createCntrl (self.name+'Fal',self.name+'_'+self.divNames[1]+'_jnt',1, 'ponteiroReto', 1)
            cmds.parentConstraint (cntrlFal, self.name+'_'+self.divNames[1]+'_jnt')
            cmds.parent (self.name+'Fal_grp', cntrl)
             
            for i in range (2,self.divNum-1):        
                cmds.addAttr(cntrlFal, ln=self.divNames[i]+'Curl', at='double', k=True)
                cmds.connectAttr(cntrlFal+'.'+self.divNames[i]+'Curl', self.name+'_'+self.divNames[i]+'_jnt.rotateZ')
        else:
            cntrl = gen.createCntrl (self.name,self.name+'_'+self.divNames[0]+'_jnt',1, 'ponteiroReto', 1)
            cmds.parentConstraint (cntrl, self.name+'_'+self.divNames[0]+'_jnt')
            
            for i in range (1,self.divNum-1):        
                cmds.addAttr(cntrl, ln=self.divNames[i]+'Curl', at='double', k=True)
                cmds.connectAttr(cntrl+'.'+self.divNames[i]+'Curl', self.name+'_'+self.divNames[i]+'_jnt.rotateZ')
            
        self.fkGrp = self.name+'_grp'
        
    def doSkinJoints(self, doFlex=False):
        self.skinJoints = self.doSkeleton('skin')        
        for name in self.divNames:
            fkCnst=None
            ikCnst=None
            if cmds.objExists (self.name+'_fk'+name+'_jnt'):
                fkCnst = cmds.parentConstraint (self.name+'_fk'+name+'_jnt', self.name+'_skin'+name+'_jnt')[0]   
            if cmds.objExists (self.name+'_ik'+name+'_jnt'):
                ikCnst = cmds.parentConstraint (self.name+'_ik'+name+'_jnt', self.name+'_skin'+name+'_jnt')[0]   
            if fkCnst and ikCnst:
                cmds.connectAttr (grp+'.IKFK', ikCnst+'.'+self.name+'_ik'+name+'_jntW1') 
                cmds.connectAttr (node+'.output.outputX',fkCnst+'.'+self.name+'_fk'+name+'_jntW0')         
        
        self.skinJntStart = self.name+'_'+'skin'+self.nameList[0]+'_jnt'    
        self.skinJntEnd =  self.name+'_'+'skin'+self.nameList[-1]+'_jnt'
        
             
##############################################################################################################
#
# HAND
#
##############################################################################################################
class Hand:
    def __init__(self, name, fingerNum=5, divNum=5, nameList=[], guidePos=[], guideDict={}, falange=True):
        self.name = name
        self.fingerNum = fingerNum
        self.divNum =divNum
        self.skinJoints=[]
        if not guidePos:
            self.guidePos = [[0,0,0],[0,0,0]]
        else:
            self.guidePos=guidePos
        if not nameList:
            self.nameList=[]
            for i in range (fingerNum):
                self.nameList.append (self.name+'Finger'+str(i))
        else:
            self.nameList=nameList
        if not guideDict:
            self.guideDict={}
            for i in range (fingerNum):
                self.guideDict[self.nameList[i]]=[[0,0,(i-2)],[0,0,0]]
        else:
            self.guideDict= guideDict      
        
        self.fingerList = []        
        for i in range(fingerNum):
            self.fingerList.append(Finger(self.name+'_'+self.nameList[i] , self.divNum , [] , self.guideDict[self.nameList[i]], {}, falange))                                        
        self.eixo=1
                
    def doGuide(self):
        if cmds.objExists (self.name+'_guide'):
		    cmds.delete (self.name+'_guide', hi='below')
        
        handGlobal = cmds.circle (n=self.name+'_guide', r=0.8, ch=True, o=True, nr=[1,0,0])[0]
        if len (self.guidePos)==3:
			cmds.xform (handGlobal, s = self.guidePos[2])
        for finger in self.fingerList:
            finger.doGuide()
            cmds.parent (finger.guideGlobal, handGlobal)
        cmds.move (self.guidePos[0][0], self.guidePos[0][1],self.guidePos[0][2], handGlobal)
        cmds.rotate (self.guidePos[1][0], self.guidePos[1][1],self.guidePos[1][2], handGlobal)

        self.guideGlobal = handGlobal

    def saveGuide(self, filename):
        currentGuideDict={}
        for fing in self.fingerList:
            print fing.name
            print os.path.join(os.path.dirname (filename),fing.name+'.guide')
            fing.saveGuide(os.path.join(os.path.dirname (filename),fing.name+'.guide'))
            
        currentGuideDict=self.guideDict        

        wt=cmds.xform (self.name+'_guide', wd=True, q=True, t=True)
        wr=cmds.xform (self.name+'_guide', wd=True, q=True, ro=True)
        ws=cmds.xform (self.name+'_guide',  q=True, r=True,  s=True)
        currentGuidePos=[wt, wr, ws]
        
        saveGuideDict={'nameList':self.nameList,'fingerNum':5, 'divNum':5, 'guideDict':currentGuideDict, 'guidePos':currentGuidePos, 'eixo':self.eixo, 'fingerList':self.fingerList}
        with open(filename, 'wb') as f:
            pickle.dump(saveGuideDict, f)
    
    def loadGuide(self, filename):
        with open(filename, 'rb') as f:
            loadGuide = pickle.load(f)
        self.nameList=loadGuide['nameList']
        self.guideDict=loadGuide['guideDict']
        self.guidePos=loadGuide['guidePos']
        self.fingerList=loadGuide['fingerList']
        self.eixo=loadGuide['eixo']
        self.fingerNum=loadGuide['fingerNum']
        self.divNum=loadGuide['divNum']
        for fing in self.fingerList:
            print fing.name
            print os.path.join(os.path.dirname (filename),fing.name+'.guide')
            fing.loadGuide(os.path.join(os.path.dirname (filename),fing.name+'.guide'))
        self.doGuide()

    def doSkeleton(self):
        allJoints=[]
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        jnt = gen.doJoint (self.name+'_jnt',self.name+'_guide')
        gen.alignObjs (self.name+'_guide', self.name+'_jnt', False)
        for finger in self.fingerList:
            skel= finger.doSkeleton()
            cmds.parent (skel[0], jnt)
            self.skinJoints=self.skinJoints+skel
        if sele:
            cmds.select (sele)
        return jnt


    def doMirrorGuide(self, eixo, local=False):
        source= self.guideGlobal
           
        if eixo=='-X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', (180-rotacaoX)*-1)
            
            self.eixo = -1          
        elif eixo=='+X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', (180-rotacaoX)*-1)
            self.eixo = 1             
        if not local:
            posicaoX= cmds.getAttr (source+'.translateX')
            cmds.setAttr (source+'.translateX', posicaoX*-1)
        
        
        escalaZ= cmds.getAttr (source+'.scaleZ')
        cmds.setAttr (source+'.scaleZ', escalaZ*-1) 
        escalaY= cmds.getAttr (source+'.scaleY')
        cmds.setAttr (source+'.scaleY', escalaY*-1)
        escalaX= cmds.getAttr (source+'.scaleX')
        cmds.setAttr (source+'.scaleX', escalaX*-1)       
        rotacaoY=cmds.getAttr(source+'.rotateY')
        cmds.setAttr (source+'.rotateY', rotacaoY*-1)
        rotacaoZ=cmds.getAttr(source+'.rotateZ')
        cmds.setAttr (source+'.rotateZ', rotacaoZ*-1)  
        
        #childList  = cmds.listRelatives (source, allDescendents=True, fullPath=True, type='transform')          
        #for child in childList:
        #    posicaoX = cmds.getAttr(child+'.translateX')
        #    cmds.setAttr(child+'.translateX', posicaoX*-1)
        #    posicaoY = cmds.getAttr (child+".translateY")
        #    cmds.setAttr (child+".translateY", posicaoY*-1)
        #    posicaoZ = cmds.getAttr (child+".translateZ")
        #    cmds.setAttr (child+".translateZ",posicaoZ*-1)
                                   
    def doCntrlFK(self):
        
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)
            
        jnt = self.doSkeleton()
        grp = cmds.group (n=self.name+'_grp', empty=True)
        cmds.parent (grp, jnt)
        for finger in self.fingerList:
            finger.doCntrlFK()       
            cmds.parent (finger.fkGrp, grp)
        
        self.skinJntStart = jnt 
        self.fkGrp = grp                


###########################################################################################
#
#FOOT
#
###########################################################################################

class Foot:
    def __init__(self, name, fingerNum=0, divNum=4, nameList=[], guidePos=[], guideDict={}):
        self.name = name
        self.fingerNum = fingerNum
        self.divNum =divNum
        self.skinJoints=[]
        if not guidePos:
            self.guidePos = [[0,0,0],[0,0,0]]
        else:
            self.guidePos=guidePos
        if not nameList:
            self.nameList=['Heel','Ankle','Ball','Toe','In','Out']
            
            for i in range (fingerNum):
                self.nameList.append (self.name+'Finger'+str(i))
        else:
            self.nameList=nameList
            
        if not guideDict:
            self.guideDict={}
            self.guideDict[self.nameList[3]]=[[0,-1.5,3.55],[0,0,0]]
            self.guideDict[self.nameList[2]]=[[0,-1.5,2.2],[0,0,0]]
            self.guideDict[self.nameList[1]]=[[0,0,0],[0,0,0]]
            self.guideDict[self.nameList[0]]=[[0,-1.5,-2],[0,0,0]]
            
            
            self.guideDict[self.nameList[4]]=[[-1,-1.5,2.2],[0,0,0]]
            self.guideDict[self.nameList[5]]=[[1,-1.5,2.2],[0,0,0]]
            
            for i in range (6,fingerNum+6):
                self.guideDict[self.nameList[i]]=[[(-4+(i*0.5)),-1.5,3.5],[0,-90,0]]
        else:
            self.guideDict= guideDict      
        
        self.fingerList = []        
        for i in range(fingerNum):
            self.fingerList.append(Finger(self.name+'_'+self.nameList[i+6] , self.divNum , [] , self.guideDict[self.nameList[i+6]]))
        
        self.eixo=1
    
        
            
    def doGuide(self):
        if cmds.objExists (self.name+'_guide'):
		    cmds.delete (self.name+'_guide', hi='below')
        
        footGlobal = cmds.circle (n=self.name+'_guide', r=0.8, ch=True, o=True, nr=[0,1,0])[0]
        if len (self.guidePos)==3:
			cmds.xform (footGlobal, s = self.guidePos[2])
			      
        for i in range(6):
            loc =gen.doLocator (self.name+'_loc'+self.nameList[i], self.guideDict[self.nameList[i]][0], self.guideDict[self.nameList[i]][1], 0.2)
            cmds.parent (loc, footGlobal )
        
        for finger in self.fingerList:
            finger.doGuide()
            cmds.parent (finger.guideGlobal, footGlobal)        
        cmds.move (self.guidePos[0][0], self.guidePos[0][1],self.guidePos[0][2], footGlobal)
        cmds.rotate (self.guidePos[1][0], self.guidePos[1][1],self.guidePos[1][2], footGlobal)
        self.guideGlobal = footGlobal

    def saveGuide(self, filename):
        currentGuideDict={}
        for fing in self.fingerList:
            print fing.name
            print os.path.join(os.path.dirname (filename),fing.name+'.guide')
            fing.saveGuide(os.path.join(os.path.dirname (filename),fing.name+'.guide'))
                    
                    
        for name in self.nameList[0:6]:
            wt=cmds.xform (self.name+'_loc'+name, wd=True, q=True, t=True)
            wr=cmds.xform (self.name+'_loc'+name, wd=True, q=True, ro=True)
            ws=cmds.xform (self.name+'_loc'+name,  q=True,r=True, s=True)
            currentGuideDict[name]=[wt, wr,ws]
                    
                    
        for name in self.nameList[6:]:
            wt=cmds.xform (self.name+'_'+name+'_guide', wd=True, q=True, t=True)
            wr=cmds.xform (self.name+'_'+name+'_guide', wd=True, q=True, ro=True)
            ws=cmds.xform (self.name+'_'+name+'_guide',  q=True,r=True, s=True)
            currentGuideDict[name]=[wt, wr,ws]
            
        print currentGuideDict
        wt=cmds.xform (self.name+'_guide', wd=True, q=True, t=True)
        wr=cmds.xform (self.name+'_guide', wd=True, q=True, ro=True)
        ws=cmds.xform (self.name+'_guide', q=True,r=True,  s=True)
        currentGuidePos=[wt, wr, ws]    
        saveGuideDict={'nameList':self.nameList,'fingerNum':self.fingerNum, 'divNum':self.divNum, 'guideDict':currentGuideDict, 'guidePos':currentGuidePos, 'eixo':self.eixo, 'fingerList':self.fingerList}
        with open(filename, 'wb') as f:
            pickle.dump(saveGuideDict, f)
		
    def loadGuide(self, filename):
        with open(filename, 'rb') as f:
            loadGuide = pickle.load(f)
        self.nameList=loadGuide['nameList']
        self.guideDict=loadGuide['guideDict']
        self.guidePos=loadGuide['guidePos']
        self.fingerList=loadGuide['fingerList']
        self.eixo=loadGuide['eixo']        
        self.fingerNum=loadGuide['fingerNum']
        self.divNum=loadGuide['divNum']
        for fing in self.fingerList:
            print fing.name
            print os.path.join(os.path.dirname (filename),fing.name+'.guide')
            fing.loadGuide(os.path.join(os.path.dirname (filename),fing.name+'.guide'))
        self.doGuide()

       
    def doMirrorGuide(self, eixo, local=False):
		source= self.guideGlobal
		
		if eixo=='-X':
			rotacaoX=cmds.getAttr(source+'.rotateX')
			cmds.setAttr (source+'.rotateX', (180-rotacaoX)*-1)
			
			self.eixo = -1          
		elif eixo=='+X':
			rotacaoX=cmds.getAttr(source+'.rotateX')
			cmds.setAttr (source+'.rotateX', (180-rotacaoX)*-1)
			self.eixo = 1             
		if not local:
			posicaoX= cmds.getAttr (source+'.translateX')
			cmds.setAttr (source+'.translateX', posicaoX*-1)
		
		
		escalaZ= cmds.getAttr (source+'.scaleZ')
		cmds.setAttr (source+'.scaleZ', escalaZ*-1) 
		escalaY= cmds.getAttr (source+'.scaleY')
		cmds.setAttr (source+'.scaleY', escalaY*-1)         
		rotacaoY=cmds.getAttr(source+'.rotateY')
		cmds.setAttr (source+'.rotateY', rotacaoY*-1)
		rotacaoZ=cmds.getAttr(source+'.rotateZ')
		cmds.setAttr (source+'.rotateZ', rotacaoZ*-1)        
		
		childList  = cmds.listRelatives (source, allDescendents=True, fullPath=True, type='transform')
		childListFilter  = [x for x in childList if 'Div' not in x  ]       
		for child in childListFilter:
			posicaoX = cmds.getAttr(child+'.translateX')
			cmds.setAttr(child+'.translateX', posicaoX*-1)
			rotacaoX=cmds.getAttr(child+'.rotateX')
			cmds.setAttr (child+'.rotateX', (180-rotacaoX)*-1)
			escalaZ= cmds.getAttr (source+'.scaleZ')
			cmds.setAttr (child+'.scaleZ', escalaZ*-1)
			escalaX= cmds.getAttr (child+'.scaleX')
			cmds.setAttr (child+'.scaleX', escalaX*-1) 
			escalaY= cmds.getAttr (child+'.scaleY')
			cmds.setAttr (child+'.scaleY', escalaY*-1)         
			rotacaoY=cmds.getAttr(child+'.rotateY')
			cmds.setAttr (child+'.rotateY', rotacaoY*-1)
			rotacaoZ=cmds.getAttr(child+'.rotateZ')
			cmds.setAttr (child+'.rotateZ', rotacaoZ*-1) 
			#posicaoY = cmds.getAttr (child+".translateY")
			#cmds.setAttr (child+".translateY", posicaoY*-1)
			#posicaoZ = cmds.getAttr (child+".translateZ")
			#cmds.setAttr (child+".translateZ",posicaoZ*-1)
		 				
                        
    def doSkeleton(self, prefix='',drawStyle=0):
        allJoints=[]
        if cmds.objExists (self.name+'_'+prefix+self.nameList[1]+'_jnt'):
            cmds.delete (self.name+'_'+prefix+self.nameList[1]+'_jnt', hi='below')
        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        
        for i in range (1,4):
            jnt = gen.doJoint (self.name+'_'+prefix+self.nameList[i]+'_jnt',self.name+'_loc'+self.nameList[i])
            allJoints.append (jnt)
            cmds.setAttr (self.name+'_'+prefix+self.nameList[i]+'_jnt.drawStyle', drawStyle)
            gen.alignObjs (self.name+'_loc'+self.nameList[i], self.name+'_'+prefix+self.nameList[i]+'_jnt', False) 

        cmds.select (self.name+'_'+prefix+self.nameList[1]+'_jnt')
        jnt = gen.doJoint (self.name+'_'+prefix+self.nameList[0]+'_jnt',self.name+'_loc'+self.nameList[0])
        allJoints.append (jnt)
        cmds.setAttr (self.name+'_'+prefix+self.nameList[0]+'_jnt.drawStyle', drawStyle)
        gen.alignObjs (self.name+'_loc'+self.nameList[0], self.name+'_'+prefix+self.nameList[0]+'_jnt', False)
        
        for finger in self.fingerList:
            skel= finger.doSkeleton()
            cmds.parent (skel[0], self.name+'_'+prefix+self.nameList[2]+'_jnt')
            alljoints=allJoints+skel
        if sele:
            cmds.select (sele)
        return allJoints  

    def doCntrlFK(self, connection=[]):
        self.doSkeleton ('fk',2)   
         
        grp = cmds.group (n=self.name+'_fkGrp', empty=True)
        ball= gen.createCntrl (self.name+'_fk'+self.nameList[2],self.name+'_fk'+self.nameList[2]+'_jnt',1, 'ponteiroReto', 1)
        
        cmds.orientConstraint (  ball, self.name+'_fk'+self.nameList[2]+'_jnt')
        cmds.parent (self.name+'_fk'+self.nameList[1]+'_jnt', self.name+'_fk'+self.nameList[2]+'_grp', grp)
        
        print self.name+'_fk'+self.nameList[1]+'_jnt', self.name+'_fk'+self.nameList[2]+'_grp'
		
        for finger in self.fingerList:
			print finger.name
			finger.doCntrlFK()
			print finger.fkGrp, grp
			cmds.parent (finger.fkGrp, grp)
                    
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)
        
        self.fkGrp = grp

    def doCntrlIK(self, connection=[]): 
        self.doSkeleton ('ik',2)
        
        footCntrl = gen.createCntrl (self.name+'_ik',self.name+'_loc'+self.nameList[0] ,1, 'cubo',1)
        
        ballHnd = cmds.ikHandle (sj= self.name+'_ik'+self.nameList[1]+'_jnt', ee= self.name+'_ik'+self.nameList[2]+'_jnt' , n=self.name+'BallIkHandle', sol='ikRPsolver')[0]
        cmds.setAttr (ballHnd+'.visibility', 0)
        toeHnd = cmds.ikHandle ( sj= self.name+'_ik'+self.nameList[2]+'_jnt', ee= self.name+'_ik'+self.nameList[3]+'_jnt', n=self.name+'ToeIkHandle', sol='ikRPsolver')[0]
        cmds.setAttr (toeHnd+'.visibility', 0)
        
        ballGrp = cmds.group (n=self.name+'_BallRot_grp', empty=True)
        gen.alignObjs (self.name+'_ik'+self.nameList[2]+'_jnt', ballGrp ,True, True, False)
        toeGrp = cmds.group (n=self.name+'_ToeRot_grp', empty=True)
        gen.alignObjs (self.name+'_ik'+self.nameList[2]+'_jnt', toeGrp ,True, True, False)
        heelGrp = cmds.group (n=self.name+'_HeelRot_grp', empty=True)
        gen.alignObjs (self.name+'_ik'+self.nameList[0]+'_jnt', heelGrp ,True, True, False)
        tipGrp = cmds.group (n=self.name+'_TipRot_grp', empty=True)
        gen.alignObjs (self.name+'_ik'+self.nameList[3]+'_jnt', tipGrp ,True, True, False)
        inGrp = cmds.group (n=self.name+'_inRot_grp', empty=True)
        gen.alignObjs (self.name+'_loc'+self.nameList[4], inGrp ,True, True, False)
        outGrp = cmds.group (n=self.name+'_outRot_grp', empty=True)
        gen.alignObjs (self.name+'_loc'+self.nameList[5], outGrp ,True, True, False)
        invFootGrp = cmds.group (n=self.name+'_invFoot_grp', empty=True)
        gen.alignObjs (self.name+'_loc'+self.nameList[1], invFootGrp ,True, True, False)
             
        cmds.parent (ballHnd, ballGrp)
        cmds.parent (toeHnd, toeGrp)
        cmds.parent (ballGrp, toeGrp, heelGrp)
        cmds.parent (heelGrp, tipGrp)
        cmds.parent (tipGrp, inGrp)
        cmds.parent (inGrp, outGrp)
        cmds.parent (outGrp, invFootGrp)
        
        cmds.parent (invFootGrp, footCntrl)
        cmds.group (self.name+'_ik'+self.nameList[1]+'_jnt', n=self.name+'_ikGrp')
        
        cond = cmds.createNode ('condition', n=self.name+'TipHeelCondition')
        cmds.setAttr (cond+'.operation', 2)
        cmds.setAttr (cond+'.colorIfFalseR', 0)
        cmds.addAttr (footCntrl, ln='TipHeel', at='double', k=True)
        cmds.connectAttr (footCntrl+'.TipHeel', cond+'.firstTerm')
        cmds.connectAttr (footCntrl+'.TipHeel', cond+'.colorIfTrueR')
        cmds.connectAttr (footCntrl+'.TipHeel', cond+'.colorIfFalseG')
        cmds.connectAttr (cond+'.outColorR', tipGrp+'.rotateX')
        cmds.connectAttr (cond+'.outColorG', heelGrp+'.rotateX')
        
        cond = cmds.createNode ('condition', n=self.name+'InOutCondition')
        cmds.setAttr (cond+'.operation', 2)
        cmds.setAttr (cond+'.colorIfFalseR', 0)
        cmds.addAttr (footCntrl, ln='InOut', at='double', k=True)
        cmds.connectAttr (footCntrl+'.InOut', cond+'.firstTerm')
        cmds.connectAttr (footCntrl+'.InOut', cond+'.colorIfTrueR')
        cmds.connectAttr (footCntrl+'.InOut', cond+'.colorIfFalseG')
        cmds.connectAttr (cond+'.outColorR', inGrp+'.rotateZ')
        cmds.connectAttr (cond+'.outColorG', outGrp+'.rotateZ')
                      
        cmds.addAttr (footCntrl, ln='Ball', at='double', k=True)
        cmds.connectAttr (footCntrl+'.Ball', ballGrp+'.rotateX')
        
        cmds.addAttr (footCntrl, ln='Toe', at='double', k=True)
        cmds.connectAttr (footCntrl+'.Toe', toeGrp+'.rotateX')
        
        cmds.addAttr (footCntrl, ln='stretchMulti', at='double', k=True)
        cmds.addAttr (footCntrl, ln='stretchBias', at='double', k=True)
              
        if connection:
            cmds.parent (connection[1], ballGrp)
            cmds.parent (self.name+'_ik'+self.nameList[1]+'_jnt', connection[0])
        
        self.ikGrp = self.name+'_ikGrp'

    def doSkinJoints (self):
        self.skinJoints = self.doSkeleton ('skin')
        if cmds.objExists (self.name+'_IKFK_Switch'):
            grp=self.name+'_IKFK_Switch' 
        else:
            grp=cmds.group (empty=True, n=self.name+'_IKFK_Switch')
        
        attrList = cmds.listAttr (grp, v=True, k=True)
        for attr in attrList:
            cmds.setAttr (grp+'.'+attr, k=0)
        
        cmds.addAttr (grp, ln='tp', dt='string', k=False)
        cmds.setAttr (grp+'.tp', 'foot',type='string')
        
        cmds.addAttr (grp, ln='from', at='message', k=False)
            
        cmds.addAttr (grp, ln='IKFK', at='double', k=True, min=0, max=1, dv=1)
        node=cmds.createNode ('reverse', n=self.name+'_IKFKrev')
        cmds.connectAttr (grp+'.IKFK', node+'.input.inputX')
        
        cmds.addAttr (grp, ln='ikCntrl', at='bool', k=False)
        cmds.addAttr (grp, ln='fkCntrl', at='bool', k=False)
        cmds.connectAttr (grp+'.fkCntrl', self.name+'_fk'+self.nameList[2]+'_grp.visibility')
        cmds.connectAttr (grp+'.ikCntrl', self.name+'_ik_grp.visibility')
        
        ikCond=cmds.createNode ('condition', n=self.name+'_ikVizCond')
        cmds.connectAttr (grp+'.IKFK', ikCond+'.firstTerm')
        cmds.setAttr (ikCond+'.secondTerm', 0)
        cmds.setAttr (ikCond+'.colorIfTrueR', 1)
        cmds.setAttr (ikCond+'.colorIfFalseR', 0)
        cmds.setAttr (ikCond+'.operation', 2)
        cmds.connectAttr (ikCond+'.outColor.outColorR', grp+'.ikCntrl')
        
        fkCond=cmds.createNode ('condition', n=self.name+'_fkVizCond')
        cmds.connectAttr (grp+'.IKFK', fkCond+'.firstTerm')
        cmds.setAttr (fkCond+'.secondTerm', 1)
        cmds.setAttr (fkCond+'.colorIfTrueR', 1)
        cmds.setAttr (fkCond+'.colorIfFalseR', 0)
        cmds.setAttr (fkCond+'.operation', 4)
        cmds.connectAttr (fkCond+'.outColor.outColorR', grp+'.fkCntrl')
        

        
        cmds.addAttr (grp, ln='ik0', at='message')
        cmds.connectAttr (self.name+'_ik_cntrl.message',grp+'.ik0')
        cmds.addAttr (grp, ln='fkJnt0', at='message')
        cmds.connectAttr (self.name+'_'+'fk'+self.nameList[0]+'_jnt.message',grp+'.fkJnt0')
        cmds.addAttr (grp, ln='fk0', at='message')
        cmds.connectAttr (self.name+'_'+'fk'+self.nameList[2]+'_cntrl.message',grp+'.fk0')
           
        for i in range (1,4):
            fkCnst=None
            ikCnst=None
            if cmds.objExists (self.name+'_fk'+self.nameList[i]+'_jnt'):
                fkCnst = cmds.orientConstraint (self.name+'_fk'+self.nameList[i]+'_jnt', self.name+'_skin'+self.nameList[i]+'_jnt')[0]
                
                cmds.addAttr (grp, ln='fkJnt'+str (i), at='message')
                cmds.connectAttr (self.name+'_'+'fk'+self.nameList[i]+'_jnt.message',grp+'.fkJnt'+str(i))              
                 
            if cmds.objExists (self.name+'_ik'+self.nameList[i]+'_jnt'):
                ikCnst = cmds.orientConstraint (self.name+'_ik'+self.nameList[i]+'_jnt', self.name+'_skin'+self.nameList[i]+'_jnt')[0]   
           
                cmds.addAttr (grp, ln='ikJnt'+str (i), at='message')
                cmds.connectAttr (self.name+'_'+'ik'+self.nameList[i]+'_jnt.message',grp+'.ikJnt'+str(i))
                           
            if fkCnst and ikCnst:
                cmds.connectAttr (grp+'.IKFK', ikCnst+'.'+self.name+'_ik'+self.nameList[i]+'_jntW1') 
                cmds.connectAttr (node+'.output.outputX',fkCnst+'.'+self.name+'_fk'+self.nameList[i]+'_jntW0')
        
        
        self.skinJntStart = self.name+'_skin'+self.nameList[1]+'_jnt'       
        self.skinJntEnd =  ''
                 


###############################################################################################
#
# SPINE
#
###############################################################################################
class Spine:
    def __init__ (self, name,nameList=[], guidePos=[], guideDict={}, cntrlList=[]):
        self.name = name
        self.skinJoints=[]
        if not nameList:
            self.nameList = ['Waist','Abdomen','Chest']
        else:
            self.nameList = nameList
          
        if not guideDict:
            self.guideDict = {self.nameList[0]:[[0,0,0],[0,0,0]],
                         self.nameList[1]: [[0,4,0],[0,0,0]], 
                         self.nameList[2]:[[0,8,0],[0,0,0]]}
        else:
            self.guideDict = guideDict
        
        if not guidePos:
            self.guidePos = [[0,0,0],[0,0,0]]
        else:
            self.guidePos = guidePos

        if not cntrlList:
            self.cntrlList = ['circuloX', 'circuloY', 'cubo']
        else:
            self.cntrlList = cntrlList
        self.eixo=1
    
    def saveGuide(self, filename):
        currentGuideDict={}
        for name in self.nameList:
            wt=cmds.xform (self.name+'_loc_'+name, wd=True, q=True, t=True)
            wr=cmds.xform (self.name+'_loc_'+name, wd=True, q=True, ro=True)
            ws=cmds.xform (self.name+'_loc_'+name,  q=True, s=True)
            currentGuideDict[name]=[wt, wr, ws]
        
        wt=cmds.xform (self.name+'_guide', wd=True, q=True, t=True)
        wr=cmds.xform (self.name+'_guide', wd=True, q=True, ro=True)
        ws=cmds.xform (self.name+'_guide', q=True, s=True)
        currentGuidePos=[wt, wr,ws]
        
        saveGuideDict={'nameList':self.nameList, 'guideDict':currentGuideDict, 'guidePos':currentGuidePos, 'cntrlList':self.cntrlList, 'eixo':self.eixo}
        with open(filename, 'wb') as f:
            pickle.dump(saveGuideDict, f)
        
    def loadGuide(self, filename):
        with open(filename, 'rb') as f:
            loadGuide = pickle.load(f)
        self.nameList=loadGuide['nameList']
        self.guideDict=loadGuide['guideDict']
        self.guidePos=loadGuide['guidePos']
        self.cntrlList=loadGuide['cntrlList']
        self.eixo=loadGuide['eixo']
        self.doGuide()
                   
    def doGuide(self):
        if cmds.objExists (self.name+'_guide'):
		    cmds.delete (self.name+'_guide', hi='below')
        
        guideGlobal = cmds.circle (n=self.name+'_guide', r=1.5, ch=True, o=True, nr=[1,0,0])[0]		
        if len (self.guidePos)==3:
			cmds.xform (guideGlobal, s = self.guidePos[2]) 
			       
        lineGrp= cmds.group (n=self.name+'Lines', empty=True)
        cmds.parent (lineGrp, guideGlobal)
        
        prev=''        
        for guide in  self.nameList:         
            loc = gen.doLocator (self.name+'_loc_'+guide,self.guideDict[guide][0],self.guideDict[guide][1])
            cmds.parent (loc, guideGlobal)
        
            if prev:
                line= gen.doLine (self.name+'_loc_'+prev, self.name+'_loc_'+ guide)
                cmds.parent (line,lineGrp)
            prev = guide
        
        cmds.move (self.guidePos[0][0], self.guidePos[0][1], self.guidePos[0][2], guideGlobal ,rpr =True)
        cmds.rotate (self.guidePos[1][0], self.guidePos[1][1], self.guidePos[1][2], guideGlobal)
        self.guideGlobal= guideGlobal

    def doMirrorGuide(self, eixo, local=False):
        source= self.guideGlobal
           
        if eixo=='-X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX+180)
            self.eixo = -1          
        elif eixo=='+X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX-180)
            self.eixo = 1             
        if not local:
            posicaoX= cmds.getAttr (source+'.translateX')
            cmds.setAttr (source+'.translateX', posicaoX*-1)
        
        rotacaoY= cmds.getAttr (source+'.rotateY')
        cmds.setAttr (source+'.rotateY', rotacaoY*-1)    
        rotacaoZ= cmds.getAttr (source+'.rotateZ')
        cmds.setAttr (source+'.rotateZ', rotacaoZ*-1) 
        
        childList  = cmds.listRelatives (source, allDescendents=True, fullPath=True, type='transform')          
        for child in childList:
            posicaoX = cmds.getAttr(child+'.translateX')
            cmds.setAttr(child+'.translateX', posicaoX*-1)
            posicaoY = cmds.getAttr (child+".translateY")
            cmds.setAttr (child+".translateY", posicaoY*-1)
            posicaoZ = cmds.getAttr (child+".translateZ")
            cmds.setAttr (child+".translateZ",posicaoZ*-1)      
        
    def doSkeleton(self, prefix='',drawStyle=0):
        allJoints=[]
        if cmds.objExists (self.name+'_'+prefix+self.nameList[0]+'_jnt'):
            cmds.delete (self.name+'_'+prefix+self.nameList[0]+'_jnt', hi='below')        
        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        
        for jntName in self.nameList:           
            jnt = gen.doJoint (self.name+'_'+prefix+jntName+'_jnt',self.name+'_loc_'+jntName )
            allJoints.append(jnt)
            cmds.setAttr (self.name+'_'+prefix+jntName+'_jnt.drawStyle', drawStyle)
            gen.alignObjs (self.name+'_loc_'+jntName, self.name+'_'+prefix+jntName+'_jnt', False)
        
        cmds.select (cl=True)
        if sele:
            cmds.select (sele)
        return allJoints

    def doCntrlFK(self):
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)
            
        self.doSkeleton('fk',2)
        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)

        prev =''
        for i in range (len(self.nameList)):     
            gen.createCntrl (self.name+'_'+'fk'+self.nameList[i],self.name+'_'+'fk'+self.nameList[i]+'_jnt',1, 'cubo', 1)           
            if prev:
                cmds.parent (self.name+'_'+'fk'+self.nameList[i]+'_grp', self.name+'_'+'fk'+prev+'_cntrl')
            prev = self.nameList[i]
            cmds.parentConstraint (self.name+'_'+'fk'+self.nameList[i]+'_cntrl', self.name+'_'+'fk'+self.nameList[i]+'_jnt', mo=True)
        
        cmds.group (self.name+'_'+'fk'+self.nameList[0]+'_grp', self.name+'_'+'fk'+self.nameList[0]+'_jnt', n=self.name+'_fkGrp')
        
        cmds.select (cl=True)
        
        if sele:
            cmds.select (sele)
        
        self.fkGrp = self.name+'_fkGrp'

    def doCntrlIK(self):
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)
        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
           
        self.doSkeleton('ik',2)
        
        grp = cmds.group (empty = True, n=self.name+'_ikGrp')
        cmds.parent (self.name+'_'+'ik'+self.nameList[0]+'_jnt', grp)
        
        for i in range (len(self.nameList)):     
            gen.createCntrl (self.name+'_'+'ik'+self.nameList[i],self.name+'_'+'ik'+self.nameList[i]+'_jnt',1, self.cntrlList[i], 1)
            cmds.parentConstraint (self.name+'_'+'ik'+self.nameList[i]+'_cntrl', self.name+'_'+'ik'+self.nameList[i]+'_jnt', mo=True)
        
        cmds.parent (self.name+'_'+'ik'+self.nameList[0]+'_grp', self.name+'_'+'ik'+self.nameList[1]+'_grp', grp)
        
        cmds.pointConstraint (self.name+'_'+'ik'+self.nameList[0]+'_cntrl', self.name+'_'+'ik'+self.nameList[2]+'_cntrl', self.name+'_'+'ik'+self.nameList[1]+'_grp')
                
        cmds.select (cl=True)
        if sele:
            cmds.select (sele)
        
        self.ikGrp = grp
        
    def doSkinJoints (self, doFlex = True):
        
        self.skinJoints = self.doSkeleton('skin')
        
        if cmds.objExists (self.name+'_IKFK_Switch'):
            grp=self.name+'_IKFK_Switch' 
        else:
            grp=cmds.group (empty=True, n=self.name+'_IKFK_Switch')
        
        attrList = cmds.listAttr (grp, v=True, k=True)
        for attr in attrList:
            cmds.setAttr (grp+'.'+attr, k=0)
        
        cmds.addAttr (grp, ln='tp', dt='string', k=False)
        cmds.setAttr (grp+'.tp', 'spine',type='string')
                
        cmds.addAttr (grp, ln='IKFK', at='double', k=True,min=0, max=1, dv=1)
        node=cmds.createNode ('reverse', n=self.name+'_IKFKrev')
        cmds.connectAttr (grp+'.IKFK', node+'.input.inputX')

        cmds.addAttr (grp, ln='ikCntrl', at='bool', k=False)
        cmds.addAttr (grp, ln='fkCntrl', at='bool', k=False)
        cmds.connectAttr (grp+'.fkCntrl', self.name+'_'+'fk'+self.nameList[0]+'_grp.visibility')
        for name in self.nameList:
            cmds.connectAttr (grp+'.ikCntrl', self.name+'_'+'ik'+name+'_grp.visibility')
           
        ikCond=cmds.createNode ('condition', n=self.name+'_ikVizCond')
        cmds.connectAttr (grp+'.IKFK', ikCond+'.firstTerm')
        cmds.setAttr (ikCond+'.secondTerm', 0)
        cmds.setAttr (ikCond+'.colorIfTrueR', 1)
        cmds.setAttr (ikCond+'.colorIfFalseR', 0)
        cmds.setAttr (ikCond+'.operation', 2)
        cmds.connectAttr (ikCond+'.outColor.outColorR', grp+'.ikCntrl')
        
        fkCond=cmds.createNode ('condition', n=self.name+'_fkVizCond')
        cmds.connectAttr (grp+'.IKFK', fkCond+'.firstTerm')
        cmds.setAttr (fkCond+'.secondTerm', 1)
        cmds.setAttr (fkCond+'.colorIfTrueR', 1)
        cmds.setAttr (fkCond+'.colorIfFalseR', 0)
        cmds.setAttr (fkCond+'.operation', 4)
        cmds.connectAttr (fkCond+'.outColor.outColorR', grp+'.fkCntrl')
        
       
        for i in range (len(self.nameList)):
            fkCnst=None
            ikCnst=None
            if cmds.objExists (self.name+'_'+'fk'+self.nameList[i]+'_jnt'):
                fkCnst = cmds.parentConstraint (self.name+'_'+'fk'+self.nameList[i]+'_jnt', self.name+'_'+'skin'+self.nameList[i]+'_jnt', mo=False)[0]
                
                cmds.addAttr (grp, ln='fkJnt'+str (i), at='message')
                cmds.connectAttr (self.name+'_'+'fk'+self.nameList[i]+'_jnt.message',grp+'.fkJnt'+str(i))
                
                cmds.addAttr (grp, ln='fk'+str(i), at='message')
                cmds.connectAttr (self.name+'_'+'fk'+self.nameList[i]+'_cntrl.message', grp+'.fk'+str(i))
                
            if cmds.objExists (self.name+'_'+'ik'+self.nameList[i]+'_jnt'):
                ikCnst = cmds.parentConstraint (self.name+'_'+'ik'+self.nameList[i]+'_jnt', self.name+'_'+'skin'+self.nameList[i]+'_jnt', mo=False)[0]
                
                cmds.addAttr (grp, ln='ikJnt'+str (i), at='message')
                cmds.connectAttr (self.name+'_'+'ik'+self.nameList[i]+'_jnt.message',grp+'.ikJnt'+str(i))
                
                cmds.addAttr (grp, ln='ik'+str(i), at='message')
                cmds.connectAttr (self.name+'_'+'ik'+self.nameList[i]+'_cntrl.message', grp+'.ik'+str(i))
                
            if fkCnst and ikCnst:
                cmds.connectAttr (grp+'.IKFK', ikCnst+'.'+self.name+'_'+'ik'+self.nameList[i]+'_jntW1') 
                cmds.connectAttr (node+'.output.outputX',fkCnst+'.'+self.name+'_'+'fk'+self.nameList[i]+'_jntW0')
                
                        
        returnList = [self.name+'_'+'skin'+self.nameList[0]+'_jnt', self.name+'_IKFK_Switch']
        
        if doFlex:
            cmds.addAttr (grp, ln='ribbonViz', at='bool', k=True)
            width = cmds.getAttr (self.name+'_skin'+self.nameList[1]+'_jnt.translateY')+cmds.getAttr (self.name+'_skin'+self.nameList[2]+'_jnt.translateY')
            flexSpine = flex.RibbonSpine(self.name+'_', width, 3, 'Y')
            
            gen.createCntrl (self.name+'_chestFlex',flexSpine.aux1,0.5,'circuloX',1)
            cmds.parentConstraint (self.name+'_chestFlex_cntrl',flexSpine.aux1, mo=False)
            
            gen.createCntrl (self.name+'_midFlex',self.name+'_aux3_cntrl',0.5,'circuloX',1)
            cmds.pointConstraint (self.name+'_midFlex_cntrl',self.name+'_aux3_cntrl')
            cns = cmds.orientConstraint (self.name+'_midFlex_cntrl',self.name+'_aux3_cntrl')[0]
            
            cmds.connectAttr (node+'.output.outputX',cns+'.'+self.name+'_midFlex_cntrlW0')
            
            gen.createCntrl (self.name+'_hipFlex',flexSpine.aux2,0.5,'circuloX',1)            
            cmds.parentConstraint (self.name+'_hipFlex_cntrl',flexSpine.aux2, mo=False)
            
            gen.alignObjs  (self.name+'_skin'+self.nameList[0]+'_jnt', self.name+'_hipFlex_grp' , True, False, False )
            cmds.parentConstraint (self.name+'_skin'+self.nameList[0]+'_jnt', self.name+'_hipFlex_grp' , mo=True)
            
            gen.alignObjs  (self.name+'_skin'+self.nameList[1]+'_jnt', self.name+'_midFlex_grp', True, False, False )
            cmds.parentConstraint (self.name+'_skin'+self.nameList[1]+'_jnt', self.name+'_midFlex_grp', mo=True)
            
            gen.alignObjs  (self.name+'_skin'+self.nameList[2]+'_jnt', self.name+'_chestFlex_grp', True, False, False )
            cmds.parentConstraint (self.name+'_skin'+self.nameList[2]+'_jnt', self.name+'_chestFlex_grp',  mo=True)
            
            cmds.connectAttr (grp+'.ribbonViz', self.name+'_chestFlex_grp.visibility') 
            cmds.connectAttr (grp+'.ribbonViz', self.name+'_midFlex_grp.visibility') 
            cmds.connectAttr (grp+'.ribbonViz', self.name+'_hipFlex_grp.visibility')   
            
            cmds.parent (flexSpine .cntrlGrp, self.name+'_'+'skin'+self.nameList[0]+'_jnt')
            
            if cmds.objExists(self.name+'_ikGrp'):
               cmds.parent (self.name+'_hipFlex_grp', self.name+'_midFlex_grp', self.name+'_chestFlex_grp', self.name+'_ikGrp')
            
            x=self.skinJoints[-1]
            self.skinJoints=flexSpine.skinJoints
            self.skinJoints.append(x)
            
            cntrlList =[[self.name+'_hipFlex_grp', self.name+'_midFlex_grp', self.name+'_chestFlex_grp'],[self.name+'_'+self.nameList[0]+'Flex_grp',self.name+'_'+self.nameList[1]+'Flex_grp']]
            returnList= returnList+cntrlList                        
        
        self.skinJntStart = self.name+'_'+'skin'+self.nameList[0]+'_jnt'      
        self.skinJntEnd =  self.name+'_'+'skin'+self.nameList[2]+'_jnt'      

###########################################################################################
#
#Chain
#
###########################################################################################
class Chain:
    def __init__ (self, name, nameList=[], guidePos=[], guideDict={}, cntrlList=[]):
        self.name= name
        self.skinJoints=[]
        if not nameList:
            self.nameList = ['jointA']
        else:
            self.nameList = nameList
        
        if not guidePos:
            self.guidePos = [[0,0,0],[0,0,0]]
        else:
            self.guidePos = guidePos
        
        if not guideDict:
            count= 0
            self.guideDict={}
            for name in self.nameList:
                self.guideDict[name] = [[count, 0, 0],[0,0,0]]
                count=count+1.5
        else:
            self.guideDict=guideDict
                    
        if not cntrlList:
            self.cntrlList=[] 
            for name in self.nameList:
                self.cntrlList.append ('cubo')
        else:
            self.cntrlList = cntrlList  
        
        self.eixo=1
        
    def saveGuide(self, filename):
        currentGuideDict={}
        for name in self.nameList:
            wt=cmds.xform (self.name+'_loc_'+name, wd=True, q=True, t=True)
            wr=cmds.xform (self.name+'_loc_'+name, wd=True, q=True, ro=True)
            currentGuideDict[name]=[wt, wr]
        
        wt=cmds.xform (self.name+'_guide', wd=True, q=True, t=True)
        wr=cmds.xform (self.name+'_guide', wd=True, q=True, ro=True)
        currentGuidePos=[wt, wr]
        
        saveGuideDict={'nameList':self.nameList, 'guideDict':currentGuideDict, 'guidePos':currentGuidePos, 'cntrlList':self.cntrlList, 'eixo':self.eixo}
        with open(filename, 'wb') as f:
            pickle.dump(saveGuideDict, f)
        
    def loadGuide(self, filename):
        with open(filename, 'rb') as f:
            loadGuide = pickle.load(f)
        self.nameList=loadGuide['nameList']
        self.guideDict=loadGuide['guideDict']
        self.guidePos=loadGuide['guidePos']
        self.cntrlList=loadGuide['cntrlList']
        self.eixo=loadGuide['eixo']
        self.doGuide()
                   
    def doGuide (self):
        if cmds.objExists (self.name+'_guide'):
		    cmds.delete (self.name+'_guide', hi='below')
        
        guideGlobal = cmds.circle (n=self.name+'_guide', r=1.5, ch=True, o=True, nr=[1,0,0])[0]		
          
        for guide in  self.nameList:         
            loc = gen.doLocator (self.name+'_loc_'+guide,self.guideDict[guide][0], self.guideDict[guide][1], 0.2)
            cmds.parent (loc, guideGlobal)

        cmds.move (self.guidePos[0][0], self.guidePos[0][1], self.guidePos[0][2], guideGlobal ,rpr =True)
        cmds.rotate (self.guidePos[1][0], self.guidePos[1][1], self.guidePos[1][2], guideGlobal)            
        
        self.guideGlobal= guideGlobal

    def doMirrorGuide(self, eixo, local=False):
        source= self.guideGlobal
           
        if eixo=='-X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX+180)
            self.eixo = -1          
        elif eixo=='+X':
            rotacaoX=cmds.getAttr(source+'.rotateX')
            cmds.setAttr (source+'.rotateX', rotacaoX-180)
            self.eixo = 1             
        if not local:
            posicaoX= cmds.getAttr (source+'.translateX')
            cmds.setAttr (source+'.translateX', posicaoX*-1)
        
        rotacaoY= cmds.getAttr (source+'.rotateY')
        cmds.setAttr (source+'.rotateY', rotacaoY*-1)    
        rotacaoZ= cmds.getAttr (source+'.rotateZ')
        cmds.setAttr (source+'.rotateZ', rotacaoZ*-1) 
        
        childList  = cmds.listRelatives (source, allDescendents=True, fullPath=True, type='transform')          
        for child in childList:
            posicaoX = cmds.getAttr(child+'.translateX')
            cmds.setAttr(child+'.translateX', posicaoX*-1)
            posicaoY = cmds.getAttr (child+".translateY")
            cmds.setAttr (child+".translateY", posicaoY*-1)
            posicaoZ = cmds.getAttr (child+".translateZ")
            cmds.setAttr (child+".translateZ",posicaoZ*-1)




                           
    def doSkeleton (self, prefix='', drawStyle=0):
        allJoints=[]    
        if cmds.objExists (self.name+'_'+prefix+self.nameList[0]+'_jnt'):
            cmds.delete (self.name+'_'+prefix+self.nameList[0]+'_jnt', hi='below')        
        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)
        
        for jntName in self.nameList:           
            jnt =gen.doJoint (self.name+'_'+prefix+jntName+'_jnt',self.name+'_loc_'+jntName )
            allJoints.append(jnt)
            cmds.setAttr (self.name+'_'+prefix+jntName+'_jnt.drawStyle', drawStyle)
            gen.alignObjs (self.name+'_loc_'+jntName, self.name+'_'+prefix+jntName+'_jnt', False)
            
        cmds.select (cl=True)
        if sele:
            cmds.select (sele)        
        return allJoints

    def doCntrlFK(self):                
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)            
        
        self.doSkeleton('fk',2)        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)         
        
        prev=''
        for i,name in enumerate (self.nameList):   
            cntrl= gen.createCntrl (self.name+'_'+'fk'+name,self.name+'_'+'fk'+name+'_jnt',1, self.cntrlList[i],1)  
            cmds.parentConstraint (cntrl, self.name+'_'+'fk'+name+'_jnt', mo=False)
            if prev:
                cmds.parent (self.name+'_'+'fk'+name+'_grp',prev)
            prev=cntrl
            
        cmds.group (self.name+'_'+'fk'+self.nameList[0]+'_jnt', self.name+'_'+'fk'+self.nameList[0]+'_grp', n=self.name+'_fkGrp')
        self.fkGrp = self.name+'_fkGrp'
                   
    def doSkinJoints(self, doFlex=False):
        self.skinJoints = self.doSkeleton('skin')        
        for name in self.nameList:
            fkCnst=None
            ikCnst=None
            if cmds.objExists (self.name+'_fk'+name+'_jnt'):
                fkCnst = cmds.parentConstraint (self.name+'_fk'+name+'_jnt', self.name+'_skin'+name+'_jnt')[0]   
            if cmds.objExists (self.name+'_ik'+name+'_jnt'):
                ikCnst = cmds.parentConstraint (self.name+'_ik'+name+'_jnt', self.name+'_skin'+name+'_jnt')[0]   
            if fkCnst and ikCnst:
                cmds.connectAttr (grp+'.IKFK', ikCnst+'.'+self.name+'_ik'+name+'_jntW1') 
                cmds.connectAttr (node+'.output.outputX',fkCnst+'.'+self.name+'_fk'+name+'_jntW0')         
        
        self.skinJntStart = self.name+'_'+'skin'+self.nameList[0]+'_jnt'    
        self.skinJntEnd =  self.name+'_'+'skin'+self.nameList[-1]+'_jnt'                 

###########################################################################################
#
#NECK
#
###########################################################################################
class Neck(Chain):    
    def __init__ (self, name, nameList=[], guidePos=[], guideDict={}, cntrlList=[]):
        self.name= name
        
        if not nameList:
            self.nameList = ['neck','head']
        else:
            self.nameList = nameList
        
        if not guidePos:
            self.guidePos = [[0,0,0],[0,0,0]]
        else:
            self.guidePos = guidePos
        
        if not guideDict:
            count= 0
            self.guideDict={}
            for name in self.nameList:
                self.guideDict[name] = [[count, 0, 0],[0,0,0]]
                count=count+1.5
        else:
            self.guideDict=guideDict
                    
        if not cntrlList:
            self.cntrlList=[] 
            for name in self.nameList:
                self.cntrlList.append ('circuloX')
        else:
            self.cntrlList = cntrlList  
    
        self.eixo=1
    
    def doCntrlFK(self):                
        if cmds.getAttr (self.name+'_guide.visibility'):
            cmds.setAttr (self.name+'_guide.visibility', False)            
        
        self.doSkeleton('fk',2)        
        sele = cmds.ls (sl=True)
        cmds.select (cl=True)         
        
        for i,name in enumerate (self.nameList):   
            cntrl= gen.createCntrl (self.name+'_'+'fk'+name,self.name+'_'+'fk'+name+'_jnt',1, self.cntrlList[i],1)  
            cmds.parentConstraint (cntrl, self.name+'_'+'fk'+name+'_jnt', mo=False)
  
        cmds.group (self.name+'_'+'fk'+self.nameList[0]+'_jnt', self.name+'_'+'fk'+self.nameList[0]+'_grp', n=self.name+'_fkGrp')
        self.fkGrp = self.name+'_fkGrp'
        
    def doSkinJoints(self, doFlex=False):
        self.skinJoints = self.doSkeleton('skin')       
      
        for name in self.nameList:
            fkCnst=None
            ikCnst=None
            if cmds.objExists (self.name+'_fk'+name+'_jnt'):
                fkCnst = cmds.parentConstraint (self.name+'_fk'+name+'_jnt', self.name+'_skin'+name+'_jnt')[0]   
            if cmds.objExists (self.name+'_ik'+name+'_jnt'):
                ikCnst = cmds.parentConstraint (self.name+'_ik'+name+'_jnt', self.name+'_skin'+name+'_jnt')[0]   
            if fkCnst and ikCnst:
                cmds.connectAttr (grp+'.IKFK', ikCnst+'.'+self.name+'_ik'+name+'_jntW1') 
                cmds.connectAttr (node+'.output.outputX',fkCnst+'.'+self.name+'_fk'+name+'_jntW0')  
                
        if cmds.objExists (self.name+'_IKFK_Switch'):
            grp=self.name+'_IKFK_Switch' 
        else:
            grp=cmds.group (empty=True, n=self.name+'_IKFK_Switch')
        
        attrList = cmds.listAttr (grp, v=True, k=True)
        for attr in attrList:
            cmds.setAttr (grp+'.'+attr, k=0)      
        
        cmds.addAttr (grp, ln='tp', dt='string', k=False)
        cmds.setAttr (grp+'.tp', 'neck',type='string')
        
        if doFlex:
            cmds.addAttr (grp, ln='ribbonViz', at='bool', k=True)
            width = cmds.getAttr (   self.name+'_skin'+self.nameList[1]+'_jnt.translateX' )              
            flexBraco = flex.RibbonNeck(self.name+'_'+self.nameList[0]+'_',width, 3, 'X')
            
            cmds.parent (flexBraco.flexName+'Cntrl_grp',  self.name+'_skin'+self.nameList[0]+'_jnt')
            
            gen.createCntrl (self.name+'_'+self.nameList[0]+'_midFlex',self.name+'_'+self.nameList[0]+'_aux3_cntrl',0.5,'bola',1)
            cmds.parentConstraint (self.name+'_'+self.nameList[0]+'_midFlex_cntrl',self.name+'_'+self.nameList[0]+'_aux3_cntrl', mo=False)

            cmds.pointConstraint (flexBraco.aux1, flexBraco.aux2 , self.name+'_'+self.nameList[0]+'_midFlex_grp')
            
            cmds.parentConstraint (self.name+'_skin'+self.nameList[0]+'_jnt' , flexBraco.aux1 ) 
            cmds.parentConstraint (self.name+'_skin'+self.nameList[1]+'_jnt' , flexBraco.aux2 )
            
            cmds.connectAttr (grp+'.ribbonViz', self.name+'_'+self.nameList[0]+'_midFlex_grp.visibility') 
            
            cmds.parent (self.name+'_'+self.nameList[0]+'_midFlex_grp', self.name+'_fkGrp')
            x = self.skinJoints[-1]
            self.skinJoints=flexBraco.skinJoints
            self.skinJoints.append(x)
            
        self.skinJntStart = self.name+'_'+'skin'+self.nameList[0]+'_jnt'    
        self.skinJntEnd =  self.name+'_'+'skin'+self.nameList[1]+'_jnt'

###########################################################################################
#
#Biped
#
###########################################################################################                
class Rig:
    def __init__(self, name):
        self.name =name
        self.skinJoints=[]
        self.listObjs =[]

    def createSpc (self, driver, name):
        drvGrp = cmds.group (empty=True, n=self.name+'_'+name+'_drv')
        if driver:
            cmds.parentConstraint (driver, drvGrp)
        spcGrp = cmds.group (empty=True, n=self.name+'_'+name+'_spc')
        cmds.parent (spcGrp, drvGrp)
        
    def addSpc (self, target, space, type):       
        switcher = cmds.listRelatives (cmds.listRelatives (target, p=True)[0], p=True)[0]
        
        if type=='parent':
            cns = cmds.parentConstraint (self.name+'_'+space+'_spc', switcher, mo=True)[0]
        elif type=='orient':
            cns =  cmds.orientConstraint (self.name+'_'+space+'_spc', switcher)[0]
        
        if cmds.attributeQuery ('spcSwitch', node=target, exists = True):
            enumTxt = cmds.attributeQuery ('spcSwitch', node=target, le = True)[0]
            connects = cmds.listConnections (target+'.spcSwitch', d=True, s=False, p=True)
            index = len (enumTxt.split (':'))
            enumTxt = enumTxt+':'+space
            cmds.deleteAttr (target, at = 'spcSwitch')
            cmds.addAttr ( target, ln='spcSwitch', at='enum', en=enumTxt, k=True)
            if connects:
                for c in connects:
                    cmds.connectAttr (target+'.spcSwitch', c)
        else:
            cmds.addAttr ( target, ln='spcSwitch', at='enum', en=space, k=True)
            index=0
            
        cond = cmds.createNode ('condition', n=self.name+switcher+space+'Cond')
        cmds.connectAttr (target+'.spcSwitch', cond+'.firstTerm')
        cmds.setAttr (cond+'.secondTerm', index)
        cmds.setAttr (cond+'.operation', 0)
        cmds.setAttr (cond+'.colorIfTrueR', 1)
        cmds.setAttr (cond+'.colorIfFalseR', 0)     
        cmds.connectAttr (cond+'.outColor.outColorR', cns+'.'+self.name+'_'+space+'_spcW'+str(index))


class Biped:   
    def __init__(self, name):
        self.name =name
        self.skinJoints=[]
        self.listObjs =[]
    
    def doGuide(self):
		
        if cmds.objExists (self.name+'_guideGrp'):
            cmds.delete (self.name+'_guideGrp', hi='below')		
        

        self.LArm=Limb ('L_Arm', ['Shoulder', 'Elbow', 'Wrist'], [[2,23,0], [0,0,0]], {'Shoulder':[[0,0,0],[90,0,0]],'Elbow': [[4,0,-0.1],[90,0,0]],'Wrist':[[8, 0, 0],[90,0,0]]}, ['cubo', 'cubo', 'cubo'] )
        self.LLeg=Limb ('L_Leg', ['Thig', 'Knee', 'Foot'], [[2,15,0], [180,0,-90]], {'Thig':[[0,0,0],[90,0,0]],'Knee': [[6.5,0,-0.1],[90,0,0]],'Foot':[[13.35, 0, 0],[90,0,0]]}, ['cubo', 'cubo', 'cubo'] )
        self.LHand =Hand('L_Hand',5, 5,['Thumb','Index','Middle','Ring','Pink'],[[10,23,0],[0,0,0]],{'Thumb':[[.82,-0.56,1.07],[85,-29,-23]] ,'Index':[[1.75,0,0.96],[0,0,0]],'Middle':[[1.75,0.221,0.206],[0,0,0]],'Ring':[[1.75,-0.064,-1.16],[0,0,0]],'Pink':[[1.75,-0.064,-2.16],[0,0,0]]}, True)
        self.LFoot =Foot('L_Foot',0,0, ['Heel','Ankle','Ball','Toe','In','Out'], [[2,1.635,0],[0,0,0]])
        #self.LFoot =Foot('L_Foot',5,3, ['Heel','Ankle','Ball','Toe','In','Out','Thumb','Index','Middle','Ring','Pink'], [[2,1.635,0],[0,0,0]])
        
        self.LClav =Chain ('L_Clav', ['Clav'], [[0.5, 23.264, 0.5], [90,0,0]], {}, ['ponteiroZ'])
        self.COG = Chain ('COG', ['COG'], [[0, 16, 0], [0,0,0]], {}, ['cubo']) 
        self.Hip = Chain ('Hip', ['Hip'], [[0, 16, 0], [0,0,0]], {}, ['cubo'])
        self.LAuxHip = Chain ('L_AuxHip', ['AuxHip'], [[1, 16, 0], [0,0,0]], {}, ['cubo'])
        self.Neck= Neck ('Neck', ['Neck','Head'], [[0, 23.8, 0], [0,0,90]], {}, ['ponteiroY', 'cubo'])
        self.MSpine= Spine ('MSpine',['Waist', 'Abdomen', 'Chest'], [[0,16,0],[0,0,0]], {'Waist':[[0,0,0],[0,0,0]],'Abdomen': [[0,2.5,0],[0,0,0]], 'Chest':[[0,5,0],[0,0,0]]})
        
        
        self.LArm.doGuide()
        self.LLeg.doGuide()   
        self.LHand.doGuide()
        self.LFoot.doGuide()
        self.LClav.doGuide()            
        self.COG.doGuide()
        self.Hip.doGuide()
        self.LAuxHip.doGuide()
        self.Neck.doGuide()
        self.MSpine.doGuide()  
        self.RArm = gen.copyMirror (self.LArm,'-X', 'L_', 'R_')
        self.RLeg= gen.copyMirror (self.LLeg,'-X', 'L_', 'R_')
        self.RClav= gen.copyMirror (self.LClav,'-X', 'L_', 'R_')
        self.RHand= gen.copyMirror (self.LHand,'-X', 'L_', 'R_')
        self.RFoot= gen.copyMirror (self.LFoot,'-X', 'L_', 'R_')
        self.RAuxHip= gen.copyMirror (self.LAuxHip,'-X', 'L_', 'R_')

        self.listObjs = [self.LArm, self.LLeg, self.LHand, self.LFoot, self.LClav, self.COG,self.Hip, self.LAuxHip, self.Neck, self.MSpine, self.RArm, self.RLeg , self.RClav, self.RHand, self.RFoot, self.RAuxHip]
        
        gd= cmds.ls ('*_guide', assemblies=True)
        cmds.group (gd, n=self.name+'_guideGrp')
        
        self.guideGlobal= self.name+'_Global_guide'

    def doLeftMirrorGuide(self):
        self.RArm = gen.copyMirror (self.LArm,'-X', 'L_', 'R_')
        self.RLeg= gen.copyMirror (self.LLeg,'-X', 'L_', 'R_')
        self.RClav= gen.copyMirror (self.LClav,'-X', 'L_', 'R_')
        self.RHand= gen.copyMirror (self.LHand,'-X', 'L_', 'R_')
        self.RFoot= gen.copyMirror (self.LFoot,'-X', 'L_', 'R_')
        self.RAuxHip=gen.copyMirror (self.LAuxHip,'-X', 'L_', 'R_')
		
    def doRightMirrorGuide(self):
        self.LArm = gen.copyMirror (self.RArm,'+X', 'R_', 'L_')
        self.LLeg= gen.copyMirror (self.RLeg,'+X', 'R_', 'L_')
        self.LClav= gen.copyMirror (self.RClav,'+X',  'R_', 'L_')
        self.LHand= gen.copyMirror (self.RHand,'+X','R_', 'L_')
        self.LFoot= gen.copyMirror (self.RFoot,'+X', 'R_', 'L_')
        self.LAuxHip= gen.copyMirror (self.RAuxHip,'+X', 'R_', 'L_')
    
    
    def saveAllGuides(self, filenameGuide):
        self.LArm.saveGuide(os.path.join(filenameGuide, self.LArm.name+'.guide'))
        self.LLeg.saveGuide(os.path.join(filenameGuide, self.LLeg.name+'.guide'))   
        self.LHand.saveGuide(os.path.join (filenameGuide, self.LHand.name+'.guide'))
        self.LFoot.saveGuide(os.path.join(filenameGuide, self.LFoot.name+'.guide'))
        self.LClav.saveGuide(os.path.join(filenameGuide, self.LClav.name+'.guide'))          
        self.COG.saveGuide(os.path.join (filenameGuide, self.COG.name+'.guide'))
        self.Hip.saveGuide(os.path.join(filenameGuide, self.Hip.name+'.guide'))
        self.Neck.saveGuide(os.path.join (filenameGuide, self.Neck.name+'.guide'))
        self.MSpine.saveGuide(os.path.join(filenameGuide, self.MSpine.name+'.guide'))
        
        self.RArm.saveGuide(os.path.join (filenameGuide, self.RArm.name+'.guide'))
        self.RLeg.saveGuide(os.path.join (filenameGuide, self.RLeg.name+'.guide'))   
        self.RHand.saveGuide(os.path.join (filenameGuide, self.RHand.name+'.guide'))
        self.RFoot.saveGuide(os.path.join (filenameGuide, self.RFoot.name+'.guide'))
        self.RClav.saveGuide(os.path.join (filenameGuide, self.RClav.name+'.guide'))          
        self.LAuxHip.saveGuide(os.path.join (filenameGuide, self.LAuxHip.name+'.guide'))
        self.RAuxHip.saveGuide(os.path.join (filenameGuide, self.RAuxHip.name+'.guide'))
		
		
    def loadAllGuides(self, filenameGuide):
        self.LArm.loadGuide(os.path.join (filenameGuide, self.LArm.name+'.guide'))
        self.LLeg.loadGuide(os.path.join (filenameGuide, self.LLeg.name+'.guide'))   
        self.LHand.loadGuide(os.path.join (filenameGuide, self.LHand.name+'.guide'))
        self.LFoot.loadGuide(os.path.join (filenameGuide, self.LFoot.name+'.guide'))
        self.LClav.loadGuide(os.path.join (filenameGuide, self.LClav.name+'.guide'))          
        self.COG.loadGuide(os.path.join (filenameGuide, self.COG.name+'.guide'))
        self.Hip.loadGuide(os.path.join (filenameGuide, self.Hip.name+'.guide'))
        self.Neck.loadGuide(os.path.join (filenameGuide, self.Neck.name+'.guide'))
        self.MSpine.loadGuide(os.path.join (filenameGuide, self.MSpine.name+'.guide'))
        
        self.RArm.loadGuide(os.path.join (filenameGuide, self.RArm.name+'.guide'))
        self.RLeg.loadGuide(os.path.join (filenameGuide, self.RLeg.name+'.guide'))   
        self.RHand.loadGuide(os.path.join (filenameGuide, self.RHand.name+'.guide'))
        self.RFoot.loadGuide(os.path.join (filenameGuide, self.RFoot.name+'.guide'))
        self.RClav.loadGuide(os.path.join (filenameGuide, self.RClav.name+'.guide'))  
        self.LAuxHip.loadGuide(os.path.join (filenameGuide, self.LAuxHip.name+'.guide'))
        self.RAuxHip.loadGuide(os.path.join (filenameGuide, self.RAuxHip.name+'.guide'))
		
		        
    def doRig(self):
        if cmds.objExists (self.name+'_Global_grp'):
            cmds.delete (self.name+'_Global_grp', hi='below')	
                    
        grp = cmds.group (empty=True, n=self.name+'_Global_grp')
        glbCntrl  = cmds.circle (n=self.name+'_Global_cntrl', r=10, ch=True, o=True, nr=[0,1,0])[0]
        cmds.parent (glbCntrl, grp)
			   
        self.Neck.doCntrlFK()
        self.Hip.doCntrlFK()
        self.COG.doCntrlFK()
        self.MSpine.doCntrlFK()
        
        self.LAuxHip.doCntrlFK()
        self.RAuxHip.doCntrlFK()
        
        self.LClav.doCntrlFK()
        self.RClav.doCntrlFK()
        
        self.LArm.doCntrlFK()
        self.RArm.doCntrlFK()
        
        self.LHand.doCntrlFK()
        self.RHand.doCntrlFK()
         
        self.LLeg.doCntrlFK()
        self.RLeg.doCntrlFK()
        
        self.RFoot.doCntrlFK()
        self.LFoot.doCntrlFK()
        
        self.MSpine.doCntrlIK()
        
        self.LClav.doSkinJoints()
        self.RClav.doSkinJoints()
        
        self.LAuxHip.doSkinJoints()
        self.RAuxHip.doSkinJoints()
        	  
        self.LArm.doCntrlIK()        
        self.RArm.doCntrlIK()
        
        self.LLeg.doCntrlIK()
        self.RLeg.doCntrlIK()
        
        self.RFoot.doCntrlIK()
        self.LFoot.doCntrlIK()
        
        self.MSpine.doSkinJoints()
        self.Neck.doSkinJoints(True)
        self.COG.doSkinJoints()
        self.Hip.doSkinJoints()
        
        self.LArm.doSkinJoints(True)
        self.RArm.doSkinJoints(True)
        
        self.LLeg.doSkinJoints(True)
        self.RLeg.doSkinJoints(True)
        
        self.RFoot.doSkinJoints()
        self.LFoot.doSkinJoints()
        self.skinJoints=self.skinJoints + self.RAuxHip.skinJoints +self.LAuxHip.skinJoints +self.LFoot.skinJoints+self.RFoot.skinJoints+self.RLeg.skinJoints+self.LLeg.skinJoints+self.RArm.skinJoints+self.LArm.skinJoints+self.LClav.skinJoints+self.RClav.skinJoints+self.MSpine.skinJoints+self.Neck.skinJoints+self.Hip.skinJoints+self.LHand.skinJoints+self.LHand.skinJoints+self.RHand.skinJoints
        
        cmds.parentConstraint (self.COG.skinJntEnd, self.Hip.fkGrp, mo=True)
        
        cmds.parentConstraint (self.Hip.skinJntEnd, self.LAuxHip.fkGrp, mo=True)
        cmds.parentConstraint (self.Hip.skinJntEnd, self.RAuxHip.fkGrp, mo=True)
        		
        cmds.parent (self.MSpine.skinJntStart,self.COG.skinJntEnd)
        cmds.parentConstraint (self.COG.skinJntEnd, self.MSpine.fkGrp, mo=True)
        cmds.parentConstraint (self.COG.skinJntEnd, self.MSpine.ikGrp, mo=True)       
        cmds.parent (self.LClav.skinJntStart, self.RClav.skinJntStart, self.Neck.skinJntStart, self.MSpine.skinJntEnd)
        cmds.parentConstraint (self.MSpine.skinJntEnd, self.LClav.fkGrp, mo=True)
        cmds.parentConstraint (self.MSpine.skinJntEnd, self.RClav.fkGrp, mo=True)
        cmds.parentConstraint (self.MSpine.skinJntEnd, self.Neck.fkGrp, mo=True)
        cmds.parent (self.LArm.skinJntStart, self.LClav.skinJntEnd)                
        cmds.parentConstraint (self.LClav.skinJntEnd, self.LArm.fkGrp, mo=True)
        cmds.parentConstraint (self.LClav.skinJntEnd, self.LArm.ikGrp, mo=True)        
        cmds.parent (self.RArm.skinJntStart, self.RClav.skinJntEnd)
        cmds.parentConstraint (self.RClav.skinJntEnd, self.RArm.fkGrp, mo=True)
        cmds.parentConstraint (self.RClav.skinJntEnd, self.RArm.ikGrp, mo=True)               
        
        cmds.parentConstraint (self.LClav.skinJntEnd , self.LArm.name+'_'+self.LArm.nameList[0]+'aux2_cntrl', mo=True )       
        cmds.parentConstraint (self.RClav.skinJntEnd , self.RArm.name+'_'+self.RArm.nameList[0]+'aux2_cntrl', mo=True)
         
        cmds.parent (self.LHand.skinJntStart, self.LArm.skinJntEnd) 
        cmds.parent (self.RHand.skinJntStart, self.RArm.skinJntEnd)       
        cmds.parent (self.LLeg.skinJntStart, self.LAuxHip.skinJntEnd)
        cmds.parent (self.RLeg.skinJntStart, self.RAuxHip.skinJntEnd)
        
        cmds.parentConstraint (self.LAuxHip.skinJntEnd , self.LLeg.name+'_'+self.LLeg.nameList[0]+'aux2_cntrl', mo=True  )          
        cmds.parentConstraint (self.RAuxHip.skinJntEnd , self.RLeg.name+'_'+self.RLeg.nameList[0]+'aux2_cntrl', mo=True )
        
        cmds.parentConstraint (self.LAuxHip.skinJntEnd, self.LLeg.ikGrp, mo=True)
        cmds.parentConstraint (self.LAuxHip.skinJntEnd, self.LLeg.fkGrp, mo=True)
        cmds.parentConstraint (self.RAuxHip.skinJntEnd , self.RLeg.ikGrp, mo=True)
        cmds.parentConstraint (self.RAuxHip.skinJntEnd , self.RLeg.fkGrp, mo=True)      
        cmds.parent (self.LFoot.skinJntStart, self.LLeg.skinJntEnd)
        cmds.parentConstraint (self.LLeg.skinJntEnd, self.LFoot.fkGrp, mo=True)
        cmds.parentConstraint (self.LLeg.skinJntEnd, self.LFoot.ikGrp, mo=True)
        cmds.parent (self.LLeg.name + '_ik'+ self.LLeg.nameList[2]+'_grp', self.LFoot.name+'_BallRot_grp')
        cmds.setAttr ( self.LFoot.name+'_BallRot_grp.visibility', 0)              
        cmds.parent (self.RFoot.skinJntStart, self.RLeg.skinJntEnd)
        cmds.parentConstraint (self.RLeg.skinJntEnd, self.RFoot.fkGrp, mo=True)
        cmds.parentConstraint (self.RLeg.skinJntEnd, self.RFoot.ikGrp, mo=True)
        cmds.connectAttr (self.LFoot.name+'_ik_cntrl.stretchMulti', self.LLeg.name + '_ik'+ self.LLeg.nameList[2]+'_cntrl.stretchMulti')
        cmds.connectAttr (self.RFoot.name+'_ik_cntrl.stretchBias', self.RLeg.name + '_ik'+ self.RLeg.nameList[2]+'_cntrl.stretchBias')
        cmds.connectAttr (self.RFoot.name+'_ik_cntrl.stretchMulti', self.RLeg.name + '_ik'+ self.RLeg.nameList[2]+'_cntrl.stretchMulti')
        cmds.connectAttr (self.LFoot.name+'_ik_cntrl.stretchBias', self.LLeg.name + '_ik'+ self.LLeg.nameList[2]+'_cntrl.stretchBias')
        
        cmds.connectAttr (self.RFoot.name+'_IKFK_Switch.message',self.RLeg.name+'_IKFK_Switch.to')
        cmds.connectAttr (self.LFoot.name+'_IKFK_Switch.message',self.LLeg.name+'_IKFK_Switch.to')
        cmds.connectAttr (self.RLeg.name+'_IKFK_Switch.message',self.RFoot.name+'_IKFK_Switch.from')
        cmds.connectAttr (self.LLeg.name+'_IKFK_Switch.message',self.LFoot.name+'_IKFK_Switch.from')
        
        cmds.connectAttr (self.RLeg.name+'_IKFK_Switch.IKFK', self.RFoot.name+'_IKFK_Switch.IKFK')
        cmds.connectAttr (self.LLeg.name+'_IKFK_Switch.IKFK', self.LFoot.name+'_IKFK_Switch.IKFK')
        
        cmds.parent (self.RLeg.name + '_ik'+ self.RLeg.nameList[2]+'_grp', self.RFoot.name+'_BallRot_grp')
        cmds.setAttr ( self.RFoot.name+'_BallRot_grp.visibility', 0)
        
        cmds.parentConstraint (self.RLeg.skinJntEnd, self.RFoot.ikGrp, mo=True)
        
        fk = cmds.ls ('*fkGrp', assemblies=True)
        fkGrp = cmds.group (fk, n=self.name+'_fkCntrlsGrp')
        ik= cmds.ls ('*ikGrp', assemblies=True)
        ikGrp = cmds.group (ik, n=self.name+'_ikCntrlsGrp')
        cmds.parent (self.LFoot.name+'_ik_grp', self.RFoot.name+'_ik_grp', ikGrp)
        sw= cmds.ls ('*_Switch', assemblies=True)
        swGrp = cmds.group (sw, n=self.name+'_switchGrp')
        rb= cmds.ls ('*Ribbon_grp', assemblies=True)
        rbGrp = cmds.group (rb, n=self.name+'_ribbonGrp')
        jt= cmds.ls ('*_jnt', assemblies=True)
        jtGrp = cmds.group (jt, n=self.name+'_jntGrp')
        
        g = cmds.group (empty=True, n=self.LArm.name+'_spcSwitcher')
        cmds.parent (g, ikGrp)
        cmds.parent (self.LArm.name+'_ik'+self.LArm.nameList[2]+'_grp', self.LArm.name+'_spcSwitcher')        
        g=cmds.group (empty=True, n=self.RArm.name+'_spcSwitcher')
        cmds.parent (g, ikGrp)
        cmds.parent (self.RArm.name+'_ik'+self.RArm.nameList[2]+'_grp', self.RArm.name+'_spcSwitcher')       
        g=cmds.group (empty=True, n=self.RLeg.name+'UpVec_spcSwitcher')
        cmds.parent (g, ikGrp)
        cmds.parent (self.RLeg.name+'_'+self.RLeg.nameList[1]+'Upvec_grp', self.RLeg.name+'UpVec_spcSwitcher')
        g=cmds.group (empty=True, n=self.LLeg.name+'UpVec_spcSwitcher')
        cmds.parent (g, ikGrp)
        cmds.parent (self.LLeg.name+'_'+self.LLeg.nameList[1]+'Upvec_grp', self.LLeg.name+'UpVec_spcSwitcher') 
        g=cmds.group (empty=True, n=self.LArm.name+'UpVec_spcSwitcher')
        cmds.parent (g, ikGrp)
        cmds.parent (self.LArm.name+'_'+self.LArm.nameList[1]+'Upvec_grp', self.LArm.name+'UpVec_spcSwitcher')
        g=cmds.group (empty=True, n=self.RArm.name+'UpVec_spcSwitcher')
        cmds.parent (g, ikGrp)
        cmds.parent (self.RArm.name+'_'+self.RArm.nameList[1]+'Upvec_grp', self.RArm.name+'UpVec_spcSwitcher')
        g=cmds.group (empty=True, n=self.MSpine.nameList[2]+'_spcSwitcher')
        cmds.parent (self.MSpine.name+'_'+'ik'+self.MSpine.nameList[2]+'_grp', self.MSpine.nameList[2]+'_spcSwitcher')      
        cmds.parent (g, ikGrp)       
        g= cmds.group (self.Neck.name+'_'+'fk'+self.Neck.nameList[1]+'_grp', n=self.Neck.nameList[1]+'_spcSwitcher')
        cmds.parent (g, ikGrp)
        
        spcGrp = cmds.group (empty=True, n=self.name+'_spaces_grp')
        self.createSpc ('', 'global')
        self.createSpc (self.COG.skinJntEnd, 'cog')
        self.createSpc (self.MSpine.skinJntEnd, 'chest')
        self.createSpc (self.LClav.skinJntEnd, 'lclav')
        self.createSpc (self.RClav.skinJntEnd, 'rclav')    
        self.createSpc (self.LFoot.name+'_ik_cntrl', 'lfoot') 
        self.createSpc (self.RFoot.name+'_ik_cntrl', 'rfoot') 
        self.createSpc (self.Neck.skinJntStart, 'neck')
        self.createSpc (self.Neck.skinJntEnd, 'head')
        cmds.group (empty=True, n=self.name+'_headPos_spc')       
        gen.alignObjs (self.Neck.skinJntEnd ,self.name+'_headPos_spc', True, False, False)
        cmds.parent (self.name+'_headPos_spc', self.name+'_neck_drv')        
        cns = cmds.pointConstraint (self.name+'_headPos_spc', self.Neck.nameList[1]+'_spcSwitcher')[0]
        
        self.addSpc (self.Neck.name+'_'+'fk'+self.Neck.nameList[1]+'_cntrl', 'global', 'orient')       
        self.addSpc (self.Neck.name+'_'+'fk'+self.Neck.nameList[1]+'_cntrl', 'cog', 'orient')
        self.addSpc (self.Neck.name+'_'+'fk'+self.Neck.nameList[1]+'_cntrl', 'chest', 'orient')
        self.addSpc (self.Neck.name+'_'+'fk'+self.Neck.nameList[1]+'_cntrl', 'neck', 'orient')
        		
        self.addSpc (self.LArm.name+'_'+'ik'+self.LArm.nameList[2]+'_cntrl', 'global', 'parent')
        self.addSpc (self.LArm.name+'_'+'ik'+self.LArm.nameList[2]+'_cntrl', 'cog', 'parent')
        self.addSpc (self.LArm.name+'_'+'ik'+self.LArm.nameList[2]+'_cntrl', 'chest', 'parent')
        self.addSpc (self.LArm.name+'_'+'ik'+self.LArm.nameList[2]+'_cntrl', 'lclav', 'parent')
        self.addSpc (self.LArm.name+'_'+'ik'+self.LArm.nameList[2]+'_cntrl', 'head', 'parent')
        
        self.addSpc (self.RArm.name+'_'+'ik'+self.RArm.nameList[2]+'_cntrl', 'global', 'parent')
        self.addSpc (self.RArm.name+'_'+'ik'+self.RArm.nameList[2]+'_cntrl', 'cog', 'parent')
        self.addSpc (self.RArm.name+'_'+'ik'+self.RArm.nameList[2]+'_cntrl', 'chest', 'parent') 
        self.addSpc (self.RArm.name+'_'+'ik'+self.RArm.nameList[2]+'_cntrl', 'rclav', 'parent')
        self.addSpc (self.RArm.name+'_'+'ik'+self.RArm.nameList[2]+'_cntrl', 'head', 'parent')
        
        self.addSpc (self.LLeg.name+'_'+self.LLeg.nameList[1]+'Upvec_cntrl', 'global', 'parent')
        self.addSpc (self.LLeg.name+'_'+self.LLeg.nameList[1]+'Upvec_cntrl', 'cog', 'parent')
        self.addSpc (self.LLeg.name+'_'+self.LLeg.nameList[1]+'Upvec_cntrl', 'lfoot', 'parent')
        
        self.addSpc (self.RLeg.name+'_'+self.RLeg.nameList[1]+'Upvec_cntrl', 'global', 'parent')
        self.addSpc (self.RLeg.name+'_'+self.RLeg.nameList[1]+'Upvec_cntrl', 'cog', 'parent')
        self.addSpc (self.RLeg.name+'_'+self.RLeg.nameList[1]+'Upvec_cntrl', 'rfoot', 'parent')
        
        self.addSpc (self.LArm.name+'_'+self.LArm.nameList[1]+'Upvec_cntrl', 'global', 'parent')
        self.addSpc (self.LArm.name+'_'+self.LArm.nameList[1]+'Upvec_cntrl', 'cog', 'parent')
        self.addSpc (self.LArm.name+'_'+self.LArm.nameList[1]+'Upvec_cntrl', 'chest', 'parent')
        
        self.addSpc (self.RArm.name+'_'+self.RArm.nameList[1]+'Upvec_cntrl', 'global', 'parent')
        self.addSpc (self.RArm.name+'_'+self.RArm.nameList[1]+'Upvec_cntrl', 'cog', 'parent')
        self.addSpc (self.RArm.name+'_'+self.RArm.nameList[1]+'Upvec_cntrl', 'chest', 'parent')
        
        self.addSpc (self.MSpine.name+'_ik'+self.MSpine.nameList[2]+'_cntrl', 'global', 'parent')
        self.addSpc (self.MSpine.name+'_ik'+self.MSpine.nameList[2]+'_cntrl', 'cog', 'parent')
        
        drv= cmds.ls ('*_drv', assemblies=True)
        cmds.parent (drv, spcGrp)
        
        cmds.parent (ikGrp, fkGrp, swGrp, jtGrp, spcGrp , glbCntrl)
        cmds.parent (rbGrp , grp)
        
        switches = cmds.ls ('*_Switch')
		
        for swt in switches:
            attr = cmds.listAttr (swt, v=True, k=True)
            name = self.COG.name+'_fk'+self.COG.nameList[0]+'_cntrl'
            for a in attr:
                if not cmds.listConnections (swt+'.'+a, d=False, s=True):
                    cmds.addAttr (name, ln = swt.replace('_IKFK_Switch','')+'_'+a,  k=True)
                    cmds.connectAttr (name+'.'+swt.replace('_IKFK_Switch','')+'_'+a,swt+'.'+a)
        
        if cmds.objExists (self.name+'_skinJoints'):
            cmds.delete (self.name+'_skinJoints', hi='below')
        setSkin = cmds.createNode( 'objectSet', name =self.name+'_skinJoints' )
        cmds.sets (self.skinJoints, forceElement = setSkin)
        
    def createSpc (self, driver, name):
        drvGrp = cmds.group (empty=True, n=self.name+'_'+name+'_drv')
        if driver:
            cmds.parentConstraint (driver, drvGrp)
        spcGrp = cmds.group (empty=True, n=self.name+'_'+name+'_spc')
        cmds.parent (spcGrp, drvGrp)
        
    def addSpc (self, target, space, type):       
        switcher = cmds.listRelatives (cmds.listRelatives (target, p=True)[0], p=True)[0]
        
        if type=='parent':
            cns = cmds.parentConstraint (self.name+'_'+space+'_spc', switcher, mo=True)[0]
        elif type=='orient':
            cns =  cmds.orientConstraint (self.name+'_'+space+'_spc', switcher)[0]
        
        if cmds.attributeQuery ('spcSwitch', node=target, exists = True):
            enumTxt = cmds.attributeQuery ('spcSwitch', node=target, le = True)[0]
            print 'antes'
            connects = cmds.listConnections (target+'.spcSwitch', d=True, s=False, p=True)
            print 'depois'
            print connects
            index = len (enumTxt.split (':'))
            enumTxt = enumTxt+':'+space
            cmds.deleteAttr (target, at = 'spcSwitch')
            cmds.addAttr ( target, ln='spcSwitch', at='enum', en=enumTxt, k=True)
            if connects:
                for c in connects:
                    cmds.connectAttr (target+'.spcSwitch', c)
        else:
            cmds.addAttr ( target, ln='spcSwitch', at='enum', en=space, k=True)
            index=0
            
        cond = cmds.createNode ('condition', n=self.name+switcher+space+'Cond')
        print cond
        print target
        cmds.connectAttr (target+'.spcSwitch', cond+'.firstTerm')
        cmds.setAttr (cond+'.secondTerm', index)
        cmds.setAttr (cond+'.operation', 0)
        cmds.setAttr (cond+'.colorIfTrueR', 1)
        cmds.setAttr (cond+'.colorIfFalseR', 0)     
        cmds.connectAttr (cond+'.outColor.outColorR', cns+'.'+self.name+'_'+space+'_spcW'+str(index))
