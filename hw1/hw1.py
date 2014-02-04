#!/usr/bin/env python
import cv2
import numpy as np

img = cv2.imread('me.jpg')

def gaussian_blur(sigma):
	blur = cv2.GaussianBlur(img,(4*sigma+1,4*sigma+1), sigma)
	cv2.imwrite('gaussion_' + str(sigma) + '.png', blur)
	return blur

def img_derivative(image, x, y, filename):
	kernel = np.zeros((3,3), np.float32);
	if x == 1:
		kernel[1,0] = 0.5
		kernel[1,2] = -0.5
	if y == 1:
		kernel[0,1] = 0.5
		kernel[2,1] = -0.5
	dst = cv2.filter2D(image, -1, kernel)*4
	cv2.imwrite(filename + '_d_' + str(x) + '_'  + str(y) + '.png', dst)
	return dst;

img_derivative(img, 1, 0, 'org')
img_derivative(img, 0, 1, 'org')

for i in range(1,4):
	gb = gaussian_blur(i)
	img_derivative(gb, 1, 0, 'gb_' + str(i))
	img_derivative(gb, 0, 1, 'gb_' + str(i))