import pynmea2
import os
"""
转成度分秒：如接收到的纬度是：4546.40891
4546.40891/100=45.4640891可以直接读出45度, 4546.40891–45*100=46.40891, 可以直接读出46分
46.40891–46 =0.40891*60=24.5346读出24秒, 纬度：45度46分24秒
转成小数：
Decimal Degrees = Degrees + minutes/60 + seconds/3600
例：57°55’56.6″ =57+55/60+56.6/3600=57.9323888888888

"""

def nmea_dms2deci(data):
    d = int(data / 100)
    m_val = data - d * 100
    m = int(m_val)
    s = (m_val - m) * 60
    deci = d + m / 60 + s / 3600

    # 保留7位小数
    return round(deci,7)


"""
$GPRMC,000853,V,3020.0427,N,11212.4996,E,0.000,0.0,290697,2.9,W*76
获取经纬度（小数形式）
"""
def nmea_peocess(str):
    msg = pynmea2.parse(str)
    print(repr(msg))
    # lon = nmea_dms2deci(float(msg.lon))
    # lat = nmea_dms2deci(float(msg.lat))
    lon = 1
    lat = 1
    return lon,lat

def main():


    path = "../ec25_com_2022-07-12_20_10_30.log"
    # path = "../test_gps.txt"
    save_path = "d:/savedata1.txt"
    # path = input("input file of data:")
    gps_data = []
    
    last_time = 0

    total_line = 0
    #读取文件中的GPS数据
    with open(path,"r", encoding='utf-8') as f:
        all_the_lines = f.readlines()

        f.seek(0)

        for line in all_the_lines:
            # lon,lat = nmea_peocess(line)
            total_line = total_line + 1
            # gps_data.append(lon)
            # gps_data.append(lat)
            gnss = line.split('] ',1)[1]
            # if gnss == "\n":
            #     break
            try:
                msg = pynmea2.parse(gnss)
                if gnss.startswith('$GNGGA'):
                    # print(repr(msg))
                    t = msg.timestamp
                    seconds = ((t.hour * 60 + t.minute) * 60 + t.second)*1000 + t.microsecond / 1000
                    if (seconds - last_time) > 1000:
                        print(t.second)
                        print(total_line,"timestamp error",seconds - last_time, last_time,seconds, t, msg.gps_qual) 
                    last_time = seconds
                    # print(seconds)
                # print(repr(msg))
            except pynmea2.ParseError as e:
                # print('Parse error: {}'.format(e))
                continue

        # print(gps_data)
    print(total_line)
    #s = "".join(map(str,gps_data))
    # 转换后的数据写入文件
    with open(save_path,'w') as f:
            f.write(str(gps_data))

if __name__ == '__main__':
    main()