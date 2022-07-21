#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
'''
#define SYS_EVT_ERR_LTE            1
#define SYS_EVT_ERR_BT             2
#define SYS_EVT_ERR_WIFI           3
#define SYS_EVT_ERR_BAT            4
#define SYS_EVT_ERR_CHARGER        5
#define SYS_EVT_ERR_SERIAL         6
#define SYS_EVT_ERR_USB_COM1       7
#define SYS_EVT_ERR_USB_COM2       8

#define SYS_EVT_ERR_TEMP_LTE       11
#define SYS_EVT_ERR_TEMP_GNSS      12

#define SYS_EVT_ERR_GNSS           16
#define SYS_EVT_ERR_IMU            17
#define SYS_EVT_ERR_MAG            18
#define SYS_EVT_ERR_BARO           19
#define SYS_EVT_ERR_AIO            20
#define SYS_EVT_ERR_OBD            21

-----------------------------------------

#define  ERR_CODE_IMU_NODEV   (0x1 <<  (ERR_TYPE_IMU + ERR_CODE_NODEV))  /* 0x01 << 0*/
#define  ERR_CODE_IMU_INIT    (0x1 <<  (ERR_TYPE_IMU + ERR_CODE_INIT))   /* 0x01 << 1*/
#define  ERR_CODE_IMU_BUSY    (0x1 <<  (ERR_TYPE_IMU + ERR_CODE_BUSY))   /* 0x01 << 2*/
#define  ERR_CODE_IMU_DATA    (0x1 <<  (ERR_TYPE_IMU + ERR_CODE_DATA))   /* 0x01 << 3*/

#define  ERR_CODE_BARO_NODEV  (0x1 <<  (ERR_TYPE_BARO + ERR_CODE_NODEV)) /* 0x01 << 4*/
#define  ERR_CODE_BARO_INIT   (0x1 <<  (ERR_TYPE_BARO + ERR_CODE_INIT))  /* 0x01 << 5*/
#define  ERR_CODE_BARO_BUSY   (0x1 <<  (ERR_TYPE_BARO + ERR_CODE_BUSY))  /* 0x01 << 6*/
#define  ERR_CODE_BARO_DATA   (0x1 <<  (ERR_TYPE_BARO + ERR_CODE_DATA))  /* 0x01 << 7*/
'''


ec25_error = ("inter error", "LTE error"   , "BT error", "WIFI error","battery error", 
            "chargre error", "serial error","USB com1 error", "USB com2 error", 
            "undefined", "undefined","LTE tempreture error"," GNSS tempreture error",
            "undefined", "undefined","undefined", "GNSS error",
            "IMU error", "magnetometer error","Barometer error","AIO error",
            "OBD error")
ag3335_error = ("IMU no device", "IMU init error", "IMU device busy","IMU data error", 
            "BARO no device", "BARO init error", "BARO device busy","BARO data error")
           
def error_code_covert(errcode):
    code = int(errcode)
    ag3335_err = code & 0xffffffff
    ec25_err   = (code >> 32) & 0xffffffff
    print("AG3335 error code [0x%x]"%ag3335_err)
    
    for i in range(8) :
        if((ag3335_err >> i) & 0x01) :
            print("ERROR bit[{0}] {1}".format(i, ag3335_error[i]))
    
    print("EC25   error code [0x%x]"%ec25_err)
    for i in range(22) :
        if((ec25_err >> i) & 0x01) :
            print("ERROR bit[{0}] {1}".format(i, ec25_error[i]))


def main(argv):

   try:
      opts, args = getopt.getopt(argv,"hi:")
   except getopt.GetoptError:
      print ('error_convert.py -i <error code>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('error_convert.py -i <error code> ')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         error_code = arg
         error_code_covert(error_code)


if __name__ == "__main__":
   main(sys.argv[1:])