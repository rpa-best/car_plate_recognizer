import json
from camera import VideoCamera


def main():
    with open('camera_config.json') as file:
        config = json.load(file)

    for params in config:
        VideoCamera(params)


if __name__ == '__main__':
    main()