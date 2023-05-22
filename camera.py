import time
import cv2
import os
import requests
from threading import Thread
from PIL import Image
import base64
from io import BytesIO
from services import CarControlService
from pytesseract import image_to_string, pytesseract

class VideoCamera:
    _vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

    def __init__(self, params: dict) -> None:
        self.params = params
        if params.get('ip'):
            self.video = cv2.VideoCapture(params.get('ip'))
            Thread(target=self.run).start()
    
    def _recognize(self, frame) -> str:
        try:
            result = image_to_string(frame, 'rus')  
        except pytesseract.TesseractNotFoundError:
            result = "123"
        if result:
            frame_base64 = self._image_to_base64(frame)
            result = self.request_to_yandex_api(frame_base64)
            return self._parse_result(result)

    def _parse_result(self, result):
        plates = []
        for r in result:
            for rr in r.get("results", []):
                for p in rr.get("textDetection", {}).get("pages", []):
                    for b in p.get("blocks", []):
                        for l in b.get("lines", []):
                            for w in l.get("words", []):
                                plates.append(w.get("text"))
        print(plates)
        return plates

    def _image_to_base64(self, image):
        with BytesIO() as buff:
            pil_img = Image.fromarray(image)
            pil_img.save(buff, format="PDF")
            return base64.b64encode(buff.getvalue()).decode("utf-8")
    
    def _get_headers(self):
        return {'Authorization': f'Api-Key {os.getenv("YANDEX_OCR_TOKEN")}'}
    
    def _get_body(self, image_as_base64: list, model="license-plates"):
        feature = {
            'type': 'TEXT_DETECTION',
            'textDetectionConfig': {
                'languageCodes': ["ru"],
            }
        }

        if model is not None:
            feature['textDetectionConfig']['model'] = model

        data = {'analyzeSpecs': [
            {
                'content': image_as_base64,
                "mime_type": 'application/pdf',
                'features': [feature]
            }
        ]}
        return data
    
    def request_to_yandex_api(self, image_as_base64):
        response = requests.post(self._vision_url, headers=self._get_headers(),
                                json=self._get_body(image_as_base64))
        print(response.json())
        return response.json().get('results', [])


    def _send_response(self, plate: str):
        try:
            CarControlService().plate_response(plate, self.params)
        except Exception as _exp:
            print(f"Plate not sended: {_exp}")

    def run(self):
        while True:
            time.sleep(15)
            ret, frame = self.video.read()
            if ret:
                plate = self._recognize(frame)
                if plate:
                    print(plate)
                    self._send_response(plate)
                else: 
                    print('Plate not found')
            else:
                print('Camera not read a frame')
