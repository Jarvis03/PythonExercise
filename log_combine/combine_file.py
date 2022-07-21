#!/usr/bin/env python
# Author: darkbit

import os
import types
import re

def ReadIntoBuffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf


# list files

def GetAllFiles(dirPath):
    file_list = []
    for root, dirs, files in os.walk(dirPath):  

        for fileObj in files:
            oriDir = os.path.join(root, fileObj)

            filename = os.path.splitext(fileObj)[0]
            filetype = os.path.splitext(fileObj)[1]
            # print(oriDir)

            if filetype == ".glog_":
                print(oriDir)
                file_list.append(oriDir)
       
    file_list.sort(reverse=True)
    return file_list


def main():
    print("Get the bit stream of file")

    FileDir = "/home/guo/GD4122204008203"

    # FileDir = input("Input path:")

    filelist =  GetAllFiles(FileDir)
    index = 0
    with open("combine.out", 'wb') as f:
     
        for filename in filelist:
            print(filename)
           
            buffer = ReadIntoBuffer(filename)
            f.write(buffer)


if __name__ == '__main__':
    main()
