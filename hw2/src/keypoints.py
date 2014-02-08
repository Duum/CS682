#!/usr/bin/env python
# Zhonghua Xi
# 2/6/2014
# Compute/Display SIFT features
import cv2
import sys
import scipy as sp

if len(sys.argv) < 2:
    print 'usage: %s img1' % sys.argv[0]
    sys.exit(1)

img_path = sys.argv[1]

img = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

# create SIFT feature detector
sift = cv2.SIFT()

# detect feature points and compute feature descriptor
kp, des = sift.detectAndCompute(img, None)

# visualize result
view = cv2.drawKeypoints(img, kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS);

cv2.namedWindow("SIFT", cv2.cv.CV_WINDOW_NORMAL)
cv2.imshow("SIFT", view)
cv2.waitKey()
