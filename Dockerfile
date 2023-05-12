FROM python:3.9

RUN apt-get update && apt-get -y install ffmpeg libsm6 libxext6 -y

COPY . /app
WORKDIR /app
ENV YANDEX_OCR_TOKEN=AQVN3VKtZcrmxPPfSd4V5d3ALgvI9Ayb_4AIuZps
RUN pip install -r requirements.txt

CMD ["python", "main.py"]