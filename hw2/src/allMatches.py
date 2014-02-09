#!/usr/bin/env python
# Zhonghua Xi
# 2/7/2014
# matching features of two images
import cv2
import sys
import scipy as sp
import glob
import numpy as np

def match(img1_path, img2_path):

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

    # create Brute Force descriptor matcher
    matcher = cv2.BFMatcher()
    # get k=2 best matches
    matches = matcher.knnMatch(d1, d2, 2)

    # keep only the reasonable matches
    # apply ratio test explained by D.Lowe
    sel_matches = [m for m,n in matches if m.distance < 0.75*n.distance]
    
    # return a matched score 0 ~ 1
    return float(len(sel_matches)) / min(len(k1), len(k2))    


def main(argv):
    if len(argv) < 2:
        print 'usage: %s folder_of_imgs' % sys.argv[0]
        sys.exit(1)

    imgs = glob.glob(argv[1] + "*.jpg")

    count = len(imgs)
    
    mat = np.zeros((count,count), np.float32);
    
    for i in range(0, count):
        for j in range(i+1, count):
            print "Matching %s %s" % (imgs[i], imgs[j]), 
            m = match(imgs[i], imgs[j])
            print "Value = %.3f " % m
            mat[i,j] = mat[j,i] = m
    
    # scale to 0 ~ 1
    mat = mat / mat.max()
    for i in range(0, count): mat[i,i] = 1.0
    
    cv2.imwrite("allMatches.png", mat*255)

if __name__ == "__main__":
    sys.exit(main(sys.argv));