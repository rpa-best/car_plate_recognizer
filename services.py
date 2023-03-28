import os
import uuid
import requests

class CarControlService:
    header = {
        'Authorization': ' '.join(['Basic ', os.getenv('CAR_CONTROL_BASIC_AUTHORIZATION')])
    }

    def plate_response(self, plate: str, camera_params: dict):
        camera_params.update(plate=plate)
        self.header.update({"Idempotency-Key": uuid.uuid4()})
        try:
            requests.post(camera_params.get('plate_response_url'), json=camera_params, headers=self.header)
        except requests.exceptions.RequestException:
            pass
