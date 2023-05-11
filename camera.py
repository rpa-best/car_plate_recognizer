import time
import imutils
import cv2.cv2 as cv2
import numpy as np
import easyocr
from threading import Thread

from services import CarControlService

reader = easyocr.Reader(["ru"])

class VideoCamera:
    def __init__(self, params: dict) -> None:
        self.params = params
        self.carplate_haar_cascade = cv2.CascadeClassifier('./haarcascades/mallick_haarcascade_russian_plate_number.xml')
        if params.get('ip'):
            self.video = cv2.VideoCapture(params.get('ip'))
            Thread(target=self.run).start()
    
    def _recognize(self, frame) -> str:
        img = cv2.resize(frame, (600,400) )

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray = cv2.bilateralFilter(gray, 13, 15, 15) 

        edged = cv2.Canny(gray, 30, 200) 
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        for c in contours:
            
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        
            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
            detected = 0
            print ("No contour detected")
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

            mask = np.zeros(gray.shape,np.uint8)
            cv2.drawContours(mask,[screenCnt],0,255,-1,)
            cv2.bitwise_and(img,img,mask=mask)

            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx+1, topy:bottomy+1]
            test = reader.recognize(Cropped, decoder="beamsearch", allowlist="1234567890АВЕКМНОРСТУХ", detail=0, batch_size=5, )
            test = "".join(test)
            print("programming_fever's License Plate Recognition\n")
            print("Detected license plate Number is:", test)
            img = cv2.resize(img,(500,300))
            Cropped = cv2.resize(Cropped,(400,200))
            return test
        else:
            print("Plate not found")

    def _send_response(self, plate: str):
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
