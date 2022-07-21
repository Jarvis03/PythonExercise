#!/usr/bin/env python
# Author: darkbit

import os
import types
import re
import time
import struct

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
                """
                f_origin = os.open(oriDir, os.O_RDONLY)
                size = os.path.getsize(oriDir)
                print(size)
                buffer = os.read(f_origin, size)
                os.close(f_origin)
            
                buffer = ReadIntoBuffer(oriDir)
                new_dir = os.path.join(root, filename + ".h")
                f_bs = os.open(new_dir, os.O_CREAT | os.O_RDWR)

                IfData = "#ifndef __%s_H \n#define __%s_H\n" % (filename, filename)
                DataName = "const unsigned char %s[] = {\n" % filename


                os.write(f_bs, bytes(IfData,encoding="utf8"))
                os.write(f_bs, bytes(DataName,encoding="utf8"))

                i = 0
                for index in buffer:
                    format_byte = b"0x%02x," % index
                    #print(format_byte,end='')
                    os.write(f_bs, format_byte)

                    i += 1

                    if i == 16:
                        i = 0
                        os.write(f_bs, b'\n')

                os.write(f_bs,b"};\n#endif")
                os.close(f_bs)
                """
    file_list.sort(reverse=True)
    return file_list
   
class use_file:
    def __init__(self,path):
        self.f = open(path,"w") 
    
    def write(self,data):
        self.f.write(str(data))
    def close(self):
        self.f.close()
    



def  imu_parser(path) :
    imu_file = use_file("imu_out.txt")
    with open(path, 'rb') as f:
        while 1:
            imu_raw = f.read(32)
            if not imu_raw :
                print("file is done")
                break
            imu_data = struct.unpack("<Q10hI",imu_raw)
            # imu_file.write(acc)
            cur_time = imu_data[0] / 1000.0
            
            str_list = time.strftime('%Y-%m-%d %H:%M:%S:', time.localtime(cur_time))
            str_list += "%03d--> " %  ((cur_time - int(cur_time)) * 1000)
            str_list += str(imu_data[1] / 100.0)
            str_list += "," + str(imu_data[2] / 4096)
            str_list += "," + str(imu_data[3] / 4096)
            str_list += "," + str(imu_data[4] / 4096)
            str_list += "," + str(imu_data[5] / (65535 / 2000))
            str_list += "," + str(imu_data[6] / (65535 / 2000))
            str_list += "," + str(imu_data[7] / (65535 / 2000))
            str_list += "," + str(imu_data[8])
            str_list += "," + str(imu_data[9])
            str_list += "," + str(imu_data[10])
            str_list += "," + str(imu_data[11] / 100.0)
            str_list += '\n'
            # print(time_str + "%3d" %  ((time_s - int(time_s)) * 1000))
            # print(time_str)
            imu_file.write(str_list)
    imu_file.close()
        

def main():
    print("Get the bit stream of file")

    FileDir = "..//imu_parser/19700101004231.imu"

    # FileDir = input("Input path:")
    imu_parser(FileDir)
   


if __name__ == '__main__':
    main()
