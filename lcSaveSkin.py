import pymel.core as pm
import cPickle as pickle
import time

def findSkinCluster(mesh):
    skincluster = None
    for each in pm.listHistory(mesh):  
        if type(each)==pm.nodetypes.SkinCluster:   
            skincluster = each
    return skincluster

def saveSkinning(mesh,path):
    dataDict ={} 
    skincluster = findSkinCluster(mesh)
    if skincluster!=None:     
        for infl in skincluster.getInfluence():
            vtxList =[]
            getData = skincluster.getPointsAffectedByInfluence(infl)  
            for vtx, wgt in zip (getData[0][0],getData[1]):
                vtxList.append ((vtx.currentItemIndex(),wgt))                   
            dataDict[infl]= vtxList
    
    with open(path, 'wb') as handle:
        pickle.dump(dataDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    
def loadSkinning(mesh,path):
    skincluster = findSkinCluster(mesh)
    
    with open(path, 'rb') as handle:
        dataDict = pickle.load(handle)
        
    if skincluster!=None:
        skincluster.setNormalizeWeights(0)
        pm.skinPercent(skincluster, mesh, nrm=False, prw=100)
        
        jointDict = {}
        for storedJoint in dataDict :
            jointDict[storedJoint]=skincluster.indexForInfluenceObject(storedJoint)
               
        for infl in dataDict :
            for vtx in x[infl]:
                pm.setAttr (skincluster.name()+'.weightList['+str(vtx[0])+'].weights['+str (jointDict[infl]) +']', vtx[1])
        skincluster.setNormalizeWeights(1)
    
             
mesh= 'pCylinder1'
path = 'C:/Users/LEO/Downloads/teste.pickle'

start_time = time.time()
saveSkinning(mesh,path)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
loadSkinning(mesh,path)
print("--- %s seconds ---" % (time.time() - start_time))


