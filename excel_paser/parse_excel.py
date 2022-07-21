#!/usr/bin/env python
# Author: 
import os
import pandas as pd
import numpy as np
import xlwt
from pandas import DataFrame,Series
import re



def excel_read(path):
    write_data = []
    df = pd.read_excel(path)
    # print(df.columns)
    # print(df.dtypes)
    write_data.append(df.columns)
    print(write_data)
    df_gps = pd.DataFrame({"test"})
    gps_sv_num = 2
    df_new=df.loc[(df['是否通过']==0)]
    df_new.to_excel('gps_error1.xls')
    # print(df_new)
    total = 0
    write_data = []
    for index, row in df_new.iterrows():
        
        if row['EXT GPS L1'] < 2 or row['EXT GPS L5'] < 2 \
        or row['EXT BDS B1'] < 2 or  row['EXT GLS G1'] < 2\
        or row['INNER GPS L1'] < 2 or row['INNER GPS L5'] < 2 \
        or row['INNER BDS B1'] < 2 or  row['INNER GLS G1'] < 2:
        #    row['EXT GPS L5'] < 2 or
        #    row['EXT GPS B1'] < 2 or
        #    row['EXT GPS G1'] < 2 or
        #    row['INNER GPS L1'] < 2 or
        #    row['INNER GPS L5'] < 2 or
        #    row['INNER GPS B1'] < 2 or
        #    row['INNER GPS G1'] < 2 :
            # row.to_excel('gps_error_all.xls')
            total += 1
            print(total)
            write_data.append(row)
            # print(write_data)
            # if total == 1:  
            #     df_start = pd.DataFrame(row,index=[total])
            #     print(type(df_start))

            # else:
            #     df_cur = pd.DataFrame(row,index=[total])

            #     print(type(df_cur))
            #     df_start = df_start.append(df_cur,ignore_index=True)  
    df_start = pd.DataFrame(write_data,columns=df.columns)  
    # df_start
    df_start.to_excel('gps_error_all_new.xls')
    


def main():
    print("Get the bit stream of file")

    file_name = "half_check_0524.xlsx"

    #FileDir = input("Input path:")
    excel_read(file_name)

    


if __name__ == '__main__':
    main()
