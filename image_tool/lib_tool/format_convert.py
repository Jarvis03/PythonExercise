import numpy as np
import os
import cv2



def parse_raw(imgpath,image_size=(360,640),type_="uint8",show=False):
    width, height = image_size
    imgData = np.fromfile(imgpath, dtype=type_)
    channel = len(imgData) // (width * height)
    if channel==0 or channel==2 or channel > 4:
        raise Exception("This raw image channels must be 1 or 3 or 4")
    imgData = imgData.reshape(height, width, channel)
    if channel == 1:
        imgData = np.concatenate((imgData, imgData, imgData), axis=-1)
    elif channel == 4:#and (np.sum(imgData[...,-1])==0 or np.sum(imgData[...,-1])==255*width*height):
        imgData = imgData[...,:-1]
    else:
        raise Exception("This raw image alpha channel must be final")
    if show:
        cv2.imshow("raw", imgData)
        cv2.waitKey(2000)
    return imgData

def format_read(input_path, raw_w = 360, raw_h = 640):
    if input_path.endswith(".raw"):
        input_data = parse_raw(input_path,image_size=(raw_w,raw_h),type_="uint8",show=False)
    else:
        input_data = input_path

    if isinstance(input_data, str) and os.path.exists(input_data):
        img = cv2.imread(input_data)
        src_img = img.copy()
    elif isinstance(input_data, np.ndarray):
        src_img = input_data.copy()
    return  src_img
def format_to_raw(src_img, c_in = 3, c_out = 3):
    ch
