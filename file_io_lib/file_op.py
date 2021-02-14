# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 21:43:05 2021

@author: Bing Zhao
"""
import os

def list_paths(folder_path , suffix):
    
    # # 获得文件夹下的文件名称
    # filepaths = os.listdir(folder_path)
    
    # #返回包含文件后缀的文件，比如 .tdms
    # # if filepaths[:] [-:-51]==  '.tdms'
    
    # find()   
    # #合并文件夹与文件名
    # for filepath in filepaths:
    
    # print(pathlist)
    pass

    
def get_filenames(folder_path,filetype):  # 输入路径、文件类型例如'.csv'
    '''
    ddd '''  
    filename = []
    path_file_name=[]
    size=[]
    for root,dirs,files in os.walk(folder_path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                filename.append(i)  
    size = len(filename)
    
    for fn in filename:
        pt_fn = folder_path +'\\'+ fn
        path_file_name.append(pt_fn)
        
    return size, path_file_name, filename            # 输出由有后缀的文件名组成的列表


#%% main
folder="D:"
num,path,files=get_filenames(folder,'.csv')
print(files)