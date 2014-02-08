CS 682 HW #2
============

Zhonghua Xi
-----------

Keypoints
---------
SIFT feature detector used
![Image](/results/keypoints1?raw=true) ![Image](/results/keypoints2?raw=true)
![Image](/results/keypoints3?raw=true) ![Image](/results/keypoints4?raw=true)

Matching
--------
Matching using k(k=2) best match with ratio test (75%) based on SIFT feature descriptor

AllMatches
----------
Scaled pairwise matching values are computed using following formular:
match(i,j) = len(matchedKeypoints(i,j)) / min (len(keypoints(i)), len(keypoints(i))) / len(matchedKeypoints.max()))

Results 6x:
![Image](/results/allMatches6x.png?raw=true)
This image clearly shows 4 distinct scenes(squares):
frame1~frame20, frame21~frame50, frame51~frame80, frame81~frame99