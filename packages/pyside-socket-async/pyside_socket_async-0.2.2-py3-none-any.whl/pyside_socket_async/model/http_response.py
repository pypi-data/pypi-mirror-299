from requests import Response as RequestsResponse


class ResponseError():
    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error

class Response():
    def __init__(self, response: RequestsResponse):
        self.status_code = response.status_code
        self.response = response