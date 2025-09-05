"""Tests for AsyncClient class."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from curl_cffi.requests import AsyncSession, Response
from curl_cffi.requests.exceptions import HTTPError

from src.client import AsyncClient


class TestAsyncClient:
    """Test class for AsyncClient."""

    def test_initialization(self):
        """Test AsyncClient initialization."""
        client = AsyncClient()
        
        # Verify session is created
        assert hasattr(client, '_session')
        assert isinstance(client._session, AsyncSession)
        
        # Verify base URL and default params are set
        assert client._BASE_URL == 'https://query2.finance.yahoo.com'
        assert 'formatted' in client._DEFAULT_PARAMS
        assert client._DEFAULT_PARAMS['formatted'] == 'false'
        assert client._DEFAULT_PARAMS['region'] == 'US'
        assert client._DEFAULT_PARAMS['lang'] == 'en-US'
        assert client._DEFAULT_PARAMS['corsDomain'] == 'finance.yahoo.com'

    @pytest.mark.asyncio
    async def test_crumb_property_success(self):
        """Test _crumb property fetches crumb successfully."""
        client = AsyncClient()
        
        # Mock the response
        mock_response = MagicMock(spec=Response)
        mock_response.text = "test_crumb_value"
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            crumb = await client._crumb
            
            # Verify the correct URL was called
            mock_get.assert_called_once_with(url='https://query2.finance.yahoo.com/v1/test/getcrumb')
            assert crumb == "test_crumb_value"

    @pytest.mark.asyncio
    async def test_crumb_property_none_response(self):
        """Test _crumb property returns None when response is None."""
        client = AsyncClient()
        
        with patch.object(client, '_get_async_request', return_value=None):
            crumb = await client._crumb
            assert crumb is None

    @pytest.mark.asyncio
    async def test_crumb_property_caching(self):
        """Test that _crumb property caches the value correctly."""
        client = AsyncClient()
        
        # Mock the response
        mock_response = MagicMock(spec=Response)
        mock_response.text = "cached_crumb"
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            # First call
            crumb1 = await client._crumb
            # Second call
            crumb2 = await client._crumb
            
            # Should be called twice since _crumb is a property, not cached
            assert mock_get.call_count == 2
            assert crumb1 == "cached_crumb"
            assert crumb2 == "cached_crumb"

    @pytest.mark.asyncio
    async def test_session_setup(self):
        """Test that session is properly configured."""
        client = AsyncClient()
        
        # Verify session configuration
        assert client._session.impersonate == 'chrome'

    @pytest.mark.asyncio
    async def test_get_async_request_success(self):
        """Test _get_async_request method with successful response."""
        client = AsyncClient()
        
        # Mock successful response
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response) as mock_get:
            url = "https://example.com/api"
            params = {"param1": "value1", "param2": "value2"}
            
            result = await client._get_async_request(url, params)
            
            # Verify session.get was called with correct parameters
            mock_get.assert_called_once_with(url, params=params)
            mock_response.raise_for_status.assert_called_once()
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_async_request_no_params(self):
        """Test _get_async_request method without parameters."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response) as mock_get:
            url = "https://example.com/api"
            
            result = await client._get_async_request(url)
            
            mock_get.assert_called_once_with(url, params=None)
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_async_request_http_error(self):
        """Test _get_async_request method handles HTTP errors."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.side_effect = HTTPError("HTTP 404 Not Found")
        
        with patch.object(client._session, 'get', return_value=mock_response):
            with pytest.raises(Exception):  # error() function raises generic Exception
                await client._get_async_request("https://example.com/api")

    def test_get_result_success(self):
        """Test _get_result method with successful response."""
        client = AsyncClient()
        
        # Mock response data
        response_data = {
            "chart": {
                "result": [{"symbol": "AAPL", "data": "test_data"}],
                "error": None
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = response_data
        
        result = client._get_result(mock_response, "chart")
        
        assert result == {"symbol": "AAPL", "data": "test_data"}
        mock_response.json.assert_called_once()

    def test_get_result_with_error(self):
        """Test _get_result method handles API errors."""
        client = AsyncClient()
        
        # Mock response data with error
        response_data = {
            "chart": {
                "result": [{"symbol": "AAPL"}],
                "error": "Invalid ticker symbol"
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = response_data
        
        with pytest.raises(Exception):  # error() function raises generic Exception
            client._get_result(mock_response, "chart")

    def test_get_result_json_parsing(self):
        """Test _get_result method properly parses JSON."""
        client = AsyncClient()
        
        # Mock complex response data
        response_data = {
            "quoteSummary": {
                "result": [{
                    "assetProfile": {"sector": "Technology"},
                    "price": {"regularMarketPrice": {"raw": 150.0}}
                }],
                "error": None
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = response_data
        
        result = client._get_result(mock_response, "quoteSummary")
        
        assert "assetProfile" in result
        assert "price" in result
        assert result["assetProfile"]["sector"] == "Technology"
        assert result["price"]["regularMarketPrice"]["raw"] == 150.0

    @pytest.mark.asyncio
    async def test_get_chart_success(self):
        """Test get_chart method with valid parameters."""
        client = AsyncClient()
        
        # Mock response data
        chart_data = {
            "meta": {"symbol": "AAPL", "currency": "USD"},
            "timestamp": [1640995200, 1641081600],
            "indicators": {
                "quote": [{
                    "open": [182.01, 179.61],
                    "high": [182.88, 180.17],
                    "low": [177.71, 174.64],
                    "close": [177.57, 174.92],
                    "volume": [59773000, 80440800]
                }]
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "chart": {
                "result": [[chart_data]],  # Note: get_chart returns result[0][0]
                "error": None
            }
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            result = await client.get_chart("AAPL", "1d", "1d", "div,split")
            
            assert result == chart_data

    @pytest.mark.asyncio
    async def test_get_chart_parameter_validation(self):
        """Test get_chart method validates parameters correctly."""
        client = AsyncClient()
        
        # Test invalid range
        with pytest.raises(Exception):
            await client.get_chart("AAPL", "invalid_range", "1d")
        
        # Test invalid interval
        with pytest.raises(Exception):
            await client.get_chart("AAPL", "1d", "invalid_interval")
        
        # Test invalid events
        with pytest.raises(Exception):
            await client.get_chart("AAPL", "1d", "1d", "invalid_events")

    @pytest.mark.asyncio
    async def test_get_chart_valid_ranges(self):
        """Test get_chart accepts all valid ranges."""
        client = AsyncClient()
        
        valid_ranges = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "chart": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            for range_val in valid_ranges:
                # Should not raise exception
                await client.get_chart("AAPL", range_val, "1d")

    @pytest.mark.asyncio
    async def test_get_chart_valid_intervals(self):
        """Test get_chart accepts all valid intervals."""
        client = AsyncClient()
        
        valid_intervals = ['1m', '5m', '15m', '30m', '1h', '6h', '1d']
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "chart": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            for interval in valid_intervals:
                # Should not raise exception
                await client.get_chart("AAPL", "1d", interval)

    @pytest.mark.asyncio
    async def test_get_chart_valid_events(self):
        """Test get_chart accepts all valid events."""
        client = AsyncClient()
        
        valid_events = ['div', 'split', 'div,split', 'split,div']
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "chart": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            for events in valid_events:
                # Should not raise exception
                await client.get_chart("AAPL", "1d", "1d", events)

    @pytest.mark.asyncio
    async def test_get_chart_url_construction(self):
        """Test get_chart constructs correct URL and parameters."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "chart": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_chart("AAPL", "1d", "1h", "div")
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/v8/finance/chart/AAPL"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com',
                'range': '1d',
                'interval': '1h',
                'events': 'div'
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_chart_default_events(self):
        """Test get_chart uses default events parameter."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "chart": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_chart("AAPL", "1d", "1d")  # No events parameter
            
            # Verify default events is used
            call_args = mock_get.call_args
            params = call_args[0][1]  # Second positional argument is params
            assert params['events'] == 'div,split'

    @pytest.mark.asyncio
    async def test_get_quote_single_ticker(self):
        """Test get_quote method with single ticker."""
        client = AsyncClient()
        
        quote_data = {
            "symbol": "AAPL",
            "regularMarketPrice": 150.0,
            "currency": "USD"
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "quoteResponse": {
                "result": [[quote_data]],  # Note: get_quote returns result[0][0]
                "error": None
            }
        }
        
        # Mock both crumb request and quote request
        def mock_get_async_request(url, params=None):
            if 'getcrumb' in url:
                crumb_response = MagicMock(spec=Response)
                crumb_response.text = "test_crumb"
                return crumb_response
            else:
                return mock_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_async_request) as mock_get:
                result = await client.get_quote("AAPL")
                
                assert result == quote_data
                
                # Verify URL and parameters
                expected_url = "https://query2.finance.yahoo.com/v7/finance/quote"
                expected_params = {
                    'formatted': 'false',
                    'region': 'US',
                    'lang': 'en-US',
                    'corsDomain': 'finance.yahoo.com',
                    'symbols': 'AAPL',
                    'crumb': 'test_crumb'
                }
                
                # Verify the quote call (second call)
                quote_call = mock_get.call_args_list[-1]
                assert quote_call[0][0] == expected_url
                assert quote_call[0][1] == expected_params

    @pytest.mark.asyncio
    async def test_get_quote_multiple_tickers(self):
        """Test get_quote method with multiple tickers."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "quoteResponse": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Mock both crumb request and quote request
        def mock_get_async_request(url, params=None):
            if 'getcrumb' in url:
                crumb_response = MagicMock(spec=Response)
                crumb_response.text = "test_crumb"
                return crumb_response
            else:
                return mock_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_async_request) as mock_get:
            await client.get_quote("AAPL,GOOGL,MSFT")
            
            # Verify symbols parameter - get the last call (quote call, not crumb call)
            quote_call = mock_get.call_args_list[-1]
            params = quote_call[0][1]  # Second positional argument is params
            assert params['symbols'] == 'AAPL,GOOGL,MSFT'

    @pytest.mark.asyncio
    async def test_get_quote_summary_valid_modules(self):
        """Test get_quote_summary method with valid modules."""
        client = AsyncClient()
        
        summary_data = {
            "assetProfile": {"sector": "Technology"},
            "price": {"regularMarketPrice": {"raw": 150.0}}
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "quoteSummary": {
                "result": [[summary_data]],  # Note: get_quote_summary returns result[0][0]
                "error": None
            }
        }
        
        # Mock both crumb request and quote summary request
        def mock_get_async_request(url, params=None):
            if 'getcrumb' in url:
                crumb_response = MagicMock(spec=Response)
                crumb_response.text = "test_crumb"
                return crumb_response
            else:
                return mock_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_async_request) as mock_get:
            result = await client.get_quote_summary("AAPL", "assetProfile,price")
            
            assert result == summary_data
            
            # Verify URL and parameters - get the last call (quote summary call, not crumb call)
            quote_summary_call = mock_get.call_args_list[-1]
            expected_url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAPL"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com',
                'modules': 'assetProfile,price',
                'crumb': 'test_crumb'
            }
            
            assert quote_summary_call[0][0] == expected_url
            assert quote_summary_call[0][1] == expected_params

    @pytest.mark.asyncio
    async def test_get_quote_summary_invalid_modules(self):
        """Test get_quote_summary method validates modules."""
        client = AsyncClient()
        
        # Test with invalid module
        with pytest.raises(Exception):
            await client.get_quote_summary("AAPL", "invalidModule")
        
        # Test with mix of valid and invalid modules
        with pytest.raises(Exception):
            await client.get_quote_summary("AAPL", "assetProfile,invalidModule")

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_valid_modules(self):
        """Test get_quote_summary accepts all valid modules."""
        client = AsyncClient()
        
        # Test with a few valid modules from ALL_MODULES
        valid_modules = ["assetProfile", "price", "summaryDetail", "financialData"]
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "quoteSummary": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Mock both crumb request and quote summary request
        def mock_get_async_request(url, params=None):
            if 'getcrumb' in url:
                crumb_response = MagicMock(spec=Response)
                crumb_response.text = "test_crumb"
                return crumb_response
            else:
                return mock_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_async_request):
            # Should not raise exception
            await client.get_quote_summary("AAPL", ",".join(valid_modules))

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module(self):
        """Test get_quote_summary with single module."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "quoteSummary": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Mock both crumb request and quote summary request
        def mock_get_async_request(url, params=None):
            if 'getcrumb' in url:
                crumb_response = MagicMock(spec=Response)
                crumb_response.text = "test_crumb"
                return crumb_response
            else:
                return mock_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_async_request) as mock_get:
            await client.get_quote_summary("AAPL", "assetProfile")
            
            # Verify modules parameter - get the last call (quote summary call, not crumb call)
            quote_summary_call = mock_get.call_args_list[-1]
            params = quote_summary_call[0][1]  # Second positional argument is params
            assert params['modules'] == 'assetProfile'

    @pytest.mark.asyncio
    async def test_get_quote_crumb_usage(self):
        """Test that get_quote properly uses crumb."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "quoteResponse": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Mock both crumb request and quote request
        def mock_get_async_request(url, params=None):
            if 'getcrumb' in url:
                crumb_response = MagicMock(spec=Response)
                crumb_response.text = "specific_crumb_value"
                return crumb_response
            else:
                return mock_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_async_request) as mock_get:
            await client.get_quote("AAPL")
            
            # Verify crumb is used - get the last call (quote call, not crumb call)
            quote_call = mock_get.call_args_list[-1]
            params = quote_call[0][1]  # Second positional argument is params
            assert params['crumb'] == 'specific_crumb_value'
            # Verify crumb was fetched (should have 2 calls: crumb + quote)
            assert len(mock_get.call_args_list) == 2

    @pytest.mark.asyncio
    async def test_get_quote_summary_crumb_usage(self):
        """Test that get_quote_summary properly uses crumb."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "quoteSummary": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Mock both crumb request and quote summary request
        def mock_get_async_request(url, params=None):
            if 'getcrumb' in url:
                crumb_response = MagicMock(spec=Response)
                crumb_response.text = "specific_crumb_value"
                return crumb_response
            else:
                return mock_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_async_request) as mock_get:
            await client.get_quote_summary("AAPL", "assetProfile")
            
            # Verify crumb is used - get the last call (quote summary call, not crumb call)
            quote_summary_call = mock_get.call_args_list[-1]
            params = quote_summary_call[0][1]  # Second positional argument is params
            assert params['crumb'] == 'specific_crumb_value'
            # Verify crumb was fetched (should have 2 calls: crumb + quote summary)
            assert len(mock_get.call_args_list) == 2

    @pytest.mark.asyncio
    async def test_get_timeseries_success(self):
        """Test get_timeseries method with valid parameters."""
        client = AsyncClient()
        
        timeseries_data = {
            "meta": {"symbol": "AAPL"},
            "timeseries": {
                "TotalRevenue": [
                    {"asOfDate": "2023-12-31", "reportedValue": {"raw": 1000000}}
                ]
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {
                "result": [[timeseries_data]],  # Note: get_timeseries returns result[0][0]
                "error": None
            }
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            result = await client.get_timeseries("AAPL", ["TotalRevenue"])
            
            assert result == timeseries_data
            
            # Verify URL construction
            expected_url = "https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/AAPL"
            mock_get.assert_called_once()
            assert mock_get.call_args[0][0] == expected_url

    @pytest.mark.asyncio
    async def test_get_timeseries_multiple_types(self):
        """Test get_timeseries method with multiple types."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            types = ["TotalRevenue", "NetIncome", "TotalAssets"]
            await client.get_timeseries("AAPL", types)
            
            # Verify types parameter is joined correctly
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['type'] == 'TotalRevenue,NetIncome,TotalAssets'

    @pytest.mark.asyncio
    async def test_get_timeseries_default_periods(self):
        """Test get_timeseries method uses default periods when not provided."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch('src.client.datetime') as mock_datetime:
            # Mock datetime.datetime(2020, 1, 1).timestamp()
            mock_datetime.datetime.return_value.timestamp.return_value = 1577836800.0
            # Mock datetime.datetime.now().timestamp()
            mock_datetime.datetime.now.return_value.timestamp.return_value = 1640995200.0
            
            with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
                await client.get_timeseries("AAPL", ["TotalRevenue"])
                
                # Verify default periods are used
                call_args = mock_get.call_args
                params = call_args[0][1]
                assert params['period1'] == 1577836800  # 2020-01-01
                assert params['period2'] == 1640995200  # now

    @pytest.mark.asyncio
    async def test_get_timeseries_custom_periods(self):
        """Test get_timeseries method with custom periods."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            period1 = 1609459200.0  # 2021-01-01
            period2 = 1640995200.0  # 2022-01-01
            
            await client.get_timeseries("AAPL", ["TotalRevenue"], period1, period2)
            
            # Verify custom periods are used
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['period1'] == int(period1)
            assert params['period2'] == int(period2)

    @pytest.mark.asyncio
    async def test_get_timeseries_period_conversion(self):
        """Test get_timeseries method converts float periods to int."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            # Use float periods
            period1 = 1609459200.5
            period2 = 1640995200.7
            
            await client.get_timeseries("AAPL", ["TotalRevenue"], period1, period2)
            
            # Verify periods are converted to int
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['period1'] == 1609459200
            assert params['period2'] == 1640995200
            assert isinstance(params['period1'], int)
            assert isinstance(params['period2'], int)

    @pytest.mark.asyncio
    async def test_get_timeseries_partial_periods(self):
        """Test get_timeseries method with only period1 or period2."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch('src.client.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value.timestamp.return_value = 1640995200.0
            
            with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
                # Test with only period1
                period1 = 1609459200.0
                await client.get_timeseries("AAPL", ["TotalRevenue"], period1=period1)
                
                call_args = mock_get.call_args
                params = call_args[0][1]
                assert params['period1'] == int(period1)
                assert params['period2'] == 1640995200  # default now

    @pytest.mark.asyncio
    async def test_get_timeseries_url_and_params(self):
        """Test get_timeseries constructs correct URL and parameters."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_timeseries("AAPL", ["TotalRevenue"], 1609459200, 1640995200)
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/AAPL"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com',
                'type': 'TotalRevenue',
                'period1': 1609459200,
                'period2': 1640995200
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_timeseries_various_type_combinations(self):
        """Test get_timeseries method with various type combinations."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Test single type
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_timeseries("AAPL", ["TotalRevenue"])
            call_args = mock_get.call_args
            # _get_async_request is called with (url, params)
            params = call_args[0][1]  # Second positional argument is params
            assert params['type'] == 'TotalRevenue'
        
        # Test multiple income statement types
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            income_types = ["annualTotalRevenue", "annualNetIncome", "annualGrossProfit"]
            await client.get_timeseries("AAPL", income_types)
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['type'] == 'annualTotalRevenue,annualNetIncome,annualGrossProfit'
        
        # Test multiple balance sheet types
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            balance_types = ["annualTotalAssets", "annualTotalDebt", "quarterlyTotalAssets"]
            await client.get_timeseries("AAPL", balance_types)
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['type'] == 'annualTotalAssets,annualTotalDebt,quarterlyTotalAssets'
        
        # Test multiple cash flow types
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            cash_flow_types = ["annualOperatingCashFlow", "annualFreeCashFlow", "quarterlyOperatingCashFlow"]
            await client.get_timeseries("AAPL", cash_flow_types)
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['type'] == 'annualOperatingCashFlow,annualFreeCashFlow,quarterlyOperatingCashFlow'

    # Tests for remaining endpoints (Task 3.6)
    
    @pytest.mark.asyncio
    async def test_get_options_success(self):
        """Test get_options method with valid ticker."""
        client = AsyncClient()
        
        options_data = {
            "underlyingSymbol": "AAPL",
            "expirationDates": [1642204800, 1642809600],
            "strikes": [170.0, 175.0, 180.0],
            "quote": {"symbol": "AAPL", "regularMarketPrice": 177.57},
            "options": [{
                "expirationDate": 1642204800,
                "calls": [{"contractSymbol": "AAPL220114C00170000", "strike": 170.0}],
                "puts": [{"contractSymbol": "AAPL220114P00170000", "strike": 170.0}]
            }]
        }
        
        # Mock response for options endpoint
        options_response = MagicMock(spec=Response)
        options_response.json.return_value = {
            "optionChain": {
                "result": [[options_data]],  # Note: get_options returns result[0][0]
                "error": None
            }
        }
        
        # Mock response for crumb endpoint
        crumb_response = MagicMock(spec=Response)
        crumb_response.text = "test_crumb"
        
        # Mock _get_async_request to return different responses based on URL
        def mock_get_request(url, params=None):
            if 'getcrumb' in url:
                return crumb_response
            else:
                return options_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_request) as mock_get:
            result = await client.get_options("AAPL")
            
            assert result == options_data
            
            # Verify the options endpoint was called with correct parameters
            options_call = None
            for call in mock_get.call_args_list:
                # call is a Call object, access args and kwargs
                if call.args and 'options' in call.args[0]:
                    options_call = call
                    break
            
            assert options_call is not None
            expected_url = "https://query2.finance.yahoo.com/v7/finance/options/AAPL"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com',
                'crumb': 'test_crumb'
            }
            
            assert options_call.args[0] == expected_url
            assert options_call.args[1] == expected_params

    @pytest.mark.asyncio
    async def test_get_options_crumb_usage(self):
        """Test that get_options properly uses crumb."""
        client = AsyncClient()
        
        # Mock response for options endpoint
        options_response = MagicMock(spec=Response)
        options_response.json.return_value = {
            "optionChain": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Mock response for crumb endpoint
        crumb_response = MagicMock(spec=Response)
        crumb_response.text = "specific_crumb_value"
        
        def mock_get_request(url, params=None):
            if 'getcrumb' in url:
                return crumb_response
            else:
                return options_response
        
        with patch.object(client, '_get_async_request', side_effect=mock_get_request) as mock_get:
            await client.get_options("AAPL")
            
            # Verify that at least one call was made with crumb parameter
            crumb_used = False
            for call in mock_get.call_args_list:
                if call.args and len(call.args) > 1 and isinstance(call.args[1], dict):
                    if 'crumb' in call.args[1] and call.args[1]['crumb'] == 'specific_crumb_value':
                        crumb_used = True
                        break
                elif call.kwargs and 'params' in call.kwargs and isinstance(call.kwargs['params'], dict):
                    if 'crumb' in call.kwargs['params'] and call.kwargs['params']['crumb'] == 'specific_crumb_value':
                        crumb_used = True
                        break
            
            assert crumb_used, "Crumb was not used in any API call"

    @pytest.mark.asyncio
    async def test_get_search_success(self):
        """Test get_search method with valid query."""
        client = AsyncClient()
        
        search_data = {
            "explains": [],
            "count": 1,
            "quotes": [{
                "exchange": "NMS",
                "shortname": "Apple Inc.",
                "symbol": "AAPL",
                "quoteType": "EQUITY",
                "score": 1000000.0
            }],
            "news": [],
            "totalTime": 12
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = search_data
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            result = await client.get_search("AAPL")
            
            assert result == search_data
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/v1/finance/search"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com',
                'q': 'AAPL'
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_search_query_parameter(self):
        """Test get_search method with different query parameters."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {"count": 0, "quotes": []}
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            # Test with company name
            await client.get_search("Apple Inc")
            call_args = mock_get.call_args
            # Parameters are passed as second positional argument
            assert call_args.args[1]['q'] == 'Apple Inc'
            
            # Test with partial ticker
            await client.get_search("AAP")
            call_args = mock_get.call_args
            assert call_args.args[1]['q'] == 'AAP'

    @pytest.mark.asyncio
    async def test_get_recommendations_success(self):
        """Test get_recommendations method with valid ticker."""
        client = AsyncClient()
        
        recommendations_data = {
            "symbol": "AAPL",
            "recommendedSymbols": [
                {"symbol": "MSFT", "score": 0.234567},
                {"symbol": "GOOGL", "score": 0.198765}
            ]
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "finance": {
                "result": [[recommendations_data]],  # Note: get_recommendations returns result[0][0]
                "error": None
            }
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            result = await client.get_recommendations("AAPL")
            
            assert result == recommendations_data
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/v6/finance/recommendationsbysymbol/AAPL"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com'
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_recommendations_url_construction(self):
        """Test get_recommendations constructs correct URL for different tickers."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "finance": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            # Test with different tickers
            tickers = ["AAPL", "GOOGL", "MSFT"]
            for ticker in tickers:
                await client.get_recommendations(ticker)
                expected_url = f"https://query2.finance.yahoo.com/v6/finance/recommendationsbysymbol/{ticker}"
                call_args = mock_get.call_args
                assert call_args[0][0] == expected_url

    @pytest.mark.asyncio
    async def test_get_insights_success(self):
        """Test get_insights method with valid ticker."""
        client = AsyncClient()
        
        insights_data = {
            "symbol": "AAPL",
            "instrumentInfo": {
                "technicalEvents": {
                    "provider": "Trading Central",
                    "shortTermOutlook": {"direction": "Bullish", "score": 4}
                },
                "keyTechnicals": {"support": 175.50, "resistance": 185.00}
            },
            "companySnapshot": {
                "sectorInfo": "Technology",
                "company": {"innovativeness": 0.9990}
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "finance": {
                "result": insights_data,  # Note: get_insights returns result directly
                "error": None
            }
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            result = await client.get_insights("AAPL")
            
            assert result == insights_data
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/ws/insights/v2/finance/insights"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com',
                'symbol': 'AAPL'
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_insights_symbol_parameter(self):
        """Test get_insights method uses symbol parameter correctly."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "finance": {"result": {"test": "data"}, "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_insights("TSLA")
            
            # Verify symbol parameter
            call_args = mock_get.call_args
            assert call_args.args[1]['symbol'] == 'TSLA'

    @pytest.mark.asyncio
    async def test_get_market_summary_success(self):
        """Test get_market_summary method."""
        client = AsyncClient()
        
        market_summary_data = [{
            "symbol": "^GSPC",
            "shortName": "S&P 500",
            "regularMarketPrice": 4808.93,
            "regularMarketChange": 65.64001,
            "regularMarketChangePercent": 1.3848957
        }]
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "marketSummaryResponse": {
                "result": [market_summary_data],  # Note: get_market_summary returns result[0] via _get_result
                "error": None
            }
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            result = await client.get_market_summary()
            
            assert result == market_summary_data
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/v6/finance/quote/marketSummary"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com'
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_market_summary_no_parameters(self):
        """Test get_market_summary method requires no additional parameters."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "marketSummaryResponse": {"result": [[]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_market_summary()
            
            # Verify only default parameters are used
            call_args = mock_get.call_args
            params = call_args.args[1]  # Second positional argument is params
            expected_keys = {'formatted', 'region', 'lang', 'corsDomain'}
            assert set(params.keys()) == expected_keys

    @pytest.mark.asyncio
    async def test_get_trending_success(self):
        """Test get_trending method."""
        client = AsyncClient()
        
        trending_data = {
            "count": 5,
            "quotes": [
                {"symbol": "AAPL"},
                {"symbol": "TSLA"},
                {"symbol": "MSFT"}
            ],
            "jobTimestamp": 1640995200
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "finance": {
                "result": [[trending_data]],  # Note: get_trending returns result[0][0]
                "error": None
            }
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            result = await client.get_trending()
            
            assert result == trending_data
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/v1/finance/trending/US"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com'
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_trending_no_parameters(self):
        """Test get_trending method requires no additional parameters."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "finance": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_trending()
            
            # Verify only default parameters are used
            call_args = mock_get.call_args
            params = call_args.args[1]
            expected_keys = {'formatted', 'region', 'lang', 'corsDomain'}
            assert set(params.keys()) == expected_keys

    @pytest.mark.asyncio
    async def test_get_currencies_success(self):
        """Test get_currencies method."""
        client = AsyncClient()
        
        currencies_data = [
            {"id": "USD=X", "fullName": "USD/USD", "symbol": "USD=X"},
            {"id": "EURUSD=X", "fullName": "EUR/USD", "symbol": "EURUSD=X"},
            {"id": "GBPUSD=X", "fullName": "GBP/USD", "symbol": "GBPUSD=X"}
        ]
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "currencies": {
                "result": [currencies_data],  # Note: get_currencies returns result[0] via _get_result
                "error": None
            }
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            result = await client.get_currencies()
            
            assert result == currencies_data
            
            # Verify URL and parameters
            expected_url = "https://query2.finance.yahoo.com/v1/finance/currencies"
            expected_params = {
                'formatted': 'false',
                'region': 'US',
                'lang': 'en-US',
                'corsDomain': 'finance.yahoo.com'
            }
            
            mock_get.assert_called_once_with(expected_url, expected_params)

    @pytest.mark.asyncio
    async def test_get_currencies_no_parameters(self):
        """Test get_currencies method requires no additional parameters."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "currencies": {"result": [[]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_currencies()
            
            # Verify only default parameters are used
            call_args = mock_get.call_args
            params = call_args.args[1]
            expected_keys = {'formatted', 'region', 'lang', 'corsDomain'}
            assert set(params.keys()) == expected_keys

    @pytest.mark.asyncio
    async def test_get_currencies_response_handling(self):
        """Test get_currencies method handles response correctly."""
        client = AsyncClient()
        
        # Test with empty currencies list
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "currencies": {"result": [[]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            result = await client.get_currencies()
            assert result == []
        
        # Test with multiple currencies
        currencies_data = [
            {"id": "EURUSD=X", "symbol": "EURUSD=X"},
            {"id": "GBPUSD=X", "symbol": "GBPUSD=X"}
        ]
        mock_response.json.return_value = {
            "currencies": {"result": [currencies_data], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            result = await client.get_currencies()
            assert result == currencies_data
            assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_timeseries_period_handling_edge_cases(self):
        """Test get_timeseries period1 and period2 parameter handling edge cases."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch('src.client.datetime') as mock_datetime:
            # Mock current time
            mock_datetime.datetime.now.return_value.timestamp.return_value = 1640995200.0
            mock_datetime.datetime.return_value.timestamp.return_value = 1577836800.0
            
            # Test with period1=0 (will use default because 0 is falsy)
            with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
                await client.get_timeseries("AAPL", ["TotalRevenue"], period1=0)
                call_args = mock_get.call_args
                params = call_args[0][1]
                assert params['period1'] == 1577836800  # default 2020-01-01 because 0 is falsy
                assert params['period2'] == 1640995200
            
            # Test with period2=0 (will use default because 0 is falsy)
            with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
                await client.get_timeseries("AAPL", ["TotalRevenue"], period2=0)
                call_args = mock_get.call_args
                params = call_args[0][1]
                assert params['period1'] == 1577836800
                assert params['period2'] == 1640995200  # default now because 0 is falsy
            
            # Test with both periods as 0 (both will use defaults because 0 is falsy)
            with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
                await client.get_timeseries("AAPL", ["TotalRevenue"], period1=0, period2=0)
                call_args = mock_get.call_args
                params = call_args[0][1]
                assert params['period1'] == 1577836800  # default 2020-01-01
                assert params['period2'] == 1640995200  # default now
            
            # Test with negative periods (should be preserved)
            with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
                await client.get_timeseries("AAPL", ["TotalRevenue"], period1=-1000, period2=-500)
                call_args = mock_get.call_args
                params = call_args[0][1]
                assert params['period1'] == -1000
                assert params['period2'] == -500

    @pytest.mark.asyncio
    async def test_get_timeseries_response_parsing_validation(self):
        """Test get_timeseries response parsing and data structure validation."""
        client = AsyncClient()
        
        # Test with realistic timeseries response structure
        # The actual structure has result[0][0] based on the get_timeseries implementation
        timeseries_data = {
            "meta": {
                "symbol": ["AAPL"],
                "type": ["annualTotalRevenue", "annualNetIncome"]
            },
            "annualTotalRevenue": [
                {
                    "asOfDate": "2021-09-25",
                    "periodType": "12M",
                    "currencyCode": "USD",
                    "reportedValue": {"raw": 365817000000, "fmt": "365.82B"}
                },
                {
                    "asOfDate": "2020-09-26", 
                    "periodType": "12M",
                    "currencyCode": "USD",
                    "reportedValue": {"raw": 274515000000, "fmt": "274.52B"}
                }
            ],
            "annualNetIncome": [
                {
                    "asOfDate": "2021-09-25",
                    "periodType": "12M", 
                    "currencyCode": "USD",
                    "reportedValue": {"raw": 94680000000, "fmt": "94.68B"}
                }
            ]
        }
        
        realistic_response = {
            "timeseries": {
                "result": [[timeseries_data]],  # Note: get_timeseries returns result[0][0]
                "error": None
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = realistic_response
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            result = await client.get_timeseries("AAPL", ["annualTotalRevenue", "annualNetIncome"])
            
            # Verify the structure is preserved
            assert "meta" in result
            assert "annualTotalRevenue" in result
            assert "annualNetIncome" in result
            assert result["meta"]["symbol"] == ["AAPL"]
            assert len(result["annualTotalRevenue"]) == 2
            assert len(result["annualNetIncome"]) == 1
            assert result["annualTotalRevenue"][0]["reportedValue"]["raw"] == 365817000000
            assert result["annualNetIncome"][0]["asOfDate"] == "2021-09-25"

    @pytest.mark.asyncio
    async def test_get_timeseries_empty_types_list(self):
        """Test get_timeseries method with empty types list."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_timeseries("AAPL", [])
            
            # Verify empty string is passed for type parameter
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['type'] == ''

    @pytest.mark.asyncio
    async def test_get_timeseries_large_type_list(self):
        """Test get_timeseries method with large number of types."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        # Create a large list of types
        large_type_list = [
            "annualTotalRevenue", "annualNetIncome", "annualGrossProfit", "annualOperatingIncome",
            "quarterlyTotalRevenue", "quarterlyNetIncome", "quarterlyGrossProfit", "quarterlyOperatingIncome",
            "annualTotalAssets", "annualTotalDebt", "quarterlyTotalAssets", "quarterlyTotalDebt",
            "annualOperatingCashFlow", "annualFreeCashFlow", "quarterlyOperatingCashFlow", "quarterlyFreeCashFlow"
        ]
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            await client.get_timeseries("AAPL", large_type_list)
            
            # Verify all types are joined correctly
            call_args = mock_get.call_args
            params = call_args[0][1]
            expected_type_string = ','.join(large_type_list)
            assert params['type'] == expected_type_string

    @pytest.mark.asyncio
    async def test_get_timeseries_period_defaults_with_datetime_mock(self):
        """Test get_timeseries default period calculation with proper datetime mocking."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch('src.client.datetime') as mock_datetime:
            # Mock datetime.datetime(2020, 1, 1).timestamp() for period1 default
            mock_datetime_2020 = MagicMock()
            mock_datetime_2020.timestamp.return_value = 1577836800.0
            mock_datetime.datetime.return_value = mock_datetime_2020
            
            # Mock datetime.datetime.now().timestamp() for period2 default
            mock_datetime_now = MagicMock()
            mock_datetime_now.timestamp.return_value = 1640995200.0
            mock_datetime.datetime.now.return_value = mock_datetime_now
            
            with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
                await client.get_timeseries("AAPL", ["TotalRevenue"])
                
                # Verify default periods are calculated correctly
                call_args = mock_get.call_args
                params = call_args[0][1]
                assert params['period1'] == 1577836800  # 2020-01-01
                assert params['period2'] == 1640995200  # mocked now
                
                # Verify datetime methods were called correctly
                mock_datetime.datetime.assert_called_with(2020, 1, 1)
                mock_datetime.datetime.now.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_timeseries_period_type_conversion_precision(self):
        """Test get_timeseries period conversion handles precision correctly."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {
            "timeseries": {"result": [[{"test": "data"}]], "error": None}
        }
        
        with patch.object(client, '_get_async_request', return_value=mock_response) as mock_get:
            # Test with high precision floats
            period1 = 1609459200.999999
            period2 = 1640995200.123456
            
            await client.get_timeseries("AAPL", ["TotalRevenue"], period1, period2)
            
            # Verify periods are truncated to int (not rounded)
            call_args = mock_get.call_args
            params = call_args[0][1]
            assert params['period1'] == 1609459200
            assert params['period2'] == 1640995200
            assert isinstance(params['period1'], int)
            assert isinstance(params['period2'], int)
    
# ========================================
    # Comprehensive Error Handling Tests
    # ========================================

    @pytest.mark.asyncio
    async def test_http_401_unauthorized_error(self):
        """Test handling of HTTP 401 Unauthorized error."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.side_effect = HTTPError("401 Unauthorized")
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(HTTPError, match="401 Unauthorized"):
                await client._get_async_request("https://example.com/api")

    @pytest.mark.asyncio
    async def test_http_404_not_found_error(self):
        """Test handling of HTTP 404 Not Found error."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(HTTPError, match="404 Not Found"):
                await client._get_async_request("https://example.com/api")

    @pytest.mark.asyncio
    async def test_http_500_internal_server_error(self):
        """Test handling of HTTP 500 Internal Server Error."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.side_effect = HTTPError("500 Internal Server Error")
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(HTTPError, match="500 Internal Server Error"):
                await client._get_async_request("https://example.com/api")

    @pytest.mark.asyncio
    async def test_http_503_service_unavailable_error(self):
        """Test handling of HTTP 503 Service Unavailable error."""
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.raise_for_status.side_effect = HTTPError("503 Service Unavailable")
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(HTTPError, match="503 Service Unavailable"):
                await client._get_async_request("https://example.com/api")

    @pytest.mark.asyncio
    async def test_network_connection_error(self):
        """Test handling of network connection errors."""
        from curl_cffi.requests.exceptions import RequestException
        
        client = AsyncClient()
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, side_effect=RequestException("Connection failed")):
            with pytest.raises(RequestException, match="Connection failed"):
                await client._get_async_request("https://example.com/api")

    @pytest.mark.asyncio
    async def test_network_timeout_error(self):
        """Test handling of network timeout errors."""
        from curl_cffi.requests.exceptions import Timeout
        
        client = AsyncClient()
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, side_effect=Timeout("Request timed out")):
            with pytest.raises(Timeout, match="Request timed out"):
                await client._get_async_request("https://example.com/api")

    @pytest.mark.asyncio
    async def test_api_error_response_chart(self):
        """Test handling of API error responses in chart endpoint."""
        client = AsyncClient()
        
        # Mock response with API error
        error_response_data = {
            "chart": {
                "result": None,
                "error": "Invalid ticker symbol: INVALID"
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = error_response_data
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(Exception, match="Invalid ticker symbol: INVALID"):
                await client.get_chart("INVALID", "1d", "1d")

    @pytest.mark.asyncio
    async def test_api_error_response_quote(self):
        """Test handling of API error responses in quote endpoint."""
        client = AsyncClient()
        
        # Mock response with API error
        error_response_data = {
            "quoteResponse": {
                "result": None,
                "error": "No data found for ticker: BADTICKER"
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = error_response_data
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            with pytest.raises(Exception, match="No data found for ticker: BADTICKER"):
                await client.get_quote("BADTICKER")

    @pytest.mark.asyncio
    async def test_api_error_response_quote_summary(self):
        """Test handling of API error responses in quote summary endpoint."""
        client = AsyncClient()
        
        # Mock response with API error
        error_response_data = {
            "quoteSummary": {
                "result": None,
                "error": "Quote not found for ticker symbol: NOTFOUND"
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = error_response_data
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client, '_get_async_request', return_value=mock_response):
            with pytest.raises(Exception, match="Quote not found for ticker symbol: NOTFOUND"):
                await client.get_quote_summary("NOTFOUND", "assetProfile")

    @pytest.mark.asyncio
    async def test_api_error_response_timeseries(self):
        """Test handling of API error responses in timeseries endpoint."""
        client = AsyncClient()
        
        # Mock response with API error
        error_response_data = {
            "timeseries": {
                "result": None,
                "error": "No timeseries data available for ticker: NODATA"
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = error_response_data
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(Exception, match="No timeseries data available for ticker: NODATA"):
                await client.get_timeseries("NODATA", ["TotalRevenue"])

    def test_malformed_json_response(self):
        """Test handling of malformed JSON responses."""
        from json import JSONDecodeError
        
        client = AsyncClient()
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.side_effect = JSONDecodeError("Invalid JSON", "doc", 0)
        
        with pytest.raises(JSONDecodeError):
            client._get_result(mock_response, "chart")

    def test_missing_result_key_in_response(self):
        """Test handling of responses missing the expected result key."""
        client = AsyncClient()
        
        # Mock response missing the expected key structure
        malformed_response_data = {
            "unexpected_key": {
                "data": "some_data"
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = malformed_response_data
        
        with pytest.raises(KeyError):
            client._get_result(mock_response, "chart")

    def test_missing_error_key_in_response(self):
        """Test handling of responses missing the error key."""
        client = AsyncClient()
        
        # Mock response missing error key
        malformed_response_data = {
            "chart": {
                "result": [{"symbol": "AAPL"}]
                # Missing "error" key
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = malformed_response_data
        
        with pytest.raises(KeyError):
            client._get_result(mock_response, "chart")

    def test_missing_result_array_in_response(self):
        """Test handling of responses missing the result array."""
        client = AsyncClient()
        
        # Mock response missing result array
        malformed_response_data = {
            "chart": {
                "error": None
                # Missing "result" key
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = malformed_response_data
        
        with pytest.raises(KeyError):
            client._get_result(mock_response, "chart")

    def test_empty_result_array_in_response(self):
        """Test handling of responses with empty result array."""
        client = AsyncClient()
        
        # Mock response with empty result array
        empty_response_data = {
            "chart": {
                "result": [],  # Empty result array
                "error": None
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = empty_response_data
        
        with pytest.raises(IndexError):
            client._get_result(mock_response, "chart")

    def test_null_result_in_response(self):
        """Test handling of responses with null result."""
        client = AsyncClient()
        
        # Mock response with null result
        null_response_data = {
            "chart": {
                "result": None,  # Null result
                "error": None
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = null_response_data
        
        with pytest.raises(TypeError):
            client._get_result(mock_response, "chart")

    @pytest.mark.asyncio
    async def test_crumb_fetch_error_handling(self):
        """Test error handling when fetching crumb fails."""
        client = AsyncClient()
        
        # Mock HTTP error during crumb fetch
        with patch.object(client, '_get_async_request', side_effect=HTTPError("Failed to fetch crumb")):
            with pytest.raises(HTTPError, match="Failed to fetch crumb"):
                await client._crumb

    @pytest.mark.asyncio
    async def test_crumb_none_response_handling(self):
        """Test handling when crumb request returns None."""
        client = AsyncClient()
        
        with patch.object(client, '_get_async_request', return_value=None):
            crumb = await client._crumb
            assert crumb is None

    @pytest.mark.asyncio
    async def test_get_chart_with_http_error_propagation(self):
        """Test that HTTP errors in get_chart are properly propagated."""
        client = AsyncClient()
        
        with patch.object(client, '_get_async_request', side_effect=HTTPError("Chart API error")):
            with pytest.raises(HTTPError, match="Chart API error"):
                await client.get_chart("AAPL", "1d", "1d")

    @pytest.mark.asyncio
    async def test_get_quote_with_http_error_propagation(self):
        """Test that HTTP errors in get_quote are properly propagated."""
        client = AsyncClient()
        
        with patch.object(client, '_get_async_request', side_effect=HTTPError("Quote API error")):
            with pytest.raises(HTTPError, match="Quote API error"):
                await client.get_quote("AAPL")

    @pytest.mark.asyncio
    async def test_get_quote_summary_with_http_error_propagation(self):
        """Test that HTTP errors in get_quote_summary are properly propagated."""
        client = AsyncClient()
        
        with patch.object(client, '_get_async_request', side_effect=HTTPError("Quote summary API error")):
            with pytest.raises(HTTPError, match="Quote summary API error"):
                await client.get_quote_summary("AAPL", "assetProfile")

    @pytest.mark.asyncio
    async def test_get_timeseries_with_http_error_propagation(self):
        """Test that HTTP errors in get_timeseries are properly propagated."""
        client = AsyncClient()
        
        with patch.object(client, '_get_async_request', side_effect=HTTPError("Timeseries API error")):
            with pytest.raises(HTTPError, match="Timeseries API error"):
                await client.get_timeseries("AAPL", ["TotalRevenue"])

    @pytest.mark.asyncio
    async def test_complex_api_error_message_extraction(self):
        """Test extraction of complex API error messages."""
        client = AsyncClient()
        
        # Mock response with complex error structure
        complex_error_response = {
            "chart": {
                "result": None,
                "error": {
                    "code": "Not Found",
                    "description": "No data found, symbol may be delisted"
                }
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = complex_error_response
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            # The error function should handle the complex error structure
            with pytest.raises(Exception):
                await client.get_chart("DELISTED", "1d", "1d")

    @pytest.mark.asyncio
    async def test_unicode_error_message_handling(self):
        """Test handling of error messages with unicode characters."""
        client = AsyncClient()
        
        # Mock response with unicode error message
        unicode_error_response = {
            "chart": {
                "result": None,
                "error": "Symbole non trouvé: AAPL (French: Symbol not found)"
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = unicode_error_response
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(Exception, match="Symbole non trouvé: AAPL"):
                await client.get_chart("AAPL", "1d", "1d")

    @pytest.mark.asyncio
    async def test_empty_error_message_handling(self):
        """Test handling of empty error messages."""
        client = AsyncClient()
        
        # Mock response with empty error message
        empty_error_response = {
            "chart": {
                "result": None,
                "error": ""
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = empty_error_response
        mock_response.raise_for_status.return_value = None
        
        with patch.object(client._session, 'get', new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(Exception):
                await client.get_chart("AAPL", "1d", "1d")

    @pytest.mark.asyncio
    async def test_none_error_message_handling(self):
        """Test handling when error message is None but truthy check fails."""
        client = AsyncClient()
        
        # Mock response where error is not None but evaluates to truthy
        none_error_response = {
            "chart": {
                "result": [{"symbol": "AAPL"}],
                "error": False  # Falsy but not None
            }
        }
        
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = none_error_response
        
        # This should not raise an error since error is falsy
        result = client._get_result(mock_response, "chart")
        assert result == {"symbol": "AAPL"}