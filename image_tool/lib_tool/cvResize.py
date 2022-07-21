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
    if width > height:
        imgData = cv2.flip(imgData, 0)
        imgData = cv2.transpose(imgData)
    if show:
        cv2.imshow("raw", imgData)
        cv2.waitKey(2000)
    return imgData

def save_raw(save_path,save_img):
    np.save(save_path,save_img.reshape(-1))

if __name__ == "__main__":
    input_path = "nir_channel_1to4_360x640.raw"
    save_path = "result.jpg"
    alpha_zero = False
    parse_raw_w,parse_raw_h = 360,640
    resize_w,resize_h = 180,320
    if input_path.endswith(".raw"):
        input_data = parse_raw(input_path,image_size=(parse_raw_w,parse_raw_h),type_="uint8",show=False)
    else:
        input_data = input_path

    if isinstance(input_data, str) and os.path.exists(input_data):
        img = cv2.imread(input_data)
        src_img = img.copy()
    elif isinstance(input_data, np.ndarray):
        src_img = input_data.copy()

    result_img = cv2.resize(src_img,(resize_w,resize_h))
    cv2.imwrite(save_path, result_img)
    alpha = np.zeros(result_img.shape[:-1]).astype(np.uint8) if alpha_zero else result_img[...,-1]
    result_raw = np.concatenate([result_img, alpha[...,None]], axis=-1).reshape(-1).astype(np.uint8)
    with open("resultc4_180x320.raw",'wb') as fd:
        for index in range(result_raw.shape[0]):
            fd.write(result_raw[index])
        #for index in range(img.shape[0]):
         #   fd.write(img[index])
    print("done")