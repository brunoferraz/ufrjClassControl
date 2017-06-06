import os
from cv2 import imshow
import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 50
img1 = cv2.imread("angry.jpg", 0)
img2 = cv2.imread("angry3.jpg", 0)

sift = cv2.SIFT()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

#cv2.waitKey(0)
print len(good)
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()



    h,w, = img1.shape

    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img3 = cv2.warpPerspective(img2, cv2.invert(M)[1],(w,h))
    cv2.imshow("window", img3);

    cv2.waitKey(0)

print os.getcwd()
__name__ = "homography"
__author__ = 'brferraz'
