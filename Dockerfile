FROM python:3.9

RUN apt-get update && apt-get -y install tesseract-ocr ffmpeg libsm6 libxext6 tesseract-ocr-rus -y

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]