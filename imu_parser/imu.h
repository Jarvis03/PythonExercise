/*
* Copyright(C), 2019-2020, Grab IOT
* File name: master.h
* Author: qiuheng
* Version: v0.0
* Date: 2020-04-08 
* Description: master
* History: Date        Author         Details 
*/

#ifndef _IMU_H_
#define _IMU_H_


/*******************************   Includes    ********************************/
#ifdef __cplusplus
#if __cplusplus
extern "C"{
#endif
#endif /* __cplusplus */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>

#define TIMESTAMP

/********************************  Macros      ********************************/
/********************************  Typedef     ********************************/
typedef unsigned char uint8_t;
typedef unsigned short uint16_t;

typedef struct tagSTRUCT_CW_BATTERY {
	unsigned int design_capacity;
	/*IC value*/
	unsigned int version;
    unsigned int voltage;	
    unsigned int capacity;
	int temp;
	/*IC config*/
	unsigned char int_config;
	unsigned char soc_alert;
	unsigned char temp_max;
	unsigned char temp_min;
	/*Get before profile write*/ 
	unsigned int volt_id;
	
	/*Get from charger power supply*/
	unsigned int charger_mode;
	
	/*Mark for change cw_bat power_supply*/
	//unsigned int change;
}STRUCT_CW_BATTERY;

typedef struct {
    size_t size;
    /** Contains GpsLocationFlags bits. */
    uint16_t flags;
    /** Represents latitude in degrees. */
    double latitude;
    /** Represents longitude in degrees. */
    double longitude;
    /**
    * Represents altitude in meters above the WGS 84 reference ellipsoid.
    */
    double altitude;
    /** Represents speed in meters per second. */
    float speed;
    /** Represents heading in degrees. */
    float bearing;
    /** Represents expected accuracy in meters. */
    float accuracy;
    /** Timestamp for the location fix. */
    int64_t timestamp;
} GpsLocation;

typedef struct {
    double latitude;
    double longitude;
    double bearing;
    double accuracy;
    int64_t timestamp;
    double speed;
    double altitude;
    int64_t source;
} GpsLocation_rpt;

typedef struct
{
    int16_t acc_x;
    int16_t acc_y;
    int16_t acc_z;
    
    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;
    
    int16_t mag_x;
    int16_t mag_y;
    int16_t mag_z;
    #ifdef TIMESTAMP
    uint8_t ts[8];
    #endif
}T_ImuAxisData;

typedef struct
{
    int64_t ts;

    int16_t temp;

    int16_t acc_x;
    int16_t acc_y;
    int16_t acc_z;

    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;

    int16_t mag_x;
    int16_t mag_y;
    int16_t mag_z;

    uint32_t press;
} ins_raw_data;

typedef struct
{
    GpsLocation   gps;
    T_ImuAxisData imu;
    STRUCT_CW_BATTERY bat;
}T_RawData;

/********************************  Variables   ********************************/
/********************************  Functions   ********************************/



#endif /* _IMU_H_ */


/********************************  End of file ********************************/
