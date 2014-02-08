#!/usr/bin/env python
import cv2
import sys
import numpy

def main(argv):

    if len(sys.argv) < 2:
        print 'usage: %s img' % sys.argv[0]
        sys.exit(1)
    
    Im = cv2.imread(argv[1])
    Img = cv2.cvtColor(Im, cv2.cv.CV_BGR2GRAY)

    dst = cv2.cornerHarris(Img, 2, 3, 0.04)
    dst_norm = dst
    dst_norm = cv2.normalize(dst, dst_norm, 0, 255, cv2.NORM_MINMAX, cv2.CV_32FC1)

    dst_abs = cv2.convertScaleAbs(dst_norm)

    dst_size = dst_abs.shape
    for j in range(dst_size[0]):
        for i in range(dst_size[1]):
            if (dst_norm.item((j,i))>200):
                cv2.circle(dst_abs, (i,j), 5, 0, 2, 5, 0)
#                print str(i)+", "+str(j)

    cv2.namedWindow("Original", cv2.cv.CV_WINDOW_AUTOSIZE )
    cv2.imshow("Original",Im)
    cv2.namedWindow("Corners detected!", cv2.cv.CV_WINDOW_AUTOSIZE )
    cv2.imshow("Corners detected!",dst_abs)

    cv2.cv.WaitKey()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv));
