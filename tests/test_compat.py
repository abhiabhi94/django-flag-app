"""This module aims to test the compatibility of the project with different django versions"""
import django
import pytest

import flag


class TestDefaultAppConfigDefinition:
    @pytest.mark.skipif(django.VERSION < (3, 2), reason='app config is automatically defined by django')
    def test_app_config_not_defined(self):
        assert hasattr(flag, 'default_app_config') is False

    @pytest.mark.skipif(django.VERSION >= (3, 2), reason='app config is  not automatically defined by django')
    def test_app_config_defined(self):
        assert hasattr(flag, 'default_app_config') is True
