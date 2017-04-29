#!/usr/bin/python

import os

import re

#list files

def listFiles(dirPath):

    fileList = []
    
    for root,dirs,files in os.walk(dirPath):  # 返回 路径，文件夹名， 文件名
      
        for fileObj in files:

            # 链接路径和文件名， 并加入fileList
            fileList.append(os.path.join(root,fileObj))

    return fileList

 

def main():

    
    fileDir = input("input dir:")
    OldStr  = input("input old string:")
    NewStr  = input("input new string:")

    #regex = ur'FUNC_SYS_ADD_ACCDETAIL'
    
    fileList = listFiles(fileDir)
    
    for fileObj in fileList:
        
        f = open(fileObj,'r+')
        
        all_the_lines = f.readlines()
    
        f.seek(0)

        # what mean?
        f.truncate()

        for line in all_the_lines:
          
            f.write(line.replace(OldStr,NewStr))    

        f.close()  

if __name__=='__main__':

    main() 
