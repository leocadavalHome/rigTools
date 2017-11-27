import pymel.core as pm
import maya.api.OpenMaya as om

p1 = pm.xform ('locator1', q=True, t=True, wd=True)
p2 = pm.xform ('locator2', q=True, t=True, wd=True)
p3 = pm.xform ('locator3', q=True, t=True, wd=True)

A= om.MVector(p1)
B= om.MVector(p2)
C= om.MVector(p3)

AB = A-B
BC = B-C
n = BC^AB
nNormal = n.normal()

x = nNormal ^ AB.normal()
t = x.normal() ^ nNormal
list = [t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, nNormal.x, nNormal.y, nNormal.z, 0, A.x, A.y,A.z,1]
m= om.MMatrix (list)

pm.select(cl=True)
j1 = pm.joint()
pm.xform (j1, m = m, wd=True) 
pm.makeIdentity (j1, apply=True, r=1, t=0, s=0, n=0, pn=0)

x = nNormal ^ BC.normal()
t = x.normal() ^ nNormal
list = [t.x, t.y, t.z, 0, x.x, x.y, x.z, 0, nNormal.x, nNormal.y, nNormal.z,0, B.x, B.y, B.z,1]
m= om.MMatrix (list)
pm.select(cl=True)
j2= pm.joint()
pm.xform (j2, m = m, wd=True) 
pm.makeIdentity (j2, apply=True, r=1, t=0, s=0, n=0, pn=0)

pm.select(cl=True)
j3=pm.joint()
pm.xform (j3, m = m, wd=True) 
pm.xform (j3, t= C, wd=True)
pm.makeIdentity (j3, apply=True, r=1, t=0, s=0, n=0, pn=0)

pm.parent (j2, j1)
pm.parent (j3, j2)
