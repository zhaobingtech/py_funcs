# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 09:37:17 2021

@author: zhaob 
"""
import numpy as np
import math
from scipy import interpolate
# from scipy import scipy.signal

#%% Order Calc

def Order_RPM_Synchronous_Resampling(rpmData,sigData,Fs,orderResoluton,maxOrder):
    '''

    Parameters
    ----------
    rpmData : TYPE
        DESCRIPTION.
    sigData : TYPE
        DESCRIPTION.
    Fs : TYPE
        DESCRIPTION.
    orderResoluton : TYPE
        DESCRIPTION.
    maxOrder : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    '''
    1. 转速转化为角度
        # rpm -> rad/s 比率： rpm = rev/min = rev/60s = 1/60 rev/s = 2*pi/60 rad/s
        # 得到的角度信号 为 时域信号rotAngle
    2. 使用角度进行角度域重采样
        #1.生成 等角度序列 even-angle
        #2.使用 等角度序列 进行插值 得到 角度域重采样信号sigData_EvenAngle
    3. 将角度域重采样信号sigData_EvenAngle 进行FFT分析，得到Order域的二维数据
    4. 看看这个二维数据如何显示为彩图
    '''
    #---------------------- 1. 转速转化为角度 ----------------------
    #  integrated rpm to angle (unit  = r)
    dt = 1 / Fs
    
    # transRatio = 1/60 # rpm = rev/min = rev/60s = 1/60 rev/s
    transRatio_rpm2rad_s = (2*np.pi) /60 # rpm = rev/min = 2*pi/60s = 2*pi/60 rad/s
    
    # rpmData 转速信号 积分成为 角度信号 rotAngle , 单位 unit。
    # 比循环快80倍
    rotAngle = np.cumsum(rpmData)*dt*transRatio_rpm2rad_s
        
    # -------------------- 2. 角度域重采样 ----------------------
    # 角度域采样频率 = 2*maxOrder : Fs
    # 采样间隔 = rev/2*maxOrder
    angleInc = (2*np.pi) / (2*maxOrder)# 2pi/rad
    
    # 角度一直累加时，单调增大时
    sigDataAngDomain = resampling_angle(rotAngle,sigData,angleInc,angUnit='rad/s')
    
    
    #-------------------- 3. 将角度域重采样信号进行FFT分析 ----------
    #-------------------    得到Order域的二维数据          ----------
    
    # 角度一会儿大，一会儿小时
    # Order参数设置, 类比FFT 
    # maxOrder: fs/2  oderResolution : freqResolution
    # blkSize = fs/freqRes := 2*maxOrder/orderResolution
    blkSize = int ((2*maxOrder)/orderResoluton )
    
    # 往前的step 分别是，占时不考虑padding.
    Overlap = 0.3  #30% Overlap
    
    # 切割数据块成为一个2D数组
    _,sigBlks = cut_to_sigBlks(sigDataAngDomain,blkSize,Overlap)
    
    # FFT 2D数据块
    sigBlks=sigBlks*np.hanning(sigBlks.shape[1])
    fftBlks2D = np.fft.fft(sigBlks)
    
    fftUseSize = int(blkSize // 2)
    row,col = sigBlks.shape
    orderBlks2D = np.zeros((row,fftUseSize+1))
    orderBlks2D[:,0] = np.abs( fftBlks2D[:,0] ) /blkSize
    orderBlks2D[:,1::] = (np.abs( fftBlks2D[:,1:fftUseSize+1] ) *2)/blkSize
    
    orderBlks2D = np.zeros((row,fftUseSize+1))
    orderBlks2D[:,0] = np.abs( fftBlks2D[:,0] ) /blkSize
    orderBlks2D[:,1::] = (np.abs( fftBlks2D[:,1:fftUseSize+1] ) *2)/blkSize
    
    
    orderBlks2D_complex = np.zeros((row,fftUseSize+1))
    orderBlks2D_complex[:,0] = fftBlks2D[:,0] /blkSize
    orderBlks2D_complex[:,1::] = (fftBlks2D[:,1:fftUseSize+1]  *2)/blkSize
    # transfer rpm to angle data
    # rpm = rev / min = rev / 60s = 2*pi rad / 60 s = 2*pi/60 rad/s
    # 
    # angle = rpmdata
    # re-sampling rpm by orderResolution,
    return orderBlks2D_complex,orderBlks2D

def Order_RPM_Synchronous_Resampling2(rotAngle,sigData,Fs,orderResoluton,maxOrder):
    '''

    Parameters
    ----------
    rpmData : TYPE
        DESCRIPTION.
    sigData : TYPE
        DESCRIPTION.
    Fs : TYPE
        DESCRIPTION.
    orderResoluton : TYPE
        DESCRIPTION.
    maxOrder : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    '''
    1. 转速转化为角度
        # rpm -> rad/s 比率： rpm = rev/min = rev/60s = 1/60 rev/s = 2*pi/60 rad/s
        # 得到的角度信号 为 时域信号rotAngle
    2. 使用角度进行角度域重采样
        #1.生成 等角度序列 even-angle
        #2.使用 等角度序列 进行插值 得到 角度域重采样信号sigData_EvenAngle
    3. 将角度域重采样信号sigData_EvenAngle 进行FFT分析，得到Order域的二维数据
    4. 看看这个二维数据如何显示为彩图
    '''
    #---------------------- 1. 转速转化为角度 ----------------------
    #  integrated rpm to angle (unit  = r)
        
    # -------------------- 2. 角度域重采样 ----------------------
    # 角度域采样频率 = 2*maxOrder
    # 采样间隔 = rev/2*maxOrder
    angleInc = (2*np.pi) / (2*maxOrder)# 2pi/rad
    
    # 角度一直累加时，单调增大时
    sigDataAngDomain = resampling_angle(rotAngle,sigData,angleInc,angUnit='rad/s')
    
    
    #-------------------- 3. 将角度域重采样信号进行FFT分析 ----------
    #-------------------    得到Order域的二维数据          ----------
    
    # 角度一会儿大，一会儿小时
    # Order参数设置, 类比FFT 
    # maxOrder: fs/2  oderResolution : freqResolution
    # blkSize = fs/freqRes := 2*maxOrder/orderResolution
    blkSize = int (2*maxOrder*orderResoluton )
    
    # 往前的step 分别是，占时不考虑padding.
    Overlap = 0.3  #30% Overlap
    
    # 切割数据块成为一个2D数组
    sigBlks = cut_to_sigBlks(sigDataAngDomain,blkSize,Overlap)
    
    # FFT 2D数据块
    fftBlks2D = np.fft.fft(sigBlks)
    
    fftUseSize = blkSize // 2
    row,col = sigBlks.shape
    orderBlks2D = np.zeros((row,fftUseSize+1))
    orderBlks2D[:,0] = np.abs( fftBlks2D[:,0] ) /blkSize
    orderBlks2D[:,1::] = (np.abs( fftBlks2D[:,1:fftUseSize+1] ) *2 )/blkSize
    
        
    # transfer rpm to angle data
    # rpm = rev / min = rev / 60s = 2*pi rad / 60 s = 2*pi/60 rad/s
    # 
    # angle = rpmdata
    # re-sampling rpm by orderResolution,
    return orderBlks2D

#--------------------- resampling_angle ---------------------
def resampling_angle(rotAngle,sigTimeDomain,angleInc,angUnit='rad/s'):
    '''

    Parameters
    ----------
    rotAngle : TYPE
        DESCRIPTION:时间域Angle信号，单位为rad/s
    sigTimeDomain : TYPE
        DESCRIPTION.时间域待分析信号
    angleInc : TYPE
        DESCRIPTION.

    Returns
    -------
    sigAngleDomain : 
        DESCRIPTION：角度域采样数据

    '''
    # 角度域采样频率 = 2*maxOrder
    # 采样间隔 = rev/2*maxOrder
    # 角度单位都用rad
    angleIncSeries = np.arange(min(rotAngle),max(rotAngle),angleInc)
    # timeIncSeries = np.arange(0,size(sigData),dt)
    f=interpolate.interp1d(rotAngle,sigTimeDomain,kind='linear')
    sigAngleDomain = f(angleIncSeries)
    return sigAngleDomain


#--------------------- cut_to_sigBlks ---------------------
def cut_to_sigBlks(sigData,blkSize,Overlap):
 
    if Overlap > 1:
        return print('overlap need less than 1')
        Overlap = Overlap/100
        
    # 1.获取其实idx的step ，由于overlap 存在 ，stepSize 小于等于blkSize
    sigLen = np.size(sigData)
    stepSize = int( np.floor(blkSize*(1-Overlap)) )
    frameNumSize = int( sigLen//stepSize )  # 获得一共有多少个 片段
    
    
    # 2.1 method 1 获得idxArray, [向量化方法]
    
    # 生成 引索数组， 大小为 row nums = frameNumSize, col nums = blocksize 
    startIdxArry = np.arange(0,stepSize*frameNumSize,stepSize)  # 生成开始引索序列，间隔为 stepSize ，考虑上 overlap 
    idxArray = np.tile(np.r_[0:blkSize],(frameNumSize,1)) + startIdxArry[:,np.newaxis] # 生成信号分块的引索数组，按行分块
    
    
    ## 2.2 method 2 获得idxArray ，比较方便思维理解
    
    # frameNumSize = int( sigLen//stepSize )      # 获得一共有多少个 片段
    # startIdxArry = np.arange(0,frameNumSize*stepSize,stepSize)
    # endIdxArry = startIdxArry + blkSize
    
    # # 获取idxArray 数组
    # 
    # if endIdxArry[-1] >= sigLen:
    #     idxArray = np.zeros((np.size(startIdxArry)-1,blkSize),dtype=np.int32)
    # else:
    #     idxArray = np.zeros((np.size(startIdxArry),blkSize),dtype=np.int32)
    #
    # k=0
    # for i,j in zip(startIdxArry,endIdxArry):
    #     if j <= sigLen:
    #         idxArray[k,:]=np.arange(i,j)
    #         k = k+1
    
    
    # 3 通过idxArray获得数组
    sigBlks = sigData[idxArray]
    lenSigBlks,_=sigBlks.shape

    return lenSigBlks,sigBlks


#%% 数据预处理
#--------------- 根据时间坐标获取数据子集 ---------------
def get_waveform_subset(chn,dt,timeStart,timeEnd,method='relative'):
    '''
    Parameters
    ----------
    chn : array like, numpy 1D value
        DESCRIPTION.
    dt : float
        time_increment of chn
    timeStart : float
        sub time start
    timeEnd : TYPE
        sub time end
    method : TYPE, optional
        sub time meothd , relative or absolutely. The default is 'relative'.

    Returns
    -------
    subChn : array like, numpy 1D value
        sub channel get by time start , time end
    dt : TYPE
        DESCRIPTION.

    '''
    
    startIdx = timeStart//dt 
    endIdx = timeEnd//dt 
    
    if endIdx >= max(chn.shape):
        endIdx =  max(chn.shape)
        
    subChn = chn[startIdx:endIdx]
    
    return subChn,dt

#%% 单通道 重采样
def resampling_chn(chn,dt,dt_new):
    # generate x_old time stamp array 1D
    x_old = np.arange(0,dt*max(chn.shape),dt)
    # generate x_new time stamp array 1D
    x_new = np.arange(0,dt*max(chn.shape),dt_new)
    
    # generate interpolate func
    f = interpolate.interp1d(x_old,chn,kind='linear')
    chn_new = f(x_new)
    
    return chn_new,dt_new