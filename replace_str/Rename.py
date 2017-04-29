#!/usr/bin/env python
#Author: shadowme

import os
import types
import re

#list files

def Rename(dirPath,oldStr,newStr):

    fileList = []
    
    for root,dirs,files in os.walk(dirPath):  # 返回 路径，文件夹名， 文件名
        
        for fileObj in files:
            
            olddir = os.path.join(root,fileObj)
            
            filename = os.path.splitext(fileObj)[0]
            filetype = os.path.splitext(fileObj)[1]
            
            new_filename = filename.replace(oldStr,newStr)
            
            newdir = os.path.join(root,new_filename+filetype)
            
            os.rename(olddir, newdir)


def main():

    print("Replace the name of all files")
    
    fileDir = input("input path:")
    OldStr  = input("input old string:")
    NewStr  = input("input new string:")

    #regex = ur'FUNC_SYS_ADD_ACCDETAIL'
    
    Rename(fileDir,OldStr,NewStr)

if __name__=='__main__':

    main() 
