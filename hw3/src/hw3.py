#!/usr/bin/env python
import cv2
import numpy as np
import scipy.ndimage as ndi

import matplotlib.pyplot as plt

def save_img(filename, img, scale=4):
    cv2.imwrite(filename, img*255)

# generate
def generate_img():
    img = np.zeros((20,20), np.float32)
    img.fill(50.0/255)
    offset = 2
    for i in range(0,16):
        for j in range(0,16):
            img[j+offset,i+offset] = 250.0/255
    return img
    
def img_derivative(img):
    
    dx = np.zeros((18,18), np.float32)
    dy = np.zeros((18,18), np.float32)
    
    for i in range(0,18):
        for j in range(0,18):
            dx[i,j] = 0.5*(img[i+1,j+2] - img[i+1,j])
            dy[i,j] = 0.5*(img[i+2,j+1] - img[i,j+1])
    
    return [dx,dy]

def edge_strength(dx, dy):
    edge = np.sqrt(dx**2 + dy**2)
    return edge
    
def edge_orientation(dx, dy):
    x = np.zeros(18*18)
    y = np.zeros(18*18)
    u = np.zeros(18*18)
    v = np.zeros(18*18)
    index = 0
    for i in range(0,18):
        for j in range(0,18):
            x[index] = j
            y[index] = i
            u[index] = dx[i,j]
            v[index] = dy[i,j]
            index = index+1
            
    plt.figure()
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.quiver(x,y,u,v, angles='uv', scale_units='xy')
    ax.set_xlim([-1,18])
    ax.set_ylim([-1,18])
    plt.draw()
    plt.savefig("orientation.png")
    
    ori = np.arctan2(dy, dx)
    return ori

def nms(mag, ori):
    abin = ((ori + np.pi) * 4 / np.pi + 0.5).astype('int') % 4
    mask = np.zeros(mag.shape, dtype='bool')
    mask[1:-1, 1:-1] = True
    edge_map = np.zeros(mag.shape)
    offsets = ((1, 0), (1, 1), (0, 1), (-1, 1))
    for a, (di, dj) in zip(range(4), offsets):
        cand_idx = np.nonzero(np.logical_and(abin == a, mask))
        for i, j in zip(*cand_idx):
            if mag[i, j] > mag[i + di, j + dj] and \
               mag[i, j] > mag[i - di, j - dj]:
                edge_map[i, j] = 1.0
    return edge_map
	
img = generate_img()
[dx,dy] = img_derivative(img)
edge = edge_strength(dx, dy)
ori = edge_orientation(dx, dy)
mag = np.sqrt(dx**2 + dy**2)
nms_result = nms(mag, ori);

# output
save_img('org.png', img)
save_img('dx.png', dx+0.5)
save_img('dy.png', dy+0.5)
save_img('edge.png', edge)
save_img('mag.png', mag)
save_img('nms.png', nms_result)