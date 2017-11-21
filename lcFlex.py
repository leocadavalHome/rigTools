import maya.cmds as cmds
import lcGeneric as gen

class Flex:
    def __init__ (self, name, width=10, div=5.0):
        self.flexName= name
        self.width=width
        self.div = div
        self.doFlex()
        
        
    def createFoll (self, name, nurbsSurf, uPos, vPos):
        nurbsSurfShape= cmds.listRelatives (nurbsSurf, shapes=True) [0]
        follShape = cmds.createNode ('follicle', n=name+'Shape')
        
        foll = cmds.listRelatives (follShape, p=True)[0]
        foll = cmds.rename (foll, name)
        follShape =foll+'Shape'
        cmds.connectAttr (nurbsSurf+'.local', foll+'.inputSurface')
        cmds.connectAttr (nurbsSurf+'.worldMatrix[0]', foll+'.inputWorldMatrix')
        cmds.connectAttr (follShape+'.outRotate', foll+'.rotate')
        cmds.connectAttr (follShape+'.outTranslate', foll+'.translate')
        cmds.setAttr (follShape+'.parameterU', uPos)
        cmds.setAttr (follShape+'.parameterV', vPos)
        cmds.setAttr (foll+'.translate', l=True)
        cmds.setAttr (foll+'.rotate', l=True)
        cmds.setAttr (follShape+'.visibility', False)
        return foll

    def doFlex(self):
        nurbsSurf = cmds.nurbsPlane (p=(0,0,0), ax=(0,1,0), w=self.width, lr = 0.1, d=3, u=self.div, v=1, ch=0, n=self.flexName+'FlexNurbsSrf')[0]    
        cmds.setAttr(nurbsSurf+'.visibility',False)
        spacing  = 1.0/ float(self.div)
        start = spacing/2.0
        grp1 = cmds.group (n=self.flexName+'Folicules_grp', empty =True)
        for i in range(self.div):
            foll= self.createFoll (self.flexName+'Follicle'+str('%02d' % i),nurbsSurf, start+spacing*i, 0.5)
            jnt1= cmds.joint( p=(0, 0, 0), n=self.flexName+str('%02d' % i)+'_jnt')
            cmds.move (0,0,0, jnt1, ls=True)
            cmds.parent (foll, grp1)
            
        nurbsSurfBlend = cmds.nurbsPlane (p=(0,0,0), ax=(0,1,0), w=self.width, lr = 0.1, d=3, u=self.div, v=1, ch=0, n=self.flexName+'FlexBlendNurbsSrf')[0]
        
        cmds.blendShape (nurbsSurfBlend, nurbsSurf,  frontOfChain=True,  tc=0, w=(0,1))
        crv= cmds.curve(d=2, p=[((self.width*-0.5), 0, 0), (0, 0, 0), ((self.width*0.5), 0, 0)], k=[ 0,0,1,1], n=self.flexName+'Crv')
        cls1 = cmds.cluster (crv+'.cv[0]', crv+'.cv[1]', rel =True, n=self.flexName+'Cls1')
        cmds.move ((self.width*-0.5),0,0, cls1[1]+'.scalePivot',  cls1[1]+'.rotatePivot')
        cls2 = cmds.cluster (crv+'.cv[2]', crv+'.cv[1]', rel =True, n=self.flexName+'Cls2')
        cmds.move ((self.width*0.5),0,0, cls2[1]+'.scalePivot',  cls2[1]+'.rotatePivot')
        cls3=cmds.cluster (crv+'.cv[1]',rel =True, n=self.flexName+'Cls3')
        cmds.percent (cls1[0],crv+'.cv[1]', v=0.5)
        cmds.percent (cls2[0],crv+'.cv[1]', v=0.5)
        twist= cmds.nonLinear(nurbsSurfBlend,  type='twist', n=self.flexName+'Twist')
        cmds.rotate (0,0,90, twist[1])
        wir = cmds.wire (nurbsSurfBlend, gw=False,  en=1.000000,  ce=0.000000, li=0.000000, w=crv , dds=(0,20) )
        gen.createCntrl (self.flexName+'aux1', cls1[1], 1, 'grp', 1)
        gen.createCntrl (self.flexName+'aux2', cls2[1], 1, 'grp', 1)
        gen.createCntrl (self.flexName+'aux3', cls3[1], 1, 'grp', 1)
        cmds.setAttr (self.flexName+"aux3_cntrl.rotateOrder", 1)
        cmds.setAttr (self.flexName+"aux3_grp.rotateOrder", 1)
        cmds.setAttr (self.flexName+"aux2_cntrl.rotateOrder", 1)
        cmds.setAttr (self.flexName+"aux2_grp.rotateOrder", 1)
        cmds.setAttr (self.flexName+"aux1_cntrl.rotateOrder", 1)
        cmds.setAttr (self.flexName+"aux1_grp.rotateOrder",1)
        cmds.pointConstraint (self.flexName+'aux1_cntrl', self.flexName+'aux3_grp')
        cmds.pointConstraint (self.flexName+'aux2_cntrl', self.flexName+'aux3_grp')
        cmds.connectAttr (self.flexName+'aux1_cntrl.translate', cls1[1]+'.translate')
        cmds.connectAttr (self.flexName+'aux2_cntrl.translate', cls2[1]+'.translate')
        cmds.connectAttr (self.flexName+'aux3_cntrl.translate', cls3[1]+'.translate')
        cmds.connectAttr (self.flexName+'aux1_cntrl.rotateX', twist[0]+'.endAngle')
        cmds.connectAttr (self.flexName+'aux2_cntrl.rotateX', twist[0]+'.startAngle')


        grp2=cmds.group (nurbsSurf, self.flexName+'aux1_grp', self.flexName+'aux2_grp', self.flexName+'aux3_grp', n=self.flexName+'FlexGlobalMove')
        cmds.setAttr(grp2+'.rotateOrder', 1)
        grp3=cmds.group (nurbsSurfBlend, cls1[1], cls2[1], cls3[1], crv, crv+'BaseWire', twist[1], n=self.flexName+'FlexNoMove')
        cmds.setAttr (grp3+'.visibility',0)
        cmds.group (grp1,grp2,grp3,n=self.flexName+'Flex_grp') 
        
        return self.flexName+'Flex'
        
        
class RibbonLimb:
    def __init__ (self, name, width=10.0, div=5.0, dir='X'):
        self.flexName= name
        self.width=float (width)
        self.div = div
        self.dir = dir
        if self.dir=='X':
            self.axisDict ={'X':{'ax':(0,0,1),'w':self.width, 'lr':0.1,'u':self.div,'v':1, 'mvA':[(self.width*0.5), 0,0], 'mvB':[(self.width*-0.5), 0,0], 'mvUpAxis':'.translateY', 'aimVector':(-1,0,0), 'upVector':(0,1,0)}}
        elif self.dir=='Y':
            self.axisDict ={'Y':{'ax':(0,0,1),'w':1,'lr':self.width,'u':1,'v':self.div, 'mvA':[0,(self.width*0.5),0], 'mvB':[0,(self.width*-0.5),0], 'mvUpAxis':'.translateX', 'aimVector':(0,-1,0), 'upVector':(1,0,0)}}
        self.aux1=self.flexName+'aux1_cntrl'
        self.aux2=self.flexName+'aux2_cntrl'
        self.aux3=self.flexName+'aux3_cntrl'
        self.extr =self.flexName+'Extr'
        self.midJnt = self.flexName+'_mid_Fk'
        self.cntrlGrp = self.flexName+'Cntrl_grp'
        self.skinJoints=[]
        self.doFlex()
        
    def createFoll (self, name, nurbsSurf, uPos, vPos):
        nurbsSurfShape= cmds.listRelatives (nurbsSurf, shapes=True) [0]
        follShape = cmds.createNode ('follicle', n=name+'Shape')
        
        foll = cmds.listRelatives (follShape, p=True)[0]
        foll = cmds.rename (foll, name)
        follShape =foll+'Shape'
        cmds.connectAttr (nurbsSurf+'.local', foll+'.inputSurface')
        cmds.connectAttr (nurbsSurf+'.worldMatrix[0]', foll+'.inputWorldMatrix')
        cmds.connectAttr (follShape+'.outRotate', foll+'.rotate')
        cmds.connectAttr (follShape+'.outTranslate', foll+'.translate')
        cmds.setAttr (follShape+'.parameterU', uPos)
        cmds.setAttr (follShape+'.parameterV', vPos)
        cmds.setAttr (foll+'.translate', l=True)
        cmds.setAttr (foll+'.rotate', l=True)
        cmds.setAttr (follShape+'.visibility', False)
        return foll
        
    def doFlex(self):
        nurbsSurf = cmds.nurbsPlane (p=(0,0,0), ax=self.axisDict[self.dir]['ax'], w=self.axisDict[self.dir]['w'], lr =self.axisDict[self.dir]['lr'], d=3, u=self.axisDict[self.dir]['u'], v=self.axisDict[self.dir]['v'], ch=0, n=self.flexName+'FlexNurbsSrf')[0] 
        locA = cmds.spaceLocator (n=self.flexName+'aux1_cntrl')[0]
        cmds.addAttr (locA, ln='squash', at='double', k=True)
        cmds.addAttr (locA, ln='glbScl', at='double', k=True)
        cmds.setAttr (locA+'.glbScl', 1)
                
        cmds.setAttr (locA+'.rotateOrder', 1)
        locAAim = cmds.spaceLocator (n=self.flexName+'A_aim')[0]
        cmds.setAttr (locAAim+'.rotateOrder', 1)
        locAUp = cmds.spaceLocator (n=self.flexName+'A_up')[0]
        locAFront = cmds.spaceLocator (n=self.flexName+'A_front')[0]
        cmds.parent (locAFront, locA)
        cmds.move (1, 0, 0, locAFront)
        cmds.parent (locAAim, locAUp, locA)
        cmds.move (self.axisDict[self.dir]['mvA'][0],self.axisDict[self.dir]['mvA'][1],self.axisDict[self.dir]['mvA'][2], locA)

        locB = cmds.spaceLocator (n=self.flexName+'aux2_cntrl')[0]
        cmds.setAttr (locB+'.rotateOrder', 1)
        locBAim = cmds.spaceLocator (n=self.flexName+'B_aim')[0]
        cmds.setAttr (locBAim+'.rotateOrder', 1)
        locBUp = cmds.spaceLocator (n=self.flexName+'B_up')[0]
        cmds.parent (locBAim, locBUp, locB)
        cmds.move (self.axisDict[self.dir]['mvB'][0],self.axisDict[self.dir]['mvB'][1],self.axisDict[self.dir]['mvB'][2], locB)
        
        locM = cmds.spaceLocator (n=self.flexName+'Mid_pos')[0]
        cmds.setAttr (locM +'.rotateOrder', 1)
        locMRot = cmds.spaceLocator (n=self.flexName+'Mid_rot')[0]
        cmds.setAttr (locMRot +'.rotateOrder', 1)
        locMOff = cmds.spaceLocator (n=self.flexName+'aux3_cntrl')[0]              
        cmds.setAttr (locMOff +'.rotateOrder', 1)
        
        cmds.parent ( locMOff, locM)
        cmds.parent (locMRot, locMOff)
        
        
        locExtr = cmds.spaceLocator (n=self.flexName+'Extr')[0]
        locTwist = cmds.spaceLocator (n=self.flexName+'Twist')[0]
        cmds.parent (locTwist, locExtr)
        cmds.rotate (-45, 0 ,0, locExtr)
        
        
        cmds.select (cl=True)
        
        jntM = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_mid_Fk')
        cmds.parent (jntM, locMRot, relative=True)
        
        cmds.select (cl=True)
        
        jntA = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_A_Fk')
        jntAend  = cmds.joint( p=(-0.3*(self.width/10), 0, 0), roo='yzx', n=self.flexName+'_A_end')
        cmds.parent (jntA, locAAim,relative=True)
        
        cmds.select (cl=True)
        
        jntB = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_B_Fk')
        jntBend  = cmds.joint( p=(0.3*(self.width/10), 0, 0), roo='yzx', n=self.flexName+'_B_end')
        cmds.parent (jntB, locBAim,relative=True)
        
        cmds.setAttr (locAUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
        cmds.setAttr (locBUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
            
        cmds.pointConstraint (locA, locB, locM)
        cmds.aimConstraint (jntM, locAAim, offset=(0, 0,0) ,weight=1, aimVector=(-1, 0 ,0) ,upVector=(0, 1, 0), worldUpType='object', worldUpObject=locAUp)
        cmds.aimConstraint (jntM, locBAim, offset=(0, 0,0) ,weight=1, aimVector=(1, 0 ,0) ,upVector=(0, 1, 0), worldUpType='object', worldUpObject=locBUp)
        
        cmds.aimConstraint (locAFront,locExtr, mo=True, aimVector= (1, 0,0), upVector = (0,1,0), worldUpType ='none')
        cmds.pointConstraint (locA,locExtr)
        cmds.orientConstraint (locA, locTwist,mo=True) 
        
        twistMulti = cmds.createNode ('multDoubleLinear', n=self.flexName+'twistMulti')
        cmds.setAttr (twistMulti+'.input2', 0.5)
        cmds.connectAttr (locTwist+'.rotateX', twistMulti+'.input1')
        cmds.connectAttr (twistMulti+'.output', locMRot+'.rotateX')
                      
        spacing  = 1.0/ float(self.div)
        start = spacing/2.0
        grp1 = cmds.group (n=self.flexName+'Folicules_grp', empty =True)
        for i in range(int(self.div)):
            if self.dir=='X':
                foll= self.createFoll (self.flexName+'Follicle'+str(i),nurbsSurf, start+spacing*i, 0.5)
            elif self.dir=='Y':
                foll= self.createFoll (self.flexName+'Follicle'+str(i),nurbsSurf, 0.5, start+spacing*i)
            jnt1= cmds.joint( p=(0, 0, 0), n=self.flexName+str(i)+'_jnt')
            self.skinJoints.append (jnt1)
            cmds.move (0,0,0, jnt1, ls=True)
            cmds.parent (foll, grp1)
            cmds.expression (s='scaleX ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all")
            cmds.expression (s='scaleY ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all")
            cmds.expression (s='scaleZ ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all") 

			
        cmds.skinCluster (jntM, jntA, jntB, nurbsSurf, dr=2*(10/self.width), maximumInfluences=2)
        
        hideList = [locA, locB, locM, locAAim, locAUp, locBAim, locBUp, nurbsSurf, locM+'Shape',locExtr ]
        for x in hideList:
            cmds.setAttr ( x+'.visibility', 0)
        
        cntrlGrp = cmds.group (locA, locB,locExtr, locM, n= self.flexName+'Cntrl_grp')
        cmds.group (nurbsSurf, grp1,cntrlGrp,  n=self.flexName+'Ribbon_grp')
        
        
class RibbonSpine:
    def __init__ (self, name, width=10.0, div=5.0, dir='X'):
        self.flexName= name
        self.width=float (width)
        self.div = div
        self.dir = dir
        if self.dir=='X':
            self.axisDict ={'X':{'ax':(0,0,1),'w':self.width, 'lr':0.1,'u':self.div,'v':1, 'mvA':[(self.width*0.5), 0,0], 'mvB':[(self.width*-0.5), 0,0], 'mvUpAxis':'.translateY', 'aimVector':(-1,0,0), 'upVector':(0,1,0)}}
        elif self.dir=='Y':
            self.axisDict ={'Y':{'ax':(0,0,1),'w':1,'lr':self.width,'u':1,'v':self.div, 'mvA':[0,(self.width*0.5),0], 'mvB':[0,(self.width*-0.5),0], 'mvUpAxis':'.translateX', 'aimVector':(0,-1,0), 'upVector':(1,0,0)}}
        self.aux1=self.flexName+'aux1_cntrl'
        self.aux2=self.flexName+'aux2_cntrl'
        self.aux3=self.flexName+'aux3_cntrl'
        self.cntrlGrp = self.flexName+'Cntrl_grp'
        self.skinJoints=[]
        self.doFlex()
        
    def createFoll (self, name, nurbsSurf, uPos, vPos):
        nurbsSurfShape= cmds.listRelatives (nurbsSurf, shapes=True) [0]
        follShape = cmds.createNode ('follicle', n=name+'Shape')
        
        foll = cmds.listRelatives (follShape, p=True)[0]
        foll = cmds.rename (foll, name)
        follShape =foll+'Shape'
        cmds.connectAttr (nurbsSurf+'.local', foll+'.inputSurface')
        cmds.connectAttr (nurbsSurf+'.worldMatrix[0]', foll+'.inputWorldMatrix')
        cmds.connectAttr (follShape+'.outRotate', foll+'.rotate')
        cmds.connectAttr (follShape+'.outTranslate', foll+'.translate')
        cmds.setAttr (follShape+'.parameterU', uPos)
        cmds.setAttr (follShape+'.parameterV', vPos)
        cmds.setAttr (foll+'.translate', l=True)
        cmds.setAttr (foll+'.rotate', l=True)
        cmds.setAttr (follShape+'.visibility', False)
        return foll
        
    def doFlex(self):
        nurbsSurf = cmds.nurbsPlane (p=(0,0,0), ax=self.axisDict[self.dir]['ax'], w=self.axisDict[self.dir]['w'], lr =self.axisDict[self.dir]['lr'], d=3, u=self.axisDict[self.dir]['u'], v=self.axisDict[self.dir]['v'], ch=0, n=self.flexName+'FlexNurbsSrf')[0] 
        locA = cmds.spaceLocator (n=self.flexName+'aux1_cntrl')[0]
        cmds.addAttr (locA, ln='squash', at='double', k=True)
        cmds.addAttr (locA, ln='glbScl', at='double', k=True)
        cmds.setAttr (locA+'.glbScl', 1)
        
        
        cmds.setAttr (locA+'.rotateOrder', 1)
        locAAim = cmds.spaceLocator (n=self.flexName+'A_aim')[0]
        cmds.setAttr (locAAim+'.rotateOrder', 1)
        locAUp = cmds.spaceLocator (n=self.flexName+'A_up')[0]
        cmds.parent (locAAim, locAUp, locA)
        cmds.move (self.axisDict[self.dir]['mvA'][0],self.axisDict[self.dir]['mvA'][1],self.axisDict[self.dir]['mvA'][2], locA)

        locB = cmds.spaceLocator (n=self.flexName+'aux2_cntrl')[0]
        cmds.setAttr (locB+'.rotateOrder', 1)
        locBAim = cmds.spaceLocator (n=self.flexName+'B_aim')[0]
        cmds.setAttr (locBAim+'.rotateOrder', 1)
        locBUp = cmds.spaceLocator (n=self.flexName+'B_up')[0]
        cmds.parent (locBAim, locBUp, locB)
        cmds.move (self.axisDict[self.dir]['mvB'][0],self.axisDict[self.dir]['mvB'][1],self.axisDict[self.dir]['mvB'][2], locB)
        
        locM = cmds.spaceLocator (n=self.flexName+'Mid_pos')[0]
        cmds.setAttr (locM +'.rotateOrder', 1)
        locMAim = cmds.spaceLocator (n=self.flexName+'Mid_aim')[0]
        cmds.setAttr (locMAim +'.rotateOrder', 1)
        locMUp = cmds.spaceLocator (n=self.flexName+'Mid_up')[0]
        locMOff = cmds.spaceLocator (n=self.flexName+'aux3_cntrl')[0]              
        cmds.setAttr (locMOff +'.rotateOrder', 1)
        
        cmds.parent (locMAim, locMUp, locM)
        cmds.parent (locMOff,locMAim)
        
        cmds.select (cl=True)
        
        jntM = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_mid_Fk')
        cmds.parent (jntM, locMOff, relative=True)
        
        cmds.select (cl=True)
        
        jntA = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_A_Fk')
        jntAend  = cmds.joint( p=(-0.3*(self.width/10), 0, 0), roo='yzx', n=self.flexName+'_A_end')
        cmds.parent (jntA, locAAim,relative=True)
        
        cmds.select (cl=True)
        
        jntB = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_B_Fk')
        jntBend  = cmds.joint( p=(0.3*(self.width/10), 0, 0), roo='yzx', n=self.flexName+'_B_end')
        cmds.parent (jntB, locBAim,relative=True)
        
        cmds.setAttr (locAUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
        cmds.setAttr (locBUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
        cmds.setAttr (locMUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
                    
        cmds.pointConstraint (locA, locB, locM)
        cmds.aimConstraint (jntM, locAAim, offset=(0, 0,0) ,weight=1, aimVector=self.axisDict[self.dir]['aimVector'] ,upVector=self.axisDict[self.dir]['upVector'], worldUpType='object', worldUpObject=locAUp)
        cmds.aimConstraint (jntM, locBAim, offset=(0, 0,0) ,weight=1, aimVector=[self.axisDict[self.dir]['aimVector'][0], self.axisDict[self.dir]['aimVector'][1]*-1,self.axisDict[self.dir]['aimVector'][2]] ,upVector=self.axisDict[self.dir]['upVector'], worldUpType='object', worldUpObject=locBUp)
        cmds.aimConstraint (locB, locMAim, offset=(0, 0,0) ,weight=1, aimVector=self.axisDict[self.dir]['aimVector'] ,upVector=self.axisDict[self.dir]['upVector'], worldUpType='object', worldUpObject=locMUp)      
        
        spacing  = 1.0/ float(self.div)
        start = spacing/2.0
        grp1 = cmds.group (n=self.flexName+'Folicules_grp', empty =True)
        for i in range(int(self.div)):
            if self.dir=='X':
                foll= self.createFoll (self.flexName+'Follicle'+str(i),nurbsSurf, start+spacing*i, 0.5)
            elif self.dir=='Y':
                foll= self.createFoll (self.flexName+'Follicle'+str(i),nurbsSurf, 0.5, start+spacing*i)
            jnt1= cmds.joint( p=(0, 0, 0), n=self.flexName+str(i)+'_jnt')
            self.skinJoints.append (jnt1)
            cmds.move (0,0,0, jnt1, ls=True)
            cmds.parent (foll, grp1)
            cmds.expression (s='scaleX ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all")
            cmds.expression (s='scaleY ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all")
            cmds.expression (s='scaleZ ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all")             
            
        cmds.skinCluster (jntM, jntA, jntB, nurbsSurf, dr=2*(10/self.width), maximumInfluences=2)
        
        hideList = [locA, locB, locM, locAAim, locAUp, locBAim, locBUp, nurbsSurf, locMUp, locM+'Shape', locMAim+'Shape']
        for x in hideList:
            cmds.setAttr ( x+'.visibility', 0)
        
        cntrlGrp = cmds.group (locA, locB, locM, n= self.flexName+'Cntrl_grp')
        cmds.group (nurbsSurf, grp1,cntrlGrp,  n=self.flexName+'Ribbon_grp')
        
        
class RibbonNeck:
    def __init__ (self, name, width=10.0, div=5.0, dir='X'):
        self.flexName= name
        self.width=float (width)
        self.div = div
        self.dir = dir
        if self.dir=='X':
            self.axisDict ={'X':{'ax':(0,0,1),'w':self.width, 'lr':0.1,'u':self.div,'v':1, 'mvA':[(self.width*0.5), 0,0], 'mvB':[(self.width*-0.5), 0,0], 'mvUpAxis':'.translateZ', 'aimVector':(-1,0,0), 'upVector':(0,0,1)}}
        elif self.dir=='Y':
            self.axisDict ={'Y':{'ax':(0,0,1),'w':1,'lr':self.width,'u':1,'v':self.div, 'mvA':[0,(self.width*0.5),0], 'mvB':[0,(self.width*-0.5),0], 'mvUpAxis':'.translateX', 'aimVector':(0,-1,0), 'upVector':(1,0,0)}}
        self.aux1=self.flexName+'aux1_cntrl'
        self.aux2=self.flexName+'aux2_cntrl'
        self.aux3=self.flexName+'aux3_cntrl'
        self.cntrlGrp = self.flexName+'Cntrl_grp'
        self.skinJoints=[]
        self.doFlex()
        
    def createFoll (self, name, nurbsSurf, uPos, vPos):
        nurbsSurfShape= cmds.listRelatives (nurbsSurf, shapes=True) [0]
        follShape = cmds.createNode ('follicle', n=name+'Shape')
        
        foll = cmds.listRelatives (follShape, p=True)[0]
        foll = cmds.rename (foll, name)
        follShape =foll+'Shape'
        cmds.connectAttr (nurbsSurf+'.local', foll+'.inputSurface')
        cmds.connectAttr (nurbsSurf+'.worldMatrix[0]', foll+'.inputWorldMatrix')
        cmds.connectAttr (follShape+'.outRotate', foll+'.rotate')
        cmds.connectAttr (follShape+'.outTranslate', foll+'.translate')
        cmds.setAttr (follShape+'.parameterU', uPos)
        cmds.setAttr (follShape+'.parameterV', vPos)
        cmds.setAttr (foll+'.translate', l=True)
        cmds.setAttr (foll+'.rotate', l=True)
        cmds.setAttr (follShape+'.visibility', False)
        return foll
        
    def doFlex(self):
        nurbsSurf = cmds.nurbsPlane (p=(0,0,0), ax=self.axisDict[self.dir]['ax'], w=self.axisDict[self.dir]['w'], lr =self.axisDict[self.dir]['lr'], d=3, u=self.axisDict[self.dir]['u'], v=self.axisDict[self.dir]['v'], ch=0, n=self.flexName+'FlexNurbsSrf')[0] 
        locA = cmds.spaceLocator (n=self.flexName+'aux1_cntrl')[0]
        cmds.setAttr (locA+'.rotateOrder', 1)
        cmds.addAttr (locA, ln='squash', at='double', k=True)
        cmds.addAttr (locA, ln='glbScl', at='double', k=True)
        cmds.setAttr (locA+'.glbScl', 1)
                
        locAAim = cmds.spaceLocator (n=self.flexName+'A_aim')[0]
        cmds.setAttr (locAAim+'.rotateOrder', 1)
        locAUp = cmds.spaceLocator (n=self.flexName+'A_up')[0]
        cmds.parent (locAAim, locAUp, locA)
        cmds.move (self.axisDict[self.dir]['mvA'][0],self.axisDict[self.dir]['mvA'][1],self.axisDict[self.dir]['mvA'][2], locA)

        locB = cmds.spaceLocator (n=self.flexName+'aux2_cntrl')[0]
        cmds.setAttr (locB+'.rotateOrder', 1)
        locBAim = cmds.spaceLocator (n=self.flexName+'B_aim')[0]
        cmds.setAttr (locBAim+'.rotateOrder', 1)
        locBUp = cmds.spaceLocator (n=self.flexName+'B_up')[0]
        cmds.parent (locBAim, locBUp, locB)
        cmds.move (self.axisDict[self.dir]['mvB'][0],self.axisDict[self.dir]['mvB'][1],self.axisDict[self.dir]['mvB'][2], locB)
        
        locM = cmds.spaceLocator (n=self.flexName+'Mid_pos')[0]
        cmds.setAttr (locM +'.rotateOrder', 1)
        locMAim = cmds.spaceLocator (n=self.flexName+'Mid_aim')[0]
        cmds.setAttr (locMAim +'.rotateOrder', 1)
        locMRot = cmds.spaceLocator (n=self.flexName+'Mid_rot')[0]
        cmds.setAttr (locMRot +'.rotateOrder', 1)
        locMUpRot = cmds.spaceLocator (n=self.flexName+'Mid_upRot')[0]
        cmds.setAttr (locMUpRot +'.rotateOrder', 1)
        locMUp = cmds.spaceLocator (n=self.flexName+'Mid_up')[0]
        locMOff = cmds.spaceLocator (n=self.flexName+'aux3_cntrl')[0]              
        cmds.setAttr (locMOff +'.rotateOrder', 1)
        
        cmds.parent (locMUpRot, locMOff, locM)
        cmds.parent (locMAim, locMOff)
        cmds.parent (locMRot, locMAim)
        cmds.parent (locMUp , locMUpRot)
        
        cmds.select (cl=True)
        
        jntM = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_mid_Fk')
        cmds.parent (jntM, locMRot, relative=True)
        
        cmds.select (cl=True)
        
        jntA = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_A_Fk')
        jntAend  = cmds.joint( p=(-0.3, 0, 0), roo='yzx', n=self.flexName+'_A_end')
        cmds.parent (jntA, locAAim,relative=True)
        
        cmds.select (cl=True)
        
        jntB = cmds.joint( p=(0, 0, 0), roo='yzx', n=self.flexName+'_B_Fk')
        jntBend  = cmds.joint( p=(0.3, 0, 0), roo='yzx', n=self.flexName+'_B_end')
        cmds.parent (jntB, locBAim,relative=True)
        
        cmds.setAttr (locAUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
        cmds.setAttr (locBUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
        cmds.setAttr (locMUp+self.axisDict[self.dir]['mvUpAxis'], 0.5)
            
        cmds.pointConstraint (locA, locB, locM)
        #mult = cmds.createNode ('multDoubleLinear', n=self.flexName+'multi')
        #cmds.connectAttr (locA+'.rotateX', mult+'.input1')
        #cmds.setAttr (mult+'.input2', 0.5)
        #cmds.connectAttr (mult+'.output', jntM+'.rotateX')
        cmds.aimConstraint (jntM, locAAim, offset=(0, 0,0) ,weight=1, aimVector=(-1, 0 ,0) ,upVector=(0, 1, 0), worldUpType='object', worldUpObject=locAUp)
        cmds.aimConstraint (jntM, locBAim, offset=(0, 0,0) ,weight=1, aimVector=(1, 0 ,0) ,upVector=(0, 1, 0), worldUpType='object', worldUpObject=locBUp)
        cmds.aimConstraint (locB, locMAim, offset=(0, 0,0) ,weight=1, aimVector=(-1, 0 ,0) ,upVector=(0, 1, 0), worldUpType='object', worldUpObject=locMUp)      
        cmds.orientConstraint (locA, locB, locMUpRot)
        cmds.orientConstraint (locMUpRot, locMRot, sk=['y','z'])
        spacing  = 1.0/ float(self.div)
        start = spacing/2.0
        grp1 = cmds.group (n=self.flexName+'Folicules_grp', empty =True)
        for i in range(int(self.div)):
            if self.dir=='X':
                foll= self.createFoll (self.flexName+'Follicle'+str(i),nurbsSurf, start+spacing*i, 0.5)
            elif self.dir=='Y':
                foll= self.createFoll (self.flexName+'Follicle'+str(i),nurbsSurf, 0.5, start+spacing*i)
            jnt1= cmds.joint( p=(0, 0, 0), n=self.flexName+str(i)+'_jnt')
            self.skinJoints.append (jnt1)
            cmds.move (0,0,0, jnt1, ls=True)
            cmds.parent (foll, grp1)
            cmds.expression (s='scaleX ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all")
            cmds.expression (s='scaleY ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all")
            cmds.expression (s='scaleZ ='+locA+'.glbScl+('+locA+'.squash*1)',o=jnt1, ae=True, uc="all") 
			
        cmds.skinCluster (jntM, jntA, jntB, nurbsSurf, dr=2*(self.width/10), maximumInfluences=2)
        
        hideList = [locA, locB, locM, locAAim, locAUp, locBAim, locBUp, nurbsSurf, locMUpRot, locMUp, locM+'Shape', locMAim+'Shape']
        #hideList = [locAAim, locAUp, locBAim, locBUp, nurbsSurf, locMUpRot, locMUp, locM+'Shape', locMAim+'Shape']
        for x in hideList:
            cmds.setAttr ( x+'.visibility', 0)
        
        cntrlGrp = cmds.group (locA, locB, locM, n= self.flexName+'Cntrl_grp')
        cmds.group (nurbsSurf, grp1,cntrlGrp,  n=self.flexName+'Ribbon_grp')
