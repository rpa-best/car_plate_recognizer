import uuid
import requests

class CarControlService:
    header = {}

    def plate_response(self, plate: list, camera_params: dict):
        for p in plate:
            camera_params.update(plate=p)
            self.header.update({"Idempotency-Key": uuid.uuid4()})
            response = requests.post(camera_params.get('plate_response_url'), json=camera_params, headers=self.header)
            print(response.json())
