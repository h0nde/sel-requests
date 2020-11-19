class RequestException(Exception):
    pass

class HTTPError(RequestException):
    pass

class Timeout(RequestException):
    pass