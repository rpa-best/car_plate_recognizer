import cv2
from camera import VideoCamera

cap = VideoCamera({})
print(cap._recognize(cv2.imread("./images/image2.png")))
