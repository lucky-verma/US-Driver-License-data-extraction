# [Research]
## Approach 1: Triangle Similarity
1. Focal length calculation requires object **bbox** and **Distance** to *calibrate* and *compute* the Focal length.
2. We can use research surveys to get estimated head/{or any} sizes according to age & gender
   (https://pubmed.ncbi.nlm.nih.gov/18727867/), OR we can use the NN to get width estimation inplace.
3. what we are doing is **not true** camera calibration. True camera calibration involves the intrinsic parameters of the camera. 
   (http://www.vision.caltech.edu/bouguetj/calib_doc/htmls/parameters.html).

References: 
1. https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
2. https://github.com/pablovela5620/Hand-Detection-and-Distance-Estimation