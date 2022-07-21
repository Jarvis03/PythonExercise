#import cv2

#img = cv2.imread("D:\\work_space\\imgs_rgb2.png")

#cv2.imshow("", img)
#cv2.waitKey(0)


import cv2
import numpy as np
import os
img_path = "IR_20_0x4_0xa0_0x2_0x0.jpg"
# imgs = cv2.imread(img_path)

# img = cv2.imread(img_path)[:,:,0].reshape(-1)



# with open(os.path.basename(img_path)[:-4]+".raw",'wb') as fd:
#     for index in range(img.shape[0]):
#         fd.write(img[index])

# import cv2
# import numpy as np
# import os
# img_path = "D:\\tsing\\app_test\\mask_no_match\\RGB_0.jpg"
# print(img_path)
# #img = cv2.imread(img_path)[:,:,0].reshape(-1)
# img = cv2.imread(img_path)
# print(img.shape)
# alpha = np.zeros(img.shape[:2])[:,:,None]
# print(img.shape[:2])
# print(alpha.shape)
# result = np.concatenate([img,alpha],axis=-1).reshape(-1).astype(np.uint8)
#
# with open(os.path.basename(img_path)[:-4]+".raw",'wb') as fd:
#     for index in range(result.shape[0]):
#         fd.write(result[index])
#     #for index in range(img.shape[0]):
#      #   fd.write(img[index])
point = [-0.551230,
-0.127207,
0.233213,
-0.212012,
-0.826845,
0.572431,
-0.212012,
0.254414,
-0.169609,
-0.360420,
0.742041,
-0.508828,
0.084805,
-0.190810,
0.402822,
-0.106006]
f = point / np.linalg.norm(point)
print (f)