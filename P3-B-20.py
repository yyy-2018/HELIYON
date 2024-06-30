# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 00:39:46 2024

@author: 14125
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np

ee =0.08
t = gp.Model("zui_xiao_cost1")
        
op = t.addMVar(shape=20,ub=1.0,name="op")
oc1 = t.addVar(lb=0,name="oc")
e = t.addMVar(shape=20,name="e")
     
c = np.array([3.06 ,3.74 ,2.69 ,4.14 ,5.05 ,7.94, 1.3  ,0.76, 3.02 ,0.38 ,1.89 ,0.15 ,2.56 ,5.33,
 2.55 ,3.15 ,6.54 ,3.82 ,0.53 ,6.81])
o0 = np.array([0.4, 0.78, 0.58, 0.83, 0.9, 0.35, 0.18, 0.05, 0.47, 0.99, 0.07, 0.21, 0.45, 0.85, 0.24, 0.83, 0.37, 0.65, 0.32, 0.19])
w=  np.array([0.06, 0.05, 0.07, 0.07, 0.02, 0.02, 0.05, 0.03, 0.06, 0.1, 0.08, 0.02, 0.03, 0.04, 0.06, 0.03, 0.04, 0.1, 0.08, 0.0])
l =  np.array([2.48, 2.86, 3.74, 3.0, 3.06, 5.32, 4.24, 3.04, 8.89, 8.55, 8.3, 2.04, 6.53, 2.26, 7.12, 8.2, 1.68, 0.5, 7.7, 6.3])
lbo =  np.array([0.52, 0.56, 0.15, 0.69, 0.89, 0.54, 0.51, 0.83, 0.69, 0.06, 0.09, 0.54, 0.95, 0.56, 0.43, 0.48, 0.41, 0.94, 0.91, 0.08])
cbo =  np.array([ 0.26, 0.83, 0.84, 0.36, 0.26, 0.99, 0.24, 0.75, 0.8, 0.75, 0.13, 0.26, 0.36, 0.28, 0.89, 0.68, 0.02, 0.71, 0.25, 0.96])
t.setObjective(c@e+cbo@e,GRB.MINIMIZE)

t.addConstr(o0-op<=e)
t.addConstr(op-o0<=e)
t.addConstr(w@op==oc1)
t.addConstrs(op[i]-oc1<=ee for i in range(20))
t.addConstrs(-op[i]+oc1<=ee for i in range(20))

        
t.optimize()
oc11=round(oc1.x,3)
print(oc11)       
try:
    m = gp.Model("zuida_fen1")
        
    #op = m.addMVar(shape=5,ub=1.0,name="op")
    o = m.addMVar(shape=20,ub=1,name="o")
    oc = m.addVar(lb=0,name="oc")
    x = m.addMVar(shape=20,lb=-float("inf"),name="x")
    y = m.addMVar(shape=20,name="y")
    z = m.addMVar(shape=20,vtype=GRB.BINARY,name="z")
    zz = m.addMVar(shape=20,vtype=GRB.BINARY,name="zz")
    zzz = m.addMVar(shape=20,vtype=GRB.BINARY,name="zzz")    
    

    M = 100000000
    opp = np.array([oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11,oc11])
    
    m.setObjective(l@y-c@x+cbo@x+lbo@y,GRB.MINIMIZE)
        
    m.addConstr(o0-o<=x)
    m.addConstr(o-o0<=x)
    m.addConstr(o0-o>=x-(1-z)*M)
    m.addConstr(o-o0>=x-(1-zz)*M)
    m.addConstr(z+zz>=1)
    m.addConstrs(oc-o0[i]<=y[i] for i in range(20))
    m.addConstrs(o0[i]-oc<=y[i] for i in range(20))
    m.addConstr(w@o==oc)
    m.addConstrs(o[i]-oc<=ee for i in range(20))
    m.addConstrs(-o[i]+oc<=ee for i in range(20))
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
print(-round(m.ObjVal,3))
print(-round(sum(l[i]*y[i].x+lbo[i]*y[i].x for i in range(20)),2))
print(-round(sum(-c[i]*x[i].x+cbo[i]*x[i].x for i in range(20)),2))
# print(sum(c[i]*e[i].x+cbo[i]*e[i].x for i in range(20)))
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