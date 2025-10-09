from typing import Any

import pytest
from curl_cffi.requests.exceptions import HTTPError

from yafin.const import TYPES
from yafin.utils import (
    _get_func_name_and_args,
    compile_url,
    error,
    get_types_with_frequency,
)


class TestUnitUtils:
    """Tests for yafin.utils module."""

    def test_error(self) -> None:
        """Test error function."""
        with pytest.raises(Exception):
            error('Error')

    def test_error_http(self) -> None:
        """Test error function with HTTP error."""
        with pytest.raises(HTTPError):
            error('Error', HTTPError)

    def test_compile_url(self) -> None:
        """Test compile_url function."""
        url = r'https://query2.finance.yahoo.com'
        params = {
            'ticker': 'META',
            'region': 'US',
        }
        compiled_url = compile_url(url, params)
        assert compiled_url == r'https://query2.finance.yahoo.com?ticker=META&region=US'

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(frequency='annual', typ='income_statement'),
            dict(frequency='quarterly', typ='income_statement'),
            dict(frequency='trailing', typ='income_statement'),
            dict(frequency='annual', typ='balance_sheet'),
            dict(frequency='quarterly', typ='balance_sheet'),
            dict(frequency='annual', typ='cash_flow'),
            dict(frequency='quarterly', typ='cash_flow'),
            dict(frequency='trailing', typ='cash_flow'),
        ],
    )
    def test_get_types_with_frequency(self, kwargs: dict[str, Any]) -> None:
        """Test get_types_with_frequency function."""
        types = get_types_with_frequency(**kwargs)
        types_list = types.split(',')
        expected_types_list = [
            f'{kwargs["frequency"]}{t}' for t in TYPES[kwargs['typ']]
        ]
        assert sorted(types_list) == sorted(expected_types_list)

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(frequency='trailing', typ='balance_sheet'),
            dict(frequency='xxx', typ='income_statement'),
            dict(frequency='annual', typ='xxx'),
        ],
    )
    def test_get_types_with_frequency_invalid_args(
        self, kwargs: dict[str, Any]
    ) -> None:
        """Test get_types_with_frequency function with invalid arguments."""
        with pytest.raises(Exception):
            get_types_with_frequency(**kwargs)

    def test_get_func_name_and_args(self) -> None:
        """Test _get_func_name_and_args function."""
        func = print
        args = ('a', 'b', 'c')
        func_name, args_copy = _get_func_name_and_args(func, args)
        assert func_name == 'print'
        assert args_copy == ('a', 'b', 'c')
