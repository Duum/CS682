CS 682 HW #2
============

###Zhonghua Xi

Keypoints
---------
Using SIFT feature detector, features are drawn in random colors as circles with radius as its size

![Image](/hw2/results/keypoints1.png?raw=true)

![Image](/hw2/results/keypoints2.png?raw=true)

![Image](/hw2/results/keypoints3.png?raw=true)

![Image](/hw2/results/keypoints4.png?raw=true)

Matching
--------
Matching using k(k=2) best match with ratio test (75%) based on SIFT feature descriptor

| Result                                            |
|:-------------------------------------------------:|
| ![Image](/hw2/results/matching_25_30.jpg?raw=true) |
| Same scene, # features img1 = 5213, img2 = 5404, # matched = 582 |
| ![Image](/hw2/results/matching_78_79.jpg?raw=true) |
| Different scene, # features img1 = 2370, img2 = 4756, # matched = 35 |

AllMatches
----------
Scaled pairwise matching values are computed using following formular:


1. match = zeros() 
2. scaleFactor = 1.0 / max(matchedKeypoints(i,j).size()) 
3. match(i,j) = matchedKeypoints(i,j).size() / min (keypoints(i).size()), keypoints(i).size()) * scaleFactor
4. match(i,i) = 1.0 

###Results 6x: 

![Image](/hw2/results/allMatches6x.png?raw=true)

This image clearly shows 4 distinct scenes(squares):

frame1~frame19, frame20~frame50, frame51~frame78, frame79~frame99
