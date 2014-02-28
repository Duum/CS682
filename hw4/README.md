CS682 HW#4 2/28/2014 Zhonghua Xi 
=================================


Edge Finding
----------
Edges were found by using Canny Edge Detector

1. Apply a Gaussian Blur with Sigma = 3 to filter out the noise
2. Apply Canny Edge Dectector with low threshold=125, high threshold=250

![Image](/hw4/exp/ST2MainHall4041_edge.jpg?raw=true)

Line Finding
------------

1. Hough Transform
2. Probablistic Hough Transform
3. Peremters

Lines shows in green were found by Hough Transform, light blue ones were found by Probablistic Hough Transform. Nearly vertical or horizontal lines are shown in orange.

Compared to Hough, HoughP can directly tell where the lines start and where they end.

![Image](/hw4/exp/ST2MainHall4041_hough.jpg?raw=true)

Hough Transform

![Image](/hw4/exp/ST2MainHall4041_houghP.jpg?raw=true)

Probablistic Hough Transform

![Image](/hw4/exp/ST2MainHall4041_houghP_ext.jpg?raw=true)

Probablistic Hough Transform, line extended

Results
-------
![Image](/hw4/exp/ST2MainHall4017_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4020_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4041_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4054_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4080_edge.jpg?raw=true)
