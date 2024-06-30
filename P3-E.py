# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 23:32:00 2023

@author: 14125
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
ee =0.15

t = gp.Model("zui_xiao_cost1")
        
op = t.addMVar(shape=4,ub=1.0,name="op")
oc1 = t.addVar(lb=0,name="oc")
e = t.addMVar(shape=4,name="e")

sbs3 = t.addMVar(shape=4,lb=-float("inf"),name="sbs")
qs3 = t.addVar(name="qs")
     
cbo = np.array([0.7,1,0.5,1])        
c = np.array([6,3,4,1])
o0 = np.array([0,0.3,0.6,1])
#w = np.array([0.375,0.25,0.1875,0.0625,0.125])
w = np.array([0.3,0.1,0.4,0.2])
#op = np.array([0.3,0.4,0.5,0.6,0.3])
    
t.setObjective(c@e+qs3,GRB.MINIMIZE)

t.addConstr(o0-op<=e)
t.addConstr(op-o0<=e)
t.addConstr(w@op==oc1)
t.addConstrs(op[i]-oc1<=ee for i in range(4))
t.addConstrs(-op[i]+oc1<=ee for i in range(4))
t.addGenConstrNorm(qs3,sbs3,2.0)
t.addConstrs(e[i]*cbo[i] == sbs3[i] for i in range(4))

        
t.optimize()
oc11=round(oc1.x,3)
print(oc11)       
try:
    m = gp.Model("zuida_fen1")
        
    #op = m.addMVar(shape=5,ub=1.0,name="op")
    o = m.addMVar(shape=4,ub=1,name="o")
    oc = m.addVar(lb=0,name="oc")
    x = m.addMVar(shape=4,lb=-float("inf"),name="x")
    y = m.addMVar(shape=4,name="y")
    z = m.addMVar(shape=4,vtype=GRB.BINARY,name="z")
    zz = m.addMVar(shape=4,vtype=GRB.BINARY,name="zz")
    zzz = m.addMVar(shape=4,vtype=GRB.BINARY,name="zzz")
    sbs = m.addMVar(shape=4,lb=-float("inf"),name="sbs")
    qs = m.addVar(name="qs")
    sbs2 = m.addMVar(shape=4,lb=-float("inf"),name="sbs2")
    qs2 = m.addVar(name="qs2")
    
    cbo = np.array([0.7,1,0.5,1])
    lbo = np.array([0.7,0.4,0.4,0.5])    
    c = np.array([6,3,4,1])
    o0 = np.array([0,0.3,0.6,1])
    #w = np.array([0.375,0.25,0.1875,0.0625,0.125])
    w = np.array([0.3,0.1,0.4,0.2])
    l = np.array([4,8,7,9])
    M = 100000000
    opp = np.array([oc11,oc11,oc11,oc11])
    
    m.setObjective(l@y-c@x+qs+qs2,GRB.MINIMIZE)
    
    m.addGenConstrNorm(qs2,sbs2,2.0)
    m.addConstrs(x[i]*cbo[i] == sbs2[i] for i in range(4))
    
    m.addGenConstrNorm(qs,sbs,2.0, "normconstr2")
    m.addConstrs(y[i]*lbo[i] == sbs[i] for i in range(4))
    
    m.addConstr(o0-o<=x)
    m.addConstr(o-o0<=x)
    m.addConstr(o0-o>=x-(1-z)*M)
    m.addConstr(o-o0>=x-(1-zz)*M)
    m.addConstr(z+zz>=1)
    m.addConstrs(oc-o0[i]<=y[i] for i in range(4))
    m.addConstrs(o0[i]-oc<=y[i] for i in range(4))
    m.addConstr(w@o==oc)
    m.addConstrs(o[i]-oc<=ee for i in range(4))
    m.addConstrs(-o[i]+oc<=ee for i in range(4))
    m.addConstr(o>=o0-M*(1-zzz))
    m.addConstr(o>=opp-M*zzz)
    m.addConstr(o<=opp+M*(1-zzz))
    m.addConstr(o<=o0+M*zzz)
        
    m.optimize()
        
        
      
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))
    
except AttributeError:
    print('Encountered an attribute error')
m.update()
m.write("EROMCMRCM.lp")
print(-round(m.ObjVal,3))
print(-round(sum(l[i]*y[i].x for i in range(4))+qs.x,2))
print(-round(sum(-c[i]*x[i].x for i in range(4))+qs2.x,2))
# print(sum(c[i]*e[i].x for i in range(4))+qs3.x)
print(round(oc1.x,3))
# print(round(op[0].x,3))
# print(round(op[1].x,3))
# print(round(op[2].x,3))
# print(round(op[3].x,3))
print(round(oc.x,3))
# print(round(o[0].x,3))
# print(round(o[1].x,3))
# print(round(o[2].x,3))
# print(round(o[3].x,3))  