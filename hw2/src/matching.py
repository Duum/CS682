#!/usr/bin/env python
# Zhonghua Xi
# 2/7/2014
# matching features of two images
import cv2
import sys
import scipy as sp

if len(sys.argv) < 3:
    print 'usage: %s img1 img2' % sys.argv[0]
    sys.exit(1)

img1_path = sys.argv[1]
img2_path = sys.argv[2]

img1_c = cv2.imread(img1_path)
img2_c = cv2.imread(img2_path)

# convert to gray scale
img1 = cv2.cvtColor(img1_c, cv2.cv.CV_BGR2GRAY)
img2 = cv2.cvtColor(img2_c, cv2.cv.CV_BGR2GRAY)

# create SIFT feature detector
sift = cv2.SIFT()

# detect feature points and compute feature descriptor
k1, d1 = sift.detectAndCompute(img1, None)
k2, d2 = sift.detectAndCompute(img2, None)
print '#keypoint of img1 = %d, img2 = %d' % (len(k1), len(k2))

# create Brute Force descriptor matcher
matcher = cv2.BFMatcher()
# get k=2 best matches
matches = matcher.knnMatch(d1, d2, 2)

# keep only the reasonable matches
# apply ratio test explained by D.Lowe
sel_matches = [m for m,n in matches if m.distance < 0.75*n.distance]

print '#selected matches:', len(sel_matches)

# #####################################
# visualization

# draw feature points of img1 and img2
view1 = cv2.drawKeypoints(img1_c, k1, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS);
view2 = cv2.drawKeypoints(img2_c, k2, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS);

h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]
view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
view[:h1, :w1] = view1
view[:h2, w1:] = view2

for m in sel_matches:
    # draw lines between the matched keypoints
    # print m.queryIdx, m.trainIdx, m.distance
    color = tuple([sp.random.randint(0, 255) for _ in xrange(3)])
    cv2.line(view, (int(k1[m.queryIdx].pt[0]), int(k1[m.queryIdx].pt[1])), (int(k2[m.trainIdx].pt[0] + w1), int(k2[m.trainIdx].pt[1])), cv2.cv.CV_RGB(color[0],color[1],color[2]),  lineType=cv2.cv.CV_AA )

cv2.namedWindow("Matching", cv2.cv.CV_WINDOW_NORMAL)
cv2.imshow("Matching", view)
cv2.waitKey()
