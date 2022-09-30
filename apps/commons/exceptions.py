from dataclasses import dataclass


class APIExceptionErrorCodes:
    BAD_REQUEST = (400, "bad_request")
    UNAUTHORIZED = (401, "unauthorized")
    NOT_FOUND = (404, "not_found")


class APIException(Exception):
    def __init__(self, exception_code: tuple, message: str, error_code: int = None):
        self.status_code = exception_code[0]
        self.status_detail = exception_code[1]
        self.error_code = error_code
        self.message = message
