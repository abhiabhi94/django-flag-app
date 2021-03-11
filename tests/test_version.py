import pytest

from flag import _get_version


class TestVersion:
    @pytest.mark.parametrize(('version', 'result'), (
        ((1, 2, 3), ('1.2.3')),  # with patch
        ((1, 2), ('1.2')),  # without patch
    ))
    def test_get_version(self, version, result):
        assert _get_version((version)) == result
