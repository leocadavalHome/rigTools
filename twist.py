import pymel.core as pm
import lcRigToolbox as tbox
import lcGeneric as gen

class twistExtractor:
    def __init__(self, twistJntIn):
        
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
        pm.parentConstraint (twistJnt, extractorIkh)
        pm.parent (extractorIkh, extractorGrp )
        
        # multiplica por 2 o valor de rot do locator
        pm.addAttr (extractorLoc, ln='extractTwist', at='double', k=1)
        multi = pm.createNode ('multDoubleLinear')
        multi.input2.set(2)
        extractorLoc.rotateX >> multi.input1
        multi.output >> extractorLoc.extractTwist
        
extr1 =  twistExtractor ('joint13')
extr2 =  twistExtractor ('joint9')