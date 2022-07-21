/*
* Copyright(C), 2019-2021, Grab IOT
* File fileName: imu.c
* Author: qiuheng
* Version: v0.0
* Date: 2020-04-08 
* Description: imu parser
* History: Date        Author         Details 
*/

/*******************************   Includes    ********************************/
#include <pthread.h>
#include <signal.h>
#include <time.h>
#include <signal.h>

#include "imu.h"

/********************************  Macros      ********************************/
#define DEBUG(format, ...) printf(format, ##__VA_ARGS__)
#define ERROR(format, ...) printf(format, ##__VA_ARGS__)

/********************************  Typedef     ********************************/
enum verType
{
    VER_TYPE_CAMERA,
    VER_TYPE_DONGLE,
    VER_TYPE_BUFF,
};

enum tranType
{
    TRAN_TYPE_NORMAL_ALL,
    TRAN_TYPE_NORMAL_ALL_TS,
    TRAN_TYPE_SCI_ALL,
    TRAN_TYPE_SCI_SEPERATED,
    TRAN_TYPE_BUFF,
};

/********************************  Variables   ********************************/
/********************************  Functions   ********************************/

/*******************************************************************************
*                                Implement                                     *
*******************************************************************************/
void printf_help(void)
{
    ERROR("usage:\n\t./imu [type [format]] <file>\n\n");
    ERROR("file type:\n\tCamera : 0 (default)\n\tDongle : 1\n\n");
    ERROR("ouput format:\n\tNormal : 0 (default, timestamp is date)\n\tts     : 1 (timestamp is number)\n\tScience: 2 (in 1 file)\n\tScience: 3 (in multiple files)\n");

    exit(1);
}

void parse_data(int argc, char *argv[])
{
    int verType = VER_TYPE_CAMERA;
    int tranType = TRAN_TYPE_NORMAL_ALL;
    char *fileName = NULL;

    switch (argc)
    {
    case 2:
        fileName = argv[1];
        break;
    case 3:
        verType = atoi(argv[1]);
        fileName = argv[2];
        break;
    case 4:
        verType = atoi(argv[1]);
        tranType = atoi(argv[2]);
        fileName = argv[3];
        break;
    default:
        printf_help();
        goto exit;
    }

    if (verType >= VER_TYPE_BUFF)
    {
        ERROR("[type] error!!!\n");
        printf_help();
    }

    if (tranType >= TRAN_TYPE_BUFF)
    {
        ERROR("[format] error!!!\n");
        printf_help();
    }

    if (NULL == fileName)
    {
        ERROR("<file> error!!!\n");
        printf_help();
    }

    /* predeal */
    int item_struct_size = 0;
    int total_buff_size = 0;
    if (verType == 0)
    {
        item_struct_size = sizeof(T_ImuAxisData);
        total_buff_size = (int)item_struct_size * 1024;
    }
    else
    {
        item_struct_size = sizeof(ins_raw_data);
        total_buff_size = (int)item_struct_size * 1024;
    }

    /* check file */
    struct stat fb;
    if (0 != stat(fileName, &fb))
    {
        ERROR("stat <%s> error: %s!!!\n\n", fileName, strerror(errno));
        printf_help();
    }

    DEBUG("file size = %ld\n", fb.st_size);
    if (fb.st_size < item_struct_size)
    {
        ERROR("file is too small\n");
        goto exit;
        ;
    }

    /* open file */
    /** open imu file */
    FILE *fp = NULL;
    if ((fp = fopen(fileName, "r")) == NULL)
    {
        ERROR("read %s error: %s\n", fileName, strerror(errno));
        goto exit;
    }

    /** open output file */
    char *out[6] = {"imu", "imu", "int", "acc", "gyro", "mag"};
    char out_name[32] = "";
    FILE *fpout = NULL;
    FILE *fpout1 = NULL;
    FILE *fpout2 = NULL;
    if (TRAN_TYPE_SCI_SEPERATED != tranType)
    {
        snprintf(out_name, sizeof(out_name), "%s.out", out[tranType]);
        if ((fpout = fopen(out_name, "wr")) == NULL)
        {
            ERROR("read file error: %s\n", strerror(errno));
            goto exit;
        }
    }
    else
    {
        snprintf(out_name, sizeof(out_name), "%s.out", out[2]);
        if ((fpout = fopen(out_name, "wr")) == NULL)
        {
            ERROR("read file error: %s\n", strerror(errno));
            goto exit;
        }
        snprintf(out_name, sizeof(out_name), "%s.out", out[3]);
        if ((fpout1 = fopen(out_name, "wr")) == NULL)
        {
            ERROR("read file error: %s\n", strerror(errno));
            goto exit;
        }
        snprintf(out_name, sizeof(out_name), "%s.out", out[4]);
        if ((fpout2 = fopen(out_name, "wr")) == NULL)
        {
            ERROR("read file error: %s\n", strerror(errno));
            goto exit;
        }
    }

    /* add header */
    if (tranType == TRAN_TYPE_NORMAL_ALL)
    {
        if (verType == VER_TYPE_DONGLE)
        {
            const char *header = "data\tacc_x\tacc_y\tacc_z\tgyro_x\tgyro_y\tgyro_z\tmag_x\tmag_y\tmag_z\ttemp\tbaro\n";
            fwrite(header, 1, strlen(header), fpout);
        }
        else
        {
            const char *header = "date\tacc_x\tacc_y\tacc_z\tgyro_x\tgyro_y\tgyro_z\tmag_x\tmag_y\tmag_z\n";
            fwrite(header, 1, strlen(header), fpout);
        }
    }
    else if (tranType == TRAN_TYPE_NORMAL_ALL_TS)
    {
        if (verType == VER_TYPE_DONGLE)
        {
            const char *header = "timestamp\tacc_x\tacc_y\tacc_z\tgyro_x\tgyro_y\tgyro_z\tmag_x\tmag_y\tmag_z\ttemp\tbaro\n";
            fwrite(header, 1, strlen(header), fpout);
        }
        else
        {
            const char *header = "timestamp\tacc_x\tacc_y\tacc_z\tgyro_x\tgyro_y\tgyro_z\tmag_x\tmag_y\tmag_z\n";
            fwrite(header, 1, strlen(header), fpout);
        }
    }

    /* allocate buffer */
    char *pbuff = malloc(total_buff_size);
    if (NULL == pbuff)
    {
        ERROR("malloc error: %s\n", strerror(errno));
        goto exit;
    }

    /* parse data */
    int frame_count = 0;
    for (;;)
    {
        int read_size = fread(pbuff, 1, total_buff_size, fp);
        int curr_size = read_size;

        if (verType == 0)
        {
            T_ImuAxisData *pdata = (T_ImuAxisData *)pbuff;
            while (curr_size >= item_struct_size)
            {
                long long ts = *(long long *)pdata->ts; //us
                double ts_s = (double)ts / 1000000;     //s
                double ts_ms = (double)ts / 1000;       //ms

                /* relative time */
                static int power_on_flag = 1;
                static double start_ts = 0;
                if (power_on_flag)
                {
                    power_on_flag = 0;
                    start_ts = ts_s;
                }

                /* generate date buffer */
                time_t tmt = (long)ts_s;
                struct tm *p = gmtime(&tmt);
                char timebuff[32] = "";
                strftime(timebuff, sizeof(timebuff), "%Y-%m-%d %H:%M:%S", p);

                /* save total info buffer to file */
                int offset = 0;
                char buffer[256];
                switch (tranType)
                {
                case TRAN_TYPE_NORMAL_ALL:
                {
                    offset = snprintf(buffer, sizeof(buffer), "%s.%03d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t\n",
                                      timebuff,
                                      (int)((long long)ts_ms % 1000),
                                      (int16_t)pdata->acc_x,
                                      (int16_t)pdata->acc_y,
                                      (int16_t)pdata->acc_z,
                                      (int16_t)pdata->gyro_x,
                                      (int16_t)pdata->gyro_y,
                                      (int16_t)pdata->gyro_z,
                                      (int16_t)pdata->mag_x,
                                      (int16_t)pdata->mag_y,
                                      (int16_t)pdata->mag_z);
                    fwrite(buffer, 1, offset, fpout);
                    break;
                }
                case TRAN_TYPE_NORMAL_ALL_TS:
                {
                    offset = snprintf(buffer, sizeof(buffer), "%lf\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t\n",
                                      ts_s,
                                      (int16_t)pdata->acc_x,
                                      (int16_t)pdata->acc_y,
                                      (int16_t)pdata->acc_z,
                                      (int16_t)pdata->gyro_x,
                                      (int16_t)pdata->gyro_y,
                                      (int16_t)pdata->gyro_z,
                                      (int16_t)pdata->mag_x,
                                      (int16_t)pdata->mag_y,
                                      (int16_t)pdata->mag_z);
                    fwrite(buffer, 1, offset, fpout);
                    break;
                }
                case TRAN_TYPE_SCI_ALL:
                {
                    ts_s -= start_ts;
                    offset = snprintf(buffer, sizeof(buffer), "%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\n",
                                      ts_s,
                                      (float)pdata->acc_x,
                                      (float)pdata->acc_y,
                                      (float)pdata->acc_z,
                                      (float)pdata->gyro_x,
                                      (float)pdata->gyro_y,
                                      (float)pdata->gyro_z,
                                      (float)pdata->mag_x,
                                      (float)pdata->mag_y,
                                      (float)pdata->mag_z);
                    fwrite(buffer, 1, offset, fpout);
                    break;
                }
                case TRAN_TYPE_SCI_SEPERATED:
                {
                    ts_s -= start_ts;
                    offset = snprintf(buffer, sizeof(buffer), "%.6e %.6e %.6e %.6e\n", ts_s, (float)pdata->acc_x, (float)pdata->acc_y, (float)pdata->acc_z);
                    fwrite(buffer, 1, offset, fpout);
                    offset = snprintf(buffer, sizeof(buffer), "%.6e %.6e %.6e %.6e\n", ts_s, (float)pdata->gyro_x, (float)pdata->gyro_y, (float)pdata->gyro_z);
                    fwrite(buffer, 1, offset, fpout1);
                    offset = snprintf(buffer, sizeof(buffer), "%.6e %.6e %.6e %.6e\n", ts_s, (float)pdata->mag_x, (float)pdata->mag_y, (float)pdata->mag_z);
                    fwrite(buffer, 1, offset, fpout2);
                    break;
                }
                default:
                    break;
                }

                curr_size -= item_struct_size;
                pdata += 1;
                frame_count++;
            }
        }
        else
        {
            ins_raw_data *pdata = (ins_raw_data *)pbuff;
            while (curr_size >= item_struct_size)
            {
                long long ts = pdata->ts;        // ms
                double ts_s = (double)ts / 1000; // s
                double ts_ms = (double)ts;       // ms

                /* relative time */
                static int power_on_flag = 1;
                static double start_ts = 0;
                if (power_on_flag)
                {
                    power_on_flag = 0;
                    start_ts = ts_s;
                }

                /* generate date buffer */
                time_t tmt = (long)ts_s;
                struct tm *p = gmtime(&tmt);
                char timebuff[32] = "";
                strftime(timebuff, sizeof(timebuff), "%Y-%m-%d %H:%M:%S", p);

                /* save total info buffer to file */
                int offset = 0;
                char buffer[256];
                switch (tranType)
                {
                case TRAN_TYPE_NORMAL_ALL:
                {
                    offset = snprintf(buffer, sizeof(buffer), "%s.%03d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%.2f\t%0.2f\n",
                                      timebuff,
                                      (int)((long long)ts_ms % 1000),
                                      (int16_t)pdata->acc_x,
                                      (int16_t)pdata->acc_y,
                                      (int16_t)pdata->acc_z,
                                      (int16_t)pdata->gyro_x,
                                      (int16_t)pdata->gyro_y,
                                      (int16_t)pdata->gyro_z,
                                      (int16_t)pdata->mag_x,
                                      (int16_t)pdata->mag_y,
                                      (int16_t)pdata->mag_z,
                                      (float)pdata->temp / 100,
                                      (float)pdata->press / 100);
                    fwrite(buffer, 1, offset, fpout);
                    break;
                }
                case TRAN_TYPE_NORMAL_ALL_TS:
                {
                    offset = snprintf(buffer, sizeof(buffer), "%lf\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%.2f\t%0.2f\n",
                                      ts_s,
                                      (int16_t)pdata->acc_x,
                                      (int16_t)pdata->acc_y,
                                      (int16_t)pdata->acc_z,
                                      (int16_t)pdata->gyro_x,
                                      (int16_t)pdata->gyro_y,
                                      (int16_t)pdata->gyro_z,
                                      (int16_t)pdata->mag_x,
                                      (int16_t)pdata->mag_y,
                                      (int16_t)pdata->mag_z,
                                      (float)pdata->temp / 100,
                                      (float)pdata->press / 100);
                    fwrite(buffer, 1, offset, fpout);
                    break;
                }
                case TRAN_TYPE_SCI_ALL:
                {
                    ts_s -= start_ts;
                    offset = snprintf(buffer, sizeof(buffer), "%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\t%.6e\n",
                                      ts_s,
                                      (float)pdata->acc_x,
                                      (float)pdata->acc_y,
                                      (float)pdata->acc_z,
                                      (float)pdata->gyro_x,
                                      (float)pdata->gyro_y,
                                      (float)pdata->gyro_z,
                                      (float)pdata->mag_x,
                                      (float)pdata->mag_y,
                                      (float)pdata->mag_z);
                    fwrite(buffer, 1, offset, fpout);
                    break;
                }
                case TRAN_TYPE_SCI_SEPERATED:
                {
                    ts_s -= start_ts;
                    offset = snprintf(buffer, sizeof(buffer), "%.6e %.6e %.6e %.6e\n", ts_s, (float)pdata->acc_x, (float)pdata->acc_y, (float)pdata->acc_z);
                    fwrite(buffer, 1, offset, fpout);
                    offset = snprintf(buffer, sizeof(buffer), "%.6e %.6e %.6e %.6e\n", ts_s, (float)pdata->gyro_x, (float)pdata->gyro_y, (float)pdata->gyro_z);
                    fwrite(buffer, 1, offset, fpout1);
                    offset = snprintf(buffer, sizeof(buffer), "%.6e %.6e %.6e %.6e\n", ts_s, (float)pdata->mag_x, (float)pdata->mag_y, (float)pdata->mag_z);
                    fwrite(buffer, 1, offset, fpout2);
                    break;
                }
                default:
                    break;
                }

                curr_size -= item_struct_size;
                pdata += 1;
                frame_count++;
            }
        }

        if (read_size < total_buff_size)
        {
            break;
        }
    }

    DEBUG("total counts: %04d\n", frame_count);

exit:
    if (pbuff)
        free(pbuff);
    if (fp)
        fclose(fp);
    if (fpout)
        fclose(fpout);
    if (fpout1)
        fclose(fpout1);
    if (fpout2)
        fclose(fpout2);
}

int main(int argc, char *argv[])
{
    parse_data(argc, argv);

    return 0;
}

/********************************  End of file ********************************/
