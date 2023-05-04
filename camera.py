import time
import re
import cv2
import numpy as np
import pytesseract
from threading import Thread

from services import CarControlService


class VideoCamera:
    def __init__(self, params: dict) -> None:
        self.video = cv2.VideoCapture(params.get('ip'))
        self.params = params
        self.carplate_haar_cascade = cv2.CascadeClassifier('plate.xml')
        Thread(target=self.run).start()

    def _carplate_extract(self, image):
        carplate_rects = self.carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5) 
        carplate_img = None
        for x,y,w,h in carplate_rects: 
            carplate_img = image[y+15:y+h-10 ,x+15:x+w-20] 
        return carplate_img
    
    
    def _enlarge_img(image, scale_percent):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        return resized_image
    
    def _recognize(self, frame) -> str:
        carplate_extract_img = self._carplate_extract(frame)
        if carplate_extract_img:
            carplate_extract_img = self._enlarge_img(carplate_extract_img, 150)
            carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
            carplate_extract_img_gray_blur = cv2.medianBlur(carplate_extract_img_gray,3) # Kernel size 3

            result = pytesseract.image_to_string(
                carplate_extract_img_gray_blur, lang='rus',
                config = f'--psm 8 --oem 3')
            regexp = r"\w{1}\d{3}\w{2}\d{2,3}"
            result = ''.join([r for r in result.replace('\n', '')])
            if re.match(regexp, result):
                return result

    def _send_response(self, plate: str):
        print(f"Plate: {plate}")
        CarControlService().plate_response(plate, self.params)

    def run(self):
        while True:
            time.sleep(1)
            ret, frame = self.video.read()
            if ret:
                try:
                    plate = self._recognize(frame)
                    if plate:
                        self._send_response(plate)
                except Exception as _exp:
                    print(_exp)
            else:
                print('Camera not read a frame')
