#!/usr/bin/env python
# Zhonghua Xi
# 2/27/2014

import cv2
import sys
import os
import math
import scipy as sp
import numpy as np
from scipy.optimize import minimize

CANNY_TH1 = 125
CANNY_TH2 = 250
CANNY_GB_SIGMA = 3
CANNY_APERTURE_SIZE = 5

HOUGH_RHO = 1
HOUGH_THETA = 1             #degree
HOUGH_TH = 180

HOUGHP_MIN_LEN = 30
HOUGHP_MAX_GAP = 5

# canny edge detection
def Canny(img):
    # blur the image first
    img = cv2.GaussianBlur(img, (0,0), CANNY_GB_SIGMA)
    threshold1 = CANNY_TH1
    threshold2 = CANNY_TH2
    edges = cv2.Canny(img, threshold1, threshold2, apertureSize=CANNY_APERTURE_SIZE, L2gradient=True)
    return edges

# find lines by using Hough Transformation
def HoughLines(img):
    rho = HOUGH_RHO              
    theta = HOUGH_THETA * cv2.cv.CV_PI/180
    threshold = HOUGH_TH
    lines = cv2.HoughLines(img, rho, theta, threshold)
    return lines

# find lines by using Probabilistic Hough Transformation
def HoughLinesP(img):
    rho = HOUGH_RHO              
    theta = HOUGH_THETA * cv2.cv.CV_PI/180
    threshold = HOUGH_TH
    min_len = HOUGHP_MIN_LEN
    max_gap = HOUGHP_MAX_GAP
    lines = cv2.HoughLinesP(img,rho,theta,threshold,minLineLength = min_len, maxLineGap = max_gap)
    return lines

# estimate vanishing point by minimize the objective fucntion
def EstimateVanisingPoint(pts):
    
    if len(pts) == 0:
        return -1,-1
    
    cx = 0
    cy = 0
    
    for x,y in pts:
        cx += x
        cy += y
    cx /= len(pts)
    cy /= len(pts)
    
    dists = []
    for x,y in pts:
        dist = (x-cx)**2 + (y-cy)**2
        dists.append(dist)
    
    dists.sort()
    
    min_dist = dists[len(dists)/2]
    
    temp = []
    
    for i in range(0, len(dists)):
        x = pts[i][0]
        y = pts[i][1]
        dist = (x-cx)**2 + (y-cy)**2
        if dist <= min_dist:
            temp.append(pts[i])
    
    pts = temp
    
    if len(pts) == 0:
        return -1,-1
    
    xs = np.zeros(len(pts))
    ys = np.zeros(len(pts))
    
    index = 0
    for x,y in pts:
        xs[index] = x
        ys[index] = y
        index += 1
        cx += x
        cy += y
    
    cx /= len(pts)
    cy /= len(pts)
    
    # give the optimization a good guess
    p0 =  np.array([cx, cy])
    
    # define objective function
    def obj(p):
        sum = 0
        for x,y in pts:
            sum += (x-p[0])**2 + (y-p[1])**2
        return sum
    
    result = minimize(obj, p0, method='nelder-mead', options={'xtol': 1e-8, 'disp': False})
    
    p_best = result.x
    
    vp = int(p_best[0]), int(p_best[1])
    
    print "Vanishing Point = (%d,%d)" % (vp[0], vp[1])
    
    return vp
    

# define a potencial line
def line(p1, p2):
    A = (p1[1] - p2[1]) #dy
    B = (p2[0] - p1[0]) #dx
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    if B == 0: 
        # vertical line ignored
        return False
    else:
        k = abs(float(A)/B)
        # nearly vertical or horizontal lines are also ignored
        if k>5 or k < 0.1:
            return False
    return A, B, -C

# find intersection of two lines
def intersection(L1, L2, w, h):    
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        # out of image
        if x <0 or x > w or y < 0 or y > h: return False
        return int(x),int(y)
    else:
        return False
    
def drawHoughResult(img, lines, DRAW_LINES = True, DRAW_CIRCLES = True, DRAW_BEST = True):
    out = img.copy()
    h, w = img.shape[:2]
    
    #compute the maximum length of the line
    max_len = math.sqrt(h*h + w*w)
    r = int(max_len * 0.01)
    
    ls = []
    
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + max_len*(-b))   
        y1 = int(y0 + max_len*(a))    
        x2 = int(x0 - max_len*(-b))   
        y2 = int(y0 - max_len*(a))
        if DRAW_LINES: cv2.line(out,(x1,y1),(x2,y2),(0,255,0), 2)
        l = line([x0,y0], [x1,y1])
        if l: ls.append(l)
    
    pts = []
    
    for i in range(0, len(ls)):
        for j in range(i+1, len(ls)):
            inter = intersection(ls[i], ls[j], w, h)
            if inter:
                if DRAW_CIRCLES: cv2.circle(out, inter, r, (0,255,255), thickness=2)
                pts.append(inter)
    
    if DRAW_BEST:
        center = EstimateVanisingPoint(pts)
        cv2.circle(out, center, r, (0,0,255), thickness=4)
    
    return out

def drawHoughPResult(img, lines, EXTEND_LINES = False, DRAW_LINES = True, DRAW_CIRCLES = True, DRAW_BEST = True):
    out = img.copy()
    if lines == None: return out
    
    h, w = img.shape[:2]
    
    #compute the maximum length of the line
    max_len = math.sqrt(h*h + w*w)
    r = int(max_len * 0.01)
    
    ls = []
    
    for x1,y1,x2,y2 in lines[0]:
        l = line([x1,y1], [x2,y2])
        if l:ls.append(l)

        if DRAW_LINES and EXTEND_LINES:
            theta = math.atan2(y2-y1, x2-x1)
            a = np.cos(theta)
            b = np.sin(theta)
            x1 = int(x1 + max_len*(a))   
            y1 = int(y1 + max_len*(b))    
            x2 = int(x1 - 2*max_len*(a))   
            y2 = int(y1 - 2*max_len*(b))
            
        if DRAW_LINES: cv2.line(out,(x1,y1),(x2,y2),(255,0,0),2)
    
    pts = []
    
    for i in range(0, len(ls)):
        for j in range(i+1, len(ls)):
            inter = intersection(ls[i], ls[j], w, h)
            if inter:
                if DRAW_CIRCLES: cv2.circle(out, inter, r, (0,255,255), thickness=2)
                pts.append(inter)
    
    if DRAW_BEST:
        center = EstimateVanisingPoint(pts)
        cv2.circle(out, center, r, (0,0,255), thickness=4)
                
    return out

def main(img_path):
    path, filename = os.path.split(img_path)
    
    filename, ext = os.path.splitext(filename);

    img_c = cv2.imread(img_path)
    img_b = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
    
    ##########################################
    edges = Canny(img_b)
    edge_filename = filename + "_edge.png"
    cv2.imwrite(edge_filename, edges)
    print "saved edges to %s" % edge_filename
    ##########################################
    
    ##########################################
    lines = HoughLines(edges)
    hough = drawHoughResult(img_c, lines)
    hough_filename = filename + "_hough.jpg"
    cv2.imwrite(hough_filename, hough)
    print "saved hough to %s" % hough_filename
    ##########################################
    
def Tune(img_path):
    WN = 'Tune'
    SHOW_CANNY = False
    SHOW_HOUGHP = False
    EXTEND_LINES = False
    DRAW_LINES = True
    DRAW_CIRCLES = True
    DRAW_BEST = True
    
        
    img = cv2.imread(img_path)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.namedWindow(WN, cv2.cv.CV_WINDOW_NORMAL)
    cv2.imshow(WN, img)
    
    changed = True
    
    view = img
    
    def update(*arg): 
        #################################################
        # Canny args
        if SHOW_CANNY:
            sigma = cv2.getTrackbarPos('sigma', WN)
            if sigma == 0: 
                sigma = 1
                cv2.setTrackbarPos('sigma', WN, sigma)
            thrs1 = cv2.getTrackbarPos('thrs1', WN)
            thrs2 = cv2.getTrackbarPos('thrs2', WN)
        else:
            sigma = CANNY_GB_SIGMA
            thrs1 = CANNY_TH1
            thrs2 = CANNY_TH2
        #################################################
        rho = cv2.getTrackbarPos('rho', WN)
        if rho == 0: 
            rho = 1
            cv2.setTrackbarPos('rho', WN, rho)
        rho /= 10.0
    
        theta = cv2.getTrackbarPos('theta', WN)
        if theta == 0:
            theta = 1
            cv2.setTrackbarPos('theta', WN, theta)
        
        theta = theta / 10.0 / 180.0 * cv2.cv.CV_PI
    
        threshold = cv2.getTrackbarPos('threshold', WN)
    
        min_len = cv2.getTrackbarPos('min_len', WN)
        max_gap = cv2.getTrackbarPos('max_gap', WN)
    
        grey_blur = cv2.GaussianBlur(grey, (0,0), sigma)
    
        edge = cv2.Canny(grey_blur, thrs1, thrs2, apertureSize=CANNY_APERTURE_SIZE, L2gradient=True)
        if SHOW_HOUGHP:
            linesP = cv2.HoughLinesP(edge, rho, theta, threshold, minLineLength = min_len, maxLineGap = max_gap)
            hough = drawHoughPResult(img/2, linesP, EXTEND_LINES = EXTEND_LINES, DRAW_LINES = DRAW_LINES, DRAW_CIRCLES = DRAW_CIRCLES, DRAW_BEST = DRAW_BEST)
        else:
            lines = cv2.HoughLines(edge, rho, theta, threshold)
            hough = drawHoughResult(img/2, lines, DRAW_LINES = DRAW_LINES, DRAW_CIRCLES = DRAW_CIRCLES, DRAW_BEST = DRAW_BEST)
    
        if SHOW_CANNY:
            h1, w1 = edge.shape[:2]
            h2, w2 = hough.shape[:2]
            view = sp.zeros((max(h1, h2), w1 + w2, 3), sp.uint8)
            view[:h1, :w1] = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
            view[:h2, w1:] = hough
        else:
            view = hough
            
        cv2.imshow(WN, view)
    
    if SHOW_CANNY:
        cv2.createTrackbar('thrs1', WN, CANNY_TH1, CANNY_TH1*2, update)
        cv2.createTrackbar('thrs2', WN, CANNY_TH2, CANNY_TH2*2, update)
        cv2.createTrackbar('sigma', WN, CANNY_GB_SIGMA, CANNY_GB_SIGMA*2, update)
    
    
    cv2.createTrackbar('rho', WN, HOUGH_RHO*10, HOUGH_RHO*10*2, update)
    cv2.createTrackbar('theta', WN, int(HOUGH_THETA*10), int(HOUGH_THETA*10*2), update)
    cv2.createTrackbar('threshold', WN, HOUGH_TH, HOUGH_TH*2, update)
    cv2.createTrackbar('min_len', WN, HOUGHP_MIN_LEN, HOUGHP_MIN_LEN*4, update)
    cv2.createTrackbar('max_gap', WN, HOUGHP_MAX_GAP, HOUGHP_MAX_GAP*4, update)

    
    print "p : toggle between Hough/HoughP"
    print "l : toggle drawing lines"
    print "c : toggle drawing circles"
    print "b : toggle drawing vanishing points"
    
    update()
    
    while True:
        ch = cv2.waitKey(5)
        if ch == 27:
            break
        elif ch == ord('p'):
            SHOW_HOUGHP = not SHOW_HOUGHP
            update()
        elif ch == ord('e'):
            EXTEND_LINES = not EXTEND_LINES
            update()
        elif ch == ord('l'):
            DRAW_LINES = not DRAW_LINES
            update()
        elif ch == ord('c'):
            DRAW_CIRCLES = not DRAW_CIRCLES
            update()
        elif ch == ord('b'):
            DRAW_BEST = not DRAW_BEST
            update()
                        
    cv2.destroyAllWindows()
    return

def HoughTune(img_path):
    return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'usage: %s img1 [tune]' % sys.argv[0]
        sys.exit(1)
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    if len(sys.argv) > 2:
        type = sys.argv[2]
    
    if len(sys.argv) == 2:
        main(img_path)
    else:
        if type == "tune": Tune(img_path)
        else: 
            print 'unknown type %s' % type
            sys.exit(1)