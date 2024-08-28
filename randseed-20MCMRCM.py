# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 18:12:59 2024

@author: 14125
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import seed 
import pandas as pd

dsjlist = []
msjlist = []
def modelws(seed_numble):
    try:
        m = gp.Model("zuida_fen1")
        m.setParam("OutputFlag", 0)
        
        num = 20
        
        o = m.addMVar(shape=num,name="o")
        oc = m.addVar(lb=0,name="oc")
        x = m.addMVar(shape=num,name="x")
        y = m.addMVar(shape=num,name="y")
        z = m.addMVar(shape=num,vtype=GRB.BINARY,name="z")
        zz = m.addMVar(shape=num,vtype=GRB.BINARY,name="zz")
        zzz = m.addMVar(shape=num,vtype=GRB.BINARY,name="zzz")    
         
    
        oc1 = m.addVar(lb=0,name="oc1")
        e = m.addMVar(shape=num,name="e")
        op = m.addMVar(shape=num,ub=1.0,name="op")
        
    
        op1 = m.addMVar(shape=num,name="op1")
        op2 = m.addMVar(shape=num,name="op2")
        op3 = m.addMVar(shape=num,name="op3")
        op4 = m.addMVar(shape=num,name="op4")
        op5 = m.addMVar(shape=num,name="op5")
        oc2 = m.addVar(lb=-float("inf"),name="oc2")
        
     #    c = np.array([3.06 ,3.74 ,2.69 ,4.14 ,5.05 ,7.94, 1.3  ,0.76, 3.02 ,0.38 ,1.89 ,0.15 ,2.56 ,5.33,
     # 2.55 ,3.15 ,6.54 ,3.82 ,0.53 ,6.81])
     #    o0 = np.array([0.4, 0.78, 0.58, 0.83, 0.9, 0.35, 0.18, 0.05, 0.47, 0.99, 0.07, 0.21, 0.45, 0.85, 0.24, 0.83, 0.37, 0.65, 0.32, 0.19])
     #    w=  np.array([0.06, 0.05, 0.07, 0.07, 0.02, 0.02, 0.05, 0.03, 0.06, 0.1, 0.08, 0.02, 0.03, 0.04, 0.06, 0.03, 0.04, 0.1, 0.08, 0.0])
        ee = 0.08
     #    l =  np.array([2.48, 2.86, 3.74, 3.0, 3.06, 5.32, 4.24, 3.04, 8.89, 8.55, 8.3, 2.04, 6.53, 2.26, 7.12, 8.2, 1.68, 0.5, 7.7, 6.3])
     #    lbo =  np.array([0.52, 0.56, 0.15, 0.69, 0.89, 0.54, 0.51, 0.83, 0.69, 0.06, 0.09, 0.54, 0.95, 0.56, 0.43, 0.48, 0.41, 0.94, 0.91, 0.08])
     #    cbo =  np.array([ 0.26, 0.83, 0.84, 0.36, 0.26, 0.99, 0.24, 0.75, 0.8, 0.75, 0.13, 0.26, 0.36, 0.28, 0.89, 0.68, 0.02, 0.71, 0.25, 0.96])
        
        c,o0,w,l,lbo,cbo = seed.sjsedd(seed_numble)
        # print(l)
        # print(lbo)
        # print(cbo)
        M = 10000000
    
        
        m.setObjective(l@y-c@x,GRB.MINIMIZE)
            
        m.addConstr(o0-o<=x)
        m.addConstr(o-o0<=x)
        m.addConstr(o0-o>=x-(1-z)*M)
        m.addConstr(o-o0>=x-(1-zz)*M)
        m.addConstr(z+zz>=1)
        m.addConstrs(oc-o0[i]<=y[i] for i in range(num))
        m.addConstrs(o0[i]-oc<=y[i] for i in range(num))
        m.addConstr(w@o==oc)
        m.addConstrs(o[i]-oc<=ee for i in range(num))
        m.addConstrs(-o[i]+oc<=ee for i in range(num))
        m.addConstrs(o[i]>=o0[i]-M*(1-zzz[i]) for i in range(num))
        m.addConstrs(o[i]>=oc1-M*zzz[i] for i in range(num))
        m.addConstrs(o[i]<=oc1+M*(1-zzz[i]) for i in range(num))
        m.addConstrs(o[i]<=o0[i]+M*zzz[i] for i in range(num))
        
    
        m.addConstr(c@e==o0@op1-o0@op2-ee*(sum(op3[i] for i in range(num)))
                       -ee*(sum(op4[i] for i in range(4)))-sum(op5[i] for i in range(num)))
        
    
        m.addConstr(o0-op<=e)
        m.addConstr(op-o0<=e)
        m.addConstr(w@op==oc1)
        m.addConstrs(op[i]-oc1<=ee for i in range(num))
        m.addConstrs(-op[i]+oc1<=ee for i in range(num))
    
    
        m.addConstr(op1+op2-c==0)                                 
        m.addConstrs(op1[i]-op2[i]+oc2*w[i]-op3[i]+op4[i]-op5[i]<=0 for i in range(num))
        m.addConstr(-oc2+sum(op3[i] for i in range(num))-sum(op4[i] for i in range(num))<=0)
        
        m.optimize()
            
            
    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))
        
    except AttributeError:
        print('Encountered an attribute error')
    m.update()
    dsjlist.append(-round(sum(l[i]*y[i].x for i in range(20)),2))
    msjlist.append(-round(sum(c[i]*x[i].x for i in range(20)),2))
    # m.write("MCMRCM.lp")
    # print(-round(m.ObjVal,3))
    # print(-round(sum(l[i]*y[i].x for i in range(20)),2))
    # print(-round(sum(c[i]*x[i].x for i in range(20)),2))
    # # print(sum(c[i]*e[i].x for i in range(4)))
    # print(round(oc1.x,3))
    # print(round(oc.x,3))
for i in range(10):
    modelws(i)

rate = 0
for i in range(10):
    if dsjlist[i]>msjlist[i]:
        rate = rate+1
print(rate)