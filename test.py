import cv2, os
from camera import VideoCamera

os.environ.setdefault("YANDEX_OCR_TOKEN", "AQVN3VKtZcrmxPPfSd4V5d3ALgvI9Ayb_4AIuZps")

cap = VideoCamera({})
print(cap._recognize(cv2.imread("./images/image2.png")))
