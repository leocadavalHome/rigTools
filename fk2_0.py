
#///////////////////////////////////////////////////////////#
#--------------------Passo 1 - Preencher--------------------#

#Prefixo da cadeia:
prefix = "FK"

# Quantos joints terá a cadeia FK:
FKnum = 5 #incluindo "_end"

# Shape do controlador:
    # Circulo -> 1
    # Lupa    -> 2
    
shape = 1
#------------------------------------------------------------
#///////////////////////////////////////////////////////////#
#----------------------Passo 2 - Guide----------------------#

#guide()

#------------------------------------------------------------
#///////////////////////////////////////////////////////////#
#--------------------Passo 3 - Construcao-------------------#
 
#sistema()


#----------------------Fim da Interface------------------------
#///////////////////////////////////////////////////////////#


#----Construindo o Guide

import maya.cmds as cmds

validacao = cmds.ls(prefix + "_*")


if validacao != []:
    print ("# Sua cena já contém elemento(s) com esse nome! O(s) item(ns) abaixo foram selecionados:")
    intensExistentes = range(len(validacao))
    for indexSelecao in intensExistentes:
        print ("# - Está cena já contém um "+str(validacao[indexSelecao]))
    print ("# Exclua os itens selecionados ou escolha outro prefixo para o novo sistema.")
    cmds.select(validacao)
    pass
else:
    
    
    allPrefix = prefix+"_guide"
    modulos = list (range(FKnum))
    
    coordenadas = [""]
    cord_atual = 0
    
    
    #-----------------------------------------------------------------
    
    def guide():
        modulosPosIn = 0
        
        for indexGuide in modulos:
            moduloAtual = indexGuide + 1
            moduloAtual_xx = str(moduloAtual).zfill(2) #modulo com dois digitos
            
            if (moduloAtual == 1):
                cmds.circle (name=(allPrefix+"_ctrl"))
                cmds.setAttr((allPrefix+"_ctrl.tx"), modulosPosIn)
                cmds.setAttr((allPrefix+"_ctrl.ry"), 90)
                cmds.setAttr((allPrefix+"_ctrl.scale"), 2,2,2)
                cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                pass
            
            cmds.spaceLocator(name = allPrefix + "_" + moduloAtual_xx + "_loc")
            cmds.setAttr((allPrefix + "_" + moduloAtual_xx + "_loc.tx"), modulosPosIn)
            cmds.parent ((allPrefix + "_" + moduloAtual_xx + "_loc"),(allPrefix+"_ctrl"))
            
            modulosPosIn += 2
        
    #----Construindo o Sistema
    
    def sistema():
        cmds.select(clear=True)
        
        # recebendo a posicao dos locators na lista de coordenadas:
        for indexCoord in modulos:
            moduloAtual = indexCoord+1
            moduloAtual_xx = str(indexCoord+1).zfill(2) #modulo com dois digitos
            
            #recebendo as coordenadas dos locators na lista coordenadas
            #para objetos frizados o rotate pivot que guarda os valores
            coordenadas.append(cmds.xform(allPrefix + "_" + moduloAtual_xx + "_loc", q=True, rp=True, ws=True)) 
            
            # excluindo os locators da cena:
        cmds.delete(allPrefix+"_ctrl")
        
        # criando uma cadeia de joints sequencial
        for indexjntBase in modulos:
            moduloAtual = indexjntBase+1
            moduloAtual_xx = str(indexjntBase+1).zfill(2) #modulo com dois digitos
            moduloAnt_xx = str(indexjntBase).zfill(2) #modulo com dois digitos
            
            cmds.joint(name=(prefix + "_" + moduloAtual_xx + "_jntBase"))
            cmds.xform ((prefix + "_" + moduloAtual_xx + "_jntBase"), t = coordenadas[moduloAtual])
            
            if (indexjntBase > 0):
                cmds.parent ((prefix + "_" + moduloAtual_xx + "_jntBase"), (prefix + "_" + moduloAnt_xx + "_jntBase"))
                pass
        
            cmds.select(clear=True)

        # orientando os joints base:
        for indexOrient in modulos:
            if (indexOrient < (FKnum-1)):
                moduloAtual = indexOrient+1
                moduloAtual_xx = str(indexOrient+1).zfill(2) #modulo com dois digitos
                
                cmds.select (prefix + "_" + moduloAtual_xx + "_jntBase", hi=True)   
                cmds.joint (edit=True, oj="xyz", sao="xup")
                cmds.select (clear = True)
            
        # salvando a orientacao numa Lista:
        rotCoordenadas = [""]
            
        for indexRotCoord in modulos:
            moduloAtual = indexRotCoord+1
            moduloAtual_xx = str(indexRotCoord+1).zfill(2) #modulo com dois digitos
            
            rotCoordenadas.append (cmds.xform(prefix + "_" + moduloAtual_xx + "_jntBase", q=True, ro=True, ws=True)) 
        
        cmds.delete (prefix + "_01_jntBase", hi=True)   
        
        # criando os controladores:
        for indexCtrl in modulos:
            if (indexCtrl < (FKnum-1)):
                moduloAtual = indexCtrl+1
                
                moduloAtual_xx = str(indexCtrl+1).zfill(2) #modulo com dois digitos
                moduloAnt_xx = str(indexCtrl).zfill(2) #modulo anterior com dois digitos
    
                cmds.circle (name=(prefix + "_" + moduloAtual_xx + "_ctrl"))

                cmds.group ((prefix + "_" + moduloAtual_xx + "_ctrl"),name=(prefix + "_" + moduloAtual_xx + "_ctrl_grp"))

                cmds.xform ((prefix + "_" + moduloAtual_xx + "_ctrl"),ro=(0,90,0))
                cmds.select(prefix + "_" + moduloAtual_xx + "_ctrl")
                cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                
                cmds.xform ((prefix + "_" + moduloAtual_xx + "_ctrl_grp"), t=coordenadas[moduloAtual])
                cmds.xform ((prefix + "_" + moduloAtual_xx + "_ctrl_grp"), ro=rotCoordenadas[moduloAtual])
                
                if (indexCtrl > 0):
                    cmds.parent ((prefix + "_" + moduloAtual_xx + "_ctrl_grp"), (prefix + "_" + moduloAnt_xx + "_ctrl")) # parentesco entre os ctrls                    
                    pass
                
                cmds.select(clear=True)
                pass

        # criando os modulos:
        for indexCriacao in modulos:
            moduloAtual = indexCriacao+1
            moduloAnt_xx = str(indexCriacao+0).zfill(2) #modulo com dois digitos
            moduloAtual_xx = str(indexCriacao+1).zfill(2) #modulo com dois digitos
            moduloProx_xx = str(indexCriacao+2).zfill(2) #modulo com dois digitos
            
            # caso seja o primeiro ponto:
            if (moduloAtual == 1):
                
                jntList = ['_cnx', '_jnt', '_end']
                jntNum = range((len(jntList)))
                
                # Criando Grupos de organizacao
                cmds.group (name=(prefix + "_sys" ), em=True)
                cmds.xform(prefix + "_sys", t = coordenadas[moduloAtual])
                
                cmds.group (name=(prefix + "_ToParent" ), em=True)
                cmds.xform(prefix + "_ToParent", t = coordenadas[moduloAtual])
                cmds.setAttr((prefix + "_ToParent.tx"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.ty"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.tz"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.rx"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.ry"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.rz"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.sx"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.sy"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.sz"), k=0, cb=1)
                cmds.setAttr((prefix + "_ToParent.v"), k=0, cb=1)
                cmds.parent ((prefix + "_ToParent" ), (prefix + "_sys" ))
                
                cmds.group (name=(prefix + "_jnt_grp" ), em=True)
                cmds.xform(prefix + "_jnt_grp", t = coordenadas[moduloAtual])
                cmds.parent ((prefix + "_jnt_grp" ), (prefix + "_sys" ))
                #----cmds.setAttr ("%s_jnt_grp.visibility" % (prefix), False)
                cmds.group (name=(prefix + "_distance_grp" ), em=True)
                cmds.xform(prefix + "_distance_grp", t = coordenadas[moduloAtual])
                cmds.parent ((prefix + "_distance_grp" ), (prefix + "_sys" ))
                cmds.setAttr ("%s_distance_grp.visibility" % (prefix), False)
                
                #cmds.xform((prefix + "_sys"), t = coordenadas[moduloAtual], ro = rotCoordenadas[moduloAtual])

                cmds.setAttr((prefix + "_sys.tx"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.ty"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.tz"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.rx"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.ry"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.rz"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.sx"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.sy"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.sz"), l=1, cb=1)
                cmds.setAttr((prefix + "_sys.v"), l=1, cb=1)
                
                cmds.xform((prefix + "_" + moduloAtual_xx + "_ctrl_grp"), t = coordenadas[moduloAtual], ro = rotCoordenadas[moduloAtual])
                cmds.parent ((prefix + "_" + moduloAtual_xx + "_ctrl_grp"), (prefix + "_ToParent"))
                
                cmds.spaceLocator (name=(prefix + "_" + moduloAtual_xx + "_upVec_loc"))
                cmds.group ((prefix + "_" + moduloAtual_xx + "_upVec_loc"), name=(prefix + "_" + moduloAtual_xx + "_upVec_loc_grp"))
                cmds.xform((prefix + "_" + moduloAtual_xx + "_upVec_loc_grp"), t = coordenadas[moduloAtual], ro = rotCoordenadas[moduloAtual])
                cmds.xform((prefix + "_" + moduloAtual_xx + "_upVec_loc"), t = (-10,0,0))
                
                cmds.group (name=(prefix + "_" +  moduloAtual_xx + "_cnx_grp"), em=True)
                cmds.xform((prefix + "_" + moduloAtual_xx + "_cnx_grp"), t = coordenadas[moduloAtual], ro = rotCoordenadas[moduloAtual])
                cmds.parent ((prefix + "_" + moduloAtual_xx + "_cnx_grp"), (prefix + "_jnt_grp"))
                
                # Criando os Joints para o primeiro modulo:
                for indexJoints in jntNum:
                    if (indexJoints < (len(jntNum)-1)): #enquanto nao for o joint_end:
                        cmds.joint (name = prefix + "_" + moduloAtual_xx + jntList[indexJoints])
                        
                        if (indexJoints == 0):
                            cmds.parentConstraint ((prefix + "_" + moduloAtual_xx + "_ctrl"),(prefix + "_" + moduloAtual_xx + jntList[indexJoints]))
                            cmds.scaleConstraint ((prefix + "_" + moduloAtual_xx + "_ctrl"),(prefix + "_" + moduloAtual_xx + jntList[indexJoints]))
                            pass
                        if (indexJoints == 1):
                            cmds.joint ((prefix + "_" + moduloAtual_xx + jntList[indexJoints]), edit=True, sc=False)
                            pass
        
                        pass
                    else: #joint_end            
                        cmds.select (clear=True)
                        cmds.joint (name = prefix + "_" + moduloAtual_xx + jntList[indexJoints])
                        cmds.xform (prefix + "_" + moduloAtual_xx + jntList[indexJoints], t = coordenadas[moduloAtual+1], ro = rotCoordenadas[moduloAtual])
                        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                        cmds.parent ((prefix + "_" + moduloAtual_xx + jntList[indexJoints]), (prefix + "_" + moduloAtual_xx + jntList[indexJoints - 1]))

                        cmds.parent ((prefix + "_" + moduloAtual_xx + "_upVec_loc_grp"), (prefix + "_" + moduloProx_xx + "_ctrl")) # parent dos upVet dentro dos ctrls
                        cmds.setAttr ((prefix + "_" + moduloAtual_xx + "_upVec_loc_grp.visibility"), False)
                        pass
                    #cmds.parent ((prefix + "_" + moduloAtual_xx + jntList[0]), (prefix + "_" + moduloAtual_xx + "_cnx_grp"))
                    
                
                # Criando loc de mesure

                
                cmds.select(clear=True)
           
                pass     
            # caso nao seja o primeiro ponto:
            else:
                if (moduloAtual < FKnum):
                    jntList = ['_trans_zero','_trans','_cnx_zero','_cnx','_jnt', '_end']
                    jntNum = range((len(jntList)))
        
                    # Criando os Joints para os demais modulos:
                    for indexJoints in jntNum:
           
                        if (indexJoints == 0): #caso seja o primeiro joint do modulo:
                            cmds.group (name=(prefix + "_" + moduloAtual_xx + "_parent_grp"), em=True)
                            cmds.joint (name = prefix + "_" + moduloAtual_xx + jntList[indexJoints], sc=False)
                            cmds.group ((prefix + "_" + moduloAtual_xx + "_parent_grp"), name=(prefix + "_" + moduloAtual_xx + "_parent_zero"))  
                            
                            cmds.xform (prefix + "_" + moduloAtual_xx + "_parent_zero", t = coordenadas[moduloAtual], ro = rotCoordenadas[moduloAtual])
                            
                            cmds.parentConstraint ((prefix + "_" + moduloAnt_xx + "_ctrl"), (prefix + "_" + moduloAtual_xx + "_parent_grp"), mo=True)
                            cmds.scaleConstraint ((prefix + "_" + moduloAnt_xx + "_ctrl"), (prefix + "_" + moduloAtual_xx + "_parent_grp"))
                            
                            cmds.parent (prefix + "_" + moduloAtual_xx + "_parent_zero", (prefix + "_jnt_grp" ))
                            cmds.select (prefix + "_" + moduloAtual_xx + jntList[indexJoints])
                            pass
                            
                        if ((indexJoints > 0) and indexJoints < (len(jntNum)-1)):
                            cmds.joint (name = prefix + "_" + moduloAtual_xx + jntList[indexJoints])
                            
                            if (indexJoints == 1):
                                cmds.connectAttr ((prefix + "_" + moduloAtual_xx + "_ctrl.translate"),(prefix + "_" + moduloAtual_xx + jntList[indexJoints]+".translate"))
                                pass
                            if (indexJoints == 3):
                                cmds.connectAttr ((prefix + "_" + moduloAtual_xx + "_ctrl.rotate"),(prefix + "_" + moduloAtual_xx + jntList[indexJoints]+".rotate"))
                                cmds.connectAttr ((prefix + "_" + moduloAtual_xx + "_ctrl.scale"),(prefix + "_" + moduloAtual_xx + jntList[indexJoints]+".scale"))
                                pass
                            if (indexJoints == 4):
                                cmds.joint ((prefix + "_" + moduloAtual_xx + jntList[indexJoints]), edit=True, sc=False)
                                pass
                            
                            pass
                            
                        if (indexJoints == (len(jntNum)-1)): #caso seja o ultimo joint do modulo, somente translacionar
                            cmds.select(clear=True)
                            
                            cmds.joint (name = prefix + "_" + moduloAtual_xx + jntList[indexJoints])
                            
                            cmds.xform (prefix + "_" + moduloAtual_xx + jntList[indexJoints], t = coordenadas[moduloAtual+1], ro = rotCoordenadas[moduloAtual])
                            cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
                            
                            cmds.parent (prefix + "_" + moduloAtual_xx + jntList[indexJoints], prefix + "_" + moduloAtual_xx + jntList[indexJoints-1])
                            
                            cmds.select(clear=True)
                            
                            pass
                             
                    pass
                    
                    #Criando locators upvectors para os demais modulos:
                    if (moduloAtual < (FKnum-1)):
                        cmds.spaceLocator (name=(prefix + "_" + moduloAtual_xx + "_upVec_loc"))
                        cmds.group ((prefix + "_" + moduloAtual_xx + "_upVec_loc"), name=(prefix + "_" + moduloAtual_xx + "_upVec_loc_grp"))
                        cmds.xform((prefix + "_" + moduloAtual_xx + "_upVec_loc_grp"), t = coordenadas[moduloAtual], ro = rotCoordenadas[moduloAtual])
                        cmds.xform((prefix + "_" + moduloAtual_xx + "_upVec_loc"), t = (-10,0,0))
                        cmds.parent ((prefix + "_" + moduloAtual_xx + "_upVec_loc_grp"), (prefix + "_" + moduloProx_xx + "_ctrl")) # parent dos upVet dentro dos ctrls

                        cmds.setAttr ((prefix + "_" + moduloAtual_xx + "_upVec_loc_grp.visibility"), False)
                        cmds.select(clear=True)
                        pass
                    pass
                pass
        
            
        for indexAim in modulos:
            moduloAtual = indexAim+1
            moduloAnt_xx = str(indexAim+0).zfill(2) #modulo com dois digitos
            moduloAtual_xx = str(indexAim+1).zfill(2)
            moduloProx_xx = str(indexAim+2).zfill(2)
            
            if (moduloAtual < (FKnum-1)):
                cmds.aimConstraint ((prefix + "_" + moduloProx_xx + "_trans"), (prefix + "_" + moduloAtual_xx + "_jnt"), u=(-1,0,0), wut=("object"), wuo=(prefix + "_" + moduloAtual_xx + "_upVec_loc"), mo=True)
                pass
            
            
    print ("#---- O Guide "+prefix+" foi gerado!\n----- Para gerar o Sistema use a função sistema()\n")


#executando Guide:
guide ()
#----














#
