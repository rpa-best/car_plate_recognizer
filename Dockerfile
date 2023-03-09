FROM python:3.9

RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get install -y python3 python3-distutils python3-pip 

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip3 install pytesseract
RUN pip3 install opencv-python

COPY . /app
WORKDIR /app

RUN pip install imutils pandas matplotlib

CMD ["python", "test.py"]