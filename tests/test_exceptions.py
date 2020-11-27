import sys
from unittest.mock import patch

from rest_framework import status

from flag.exceptions import FlagBadRequest
from tests.base import TestCase


class FlagExceptionTest(TestCase):
    _default_detail = 'Bad Request'

    def test_can_create_custom_error_without_params(self):
        exception = FlagBadRequest()
        self.assertEqual(exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(exception.detail, self._default_detail)

    def test_create_custom_error_with_params(self):
        detail = 'not found'
        exception = FlagBadRequest(detail=detail, status_code=404)
        self.assertEqual(exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(exception.detail, detail)

    def test_create_custom_error_without_drf_installed(self):
        with patch.dict(sys.modules, {'rest_framework.exceptions': None}):
            from importlib import reload
            reload(sys.modules['flag.exceptions'])
            from flag.exceptions import FlagBadRequest
            exception = FlagBadRequest()

        self.assertEqual(exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(exception.detail, self._default_detail)
