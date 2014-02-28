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
   1. abc
   2. abc

Lines shows in green were found by Hough Transform, light blue ones were found by Probablistic Hough Transform. Nearly vertical or horizontal lines are shown in orange in both algorithms.

Compared to Hough, HoughP can directly tell where the lines start and where they end. And by providing minimum-length of the line and maximum gap, HoughP could be more rubost than Hough.

![Image](/hw4/exp/ST2MainHall4041_hough.jpg?raw=true)

Hough Transform

![Image](/hw4/exp/ST2MainHall4041_houghP.jpg?raw=true)

Probablistic Hough Transform

![Image](/hw4/exp/ST2MainHall4041_houghP_ext.jpg?raw=true)

Probablistic Hough Transform, line extended

Vanishing Points
----------------
"Vanishing point" is found by intersecting all potecial lines (where vertical and horitonzal lines will not be taken into concideration) which should be intersected at the same position: the vanishing point. However, in the real world case, multiple vanishing points will be calculated from one image. The way I used to estimate the real vanishing point is as follow:

1. Compute the COM of all "vanishing points"
2. For each "vasning point", compute the distance from it to COM
3. Filter out bad points whose distance > median distance ( 50% thrown )
5. Apply optimization method to find optimal vanishing point v by minimize the Σ||v-v<sub>i</sub>||<sup>2</sup>

Finally, the estimated vanishing point is shown in red in both algorithms.

![Image](/hw4/exp/ST2MainHall4041_hough_inter.jpg?raw=true)
Vanishing points found by using Hough

![Image](/hw4/exp/ST2MainHall4041_houghP_inter.jpg?raw=true)
Vanishing points found by using HoughP

Code ans Usage
--------------
You can find the code in src directory.
This code provide two ways to use:

1. Directly use: ./hw4.py img_path, will output all the images (Canny Edges, Hough, HoughP, vasnishing poitns, etc)
2. Interative mode: ./hw4.py img_path tune, will give you a UI to play with like below

![Image](/hw4/exp/tune1.jpg?raw=true)
![Image](/hw4/exp/tune2.jpg?raw=true)



Results
-------
![Image](/hw4/exp/ST2MainHall4017_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4020_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4041_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4054_edge.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4080_edge.jpg?raw=true)

![Image](/hw4/exp/ST2MainHall4017_hough_inter.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4017_houghP_inter.jpg?raw=true)

![Image](/hw4/exp/ST2MainHall4020_hough_inter.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4020_houghP_inter.jpg?raw=true)

![Image](/hw4/exp/ST2MainHall4041_hough_inter.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4041_houghP_inter.jpg?raw=true)

![Image](/hw4/exp/ST2MainHall4054_hough_inter.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4054_houghP_inter.jpg?raw=true)

![Image](/hw4/exp/ST2MainHall4080_hough_inter.jpg?raw=true)
![Image](/hw4/exp/ST2MainHall4080_houghP_inter.jpg?raw=true)

