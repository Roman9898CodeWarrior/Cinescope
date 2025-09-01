import json
import requests

class RequestUtils:
    @staticmethod
    def get_request_body(response: requests.Response):
        if response is None or response.request is None:
            return None
        request_body_string = response.request.body.decode('utf-8')
        return json.loads(request_body_string)