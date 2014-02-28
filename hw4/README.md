CS682 HW#4 2/28/2014 Zhonghua Xi 
=================================


Edge Finding
----------
Edges were found by using Canny Edge Detector

1. Apply a Gaussian Blur with Sigma = 2 to filter out the noise
2. Apply Canny Edge Dectector with low threshold=250, high threshold=500

Canny use a hysteresis thresholding. We can get quite decent edges at 250/500 (low threshold should be 40%~50% of the high threshold). The higher the thrasholds are, the fewer edges we will be given.

|     Edges detected by Canny Edge Detector            |
|:----------------------------------------------------:|
| ![Image](/hw4/exp/ST2MainHall4041_edge.jpg?raw=true) |

Line Finding
------------
Lines are found by Hough Transform and Probablistic Hough Transform with below peremter settings

| Parameter | Value | Description  |
|:---------:|:-----:| ------------ |
| rho       |     1 | distance resolution of the accumulator in pixels, bigger one returns more lines |
| theta     | 1 deg | angle resolution of the accumulator, smaller one returns more lines |
| threshold |   150 | control the number of returned lines, should be big enough to filter out low votes lines |
| min_len   |    30 | HoughP only, minimum length required for a line, larger ones can fiter out noise |
| max_gap   |     5 | HoughP only, maximum gap allowed for a line, smaller ones can filter out noise |


Lines show in green were found by Hough Transform, light blue ones were found by Probablistic Hough Transform. Nearly vertical or horizontal lines are shown in orange in both algorithms.

Compared to Hough, HoughP can directly tell where the lines start and where they end. And by providing minimum-length of the line and maximum gap, HoughP could be more rubost than Hough.




| Hough Transform |
|:---------------:|
| ![Image](/hw4/exp/ST2MainHall4041_hough.jpg?raw=true) |


| Probablistic Hough Transform |
|:----------------------------:|
| ![Image](/hw4/exp/ST2MainHall4041_houghP.jpg?raw=true) |


| Probablistic Hough Transform, line extended |
|:----------------------------:|
| ![Image](/hw4/exp/ST2MainHall4041_houghP_ext.jpg?raw=true) |



Vanishing Points
----------------
"Vanishing point" is found by intersecting all potential lines (where vertical and horitonzal lines will not be taken into concideration). All potencial lines should be intersected at the same position: the vanishing point. However, in the real world case, multiple vanishing points will be calculated from one image shown in yellow in below images. The way I used to estimate the real vanishing point (shown in red) is as follow:

1. Compute the center of mess of all intersection points as COM1
2. For each intersection point, compute its distance from to COM1
3. Filter out bad points whose distance > threshold distance ( 25% thrown )
4. Re-compute the center of mess of good points as COM2 for optimization as an initial guess
5. Apply optimization method to find optimal vanishing point v by minimizing the Σ||v-v<sub>i</sub>||<sup>2</sup>

| Vanishing points found by using Hough |
|:-------------------------------------:|
| ![Image](/hw4/exp/ST2MainHall4041_hough_inter.jpg?raw=true) |
| COM1 = (746, 581) COM2 = (734, 592) Vanishing Point = (729,588) |

| Vanishing points found by using HoughP |
|:-------------------------------------:|
| ![Image](/hw4/exp/ST2MainHall4041_houghP_inter.jpg?raw=true) |
| COM1 = (750, 579) COM2 = (746, 592) Vanishing Point = (738,586) |

Code ans Usage
--------------
You can find the code in src directory.
The program provides two ways to use:

1. Directly mode: ./hw4.py img_path, will output all the images (Canny Edges, Hough, HoughP, vasnishing poitns, etc)
2. Interative mode: ./hw4.py img_path tune, will give you a UI to play with like below

![Image](/hw4/exp/tune1.jpg?raw=true)
![Image](/hw4/exp/tune2.jpg?raw=true)



Results
-------

NOTE: 

1. All the images below use the same parameters metioned above. However, the parameters should be tuned for each image seperately in practice.
2. All the operations are done is full resultion (1600*1200), results are shown in 800*600

| 4017 |
|:----:|
| ![Image](/hw4/exp/ST2MainHall4017_edge.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4017_hough_inter.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4017_houghP_inter.jpg?raw=true) |

| 4020 |
|:----:|
| ![Image](/hw4/exp/ST2MainHall4020_edge.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4020_hough_inter.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4020_houghP_inter.jpg?raw=true) |

| 4041 |
|:----:|
| ![Image](/hw4/exp/ST2MainHall4041_edge.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4041_hough_inter.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4041_houghP_inter.jpg?raw=true) |

| 4054 |
|:----:|
| ![Image](/hw4/exp/ST2MainHall4054_edge.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4054_hough_inter.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4054_houghP_inter.jpg?raw=true) |

| 4086 |
|:----:|
| ![Image](/hw4/exp/ST2MainHall4086_edge.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4086_hough_inter.jpg?raw=true) |
| ![Image](/hw4/exp/ST2MainHall4086_houghP_inter.jpg?raw=true) |

