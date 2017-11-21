import maya.cmds as cmds
import os.path

def setCamera(cam):
    if cam=='sequence' or cam=='allshots':
        cmds.sequenceManager(e=True, modelPanel='previewer')
        cmds.textField('camTxt', e=True, tx=cam)
    else:
        print cam  
        camShape=cmds.listRelatives(cam, children=True)[0]
        print camShape
        cmds.setAttr (camShape+'.overscan', 1)
        cmds.setAttr (camShape+'.filmFit', 3)
        cmds.setAttr (camShape+'.displayFieldChart', 0)
        cmds.setAttr (camShape+'.displaySafeAction', 0)
        cmds.setAttr (camShape+'.displaySafeTitle', 0)
        cmds.setAttr (camShape+'.displayFilmOrigin', 0)
        cmds.setAttr (camShape+'.displayFilmPivot', 0)
        cmds.setAttr (camShape+'.displayResolution', 0)
        cmds.modelEditor("previewer", e=True, camera=cam)
        cmds.textField('camTxt', e=True, tx=cam)
        print 'ok'

def refreshSceneName():
    nome = cmds.file (q=True, shn=True,sn=True)[0:-3]
    cmds.textField('NameTxt', e=True, tx=nome)
    print nome
    print 'mudou nome'
    
    camsInScene = getSceneCameras()
    if camsInScene:
        cmds.textField('camTxt', e=True, tx=camsInScene[0])
        cmds.popupMenu ('camMenu', e=True, dai=True )
        setCamera(camsInScene[0])
        for cam in camsInScene:
            cmds.menuItem (label=cam,c=lambda x: setCamera(cam), p='camMenu')                                  
    audios=cmds.ls (type='audio')
    if audios:
        cmds.textField('audioTxt', e=True, tx=audios[0])
        cmds.popupMenu ('audioMenu', e=True, dai=True)
        
        for aud in audios:
            cmds.menuItem (label=aud, c='cmds.textField("audioTxt", e=True,tx="'+aud+'")', p='audioMenu')
    setHUD()
    
def browsePreview():
    projectPath = cmds.workspace(q=True, rd=True)
    nome =  cmds.textField('NameTxt',q=True, tx=True)
    path =  cmds.textField('dirTxt',q=True, tx=True) 
    if  path == '/movies':
        startdir= projectPath+os.path.join('movies')
    else:
        startdir = cmds.textField('dirTxt', q=True, tx=True)
    fullPath = cmds.fileDialog2(okc='open', fm=3, dir=startdir)
    if fullPath:
        cmds.textField('dirTxt', e=True,  tx=fullPath[0])

def getSceneCameras():
    camShapes=cmds.ls (ca=True)
    orto=['frontShape','perspShape','sideShape','topShape', 'backShape']
    camShapes = [x for x in camShapes if x not in orto]
    cameras=[]
    for cam in camShapes:
        transf=cmds.listRelatives (cam, parent=True)
        if transf:
            cameras.append(transf[0])
    return cameras

def setHUD():
    animName = ''
    nome = cmds.file (q=True, shn=True,sn=True)[0:-3]   
    
    if not cmds.headsUpDisplay(nfb=0)==0:
        cmds.headsUpDisplay(rp = (0,0))
    if not cmds.headsUpDisplay(nfb=9)==0:    
        cmds.headsUpDisplay(rp = (9,0))
    if not cmds.headsUpDisplay(nfb=4)==0:
        cmds.headsUpDisplay(rp = (4,0))
    if not cmds.headsUpDisplay(nfb=7)==0:
        cmds.headsUpDisplay(rp = (7,0))
    
    if cmds.headsUpDisplay( 'HUDFileName' , exists=True ):
        cmds.headsUpDisplay( 'HUDFileName' , rem=True )
    if cmds.headsUpDisplay( 'HUDAnimator' , exists=True ):
        cmds.headsUpDisplay( 'HUDAnimator' , rem=True )
    if cmds.headsUpDisplay( 'HUDCurrentFr' , exists=True ):
        cmds.headsUpDisplay( 'HUDCurrentFr' , rem=True )
    if cmds.headsUpDisplay( 'HUDFocalLength' , exists=True ):
        cmds.headsUpDisplay( 'HUDFocalLength' , rem=True )

    cmds.headsUpDisplay( 'HUDFocalLength', section=7, block=0, blockSize='medium',labelFontSize='large',dataFontSize='large', c =getFocal, ev= 'timeChanged', label='')
    cmds.expression( s='headsUpDisplay -r HUDFocalLength' )
    #cmds.headsUpDisplay( 'HUDFocalLength',e=True, section=5, block=0, blockSize='medium',labelFontSize='large',dataFontSize='large', label='')       
    cmds.headsUpDisplay( 'HUDFileName', section=0, block=0, blockSize='medium', label=nome, labelFontSize='large')    
    cmds.headsUpDisplay( 'HUDAnimator', section=4, block=0, blockSize='medium', label=(animName), labelFontSize='large')    
    cmds.headsUpDisplay ('HUDCurrentFr', section=9, block=0,blockSize='medium', labelFontSize='large', dataFontSize='large', pre ='currentFrame' )

#cmds.headsUpDisplay(le=True)

def getFocal():
    cam = cmds.modelEditor('previewer', q=True, camera=True)
    camShape = cmds.listRelatives (cam, s=True)[0]
    focal = int (cmds.getAttr (camShape+'.focalLength'))
    return focal

def setDisplayPrefs():
    cmds.modelEditor('previewer',e=True,rnm='vp2Renderer' )
    cmds.modelEditor('previewer',e=True,da='smoothShaded',alo=False,ns=True,pm=True)
    cmds.modelEditor("previewer",e=True, dl="all")
    cmds.modelEditor("previewer",e=True, dtx=True)
    cmds.modelEditor("previewer",e=True, hud=True)
    cmds.setAttr ('hardwareRenderingGlobals.ssaoEnable', 1)
    
def doPlayBlast(*args):
    projectPath = cmds.workspace(q=True, rd=True)
    nome =  cmds.textField('NameTxt',q=True, tx=True)
    path =  cmds.textField('dirTxt',q=True, tx=True) 
    if  path == '/movies':
        fname= projectPath+os.path.join('movies',nome+'.mov')
    else:
        fname = os.path.join(path,nome+'.mov')   
    audio = cmds.textField('audioTxt', q=True, tx=True)
    cameraName = cmds.textField('camTxt', q=True, tx=True)
    print fname
    print audio
    
    cmds.modelEditor('previewer', e=True, activeView=True)
    if cameraName=='sequence':
        allShots = cmds.ls (type='shot')
        endAll= -10000
        lastEnd = -10000
        startAll = 10000
        lastStart = 10000
        for member in allShots:
            seqEnd= cmds.shot (member, q=True, set=True)
            seqStart= cmds.shot (member, q=True, sst=True)
            end=int(seqEnd)
            start = int(seqStart)
            endAll = max (end, lastEnd)
            startAll = min(start, lastStart)
            lastStart = startAll
            lastEnd = endAll
        print  startAll, endAll
        cmds.playblast  (fmt="qt", startTime=startAll , endTime=endAll , useTraxSounds=True, sequenceTime=True, forceOverwrite=1, filename=fname, clearCache=1, showOrnaments=1, percent=100, wh=(1280,720), offScreen=1, viewer=0, compression="H.264", quality=100)    
    
    elif cameraName =='allshots':
        allShots = cmds.ls (type='shot')
        for member in allShots:
            seqEnd= cmds.shot (member, q=True, set=True)
            seqStart= cmds.shot (member, q=True, sst=True)
            cmds.playblast  (fmt="qt", startTime=seqStart , endTime=seqEnd , useTraxSounds=True, sequenceTime=True, forceOverwrite=1, filename=fname+'_'+member, clearCache=1, showOrnaments=1, percent=100, wh=(1280,720), offScreen=1, viewer=0, compression="H.264", quality=100)                          
    else:
        
        cameraShape = cmds.listRelatives(cameraName, s=True)[0]
        print cameraShape
        shotConnected = cmds.listConnections (cameraShape, s=False, d =True, type='shot')
        if shotConnected:
            for sht in shotConnected:
                seqEnd= cmds.shot (sht, q=True, set=True)
                seqStart= cmds.shot (sht, q=True, sst=True)
                print seqEnd, seqStart
                useShotRange = cmds.confirmDialog( title='shot', message='Use shot range?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
                print useShotRange
                if useShotRange=='Yes':
                    cmds.playblast  (fmt="qt",startTime=seqStart , endTime=seqEnd, useTraxSounds=True, sequenceTime=True, forceOverwrite=1, filename=fname+'_'+sht, clearCache=1, showOrnaments=1, percent=100, wh=(1280,720), offScreen=1, viewer=0, compression="H.264", quality=100)
                else:
                    cmds.playblast  (fmt="qt",sound=audio, forceOverwrite=1, filename=fname+'_'+sht, clearCache=1, showOrnaments=1, percent=100, wh=(1280,720), offScreen=1, viewer=0, compression="H.264", quality=100)
        else:
            cmds.playblast  (fmt="qt",sound=audio, forceOverwrite=1, filename=fname, clearCache=1, showOrnaments=1, percent=100, wh=(1280,720), offScreen=1, viewer=0, compression="H.264", quality=100)            

def previewer():
    print 'versao 1.2'
    if (cmds.window ('previewerWin', exists=True)):
    	cmds.deleteUI ('previewerWin', window=True)
    	
    window = cmds.window('previewerWin', width=1280, height=720, sizeable=False)
    
    form = cmds.formLayout(height = 720,width = 1430)
    editor = cmds.modelEditor('previewer')
    
    column = cmds.columnLayout('Menus', rowSpacing=5, width = 150,cal='center' )    
    
    nome = cmds.file (q=True, shn=True,sn=True)[0:-3]
    cmds.text(l='nome')
    cmds.textField('NameTxt', width = 150, height = 20, tx=nome)    
    cmds.text(l='animador')
    cmds.textField('animTxt', width = 150, height = 20, tx='') 
    cmds.popupMenu (button=1)
    cmds.menuItem (label='LEO',c='cmds.textField("animTxt", e=True, tx="LEO");cmds.headsUpDisplay( "HUDAnimator",e=True, label="LEO")')
    cmds.menuItem (label='RENAN',c='cmds.textField("animTxt", e=True, tx="RENAN");cmds.headsUpDisplay( "HUDAnimator",e=True, label="RENAN")')
    cmds.menuItem (label='ROGERIO',c='cmds.textField("animTxt", e=True, tx="ROGERIO");cmds.headsUpDisplay( "HUDAnimator",e=True, label="ROGERIO")')
            
    cmds.text(l='camera')
    cmds.textField('camTxt', width = 150, height = 20, tx='no camera') 
    cmds.popupMenu ('camMenu', button=1 )
    ########SETA CAMERA#########
    camsInScene = getSceneCameras()
    if camsInScene:
        setCamera(camsInScene[0])
        for cam in camsInScene:
            cmds.menuItem (label=cam,c='pb.setCamera("'+cam+'")')
        cmds.menuItem (label='sequence',c=lambda x: setCamera("sequence"))
        cmds.menuItem (label='allshots',c=lambda x: setCamera("allshots"))
    else:
        cmds.textField('cameraTxt', width = 150, height = 20, tx='no camera')
 
    ########SETA AUDIO#########         
    cmds.text(l='audio')
    audios=cmds.ls (type='audio')
    if audios:
        cmds.textField('audioTxt', width = 150, height = 20, tx=audios[0])
        cmds.popupMenu ('audioMenu', button=1)
        for aud in audios:
            cmds.menuItem (label=aud, c='cmds.textField("audioTxt", e=True,tx="'+aud+'")')
    else:
        cmds.textField('audioTxt', width = 150, height = 20, tx='no audio')
    
    ####### 
    
    cmds.text(l='  ')
    cmds.text(l='Display Options')    
    cmds.checkBox ('hudCheck', l='hud',v=True, onc='cmds.modelEditor("previewer",e=True, hud=True)', ofc='cmds.modelEditor("previewer",e=True, hud=False)')
    cmds.checkBox ('texCheck', l='textured',v=True, onc='cmds.modelEditor("previewer",e=True, dtx=True)', ofc='cmds.modelEditor("previewer",e=True, dtx=False)')
    cmds.checkBox ('occCheck', l='occlusion',v=True, onc='cmds.setAttr ("hardwareRenderingGlobals.ssaoEnable", 1)', ofc='cmds.setAttr ("hardwareRenderingGlobals.ssaoEnable", 0)')
    cmds.checkBox ('lightsCheck', l='use light',v=True, onc='cmds.modelEditor("previewer",e=True, dl="all")', ofc='cmds.modelEditor("previewer",e=True, dl="default")')
    cmds.checkBox ('greenCheck', l='fundo verde',v=False, onc='cmds.displayRGBColor( "background", 0, 1, 0 )', ofc='cmds.displayRGBColor( "background", 0.461, 0.461, 0.461)')

    cmds.text(l='  ')    
    cmds.button(label = '...', width = 50, height = 20, command=browsePreview)
    cmds.textField('dirTxt', width = 150, height = 20, tx=r'/movies')
    cmds.popupMenu (button=1)
    cmds.menuItem (label='/movies',c='cmds.textField("dirTxt", e=True, tx="/movies")')
    cmds.button(label = 'playblast', width = 150, height = 50, command=doPlayBlast)
    

    cmds.formLayout(form, edit=True, attachForm=[(column, 'top', 0), (column, 'left', 0), (editor, 'top', 0), (editor, 'bottom', 0), (editor, 'right', 0)], 
                    attachNone=[(column, 'bottom'), (column, 'right')], 
                    attachControl=(editor, 'left', 0, column))
   

    cmds.showWindow('previewerWin')
    setHUD()
    setDisplayPrefs()    
    cmds.scriptJob ( event=['SceneOpened','pb.refreshSceneName()'],  p='previewerWin' )