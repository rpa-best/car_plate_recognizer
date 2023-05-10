FROM python:3.9

RUN apt-get update && apt-get -y install ffmpeg libsm6 libxext6 -y

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]