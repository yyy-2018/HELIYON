# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 07:27:12 2024

@author: 14125
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np





from random_forest_predictor import RandomForestPredictor

fixed_values = [6, 3, 4, 1]
fluctuation_values_box = [1,1,1,1]
fluctuation_values_ellipse = [1,1,1,1]

predictor = RandomForestPredictor()


predictor.train_models(fixed_values)


predicted_c_box = predictor.predict(fluctuation_values_box, mode='box')
predicted_c_ellipse = predictor.predict(fluctuation_values_ellipse, mode='ellipse')


fixed_values1 = [4,8,7,9]
fluctuation_values_box = [1,1,1,1]
fluctuation_values_ellipse = [1,1,1,1]

predictor = RandomForestPredictor()


predictor.train_models(fixed_values1)


predicted_c_box1 = predictor.predict(fluctuation_values_box, mode='box')
predicted_c_ellipse1 = predictor.predict(fluctuation_values_ellipse, mode='ellipse')


try:
    m = gp.Model("zuida_fen1")
    m.setParam("OutputFlag", 0)
    
    o = m.addMVar(shape=4,name="o")
    oc = m.addVar(lb=0,name="oc")
    x = m.addMVar(shape=4,name="x")
    y = m.addMVar(shape=4,name="y")
    z = m.addMVar(shape=4,vtype=GRB.BINARY,name="z")
    zz = m.addMVar(shape=4,vtype=GRB.BINARY,name="zz")
    zzz = m.addMVar(shape=4,vtype=GRB.BINARY,name="zzz")    
     

    oc1 = m.addVar(lb=0,name="oc1")
    e = m.addMVar(shape=4,name="e")
    op = m.addMVar(shape=4,ub=1.0,name="op")
    

    op1 = m.addMVar(shape=4,name="op1")
    op2 = m.addMVar(shape=4,name="op2")
    op3 = m.addMVar(shape=4,name="op3")
    op4 = m.addMVar(shape=4,name="op4")
    op5 = m.addMVar(shape=4,name="op5")
    oc2 = m.addVar(lb=-float("inf"),name="oc2")
    
    c = np.array(predicted_c_ellipse)
    o0 = np.array([0,0.3,0.6,1])
    w = np.array([0.3,0.1,0.4,0.2])
    ee = 0.08
    l = np.array(predicted_c_ellipse1)
    M = 10000000

    
    m.setObjective(l@y-c@x,GRB.MINIMIZE)
        
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
    m.addConstrs(o[i]>=o0[i]-M*(1-zzz[i]) for i in range(4))
    m.addConstrs(o[i]>=oc1-M*zzz[i] for i in range(4))
    m.addConstrs(o[i]<=oc1+M*(1-zzz[i]) for i in range(4))
    m.addConstrs(o[i]<=o0[i]+M*zzz[i] for i in range(4))
    

    m.addConstr(c@e==o0@op1-o0@op2-ee*(sum(op3[i] for i in range(4)))
                   -ee*(sum(op4[i] for i in range(4)))-sum(op5[i] for i in range(4)))
    

    m.addConstr(o0-op<=e)
    m.addConstr(op-o0<=e)
    m.addConstr(w@op==oc1)
    m.addConstrs(op[i]-oc1<=ee for i in range(4))
    m.addConstrs(-op[i]+oc1<=ee for i in range(4))


    m.addConstr(op1+op2-c==0)                                 
    m.addConstrs(op1[i]-op2[i]+oc2*w[i]-op3[i]+op4[i]-op5[i]<=0 for i in range(4))
    m.addConstr(-oc2+sum(op3[i] for i in range(4))-sum(op4[i] for i in range(4))<=0)
    
    m.optimize()
        
        
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))
    
except AttributeError:
    print('Encountered an attribute error')
m.update()
m.write("MCMRCM.lp")
print(-round(m.ObjVal,3))
print(-round(sum(l[i]*y[i].x for i in range(4)),2))
print(-round(sum(c[i]*x[i].x for i in range(4)),2))
# print(sum(c[i]*e[i].x for i in range(4)))
print(round(oc1.x,3))
print(round(oc.x,3))