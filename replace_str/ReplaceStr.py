#!/usr/bin/python

import os

import re

#list files

def listFiles(dirPath):

    fileList=[]
    
    for root,dirs,files in os.walk(dirPath):
        print(files)
        for fileObj in files:
            print(fileObj)
            fileList.append(os.path.join(root,fileObj))

    return fileList

 

def main():

    fileDir = "D:\\3MyCode\@python\\test"

    #regex = ur'FUNC_SYS_ADD_ACCDETAIL'

    fileList = listFiles(fileDir)
    
    for fileObj in fileList:
        
        f = open(fileObj,'r+')
        
        all_the_lines=f.readlines()
        print(all_the_lines) 
        f.seek(0)

        f.truncate()

        for line in all_the_lines:
            print(line) 
            f.write(line.replace('ok','OK'))    

        f.close()  

if __name__=='__main__':

    main() 
