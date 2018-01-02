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

    #遍历所有文件
    for root, dirs, files in os.walk(dirPath):  # 返回 路径，文件夹名， 文件名

        for fileObj in files:
            oriDir = os.path.join(root, fileObj)

            filename = os.path.splitext(fileObj)[0]
            filetype = os.path.splitext(fileObj)[1]

            if filetype == ".mp3":
                print(oriDir)
                """
                f_origin = os.open(oriDir, os.O_RDONLY)
                size = os.path.getsize(oriDir)
                print(size)
                buffer = os.read(f_origin, size)
                os.close(f_origin)
                """
                buffer = ReadIntoBuffer(oriDir)
                new_dir = os.path.join(root, filename + ".h")
                f_bs = os.open(new_dir, os.O_CREAT | os.O_RDWR)

                #头文件预编译 格式
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

                    #16字节换一行
                    if i == 16:
                        i = 0
                        os.write(f_bs, b'\n')

                os.write(f_bs,b"};\n#endif")
                os.close(f_bs)



def main():
    print("Get the bit stream of file")

    #FileDir = "D:\ENG"

    FileDir = input("Input path:")

    GetAllFiles(FileDir)


if __name__ == '__main__':
    main()