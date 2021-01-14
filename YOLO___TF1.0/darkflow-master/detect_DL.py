from typing import Optional
import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt


options = {
    'pbLoad' : 'built_graph/tiny-yolo-4c.pb',
    'metaLoad' : 'built_graph/tiny-yolo-4c.meta',
    'threshold' : 0.1
}

tfnet = TFNet(options)

# img = cv2.imread('sample_img/test2.png')
# result = tfnet.return_predict(img)


# read the color image and covert to RGB

img = cv2.imread('sample_img/Illinois.jpg', cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# use YOLO to predict the image
result = tfnet.return_predict(img)

print(result)
print(img.shape)

# pull out some info from the results

tl = (result[0]['topleft']['x'], result[0]['topleft']['y'])
br = (result[0]['bottomright']['x'], result[0]['bottomright']['y'])
label = result[0]['label']


# add the box and label and display it
img = cv2.rectangle(img, tl, br, (0, 255, 0), 7)
img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
plt.imshow(img)
plt.show()