import pymel.core as pm
import pymel.core.windows as pmWin
import maya.OpenMaya as om

widgets={}        
def spcMatchUI():  
	if (pmWin.window ('window', exists=True)):
	    pm.deleteUI ('window', window=True)
	
	widgets['win']=pmWin.window ('window', title='Snap', h=400, w= 300)
	widgets['topFrame']=pmWin.frameLayout (l='IKFK', w=300)
	widgets['topColumn']= pmWin.columnLayout()
	widgets['text1']=pmWin.text (l='select IKFK cntrl and press the button')
	widgets['ikfkButton']=pmWin.button (l='ikfk snap', w=300, h=50 , c=ikfkMatch)
	
	
	widgets['topFrame2']=pmWin.frameLayout (l='SPACE SWITCH', w=300)
	widgets['topColumn2']= pmWin.columnLayout()
	widgets['text1']=pmWin.text (l='select obj, press the button. Choose the availble space ')
	widgets['objTFG'] = pmWin.textFieldGrp (l='selected Object', w=300)
	widgets['objButton']=pmWin.button (l='get spaces for selection', w=300,h=50, c=getObj)
	
	
	pmWin.setParent (widgets['win'])    
	widgets['bottonFrame']= pmWin.frameLayout (l='space selection', w=300)
	widgets['bottomColumn']=pmWin.columnLayout()
		
	pmWin.showWindow (widgets['win'])

def clearList (*args):
    pmWin.deleteUI (widgets['bottomColumn'])
    widgets['bottomColumn']=pmWin.columnLayout (p=widgets['bottonFrame'])
    
   
def spaceMatch (value, *args):
    objName = pmWin.textFieldGrp (widgets['objTFG'], q=True, tx= True)
    obj= pm.ls (objName)[0]
    wst = pm.xform (obj.name(), q=True, ws=True, t=True)
    wsr = pm.xform (obj.name(), q=True, ws=True, ro=True)
    
    obj.spcSwitch.set(value)
    
    pm.xform (obj.name(), ws=True, t=wst)
    pm.xform (obj.name(), ws=True, ro=wsr)
    

def getObj (*args):   
    sele = pm.selected()
    if sele:
        clearList()
        obj=sele[0]
        
        pmWin.textFieldGrp (widgets['objTFG'], e=True, tx=obj.name())
        
        if obj.hasAttr('spcSwitch'):
            spcListRaw = pm.attributeQuery ('spcSwitch',node = obj, le=True) 
            spcList = spcListRaw[0].split (':')
            print spcList
            
            for i in range (len(spcList)):
                widgets['value%s'%i] = pmWin.button (l=spcList[i], w=300, h=50, c=pm.Callback (spaceMatch, i))

def ikfkMatch(*args):
    sele = pm.selected()
    if sele:
        obj=sele[0]
        ikfkSwitch = obj.message.outputs()[0]
        print ikfkSwitch
                
        if ikfkSwitch.tp.get()=='limb':       
            if ikfkSwitch.IKFK.get()  == 1:
                limbToFk (ikfkSwitch)                
            elif  ikfkSwitch.IKFK.get()== 0:
                limbToIk (ikfkSwitch)                          
        elif ikfkSwitch.tp.get()=='spine': 
            if ikfkSwitch.IKFK.get() == 1:
                spineToFk (ikfkSwitch)        
            elif ikfkSwitch.IKFK.get() == 0:
                 spineToIk (ikfkSwitch)
        elif ikfkSwitch.tp.get()=='foot':
            
            leg = ikfkSwitch.attr('from').inputs()[0]
            
            if ikfkSwitch.IKFK.get() == 1:
                limbToFk (leg)        
            elif ikfkSwitch.IKFK.get() == 0:
                limbToIk (leg)
            
                 
def spineToFk (ikfkSwitch):
    ikJnt0 = ikfkSwitch.attr('ikJnt1').inputs()[0]
    ikJnt1 = ikfkSwitch.attr('ikJnt2').inputs()[0]
    fk0 = ikfkSwitch.attr('fk1').inputs()[0]
    fk1 = ikfkSwitch.attr('fk2').inputs()[0]
    print 'ik'
    wst1 = pm.xform (ikJnt0, ws=True, q=True, t=True)
    pm.xform (fk0, ws=True, t=wst1)        
    wsr1 = pm.xform (ikJnt0, ws=True, q=True, ro=True)
    pm.xform (fk0, ws=True, ro=wsr1)
        
    wst2 = pm.xform (ikJnt1, ws=True, q=True, t=True)
    pm.xform (fk1, ws=True, t=wst2)        
    wsr2 = pm.xform (ikJnt1, ws=True, q=True, ro=True)
    pm.xform (fk1, ws=True, ro=wsr2)
    
    #ikfkSwitch.IKFK.set(0)
    
    x = pm.listConnections (ikfkSwitch+'.IKFK', s=True, d=False,p=True)[0]
    print x
    x.set(0)
    
    
    pm.select (cl=True)

def spineToIk (ikfkSwitch):
    fkJnt0 = ikfkSwitch.attr('fkJnt1').inputs()[0]
    fkJnt1 = ikfkSwitch.attr('fkJnt2').inputs()[0]    
    ik0 = ikfkSwitch.attr('ik1').inputs()[0]
    ik1 = ikfkSwitch.attr('ik2').inputs()[0]
    print 'fk'
    wst1 = pm.xform (fkJnt0, ws=True, q=True, t=True)
    pm.xform (ik0, ws=True, t=wst1)        
    wsr1 = pm.xform (fkJnt0, ws=True, q=True, ro=True)
    pm.xform (ik0, ws=True, ro=wsr1)
        
    wst2 = pm.xform (fkJnt1, ws=True, q=True, t=True)
    pm.xform (ik1, ws=True, t=wst2)        
    wsr2 = pm.xform (fkJnt1, ws=True, q=True, ro=True)
    pm.xform (ik1, ws=True, ro=wsr2)
    
    
    x = pm.listConnections (ikfkSwitch+'.IKFK', s=True, d=False,p=True)[0]
    print x
    x.set(1)
	
    pm.select (cl=True)

def limbToFk (ikfkSwitch):
    
    ikJnt1 = ikfkSwitch.attr('ikJnt0').inputs()[0]
    ikJnt2 = ikfkSwitch.attr('ikJnt1').inputs()[0]  
    ikJnt3 = ikfkSwitch.attr('ikJnt2').inputs()[0]     
    fk1= ikfkSwitch.attr('fk0').inputs()[0]
    fk2= ikfkSwitch.attr('fk1').inputs()[0]
    fk3= ikfkSwitch.attr('fk2').inputs()[0]
    
    
    wst1 = pm.xform (ikJnt1, ws=True, q=True, t=True)
    pm.xform (fk1, ws=True, t=wst1) 
    wsr1 = pm.xform (ikJnt1, ws=True, q=True, ro=True)
    pm.xform (fk1, ws=True, ro=wsr1)
    
    wst2 = pm.xform (ikJnt2, ws=True, q=True, t=True)
    pm.xform (fk2, ws=True, t=wst2)    
    wsr2 = pm.xform (ikJnt2, ws=True, q=True, ro=True)
    pm.xform (fk2, ws=True, ro=wsr2) 
     
    wst3 = pm.xform (ikJnt3, ws=True, q=True, t=True)
    pm.xform (fk3, ws=True, t=wst3) 
    wsr3 = pm.xform (ikJnt3, ws=True, q=True, ro=True)
    pm.xform (fk3, ws=True, ro=wsr3)
    
    x = pm.listConnections (ikfkSwitch+'.IKFK', s=True, d=False,p=True)[0]
    print x
    x.set(0)
	
    pm.select (cl=True)    
    
def limbToIk (ikfkSwitch):
    inp= ikfkSwitch.to.inputs()
    if inp:
        foot=inp[0]
        fkJnt0= foot.attr ('fkJnt0').inputs()[0]
        ik0=foot.attr ('ik0').inputs()[0]
        wst = pm.xform (fkJnt0, ws=True, q=True, t=True)
        wsr = pm.xform (fkJnt0, ws=True, q=True, ro=True)
        pm.xform (ik0, ws=True, t=wst)
        pm.xform (ik0, ws=True, ro=wsr)
       
    fkJnt1 = ikfkSwitch.attr('fkJnt0').inputs()[0]
    fkJnt2 = ikfkSwitch.attr('fkJnt1').inputs()[0]  
    fkJnt3 = ikfkSwitch.attr('fkJnt2').inputs()[0]     
    ik1= ikfkSwitch.attr('ik0').inputs()[0]
    ikUp= ikfkSwitch.attr('ikUp').inputs()[0]
    
    fk3Raw = pm.xform (fkJnt3, ws=True, q=True, t=True)
    fk3Pos = om.MVector (fk3Raw[0], fk3Raw[1], fk3Raw[2])
    
    fk2Raw = pm.xform (fkJnt2, ws=True, q=True, t=True)
    fk2Pos = om.MVector (fk2Raw[0], fk2Raw[1], fk2Raw[2])

    fk1Raw = pm.xform (fkJnt1, ws=True, q=True, t=True)
    fk1Pos = om.MVector (fk1Raw[0], fk1Raw[1], fk1Raw[2])
    
    fk3Rot = pm.xform (fkJnt3, ws=True, q=True, ro=True)
    pm.xform (ik1, ws=True, ro=fk3Rot)
    pm.move (fk3Pos.x, fk3Pos.y, fk3Pos.z, ik1)
    
    midPoint = (fk3Pos + fk1Pos)/2
    pvOrigin = fk2Pos - midPoint
    pvRaw = pvOrigin *2
    pvPos = pvRaw + midPoint
    pm.move (pvPos.x, pvPos.y, pvPos.z, ikUp)
    
    x = pm.listConnections (ikfkSwitch+'.IKFK', s=True, d=False,p=True)[0]
    print x
    x.set(1)
	
    pm.select (cl=True)
