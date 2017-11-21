import maya.cmds as cmds
import copy

##generic
##doLocator Python
def doLocator (name, pos, rot, locScale=1):
    loc = cmds.spaceLocator (n=name, p=[0,0,0])[0]
    cmds.xform (loc, t = pos)
    cmds.xform (loc, ro = rot)
    if not locScale ==1:
        cmds.setAttr (loc + "Shape.localScaleX",locScale)
        cmds.setAttr (loc + "Shape.localScaleY",locScale)
        cmds.setAttr (loc + "Shape.localScaleZ",locScale)
    cmds.setAttr(loc+'.rotateOrder', 1)
    return loc

##doLine Python
def doLine (lineSorce, lineTarget):
    childList = cmds.listRelatives (lineTarget, children=True, type='transform') 
    if childList:
        cmds.parent (filhos, w=True)
        
    dinLineShape = cmds.annotate (lineTarget, tx='')
    dinNameLinha = cmds.listRelatives (dinLineShape, type='transform', parent=True)
    cmds.pointConstraint (lineSorce, dinNameLinha, offset=[0,0,0], weight=1)
    cmds.rename (dinNameLinha[0], lineTarget+'_line')
   
    if childList:
        cmds.parent (filhos, lineTarget)
   
    return lineTarget+'_line'

##doLine Python
def doJoint (name, guideLocName):
     pos = cmds.xform (guideLocName, ws=True, q=True, t =True)
     jnt= cmds.joint (p=pos, n=name, roo='yzx')
     #cmds.setAttr(jnt+'.rotateOrder', 1)
     return jnt

##alignRot Python
def alignRot (source, target):
    rot = cmds.xform (source, ws=True, q=True, ro =True)
    cmds.xform (target, ws=True, ro=rot)
    cmds.makeIdentity (target, apply=True, t=True, r=True, s=True, n = False)

def alignObjs(source, target, po= True, ro=True, fr=True):
    if ro:
        rot = cmds.xform (source, ws=True, q=True, ro =True)
        cmds.xform (target, ws=True, ro=rot)
    if po:
        pos =cmds.xform (source, ws=True, q=True, t =True)
        cmds.xform (target, ws=True, t=pos)
    if fr:
        cmds.makeIdentity (target, apply=True, t=True, r=True, s=True, n = False)


def doMirror(source, eixo, local=False):   
    if eixo=='-X':
        rotacaoX=cmds.getAttr(source+'.rotateX')
        cmds.setAttr (source+'.rotateX', rotacaoX+180)
    elif eixo=='+X':
        rotacaoX=cmds.getAttr(source+'.rotateX')
        cmds.setAttr (source+'.rotateX', rotacaoX-180)  
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
    
		
##doCntrlFK Python
def createCntrl (name,targetName,radius,icone, cntrlScale):
    if icone == "circuloX" :
        cmds.circle (n=name+'_cntrl',r=radius,ch=True,o=True,nr=[1, 0, 0],s=5)
    elif icone == "circuloY":
        cmds.circle (n=name+'_cntrl',r=radius,ch=True,o=True,nr=[0, 1, 0],s=5)
    elif icone == "circuloZ":
        cmds.circle (n=name+'_cntrl',r=radius,ch=True,o=True,nr=[0, 0, 1],s=5)
    elif icone == "quadradoX":
        cmds.curve(n=name+"_cntrl",d=1,p=[(-3.984495, 0, 4.073894),(-3.940628, 0, -4.041594),(3.99939,0, -3.997726),(3.99939, 0, 4.073894),(-3.89676,0, 4.117762)],k=[0,1,2, 3, 4] )
        cmds.setAttr (name+"_cntrl.rotateZ",-90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "quadradoY":
        cmds.curve(n=name+"_cntrl",d=1,p=[(-3.984495, 0, 4.073894),(-3.940628, 0, -4.041594),(3.99939,0, -3.997726),(3.99939, 0, 4.073894),(-3.89676,0, 4.117762)],k=[0,1,2, 3, 4] )
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "quadradoZ":
        cmds.curve(n=name+"_cntrl",d=1,p=[(-3.984495, 0, 4.073894),(-3.940628, 0, -4.041594),(3.99939,0, -3.997726),(3.99939, 0, 4.073894),(-3.89676,0, 4.117762)],k=[0,1,2, 3, 4] )
        cmds.setAttr (name+"_cntrl.rotateZ",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "ponteiroX":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0, 0, 0),(1.691495,1.691495,0),(1.697056, 2.537859, 0),(2.545584, 2.545584, 0),(2.545584, 1.707095, 0),(1.691504, 1.692763, 0)], k=[0 ,1,2, 3, 4, 5])
        cmds.setAttr (name+"_cntrl.rotateZ",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "ponteiroY":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0, 0, 0),(1.691495,1.691495,0),(1.697056, 2.537859, 0),(2.545584, 2.545584, 0),(2.545584, 1.707095, 0),(1.691504, 1.692763, 0)], k=[0 ,1,2, 3, 4, 5])
        cmds.setAttr (name+"_cntrl.rotateY",90)
        cmds.setAttr (name+"_cntrl.rotateX",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "ponteiroZ":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0, 0, 0),(1.691495,1.691495,0),(1.697056, 2.537859, 0),(2.545584, 2.545584, 0),(2.545584, 1.707095, 0),(1.691504, 1.692763, 0)], k=[0 ,1,2, 3, 4, 5])
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone == "trianguloX":
        cmds.curve (n=name+"_cntrl",d=1,p=[(0,0,-0.471058),(-0.471058,0,0.471058),(0.471058,0,0.471058),(0,0,-0.471058)] ,k=[0,1, 2, 3])
        cmds.setAttr (name+"_cntrl.rotateX",90)
        cmds.setAttr (name+"_cntrl.rotateY",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone == "trianguloY":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0,0,-0.471058),(-0.471058,0,0.471058),(0.471058,0,0.471058),(0,0 ,-0.471058)] ,k=[0,1, 2, 3])
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone == "trianguloZ":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0,0,-0.471058),(-0.471058,0,0.471058),(0.471058,0,0.471058),(0,0 ,-0.471058)] ,k=[0,1, 2, 3])
        cmds.setAttr (name+"_cntrl.rotateX",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    	    
    elif icone == "ponteiroReto":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0,0,0), (0, 1.414597, 0),(0.569164, 2, 0),( 0, 2.569164, 0),(-0.569164, 2, 0),( 0.00139909, 1.432235, 0)] ,k=[0,1,2,3,4, 5])
        cmds.setAttr (name+"_cntrl.rotateY", 90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone =='bola':
        cv1 = cmds.circle (n=name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=1,d=3,ut=0,ch=0)[0]
        cv2 = cmds.circle (c=(0,0,0),nr=(1,0,0),sw=360,r=1,d=3,ut=0,ch=0)[0]
        cv2Shape = cmds.listRelatives (cv2, shapes=True)[0]
        cv3 = cmds.circle (c=(0,0,0),nr=(0,0,1),sw=360,r=1,d=3,ut=0,ch=0)[0]
        cv3Shape = cmds.listRelatives (cv3, shapes=True)[0]
        cmds.makeIdentity ([cv1,cv2,cv3],apply=True,t=1,r=1,s=1,n=0)
        cmds.parent ([cv2Shape,cv3Shape], cv1, shape=True, r=True)
        cmds.delete (cv2, cv3)
             
    elif icone== "cubo":
        cmds.curve (n=name+"_cntrl", d=1,p=[(-0.5,0.5,0.5), (-0.5,0.5,-0.5), (0.5,0.5,-0.5),(0.5,0.5,0.5),(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),(-0.5,0.5,0.5),(-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(-0.5,0.5,-0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(0.5,-0.5,0.5)],k=[0,1,2,3,4 ,5,6,7,8,9,10,11,12,13,14,15,16])
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=1,r=1,s=1,n=0)
    elif icone=='grp':
        cmds.group (  n=name+"_cntrl", empty=True)
         
    cmds.setAttr (name+"_cntrl.rotateOrder", 1)
    grp = cmds.group (name+"_cntrl", n=name+"_grp")
    cmds.setAttr (grp+'.rotateOrder', 1)
    cmds.xform (grp, os=True, piv=[0,0,0])
    pos = cmds.xform (targetName, q=True,  ws=True ,rp=True) 
    rot = cmds.xform (targetName, q=True,  ws=True ,ro=True)
    cmds.xform (grp, ws=True,  t=pos)
    cmds.xform (grp, ws=True,  ro=rot)
    cmds.xform (grp, ws=True, s=[cntrlScale,cntrlScale,cntrlScale])
    return name+"_cntrl"

def doCntrl (name,targetName,radius,icone, cntrlScale,rp=False):
    if icone == "circuloX" :
        cmds.circle (n=name+'_cntrl',r=radius,ch=True,o=True,nr=[1, 0, 0],s=5)
    elif icone == "circuloY":
        cmds.circle (n=name+'_cntrl',r=radius,ch=True,o=True,nr=[0, 1, 0],s=5)
    elif icone == "circuloZ":
        cmds.circle (n=name+'_cntrl',r=radius,ch=True,o=True,nr=[0, 0, 1],s=5)
    elif icone == "quadradoX":
        cmds.curve(n=name+"_cntrl",d=1,p=[(-3.984495, 0, 4.073894),(-3.940628, 0, -4.041594),(3.99939,0, -3.997726),(3.99939, 0, 4.073894),(-3.89676,0, 4.117762)],k=[0,1,2, 3, 4] )
        cmds.setAttr (name+"_cntrl.rotateZ",-90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "quadradoY":
        cmds.curve(n=name+"_cntrl",d=1,p=[(-3.984495, 0, 4.073894),(-3.940628, 0, -4.041594),(3.99939,0, -3.997726),(3.99939, 0, 4.073894),(-3.89676,0, 4.117762)],k=[0,1,2, 3, 4] )
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "quadradoZ":
        cmds.curve(n=name+"_cntrl",d=1,p=[(-3.984495, 0, 4.073894),(-3.940628, 0, -4.041594),(3.99939,0, -3.997726),(3.99939, 0, 4.073894),(-3.89676,0, 4.117762)],k=[0,1,2, 3, 4] )
        cmds.setAttr (name+"_cntrl.rotateZ",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "ponteiroX":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0, 0, 0),(1.691495,1.691495,0),(1.697056, 2.537859, 0),(2.545584, 2.545584, 0),(2.545584, 1.707095, 0),(1.691504, 1.692763, 0)], k=[0 ,1,2, 3, 4, 5])
        cmds.setAttr (name+"_cntrl.rotateZ",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "ponteiroY":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0, 0, 0),(1.691495,1.691495,0),(1.697056, 2.537859, 0),(2.545584, 2.545584, 0),(2.545584, 1.707095, 0),(1.691504, 1.692763, 0)], k=[0 ,1,2, 3, 4, 5])
        cmds.setAttr (name+"_cntrl.rotateY",90)
        cmds.setAttr (name+"_cntrl.rotateX",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    elif icone == "ponteiroZ":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0, 0, 0),(1.691495,1.691495,0),(1.697056, 2.537859, 0),(2.545584, 2.545584, 0),(2.545584, 1.707095, 0),(1.691504, 1.692763, 0)], k=[0 ,1,2, 3, 4, 5])
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone == "trianguloX":
        cmds.curve (n=name+"_cntrl",d=1,p=[(0,0,-0.471058),(-0.471058,0,0.471058),(0.471058,0,0.471058),(0,0,-0.471058)] ,k=[0,1, 2, 3])
        cmds.setAttr (name+"_cntrl.rotateX",90)
        cmds.setAttr (name+"_cntrl.rotateY",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone == "trianguloY":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0,0,-0.471058),(-0.471058,0,0.471058),(0.471058,0,0.471058),(0,0 ,-0.471058)] ,k=[0,1, 2, 3])
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone == "trianguloZ":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0,0,-0.471058),(-0.471058,0,0.471058),(0.471058,0,0.471058),(0,0 ,-0.471058)] ,k=[0,1, 2, 3])
        cmds.setAttr (name+"_cntrl.rotateX",90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    	    
    elif icone == "ponteiroReto":
        cmds.curve(n=name+"_cntrl",d=1,p=[(0,0,0), (0, 1.414597, 0),(0.569164, 2, 0),( 0, 2.569164, 0),(-0.569164, 2, 0),( 0.00139909, 1.432235, 0)] ,k=[0,1,2,3,4, 5])
        cmds.setAttr (name+"_cntrl.rotateY", 90)
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=0,r=1,s=0,n=0)
    
    elif icone =='bola':
        cv1 = cmds.circle (n=name+"_cntrl" , c=(0,0,0),nr=(0,1,0),sw=360,r=1,d=3,ut=0,ch=0)[0]
        cv2 = cmds.circle (c=(0,0,0),nr=(1,0,0),sw=360,r=1,d=3,ut=0,ch=0)[0]
        cv2Shape = cmds.listRelatives (cv2, shapes=True)[0]
        cv3 = cmds.circle (c=(0,0,0),nr=(0,0,1),sw=360,r=1,d=3,ut=0,ch=0)[0]
        cv3Shape = cmds.listRelatives (cv3, shapes=True)[0]
        cmds.makeIdentity ([cv1,cv2,cv3],apply=True,t=1,r=1,s=1,n=0)
        cmds.parent ([cv2Shape,cv3Shape], cv1, shape=True, r=True)
        cmds.delete (cv2, cv3)
             
    elif icone== "cubo":
        cmds.curve (n=name+"_cntrl", d=1,p=[(-0.5,0.5,0.5), (-0.5,0.5,-0.5), (0.5,0.5,-0.5),(0.5,0.5,0.5),(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5),(-0.5,0.5,0.5),(-0.5,-0.5,0.5),(-0.5,-0.5,-0.5),(-0.5,0.5,-0.5),(-0.5,-0.5,-0.5),(0.5,-0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(0.5,-0.5,0.5)],k=[0,1,2,3,4 ,5,6,7,8,9,10,11,12,13,14,15,16])
        cmds.setAttr (name+"_cntrl.scaleX", radius)
        cmds.setAttr (name+"_cntrl.scaleY", radius*cntrlScale)
        cmds.setAttr (name+"_cntrl.scaleZ", radius*cntrlScale)
        cmds.makeIdentity ( name+"_cntrl",apply=True,t=1,r=1,s=1,n=0)
    elif icone=='grp':
        cmds.group (  n=name+"_cntrl", empty=True)
         
    cmds.setAttr (name+"_cntrl.rotateOrder", 1)
    grp = cmds.group (name+"_cntrl", n=name+"_grp")
    cmds.setAttr (grp+'.rotateOrder', 1)
    cmds.xform (grp, os=True, piv=[0,0,0])

    if rp:
        print 'rp'
        pos = cmds.xform (targetName, q=True,  ws=True , rp=True)
        rot = cmds.xform (targetName, q=True,  ws=True , ro=True)
        cmds.xform (grp, ws=True,  t=pos )
        cmds.xform (grp, ws=True,  ro=rot )
    else:
        matrix = cmds.xform (targetName, q=True,  ws=True , m=True) 
        cmds.xform (grp, ws=True,  m=matrix )
                        
    cmds.xform (grp, ws=True, s=[cntrlScale,cntrlScale,cntrlScale])
    return name+"_cntrl"
    
def copyMirror (obj,dir,  find, replace):
    cpObj = copy.deepcopy(obj)
    cpObj.name = obj.name.replace (find, replace)
    newGlobalGuide = obj.guideGlobal.replace (find, replace)
    if cmds.objExists (newGlobalGuide):
        cmds.delete (newGlobalGuide)
    cpObj.guideGlobal = obj.guideGlobal    
    dup  = cmds.duplicate (obj.guideGlobal, rr=True, un=True) [0]
    cmds.rename (dup, newGlobalGuide)
    cpObj.guideGlobal = newGlobalGuide

    listObjs = cmds.listRelatives (cpObj.guideGlobal, ad=True, type='transform', path=True)
    for child in listObjs:
        newNome = child.replace (find, replace)
        cmds.rename (child, newNome.split('|')[-1])
    
    if hasattr (cpObj, 'fingerList'):
        if dir =='-X':
            for f in cpObj.fingerList:
                f.name=f.name.replace ('L_', 'R_')
        elif dir=='+X':
            for f in cpObj.fingerList:
                f.name=f.name.replace ('R_', 'L_')            
    cpObj.doMirrorGuide (dir)
    return cpObj


def createSpc (driver, name):
	drvGrp = cmds.group (empty=True, n=name+'_drv')
	if driver:
		cmds.parentConstraint (driver, drvGrp)
	spcGrp = cmds.group (empty=True, n=name+'_spc')
	cmds.parent (spcGrp, drvGrp)
        
def addSpc (target, space, switcher, type):
	
	if type=='parent':
		cns = cmds.parentConstraint (space+'_spc', switcher, mo=True)[0]
	elif type=='orient':
		cns =  cmds.orientConstraint (space+'_spc', switcher)[0]
	
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
		
	cond = cmds.createNode ('condition', n=switcher+space+'Cond')
	print cond
	print target
	cmds.connectAttr (target+'.spcSwitch', cond+'.firstTerm')
	cmds.setAttr (cond+'.secondTerm', index)
	cmds.setAttr (cond+'.operation', 0)
	cmds.setAttr (cond+'.colorIfTrueR', 1)
	cmds.setAttr (cond+'.colorIfFalseR', 0)     
	cmds.connectAttr (cond+'.outColor.outColorR', cns+'.'+space+'_spcW'+str(index))
	
	
def doCntrlClicked(*args):
    sele=cmds.ls (sl=True)
    tipo = cmds.optionMenu('cntrlMenu', q=True, v=True )
    rp =   cmds.checkBox('rpChk',query=True, value=True)
    print rp 
    for obj in sele: 
        cntrl = doCntrl (obj,obj,.5, tipo, 1, rp)
        cmds.parentConstraint (cntrl, obj, mo=True)

def doCntrlWin():
    options = ['cubo','bola','ponteiroReto',
                "circuloX","circuloY","circuloZ",
                "quadradoX","quadradoY","quadradoZ",
                "ponteiroX","ponteiroY","ponteiroZ",
                "trianguloX","trianguloY","trianguloZ"]           
                          
    if (cmds.window ('doCntrlOptions', exists=True)):
        cmds.deleteUI ('doCntrlOptions', window=True)
    cmds.window ('doCntrlOptions', w=170)
    cmds.columnLayout ( columnAttach=('both', 10))
    cmds.text (l='tipo')
    a = cmds.optionMenu('cntrlMenu', w=150)
    print a
    for op in options:
        cmds.menuItem (label=op)
    x = cmds.checkBox( 'rpChk' , l = 'rp', value=False)
    print x
    cmds.text (l='escala')
    cmds.textField ('scl', tx='0.5', w=150)
    cmds.text (l='')
    cmds.button ('do cntrls',w=150, h=40, c = doCntrlClicked )
    cmds.showWindow('doCntrlOptions')
