"""Unit tests for utility functions."""

import logging
from unittest.mock import Mock, patch

import pytest

from src.utils import error, print_url


class TestUtils:
    """Test cases for utility functions."""

    def test_error_function_default_exception(self, caplog):
        """Test error function with default Exception class."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(Exception) as exc_info:
                error("Test error message")
        
        # Verify the exception was raised with correct message
        assert str(exc_info.value) == "Test error message"
        
        # Verify the error was logged
        assert "Test error message" in caplog.text
        assert caplog.records[0].levelname == "ERROR"

    def test_error_function_custom_exception(self, caplog):
        """Test error function with custom exception class."""
        class CustomError(Exception):
            pass
        
        with caplog.at_level(logging.ERROR):
            with pytest.raises(CustomError) as exc_info:
                error("Custom error message", CustomError)
        
        # Verify the custom exception was raised with correct message
        assert str(exc_info.value) == "Custom error message"
        assert isinstance(exc_info.value, CustomError)
        
        # Verify the error was logged
        assert "Custom error message" in caplog.text
        assert caplog.records[0].levelname == "ERROR"

    def test_error_function_logging_behavior(self, caplog):
        """Test proper logging behavior in error function."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                error("Logging test message", ValueError)
        
        # Verify logging details
        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelname == "ERROR"
        assert record.message == "Logging test message"
        assert record.name == "src.utils"

    def test_print_url_no_params(self, capsys):
        """Test print_url with URL only (no parameters)."""
        url = "https://example.com/api"
        print_url(url)
        
        captured = capsys.readouterr()
        assert captured.out.strip() == url

    def test_print_url_with_single_param(self, capsys):
        """Test print_url with single parameter."""
        url = "https://example.com/api"
        params = {"symbol": "AAPL"}
        print_url(url, params)
        
        captured = capsys.readouterr()
        assert captured.out.strip() == "https://example.com/api?symbol=AAPL"

    def test_print_url_with_multiple_params(self, capsys):
        """Test print_url with multiple parameters."""
        url = "https://example.com/api"
        params = {"symbol": "AAPL", "range": "1d", "interval": "1m"}
        print_url(url, params)
        
        captured = capsys.readouterr()
        expected_params = ["symbol=AAPL", "range=1d", "interval=1m"]
        output = captured.out.strip()
        
        # Verify URL base is correct
        assert output.startswith("https://example.com/api?")
        
        # Verify all parameters are present (order may vary due to dict iteration)
        for param in expected_params:
            assert param in output

    def test_print_url_with_empty_params(self, capsys):
        """Test print_url with empty parameters dictionary."""
        url = "https://example.com/api"
        params = {}
        print_url(url, params)
        
        captured = capsys.readouterr()
        assert captured.out.strip() == url

    def test_print_url_with_none_params(self, capsys):
        """Test print_url with None parameters."""
        url = "https://example.com/api"
        print_url(url, None)
        
        captured = capsys.readouterr()
        assert captured.out.strip() == url

    def test_print_url_with_custom_print_function(self):
        """Test print_url with different print function callbacks."""
        url = "https://example.com/api"
        params = {"test": "value"}
        
        # Test with mock print function
        mock_print = Mock()
        print_url(url, params, mock_print)
        
        mock_print.assert_called_once_with("https://example.com/api?test=value")

    def test_print_url_with_lambda_print_function(self):
        """Test print_url with lambda print function."""
        url = "https://example.com/api"
        params = {"key": "value"}
        
        # Capture output using a list
        output = []
        print_url(url, params, lambda x: output.append(x))
        
        assert len(output) == 1
        assert output[0] == "https://example.com/api?key=value"

    def test_print_url_special_characters_in_params(self, capsys):
        """Test print_url with special characters in parameters."""
        url = "https://example.com/api"
        params = {"query": "test value", "symbol": "BRK.A"}
        print_url(url, params)
        
        captured = capsys.readouterr()
        output = captured.out.strip()
        
        # Verify URL base is correct
        assert output.startswith("https://example.com/api?")
        
        # Verify parameters with special characters are handled
        assert "query=test value" in output
        assert "symbol=BRK.A" in output