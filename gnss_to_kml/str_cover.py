#!/usr/bin/python3
# -*- coding: utf-8 -*-
from parse import parse

def test() :
    print("it is a tes ")
    gbr_deal('/Users/xuan.guo/test_data/274_bgr.txt')

def gbr_deal(path):
    array=[]
    gps={}
    with open(path, 'r') as f :
        lines = f.readlines()
        for line in lines :
            # print(line)
            str = line.split("\t")
            # print(str)
            lo = parse("gps\t{test}\tlo:{lng:f}\tla:{lat:f}\tal:{alt:f}\tsp:{speed:f}\t --- tm:{time:tc}\n",line)
            array.append(lo.named)
            print(lo.named)
            break
    print(array)


if __name__ == '__main__' :
    print("test start\n")
    # lo = parse ("lo{}","lo:1398")
    # print(lo)
    test();