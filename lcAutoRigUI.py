import maya.cmds as cmds
import lcRig as rig
import lcGeneric as gen
reload(rig)
reload (gen)

class AutoRigUI:
    def __init__(self):
		self.win = cmds.loadUI (f = r'C:\Users\leo.cadaval\AppData\Roaming\VetorLobo\MayaAppDir\scripts\lcAutoRig.ui')
		cmds.showWindow (self.win)
		
		cmds.textField ('nameTxtField', e=True, text='Char')
		cmds.button ('guideBtn', e = True, c = self.doGuideUI)
		cmds.button ('browseGuidesBtn', e = True, c = self.browseGuide)
		cmds.button ('saveGuideBtn', e = True, c = self.saveGuideUI)
		cmds.button ('loadGuideBtn', e = True, c = self.loadGuideUI)
		cmds.button ('leftBtn', e = True, c = self.doLeftMirrorUI)
		cmds.button ('rightBtn', e = True, c = self.doRightMirrorUI)
		cmds.button ('rigBtn', e=True, c=self.doRigUI)
        
    def browseGuide(self,*args):
        fullPath = cmds.fileDialog2(okc='open', fm=2)
        if fullPath:
            cmds.textField('guidePathTxtField', e=True,  tx=fullPath[0])    
	
    def saveGuideUI(self,*args):
        print 'entrou'
        guidedir = cmds.textField ('guidePathTxtField', q=True, text=True)
        self.bp.saveAllGuides(guidedir)			

    def loadGuideUI(self,*args):
        guideFilename = cmds.textField ('guidePathTxtField', q=True, text=True)
        self.bp.loadAllGuides (guideFilename)
    		       
    def doGuideUI(self, *args):
        bpName = cmds.textField ('nameTxtField', q=True, text=True)
        self.bp=rig.Biped(bpName)
        self.bp.doGuide()
    
    def doLeftMirrorUI (self, *args):
        self.bp.doLeftMirrorGuide()
        
    def doRightMirrorUI (self, *args):
        self.bp.doRightMirrorGuide()
        
    def doRigUI (self, *args):
        self.bp.doRig()

def autoRig():
	x= AutoRigUI()
