# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:02:50 2021

@author: zhaob
"""

#%%


import matplotlib.pyplot as plt
import numpy as np

from HeadConvertLib import HeadFile # 从自定义文件中导入HeadFile库


# path=b"D:\\test\\Test1.hdf"

# path=b"D:\\test\\test.hdf"
# path=b"D:\\test\\test2.hdf"
# path=b"D:\\test\\test3.hdf"
# path="D:\\test\\test3.hdf"
# path=b"D:\\test\\FAW D090 PV EOLT limit Veh_G36609_RUN3.hdf"
path="D:\\test\\N012352 CS_02.hdf"
# create HeadFile Object
testfile=HeadFile() 

# open HeadFile data
testfile.open(path)

# print attribution group and chennels
print('group:',testfile.group)
print('channels:',testfile.channels)

# method 1: read some selected data by object attribution , 
#           last 1000 quantities,some channels
data_slt1 = testfile.read_data(testfile.group,testfile.channels[1:3],-1000)

# method 2: read selected data , with str name
s = testfile.channels[1]
print('channel 1 Name:', s)
data_slt2 = testfile.read_data(testfile.group,s)

# method 3: read all data 
data_slt_all = testfile.read_data(testfile.group,testfile.channels[:])


# plot some channles data
i=0
for chn_data in data_slt1.data:
    plt.figure()
    t=np.arange(0,data_slt1.increment[i]*(len(chn_data)-1),data_slt1.increment[i])
    plt.plot(t,chn_data[0:np.size(t)])
    plt.title(testfile.channels[i])
    i=i+1
    
# close HeadFile Object
del testfile



#%%
# method 2
# from HeadConvertLib import test
# test()
