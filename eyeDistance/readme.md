
## Approach 1: Triangle Similarity
   The triangle similarity goes something like this: Let’s say we have a marker or object with a known width W. We then place this marker some distance D from our camera. We take a picture of our object using our camera and then measure the apparent width in pixels P. This allows us to derive the perceived focal length F of our camera:

      F = (P x  D) / W
   I can apply the triangle similarity to determine the distance of the object to the camera:

      D’ = (W x F) / P


### Challenges and Requirements:
1. Focal length calculation requires object **bbox** and **Distance** to *calibrate* and *compute* the Focal length.
2. We can use research surveys to get estimated head/{or any} sizes according to age & gender
   (https://pubmed.ncbi.nlm.nih.gov/18727867/), OR we can use the NN to get width estimation inplace.
3. what we are doing is **not true** camera calibration. True camera calibration involves the intrinsic parameters of the camera. 
   (http://www.vision.caltech.edu/bouguetj/calib_doc/htmls/parameters.html).

## Approach 2: UPDATED 
1. get the width approximation based on survey data and user details from backend DB.
2. get the Focal length approximated based on average human hand distance OR can use the approx. **FOV** to calculate the focal length. (https://learnopencv.com/approximate-focal-length-for-webcams-and-cell-phone-cameras/).
3. Make an algo to adjust the Focal-length/pixels w.r.t. the width provided from user details.
4. Fix the width after initiating the script.

# Best Frame calculation.
1. Use `Numpy` to get the n-D Array of all frames and then find the most similar arrays and pick any 3 centre weighted array as your best frame.
2. If the `std` is not more than some upper limit than continue to distance estimation else, redo the whole to get less `std`. 


References: 
1. https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
2. https://github.com/pablovela5620/Hand-Detection-and-Distance-Estimation
3. https://thesai.org/Downloads/Volume9No9/Paper_77-Deep_Learning_based_Object_Distance_Measurement.pdf
4. https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
5. https://github.com/NVlabs/ffhq-dataset # Dataset (FACE)
6. https://www.researchgate.net/figure/Average-face-index-average-width-and-average-height-along-with-the-face-classifications_tbl4_289499995


# [Test]

1. '893' image has Focal Length: 426.6666666666667
   [[2503 1602]
   [2503 1559]
   [2631 1559]
   [2631 1602]]
2. '1069' image has Focal Length: 1105.8103434244792
   [[2506 2123] 
   [2411 1598] 
   [2738 1539] 
   [2833 2064]]
3. '1125' image has Focal Length: 516.6666666666666
   [[2233 1061]
   [2233 1007]
   [2388 1007]
   [2388 1061]]
