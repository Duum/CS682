CS 682 HW #2
============

Zhonghua Xi
-----------

Keypoints
---------
SIFT feature detector used
![Image](/hw2/results/keypoints1.png?raw=true)

![Image](/hw2/results/keypoints2.png?raw=true)

![Image](/hw2/results/keypoints3.png?raw=true) 

![Image](/hw2/results/keypoints4.png?raw=true)

Matching
--------
Matching using k(k=2) best match with ratio test (75%) based on SIFT feature descriptor

AllMatches
----------
Scaled pairwise matching values are computed using following formular:

match = zeros()

scaleFactor = 1.0 / max(matchedKeypoints(i,j).size())

match(i,j) = matchedKeypoints(i,j).size() / min (keypoints(i).size()), keypoints(i).size()) * scaleFactor

###Results 6x:

![Image](/hw2/results/allMatches6x.png?raw=true)

This image clearly shows 4 distinct scenes(squares):

frame1~frame20, frame21~frame50, frame51~frame80, frame81~frame99