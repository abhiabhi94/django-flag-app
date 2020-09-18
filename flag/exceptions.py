"""Application wide exceptions"""
try:
    from rest_framework.exceptions import APIException
except ModuleNotFoundError:
    APIException = Exception


class FlagBadRequest(APIException):
    status_code = 400
    default_detail = 'Bad Request'

    def __init__(self, detail=None, status_code=None):
        if status_code:
            self.status_code = status_code
        if not detail:
            detail = self.default_detail
        self.detail = detail
