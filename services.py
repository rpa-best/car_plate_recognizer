import os
import requests


class InviteService:
    header = {
        'Authorization': ' '.join('Basic', os.getenv('INVITE_BASIC_AUTHORIZATION'))
    }

    def check_import(self, plate: str, camera_params: dict):
        endpoint = f"api/invite/check/{plate}/"
        check = self._check_web(endpoint, camera_params)
        if not check:
            check = self._check_local_web(endpoint, camera_params)
        return check
    
    def _check_local_web(self, endpoint, camera_params):
        local_url = '/'.join((camera_params.get('local_web_host'), endpoint))
        return self._check(local_url, camera_params)
    
    def _check(self, url, data):
        try:
            response = requests.post(url, json=data, headers=self.header)
        
            if response.status == 200:
                return True
            return False
        except requests.exceptions.RequestException:
            return False

    def _check_web(self, endpoint, camera_params):
        url = '/'.join((camera_params.get('web_host'), endpoint))
        return self._check(url, camera_params)

    def check_export(self, plate: str, camera_params: dict):
        endpoint = f"api/import_invite/check/{plate}/"
        check = self._check_web(endpoint, camera_params)
        if not check:
            check = self._check_local_web(endpoint, camera_params)
        return check
    
    def check_invite(self, plate: str, camera_params: dict):
        mode = camera_params.get('mode')
        if mode == 'import':
            return self.check_import(plate, camera_params)
        elif mode == 'export':
            return self.check_export(plate, camera_params)
        raise ValueError('Camera params not found mode or invalid mode')


class CarControlService:
    header = {
        'Authorization': ' '.join('Basic', os.getenv('CAR_CONTROL_BASIC_AUTHORIZATION'))
    }

    def plate_response(self, plate: str, camera_params: dict):
        camera_params.update(plate=plate)
        try:
            requests.post(camera_params.get('plate_response_url'), json=camera_params, headers=self.header)
        except requests.exceptions.RequestException:
            pass
