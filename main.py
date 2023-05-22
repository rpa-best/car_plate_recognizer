import os
import json
from dotenv import load_dotenv
from camera import VideoCamera

os.environ.setdefault("YANDEX_OCR_TOKEN", "AQVN3VKtZcrmxPPfSd4V5d3ALgvI9Ayb_4AIuZps")

def main():
    with open('camera_config.json') as file:
        config = json.load(file)

    for params in config:
        VideoCamera(params)


if __name__ == '__main__':
    if os.path.exists(".env"):
        load_dotenv()
    main()
