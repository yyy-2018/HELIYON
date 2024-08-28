# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:31:02 2024

@author: 14125
"""
import numpy as np
randomSeedArray = [1,2,3,4,5,6,7,8,9,10]

def  sjsedd(i):
    np.random.seed(randomSeedArray[i])
    c = np.random.uniform(0,10,size=20)
    o0 = np.random.uniform(0,1,size=20)
    wcc = np.random.rand(20)

# 将数组归一化，使得所有元素之和等于1
    w = wcc / np.sum(wcc)
    l = np.random.uniform(0,10,size=20)
    lbo = np.random.uniform(0,1,size=20)
    cbo = np.random.uniform(0,1,size=20)
    return c,o0,w,l,lbo,cbo
print(sjsedd(1))