"""Unit tests for the Stonk class."""

import pytest
import respx
from unittest.mock import AsyncMock, patch, MagicMock

from src.stonk import Stonk
from src.client import AsyncClient


class TestStonkInitialization:
    """Test Stonk class initialization and basic functionality."""

    def test_stonk_initialization_with_ticker(self):
        """Test that Stonk initializes correctly with a ticker."""
        ticker = "AAPL"
        stonk = Stonk(ticker)
        
        assert stonk.ticker == ticker
        assert hasattr(stonk, '_client')
        assert isinstance(stonk._client, AsyncClient)

    def test_stonk_initialization_with_different_tickers(self, valid_tickers):
        """Test that Stonk initializes correctly with various valid tickers."""
        for ticker in valid_tickers:
            stonk = Stonk(ticker)
            assert stonk.ticker == ticker
            assert hasattr(stonk, '_client')

    def test_stonk_shared_client_instance(self):
        """Test that all Stonk instances share the same AsyncClient instance."""
        stonk1 = Stonk("AAPL")
        stonk2 = Stonk("GOOGL")
        
        # Both instances should share the same client
        assert stonk1._client is stonk2._client
        assert id(stonk1._client) == id(stonk2._client)

    def test_stonk_initialization_with_empty_ticker(self):
        """Test that Stonk can be initialized with empty ticker (edge case)."""
        stonk = Stonk("")
        assert stonk.ticker == ""
        assert hasattr(stonk, '_client')

    def test_stonk_initialization_with_special_characters(self):
        """Test that Stonk can be initialized with special characters in ticker."""
        special_tickers = ["BRK.A", "BRK-B", "GOOGL.L"]
        for ticker in special_tickers:
            stonk = Stonk(ticker)
            assert stonk.ticker == ticker
            assert hasattr(stonk, '_client')


class TestStonkBasicDelegation:
    """Test basic delegation to AsyncClient methods."""

    @pytest.mark.asyncio
    async def test_get_chart_delegation(self, chart_success_response):
        """Test that get_chart properly delegates to AsyncClient."""
        stonk = Stonk("AAPL")
        
        # Mock the client method to verify it's called correctly
        with patch.object(stonk._client, 'get_chart', new_callable=AsyncMock) as mock_get_chart:
            mock_get_chart.return_value = chart_success_response
            
            result = await stonk.get_chart("1d", "1d", "div,split")
            
            # Verify the client method was called with correct parameters
            mock_get_chart.assert_called_once_with("AAPL", "1d", "1d", "div,split")
            assert result == chart_success_response

    @pytest.mark.asyncio
    async def test_get_quote_delegation(self, quote_success_response):
        """Test that get_quote properly delegates to AsyncClient."""
        stonk = Stonk("AAPL")
        
        # Mock the client method to verify it's called correctly
        with patch.object(stonk._client, 'get_quote', new_callable=AsyncMock) as mock_get_quote:
            mock_get_quote.return_value = quote_success_response
            
            result = await stonk.get_quote()
            
            # Verify the client method was called with correct parameters
            mock_get_quote.assert_called_once_with("AAPL")
            assert result == quote_success_response

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules_delegation(self, quote_summary_success_response):
        """Test that get_quote_summary_all_modules properly delegates to AsyncClient."""
        from src.const import ALL_MODULES
        
        stonk = Stonk("AAPL")
        
        # Mock the client method to verify it's called correctly
        with patch.object(stonk._client, 'get_quote_summary', new_callable=AsyncMock) as mock_get_quote_summary:
            mock_get_quote_summary.return_value = quote_summary_success_response
            
            result = await stonk.get_quote_summary_all_modules()
            
            # Verify the client method was called with correct parameters
            mock_get_quote_summary.assert_called_once_with("AAPL", ALL_MODULES)
            assert result == quote_summary_success_response

    @pytest.mark.asyncio
    async def test_get_options_delegation(self, options_success_response):
        """Test that get_options properly delegates to AsyncClient."""
        stonk = Stonk("AAPL")
        
        # Mock the client method to verify it's called correctly
        with patch.object(stonk._client, 'get_options', new_callable=AsyncMock) as mock_get_options:
            mock_get_options.return_value = options_success_response
            
            result = await stonk.get_options()
            
            # Verify the client method was called with correct parameters
            mock_get_options.assert_called_once_with("AAPL")
            assert result == options_success_response

    @pytest.mark.asyncio
    async def test_get_search_delegation(self, search_success_response):
        """Test that get_search properly delegates to AsyncClient."""
        stonk = Stonk("AAPL")
        
        # Mock the client method to verify it's called correctly
        with patch.object(stonk._client, 'get_search', new_callable=AsyncMock) as mock_get_search:
            mock_get_search.return_value = search_success_response
            
            result = await stonk.get_search()
            
            # Verify the client method was called with correct parameters
            mock_get_search.assert_called_once_with("AAPL")
            assert result == search_success_response

    @pytest.mark.asyncio
    async def test_get_recommendations_delegation(self, recommendations_success_response):
        """Test that get_recommendations properly delegates to AsyncClient."""
        stonk = Stonk("AAPL")
        
        # Mock the client method to verify it's called correctly
        with patch.object(stonk._client, 'get_recommendations', new_callable=AsyncMock) as mock_get_recommendations:
            mock_get_recommendations.return_value = recommendations_success_response
            
            result = await stonk.get_recommendations()
            
            # Verify the client method was called with correct parameters
            mock_get_recommendations.assert_called_once_with("AAPL")
            assert result == recommendations_success_response

    @pytest.mark.asyncio
    async def test_get_insights_delegation(self, insights_success_response):
        """Test that get_insights properly delegates to AsyncClient."""
        stonk = Stonk("AAPL")
        
        # Mock the client method to verify it's called correctly
        with patch.object(stonk._client, 'get_insights', new_callable=AsyncMock) as mock_get_insights:
            mock_get_insights.return_value = insights_success_response
            
            result = await stonk.get_insights()
            
            # Verify the client method was called with correct parameters
            mock_get_insights.assert_called_once_with("AAPL")
            assert result == insights_success_response


class TestStonkChartAndQuoteMethods:
    """Test chart and quote methods with parameter validation."""

    @pytest.mark.asyncio
    async def test_get_chart_with_default_events(self, chart_success_response):
        """Test get_chart with default events parameter."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_chart', new_callable=AsyncMock) as mock_get_chart:
            mock_get_chart.return_value = chart_success_response
            
            # Test with default events parameter
            result = await stonk.get_chart("1d", "1d")
            
            # Should use default events='div,split'
            mock_get_chart.assert_called_once_with("AAPL", "1d", "1d", "div,split")
            assert result == chart_success_response

    @pytest.mark.asyncio
    async def test_get_chart_with_custom_events(self, chart_success_response):
        """Test get_chart with custom events parameter."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_chart', new_callable=AsyncMock) as mock_get_chart:
            mock_get_chart.return_value = chart_success_response
            
            # Test with custom events
            result = await stonk.get_chart("1d", "1d", "div")
            
            mock_get_chart.assert_called_once_with("AAPL", "1d", "1d", "div")
            assert result == chart_success_response

    @pytest.mark.asyncio
    async def test_get_chart_parameter_passing(self, chart_success_response, valid_ranges, valid_intervals):
        """Test get_chart passes parameters correctly for various combinations."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_chart', new_callable=AsyncMock) as mock_get_chart:
            mock_get_chart.return_value = chart_success_response
            
            # Test various parameter combinations
            test_cases = [
                ("1d", "1m", "div,split"),
                ("5d", "5m", "split"),
                ("1mo", "1h", "div"),
                ("1y", "1d", "div,split"),
            ]
            
            for period_range, interval, events in test_cases:
                mock_get_chart.reset_mock()
                
                result = await stonk.get_chart(period_range, interval, events)
                
                mock_get_chart.assert_called_once_with("AAPL", period_range, interval, events)
                assert result == chart_success_response

    @pytest.mark.asyncio
    async def test_get_quote_simple_delegation(self, quote_success_response):
        """Test get_quote simple delegation without parameters."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_quote', new_callable=AsyncMock) as mock_get_quote:
            mock_get_quote.return_value = quote_success_response
            
            result = await stonk.get_quote()
            
            mock_get_quote.assert_called_once_with("AAPL")
            assert result == quote_success_response

    @pytest.mark.asyncio
    async def test_get_quote_with_different_tickers(self, quote_success_response, valid_tickers):
        """Test get_quote works with different ticker symbols."""
        for ticker in valid_tickers[:3]:  # Test first 3 tickers
            stonk = Stonk(ticker)
            
            with patch.object(stonk._client, 'get_quote', new_callable=AsyncMock) as mock_get_quote:
                mock_get_quote.return_value = quote_success_response
                
                result = await stonk.get_quote()
                
                mock_get_quote.assert_called_once_with(ticker)
                assert result == quote_success_response

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules_constant_usage(self, quote_summary_success_response):
        """Test get_quote_summary_all_modules uses ALL_MODULES constant correctly."""
        from src.const import ALL_MODULES
        
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_quote_summary', new_callable=AsyncMock) as mock_get_quote_summary:
            mock_get_quote_summary.return_value = quote_summary_success_response
            
            result = await stonk.get_quote_summary_all_modules()
            
            # Verify it uses the exact ALL_MODULES constant
            mock_get_quote_summary.assert_called_once_with("AAPL", ALL_MODULES)
            assert result == quote_summary_success_response

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules_with_different_tickers(self, quote_summary_success_response):
        """Test get_quote_summary_all_modules with different tickers."""
        from src.const import ALL_MODULES
        
        test_tickers = ["AAPL", "GOOGL", "MSFT"]
        
        for ticker in test_tickers:
            stonk = Stonk(ticker)
            
            with patch.object(stonk._client, 'get_quote_summary', new_callable=AsyncMock) as mock_get_quote_summary:
                mock_get_quote_summary.return_value = quote_summary_success_response
                
                result = await stonk.get_quote_summary_all_modules()
                
                mock_get_quote_summary.assert_called_once_with(ticker, ALL_MODULES)
                assert result == quote_summary_success_response

    @pytest.mark.asyncio
    async def test_chart_method_error_propagation(self):
        """Test that errors from AsyncClient.get_chart are properly propagated."""
        stonk = Stonk("AAPL")
        
        # Mock client method to raise an exception
        with patch.object(stonk._client, 'get_chart', new_callable=AsyncMock) as mock_get_chart:
            mock_get_chart.side_effect = ValueError("Invalid range")
            
            # Verify the exception is propagated
            with pytest.raises(ValueError, match="Invalid range"):
                await stonk.get_chart("invalid", "1d")

    @pytest.mark.asyncio
    async def test_quote_method_error_propagation(self):
        """Test that errors from AsyncClient.get_quote are properly propagated."""
        stonk = Stonk("AAPL")
        
        # Mock client method to raise an exception
        with patch.object(stonk._client, 'get_quote', new_callable=AsyncMock) as mock_get_quote:
            mock_get_quote.side_effect = ConnectionError("Network error")
            
            # Verify the exception is propagated
            with pytest.raises(ConnectionError, match="Network error"):
                await stonk.get_quote()

    @pytest.mark.asyncio
    async def test_quote_summary_all_modules_error_propagation(self):
        """Test that errors from AsyncClient.get_quote_summary are properly propagated."""
        stonk = Stonk("AAPL")
        
        # Mock client method to raise an exception
        with patch.object(stonk._client, 'get_quote_summary', new_callable=AsyncMock) as mock_get_quote_summary:
            mock_get_quote_summary.side_effect = RuntimeError("API error")
            
            # Verify the exception is propagated
            with pytest.raises(RuntimeError, match="API error"):
                await stonk.get_quote_summary_all_modules()

class TestStonkQuoteSummarySingleModule:
    """Test quote summary single module methods and data extraction."""

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module_private_method(self):
        """Test _get_quote_summary_single_module private method."""
        stonk = Stonk("AAPL")
        
        # Mock response with module data
        mock_response = {
            "quoteType": {
                "exchange": "NMS",
                "shortName": "Apple Inc.",
                "longName": "Apple Inc.",
                "exchangeTimezoneName": "America/New_York",
                "exchangeTimezoneShortName": "EST",
                "isEsgPopulated": False,
                "gmtOffSetMilliseconds": "-18000000",
                "quoteType": "EQUITY",
                "symbol": "AAPL",
                "messageBoardId": "finmb_24937",
                "market": "us_market"
            }
        }
        
        with patch.object(stonk._client, 'get_quote_summary', new_callable=AsyncMock) as mock_get_quote_summary:
            mock_get_quote_summary.return_value = mock_response
            
            result = await stonk._get_quote_summary_single_module("quoteType")
            
            # Verify client method was called correctly
            mock_get_quote_summary.assert_called_once_with("AAPL", "quoteType")
            
            # Verify it extracts the specific module data
            assert result == mock_response["quoteType"]

    @pytest.mark.asyncio
    async def test_get_quote_type(self):
        """Test get_quote_type method."""
        stonk = Stonk("AAPL")
        
        expected_data = {
            "exchange": "NMS",
            "quoteType": "EQUITY",
            "symbol": "AAPL"
        }
        
        with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
            mock_single_module.return_value = expected_data
            
            result = await stonk.get_quote_type()
            
            mock_single_module.assert_called_once_with('quoteType')
            assert result == expected_data

    @pytest.mark.asyncio
    async def test_get_asset_profile(self):
        """Test get_asset_profile method."""
        stonk = Stonk("AAPL")
        
        expected_data = {
            "address1": "One Apple Park Way",
            "city": "Cupertino",
            "state": "CA",
            "country": "United States",
            "industry": "Consumer Electronics"
        }
        
        with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
            mock_single_module.return_value = expected_data
            
            result = await stonk.get_asset_profile()
            
            mock_single_module.assert_called_once_with('assetProfile')
            assert result == expected_data

    @pytest.mark.asyncio
    async def test_get_summary_profile(self):
        """Test get_summary_profile method."""
        stonk = Stonk("AAPL")
        
        expected_data = {
            "address1": "One Apple Park Way",
            "city": "Cupertino",
            "phone": "408 996 1010",
            "website": "https://www.apple.com"
        }
        
        with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
            mock_single_module.return_value = expected_data
            
            result = await stonk.get_summary_profile()
            
            mock_single_module.assert_called_once_with('summaryProfile')
            assert result == expected_data

    @pytest.mark.asyncio
    async def test_get_summary_detail(self):
        """Test get_summary_detail method."""
        stonk = Stonk("AAPL")
        
        expected_data = {
            "previousClose": 177.57,
            "regularMarketOpen": 179.61,
            "twoHundredDayAverage": 181.89,
            "trailingAnnualDividendYield": 0.0044
        }
        
        with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
            mock_single_module.return_value = expected_data
            
            result = await stonk.get_summary_detail()
            
            mock_single_module.assert_called_once_with('summaryDetail')
            assert result == expected_data

    @pytest.mark.asyncio
    async def test_get_price(self):
        """Test get_price method."""
        stonk = Stonk("AAPL")
        
        expected_data = {
            "maxAge": 1,
            "preMarketChangePercent": 0.0011,
            "preMarketChange": 0.19,
            "preMarketTime": 1641906599,
            "preMarketPrice": 174.92,
            "regularMarketChangePercent": -0.0149,
            "postMarketChangePercent": 0.0011,
            "postMarketChange": 0.19,
            "postMarketPrice": 175.11,
            "regularMarketChange": -2.65,
            "regularMarketTime": 1641934800,
            "priceHint": 2,
            "regularMarketPrice": 174.92,
            "regularMarketDayHigh": 180.17,
            "regularMarketDayLow": 174.64,
            "regularMarketVolume": 80440800,
            "averageDailyVolume10Day": 88071540,
            "averageDailyVolume3Month": 88071540,
            "regularMarketPreviousClose": 177.57,
            "regularMarketSource": "FREE_REALTIME",
            "regularMarketOpen": 179.61,
            "strikePrice": None,
            "openInterest": None,
            "exchange": "NMS",
            "exchangeName": "NasdaqGS",
            "exchangeDataDelayedBy": 0,
            "marketState": "CLOSED",
            "quoteType": "EQUITY",
            "symbol": "AAPL",
            "underlyingSymbol": None,
            "shortName": "Apple Inc.",
            "longName": "Apple Inc.",
            "currency": "USD",
            "quoteSourceName": "Nasdaq Real Time Price",
            "currencySymbol": "$",
            "fromCurrency": None,
            "toCurrency": None,
            "lastMarket": None,
            "marketCap": 2865188700160
        }
        
        with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
            mock_single_module.return_value = expected_data
            
            result = await stonk.get_price()
            
            mock_single_module.assert_called_once_with('price')
            assert result == expected_data

    @pytest.mark.asyncio
    async def test_get_financial_data(self):
        """Test get_financial_data method."""
        stonk = Stonk("AAPL")
        
        expected_data = {
            "maxAge": 86400,
            "currentPrice": 174.92,
            "targetHighPrice": 200.0,
            "targetLowPrice": 140.0,
            "targetMeanPrice": 175.0,
            "targetMedianPrice": 175.0,
            "recommendationMean": 2.0,
            "recommendationKey": "buy",
            "numberOfAnalystOpinions": 38,
            "totalCash": 62639001600,
            "totalCashPerShare": 3.85,
            "ebitda": 123136999424,
            "totalDebt": 124719996928,
            "quickRatio": 1.038,
            "currentRatio": 1.075,
            "totalRevenue": 365817004032,
            "debtToEquity": 172.985,
            "revenuePerShare": 22.84,
            "returnOnAssets": 0.20108,
            "returnOnEquity": 1.50071,
            "grossProfits": 152836000000,
            "freeCashflow": 92953001984,
            "operatingCashflow": 104038002688,
            "earningsGrowth": 0.647,
            "revenueGrowth": 0.112,
            "grossMargins": 0.41778,
            "ebitdaMargins": 0.33668,
            "operatingMargins": 0.29782,
            "profitMargins": 0.25882,
            "financialCurrency": "USD"
        }
        
        with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
            mock_single_module.return_value = expected_data
            
            result = await stonk.get_financial_data()
            
            mock_single_module.assert_called_once_with('financialData')
            assert result == expected_data

    @pytest.mark.asyncio
    async def test_multiple_quote_summary_methods(self):
        """Test multiple quote summary methods to ensure they call correct modules."""
        stonk = Stonk("AAPL")
        
        # Test cases: (method_name, expected_module)
        test_cases = [
            ('get_default_key_statistics', 'defaultKeyStatistics'),
            ('get_calendar_events', 'calendarEvents'),
            ('get_sec_filings', 'secFilings'),
            ('get_upgrade_downgrade_history', 'upgradeDowngradeHistory'),
            ('get_institution_ownership', 'institutionOwnership'),
            ('get_fund_ownership', 'fundOwnership'),
            ('get_major_direct_holders', 'majorDirectHolders'),
            ('get_major_holders_breakdown', 'majorHoldersBreakdown'),
            ('get_insider_transactions', 'insiderTransactions'),
            ('get_insider_holders', 'insiderHolders'),
            ('get_net_share_purchase_activity', 'netSharePurchaseActivity'),
            ('get_earnings', 'earnings'),
            ('get_earnings_history', 'earningsHistory'),
            ('get_earnings_trend', 'earningsTrend'),
            ('get_industry_trend', 'industryTrend'),
            ('get_index_trend', 'indexTrend'),
            ('get_sector_trend', 'sectorTrend'),
            ('get_recommendation_trend', 'recommendationTrend'),
            ('get_page_views', 'pageViews'),
        ]
        
        for method_name, expected_module in test_cases:
            with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
                mock_single_module.return_value = {"test": "data"}
                
                # Get the method and call it
                method = getattr(stonk, method_name)
                result = await method()
                
                # Verify correct module was requested
                mock_single_module.assert_called_once_with(expected_module)
                assert result == {"test": "data"}

    @pytest.mark.asyncio
    async def test_historical_statement_methods(self):
        """Test historical statement methods."""
        stonk = Stonk("AAPL")
        
        # Test cases for historical statement methods
        test_cases = [
            ('get_income_statement_history', 'incomeStatementHistory'),
            ('get_income_statement_history_quarterly', 'incomeStatementHistoryQuarterly'),
            ('get_balance_sheet_history', 'balanceSheetHistory'),
            ('get_balance_sheet_history_quarterly', 'balanceSheetHistoryQuarterly'),
            ('get_cashflow_statement_history', 'cashflowStatementHistory'),
            ('get_cashflow_statement_history_quarterly', 'cashflowStatementHistoryQuarterly'),
        ]
        
        for method_name, expected_module in test_cases:
            with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
                mock_single_module.return_value = {"historicalData": "test"}
                
                # Get the method and call it
                method = getattr(stonk, method_name)
                result = await method()
                
                # Verify correct module was requested
                mock_single_module.assert_called_once_with(expected_module)
                assert result == {"historicalData": "test"}

    @pytest.mark.asyncio
    async def test_esg_scores_method(self):
        """Test get_esg_scores method."""
        stonk = Stonk("AAPL")
        
        expected_data = {
            "maxAge": 86400,
            "totalEsg": 18.12,
            "environmentScore": 0.79,
            "socialScore": 10.72,
            "governanceScore": 6.61,
            "ratingYear": 2021,
            "ratingMonth": 5
        }
        
        with patch.object(stonk, '_get_quote_summary_single_module', new_callable=AsyncMock) as mock_single_module:
            mock_single_module.return_value = expected_data
            
            result = await stonk.get_esg_scores()
            
            mock_single_module.assert_called_once_with('esgScores')
            assert result == expected_data

    @pytest.mark.asyncio
    async def test_quote_summary_single_module_error_propagation(self):
        """Test that errors from _get_quote_summary_single_module are properly propagated."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_quote_summary', new_callable=AsyncMock) as mock_get_quote_summary:
            mock_get_quote_summary.side_effect = KeyError("Module not found")
            
            # Verify the exception is propagated
            with pytest.raises(KeyError, match="Module not found"):
                await stonk._get_quote_summary_single_module("invalidModule")

    @pytest.mark.asyncio
    async def test_quote_summary_module_data_extraction(self):
        """Test that module data is correctly extracted from response."""
        stonk = Stonk("AAPL")
        
        # Mock response with nested module data
        mock_response = {
            "assetProfile": {
                "address1": "One Apple Park Way",
                "city": "Cupertino",
                "state": "CA",
                "zip": "95014",
                "country": "United States",
                "phone": "408 996 1010",
                "website": "https://www.apple.com",
                "industry": "Consumer Electronics",
                "sector": "Technology",
                "longBusinessSummary": "Apple Inc. designs, manufactures, and markets smartphones...",
                "fullTimeEmployees": 154000,
                "companyOfficers": []
            }
        }
        
        with patch.object(stonk._client, 'get_quote_summary', new_callable=AsyncMock) as mock_get_quote_summary:
            mock_get_quote_summary.return_value = mock_response
            
            result = await stonk._get_quote_summary_single_module("assetProfile")
            
            # Verify it returns only the module data, not the full response
            assert result == mock_response["assetProfile"]
            assert "address1" in result
            assert "city" in result
            assert "industry" in result


class TestStonkFinancialStatementMethods:
    """Test financial statement methods and validation."""

    @pytest.mark.asyncio
    async def test_get_financials_private_method_valid_parameters(self, timeseries_success_response):
        """Test _get_financials private method with valid parameters."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_timeseries', new_callable=AsyncMock) as mock_get_timeseries:
            mock_get_timeseries.return_value = timeseries_success_response
            
            result = await stonk._get_financials("annual", "income_stmt", 1640995200, 1672531200)
            
            # Verify client method was called with correct parameters
            expected_types = ['annualTotalRevenue', 'annualNetIncome']  # First few from income_stmt types
            mock_get_timeseries.assert_called_once()
            call_args = mock_get_timeseries.call_args
            assert call_args[0][0] == "AAPL"  # ticker
            assert call_args[0][2] == 1640995200  # period1
            assert call_args[0][3] == 1672531200  # period2
            
            # Verify types are prefixed with frequency
            types_args = call_args[0][1]  # types argument
            assert all(t.startswith("annual") for t in types_args)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_financials_quarterly_frequency(self, timeseries_success_response):
        """Test _get_financials with quarterly frequency."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_timeseries', new_callable=AsyncMock) as mock_get_timeseries:
            mock_get_timeseries.return_value = timeseries_success_response
            
            result = await stonk._get_financials("quarterly", "income_stmt", 1640995200, 1672531200)
            
            # Verify client method was called
            mock_get_timeseries.assert_called_once()
            call_args = mock_get_timeseries.call_args
            
            # Verify types are prefixed with frequency
            types_args = call_args[0][1]  # types argument
            assert all(t.startswith("quarterly") for t in types_args)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_financials_invalid_frequency(self):
        """Test _get_financials with invalid frequency raises error."""
        stonk = Stonk("AAPL")
        
        # Mock the error function to raise an exception
        with patch('src.stonk.error') as mock_error:
            mock_error.side_effect = ValueError("Invalid frequency")
            
            with pytest.raises(ValueError, match="Invalid frequency"):
                await stonk._get_financials("invalid", "income_stmt")

    @pytest.mark.asyncio
    async def test_get_financials_invalid_type(self):
        """Test _get_financials with invalid type raises error."""
        stonk = Stonk("AAPL")
        
        # Mock the error function to raise an exception
        with patch('src.stonk.error') as mock_error:
            mock_error.side_effect = ValueError("Invalid type")
            
            with pytest.raises(ValueError, match="Invalid type"):
                await stonk._get_financials("annual", "invalid_type")

    @pytest.mark.asyncio
    async def test_get_income_statement_delegation(self, timeseries_success_response):
        """Test get_income_statement properly delegates to _get_financials."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
            mock_get_financials.return_value = timeseries_success_response
            
            result = await stonk.get_income_statement("annual", 1640995200, 1672531200)
            
            mock_get_financials.assert_called_once_with("annual", "income_stmt", 1640995200, 1672531200)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_balance_sheet_delegation(self, timeseries_success_response):
        """Test get_balance_sheet properly delegates to _get_financials."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
            mock_get_financials.return_value = timeseries_success_response
            
            result = await stonk.get_balance_sheet("annual", 1640995200, 1672531200)
            
            mock_get_financials.assert_called_once_with("annual", "balance_sheet", 1640995200, 1672531200)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_balance_sheet_trailing_frequency_error(self):
        """Test get_balance_sheet rejects trailing frequency."""
        stonk = Stonk("AAPL")
        
        # Mock the error function to raise an exception
        with patch('src.stonk.error') as mock_error:
            mock_error.side_effect = ValueError("trailing not allowed for balance sheet")
            
            with pytest.raises(ValueError, match="trailing not allowed for balance sheet"):
                await stonk.get_balance_sheet("trailing")

    @pytest.mark.asyncio
    async def test_get_cash_flow_delegation(self, timeseries_success_response):
        """Test get_cash_flow properly delegates to _get_financials."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
            mock_get_financials.return_value = timeseries_success_response
            
            result = await stonk.get_cash_flow("annual", 1640995200, 1672531200)
            
            mock_get_financials.assert_called_once_with("annual", "cash_flow", 1640995200, 1672531200)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_financial_methods_with_default_periods(self, timeseries_success_response):
        """Test financial methods work with default period parameters."""
        stonk = Stonk("AAPL")
        
        methods_and_types = [
            (stonk.get_income_statement, "income_stmt"),
            (stonk.get_balance_sheet, "balance_sheet"),
            (stonk.get_cash_flow, "cash_flow"),
        ]
        
        for method, expected_type in methods_and_types:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.return_value = timeseries_success_response
                
                # Call method with only frequency (no periods)
                if expected_type == "balance_sheet":
                    # Skip balance sheet with trailing frequency
                    result = await method("annual")
                    mock_get_financials.assert_called_once_with("annual", expected_type, None, None)
                else:
                    result = await method("quarterly")
                    mock_get_financials.assert_called_once_with("quarterly", expected_type, None, None)
                
                assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_financial_methods_error_propagation(self):
        """Test that errors from _get_financials are properly propagated."""
        stonk = Stonk("AAPL")
        
        methods = [stonk.get_income_statement, stonk.get_cash_flow]
        
        for method in methods:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.side_effect = RuntimeError("Financial data error")
                
                with pytest.raises(RuntimeError, match="Financial data error"):
                    await method("annual")


class TestStonkRemainingMethods:
    """Test remaining Stonk methods for options, search, recommendations, and insights."""

    @pytest.mark.asyncio
    async def test_get_options_delegation_and_parameters(self, options_success_response):
        """Test get_options properly delegates to AsyncClient with correct parameters."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_options', new_callable=AsyncMock) as mock_get_options:
            mock_get_options.return_value = options_success_response
            
            result = await stonk.get_options()
            
            # Verify the client method was called with correct ticker
            mock_get_options.assert_called_once_with("AAPL")
            assert result == options_success_response

    @pytest.mark.asyncio
    async def test_get_options_with_different_tickers(self, options_success_response, valid_tickers):
        """Test get_options works correctly with different ticker symbols."""
        for ticker in valid_tickers[:3]:  # Test first 3 tickers
            stonk = Stonk(ticker)
            
            with patch.object(stonk._client, 'get_options', new_callable=AsyncMock) as mock_get_options:
                mock_get_options.return_value = options_success_response
                
                result = await stonk.get_options()
                
                mock_get_options.assert_called_once_with(ticker)
                assert result == options_success_response

    @pytest.mark.asyncio
    async def test_get_search_delegation_and_parameters(self, search_success_response):
        """Test get_search properly delegates to AsyncClient with correct parameters."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_search', new_callable=AsyncMock) as mock_get_search:
            mock_get_search.return_value = search_success_response
            
            result = await stonk.get_search()
            
            # Verify the client method was called with correct ticker
            mock_get_search.assert_called_once_with("AAPL")
            assert result == search_success_response

    @pytest.mark.asyncio
    async def test_get_search_with_different_tickers(self, search_success_response, valid_tickers):
        """Test get_search works correctly with different ticker symbols."""
        for ticker in valid_tickers[:3]:  # Test first 3 tickers
            stonk = Stonk(ticker)
            
            with patch.object(stonk._client, 'get_search', new_callable=AsyncMock) as mock_get_search:
                mock_get_search.return_value = search_success_response
                
                result = await stonk.get_search()
                
                mock_get_search.assert_called_once_with(ticker)
                assert result == search_success_response

    @pytest.mark.asyncio
    async def test_get_recommendations_delegation_and_parameters(self, recommendations_success_response):
        """Test get_recommendations properly delegates to AsyncClient with correct parameters."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_recommendations', new_callable=AsyncMock) as mock_get_recommendations:
            mock_get_recommendations.return_value = recommendations_success_response
            
            result = await stonk.get_recommendations()
            
            # Verify the client method was called with correct ticker
            mock_get_recommendations.assert_called_once_with("AAPL")
            assert result == recommendations_success_response

    @pytest.mark.asyncio
    async def test_get_recommendations_with_different_tickers(self, recommendations_success_response, valid_tickers):
        """Test get_recommendations works correctly with different ticker symbols."""
        for ticker in valid_tickers[:3]:  # Test first 3 tickers
            stonk = Stonk(ticker)
            
            with patch.object(stonk._client, 'get_recommendations', new_callable=AsyncMock) as mock_get_recommendations:
                mock_get_recommendations.return_value = recommendations_success_response
                
                result = await stonk.get_recommendations()
                
                mock_get_recommendations.assert_called_once_with(ticker)
                assert result == recommendations_success_response

    @pytest.mark.asyncio
    async def test_get_insights_delegation_and_parameters(self, insights_success_response):
        """Test get_insights properly delegates to AsyncClient with correct parameters."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_insights', new_callable=AsyncMock) as mock_get_insights:
            mock_get_insights.return_value = insights_success_response
            
            result = await stonk.get_insights()
            
            # Verify the client method was called with correct ticker
            mock_get_insights.assert_called_once_with("AAPL")
            assert result == insights_success_response

    @pytest.mark.asyncio
    async def test_get_insights_with_different_tickers(self, insights_success_response, valid_tickers):
        """Test get_insights works correctly with different ticker symbols."""
        for ticker in valid_tickers[:3]:  # Test first 3 tickers
            stonk = Stonk(ticker)
            
            with patch.object(stonk._client, 'get_insights', new_callable=AsyncMock) as mock_get_insights:
                mock_get_insights.return_value = insights_success_response
                
                result = await stonk.get_insights()
                
                mock_get_insights.assert_called_once_with(ticker)
                assert result == insights_success_response

    @pytest.mark.asyncio
    async def test_remaining_methods_return_correct_data_structure(self):
        """Test that remaining methods return the expected data structure."""
        stonk = Stonk("AAPL")
        
        # Test data structures for each method
        test_cases = [
            (stonk.get_options, "get_options", {"optionChain": {"result": [{"underlyingSymbol": "AAPL"}]}}),
            (stonk.get_search, "get_search", {"quotes": [{"symbol": "AAPL", "shortname": "Apple Inc."}]}),
            (stonk.get_recommendations, "get_recommendations", {"finance": {"result": [{"symbol": "AAPL"}]}}),
            (stonk.get_insights, "get_insights", {"finance": {"result": {"symbol": "AAPL"}}})
        ]
        
        for method, client_method_name, expected_response in test_cases:
            with patch.object(stonk._client, client_method_name, new_callable=AsyncMock) as mock_client_method:
                mock_client_method.return_value = expected_response
                
                result = await method()
                
                mock_client_method.assert_called_once_with("AAPL")
                assert result == expected_response

    @pytest.mark.asyncio
    async def test_remaining_methods_with_special_ticker_characters(self):
        """Test remaining methods work with special characters in ticker symbols."""
        special_tickers = ["BRK.A", "BRK-B", "GOOGL.L"]
        
        for ticker in special_tickers:
            stonk = Stonk(ticker)
            
            # Test each method with special ticker
            methods_and_client_methods = [
                (stonk.get_options, "get_options"),
                (stonk.get_search, "get_search"),
                (stonk.get_recommendations, "get_recommendations"),
                (stonk.get_insights, "get_insights")
            ]
            
            for method, client_method_name in methods_and_client_methods:
                with patch.object(stonk._client, client_method_name, new_callable=AsyncMock) as mock_client_method:
                    mock_client_method.return_value = {"test": "data"}
                    
                    result = await method()
                    
                    mock_client_method.assert_called_once_with(ticker)
                    assert result == {"test": "data"}


class TestStonkErrorPropagation:
    """Test error propagation from AsyncClient to Stonk methods."""

    @pytest.mark.asyncio
    async def test_get_options_error_propagation(self):
        """Test that errors from AsyncClient.get_options are properly propagated."""
        stonk = Stonk("AAPL")
        
        error_scenarios = [
            (ValueError("Invalid ticker"), "Invalid ticker"),
            (ConnectionError("Network error"), "Network error"),
            (RuntimeError("API error"), "API error"),
            (KeyError("Missing data"), "Missing data"),
            (TimeoutError("Request timeout"), "Request timeout")
        ]
        
        for exception, error_message in error_scenarios:
            with patch.object(stonk._client, 'get_options', new_callable=AsyncMock) as mock_get_options:
                mock_get_options.side_effect = exception
                
                with pytest.raises(type(exception), match=error_message):
                    await stonk.get_options()

    @pytest.mark.asyncio
    async def test_get_search_error_propagation(self):
        """Test that errors from AsyncClient.get_search are properly propagated."""
        stonk = Stonk("AAPL")
        
        error_scenarios = [
            (ValueError("Invalid search query"), "Invalid search query"),
            (ConnectionError("Network error"), "Network error"),
            (RuntimeError("Search API error"), "Search API error"),
            (KeyError("Missing search data"), "Missing search data")
        ]
        
        for exception, error_message in error_scenarios:
            with patch.object(stonk._client, 'get_search', new_callable=AsyncMock) as mock_get_search:
                mock_get_search.side_effect = exception
                
                with pytest.raises(type(exception), match=error_message):
                    await stonk.get_search()

    @pytest.mark.asyncio
    async def test_get_recommendations_error_propagation(self):
        """Test that errors from AsyncClient.get_recommendations are properly propagated."""
        stonk = Stonk("AAPL")
        
        error_scenarios = [
            (ValueError("Invalid ticker for recommendations"), "Invalid ticker for recommendations"),
            (ConnectionError("Network error"), "Network error"),
            (RuntimeError("Recommendations API error"), "Recommendations API error"),
            (KeyError("Missing recommendations data"), "Missing recommendations data")
        ]
        
        for exception, error_message in error_scenarios:
            with patch.object(stonk._client, 'get_recommendations', new_callable=AsyncMock) as mock_get_recommendations:
                mock_get_recommendations.side_effect = exception
                
                with pytest.raises(type(exception), match=error_message):
                    await stonk.get_recommendations()

    @pytest.mark.asyncio
    async def test_get_insights_error_propagation(self):
        """Test that errors from AsyncClient.get_insights are properly propagated."""
        stonk = Stonk("AAPL")
        
        error_scenarios = [
            (ValueError("Invalid ticker for insights"), "Invalid ticker for insights"),
            (ConnectionError("Network error"), "Network error"),
            (RuntimeError("Insights API error"), "Insights API error"),
            (KeyError("Missing insights data"), "Missing insights data"),
            (AttributeError("Invalid response format"), "Invalid response format")
        ]
        
        for exception, error_message in error_scenarios:
            with patch.object(stonk._client, 'get_insights', new_callable=AsyncMock) as mock_get_insights:
                mock_get_insights.side_effect = exception
                
                with pytest.raises(type(exception), match=error_message):
                    await stonk.get_insights()

    @pytest.mark.asyncio
    async def test_multiple_methods_error_propagation_consistency(self):
        """Test that all remaining methods consistently propagate the same types of errors."""
        stonk = Stonk("AAPL")
        
        # Common error that should be propagated by all methods
        common_error = ConnectionError("Network connection failed")
        
        methods_and_client_methods = [
            (stonk.get_options, "get_options"),
            (stonk.get_search, "get_search"),
            (stonk.get_recommendations, "get_recommendations"),
            (stonk.get_insights, "get_insights")
        ]
        
        for method, client_method_name in methods_and_client_methods:
            with patch.object(stonk._client, client_method_name, new_callable=AsyncMock) as mock_client_method:
                mock_client_method.side_effect = common_error
                
                with pytest.raises(ConnectionError, match="Network connection failed"):
                    await method()

    @pytest.mark.asyncio
    async def test_error_propagation_preserves_exception_details(self):
        """Test that error propagation preserves original exception details."""
        stonk = Stonk("AAPL")
        
        # Create a custom exception with specific attributes
        class CustomAPIError(Exception):
            def __init__(self, message, error_code=None, status_code=None):
                super().__init__(message)
                self.error_code = error_code
                self.status_code = status_code
        
        custom_error = CustomAPIError("API rate limit exceeded", error_code="RATE_LIMIT", status_code=429)
        
        methods_and_client_methods = [
            (stonk.get_options, "get_options"),
            (stonk.get_search, "get_search"),
            (stonk.get_recommendations, "get_recommendations"),
            (stonk.get_insights, "get_insights")
        ]
        
        for method, client_method_name in methods_and_client_methods:
            with patch.object(stonk._client, client_method_name, new_callable=AsyncMock) as mock_client_method:
                mock_client_method.side_effect = custom_error
                
                with pytest.raises(CustomAPIError) as exc_info:
                    await method()
                
                # Verify exception details are preserved
                assert str(exc_info.value) == "API rate limit exceeded"
                assert exc_info.value.error_code == "RATE_LIMIT"
                assert exc_info.value.status_code == 429

    @pytest.mark.asyncio
    async def test_async_error_handling_in_remaining_methods(self):
        """Test that async-specific errors are properly handled in remaining methods."""
        stonk = Stonk("AAPL")
        
        # Test asyncio-specific errors
        import asyncio
        async_errors = [
            asyncio.TimeoutError("Async operation timed out"),
            asyncio.CancelledError("Async operation was cancelled")
        ]
        
        methods_and_client_methods = [
            (stonk.get_options, "get_options"),
            (stonk.get_search, "get_search"),
            (stonk.get_recommendations, "get_recommendations"),
            (stonk.get_insights, "get_insights")
        ]
        
        for error in async_errors:
            for method, client_method_name in methods_and_client_methods:
                with patch.object(stonk._client, client_method_name, new_callable=AsyncMock) as mock_client_method:
                    mock_client_method.side_effect = error
                    
                    with pytest.raises(type(error)):
                        await method()

    @pytest.mark.asyncio
    async def test_error_propagation_with_empty_ticker(self):
        """Test error propagation works correctly even with empty ticker."""
        stonk = Stonk("")  # Empty ticker
        
        error = ValueError("Empty ticker not allowed")
        
        methods_and_client_methods = [
            (stonk.get_options, "get_options"),
            (stonk.get_search, "get_search"),
            (stonk.get_recommendations, "get_recommendations"),
            (stonk.get_insights, "get_insights")
        ]
        
        for method, client_method_name in methods_and_client_methods:
            with patch.object(stonk._client, client_method_name, new_callable=AsyncMock) as mock_client_method:
                mock_client_method.side_effect = error
                
                with pytest.raises(ValueError, match="Empty ticker not allowed"):
                    await method()
                
                # Verify the empty ticker was still passed to the client
                mock_client_method.assert_called_once_with("")

    @pytest.mark.asyncio
    async def test_get_financials_invalid_frequency(self):
        """Test _get_financials with invalid frequency raises error."""
        from src.utils import error
        
        stonk = Stonk("AAPL")
        
        # Mock the error function to raise an exception
        with patch('src.stonk.error') as mock_error:
            mock_error.side_effect = ValueError("Invalid frequency")
            
            with pytest.raises(ValueError, match="Invalid frequency"):
                await stonk._get_financials("invalid_freq", "income_stmt")
            
            # Verify error was called with correct message
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0][0]
            assert "Invalid frequency" in call_args
            assert "invalid_freq" in call_args

    @pytest.mark.asyncio
    async def test_get_financials_invalid_type(self):
        """Test _get_financials with invalid type raises error."""
        stonk = Stonk("AAPL")
        
        # Mock the error function to raise an exception
        with patch('src.stonk.error') as mock_error:
            mock_error.side_effect = ValueError("Invalid type")
            
            with pytest.raises(ValueError, match="Invalid type"):
                await stonk._get_financials("annual", "invalid_type")
            
            # Verify error was called with correct message
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0][0]
            assert "Invalid typ" in call_args
            assert "invalid_type" in call_args

    @pytest.mark.asyncio
    async def test_get_financials_frequency_validation(self):
        """Test _get_financials validates frequency against FREQUENCIES constant."""
        from src.const import FREQUENCIES
        
        stonk = Stonk("AAPL")
        
        # Test each valid frequency doesn't raise error
        for frequency in FREQUENCIES:
            with patch.object(stonk._client, 'get_timeseries', new_callable=AsyncMock) as mock_get_timeseries:
                mock_get_timeseries.return_value = {"test": "data"}
                
                # Should not raise error for valid frequencies
                result = await stonk._get_financials(frequency, "income_stmt")
                assert result == {"test": "data"}

    @pytest.mark.asyncio
    async def test_get_financials_type_validation(self):
        """Test _get_financials validates type against TYPES constant."""
        from src.const import TYPES
        
        stonk = Stonk("AAPL")
        
        # Test each valid type doesn't raise error
        for typ in TYPES.keys():
            with patch.object(stonk._client, 'get_timeseries', new_callable=AsyncMock) as mock_get_timeseries:
                mock_get_timeseries.return_value = {"test": "data"}
                
                # Should not raise error for valid types
                result = await stonk._get_financials("annual", typ)
                assert result == {"test": "data"}

    @pytest.mark.asyncio
    async def test_get_financials_types_with_frequency_prefix(self, timeseries_success_response):
        """Test _get_financials correctly prefixes types with frequency."""
        from src.const import TYPES
        
        stonk = Stonk("AAPL")
        
        with patch.object(stonk._client, 'get_timeseries', new_callable=AsyncMock) as mock_get_timeseries:
            mock_get_timeseries.return_value = timeseries_success_response
            
            await stonk._get_financials("quarterly", "income_stmt")
            
            # Verify types are prefixed with frequency
            call_args = mock_get_timeseries.call_args
            types_arg = call_args[0][1]
            expected_types = [f'quarterly{t}' for t in TYPES['income_stmt']]
            assert types_arg == expected_types

    @pytest.mark.asyncio
    async def test_get_income_statement_delegation(self, timeseries_success_response):
        """Test get_income_statement properly delegates to _get_financials."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
            mock_get_financials.return_value = timeseries_success_response
            
            result = await stonk.get_income_statement("annual", 1640995200, 1672531200)
            
            # Verify _get_financials was called with correct parameters
            mock_get_financials.assert_called_once_with("annual", "income_stmt", 1640995200, 1672531200)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_income_statement_with_different_frequencies(self, timeseries_success_response):
        """Test get_income_statement with different frequency values."""
        from src.const import FREQUENCIES
        
        stonk = Stonk("AAPL")
        
        for frequency in FREQUENCIES:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.return_value = timeseries_success_response
                
                result = await stonk.get_income_statement(frequency)
                
                mock_get_financials.assert_called_once_with(frequency, "income_stmt", None, None)
                assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_income_statement_optional_parameters(self, timeseries_success_response):
        """Test get_income_statement with optional period parameters."""
        stonk = Stonk("AAPL")
        
        test_cases = [
            # (period1, period2)
            (None, None),
            (1640995200, None),
            (None, 1672531200),
            (1640995200, 1672531200),
        ]
        
        for period1, period2 in test_cases:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.return_value = timeseries_success_response
                
                result = await stonk.get_income_statement("annual", period1, period2)
                
                mock_get_financials.assert_called_once_with("annual", "income_stmt", period1, period2)
                assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_balance_sheet_delegation(self, timeseries_success_response):
        """Test get_balance_sheet properly delegates to _get_financials."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
            mock_get_financials.return_value = timeseries_success_response
            
            result = await stonk.get_balance_sheet("annual", 1640995200, 1672531200)
            
            # Verify _get_financials was called with correct parameters
            mock_get_financials.assert_called_once_with("annual", "balance_sheet", 1640995200, 1672531200)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_balance_sheet_trailing_frequency_rejection(self):
        """Test get_balance_sheet rejects trailing frequency."""
        stonk = Stonk("AAPL")
        
        # Mock the error function to raise an exception
        with patch('src.stonk.error') as mock_error:
            mock_error.side_effect = ValueError("trailing not allowed for balance sheet")
            
            with pytest.raises(ValueError, match="trailing not allowed for balance sheet"):
                await stonk.get_balance_sheet("trailing")
            
            # Verify error was called with correct message
            mock_error.assert_called_once()
            call_args = mock_error.call_args[0][0]
            assert "trailing" in call_args
            assert "not allowed for balance sheet" in call_args

    @pytest.mark.asyncio
    async def test_get_balance_sheet_valid_frequencies(self, timeseries_success_response):
        """Test get_balance_sheet accepts annual and quarterly frequencies."""
        stonk = Stonk("AAPL")
        
        valid_frequencies = ["annual", "quarterly"]
        
        for frequency in valid_frequencies:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.return_value = timeseries_success_response
                
                result = await stonk.get_balance_sheet(frequency)
                
                # Should not call error function and should delegate to _get_financials
                mock_get_financials.assert_called_once_with(frequency, "balance_sheet", None, None)
                assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_balance_sheet_trailing_check_before_delegation(self):
        """Test get_balance_sheet checks for trailing frequency before calling _get_financials."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
            with patch('src.stonk.error') as mock_error:
                mock_error.side_effect = ValueError("trailing not allowed")
                
                with pytest.raises(ValueError):
                    await stonk.get_balance_sheet("trailing")
                
                # _get_financials should not be called when trailing frequency is used
                mock_get_financials.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_cash_flow_delegation(self, timeseries_success_response):
        """Test get_cash_flow properly delegates to _get_financials."""
        stonk = Stonk("AAPL")
        
        with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
            mock_get_financials.return_value = timeseries_success_response
            
            result = await stonk.get_cash_flow("annual", 1640995200, 1672531200)
            
            # Verify _get_financials was called with correct parameters
            mock_get_financials.assert_called_once_with("annual", "cash_flow", 1640995200, 1672531200)
            assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_cash_flow_with_different_frequencies(self, timeseries_success_response):
        """Test get_cash_flow with different frequency values including trailing."""
        from src.const import FREQUENCIES
        
        stonk = Stonk("AAPL")
        
        # Cash flow should accept all frequencies including trailing
        for frequency in FREQUENCIES:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.return_value = timeseries_success_response
                
                result = await stonk.get_cash_flow(frequency)
                
                mock_get_financials.assert_called_once_with(frequency, "cash_flow", None, None)
                assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_cash_flow_optional_parameters(self, timeseries_success_response):
        """Test get_cash_flow with optional period parameters."""
        stonk = Stonk("AAPL")
        
        test_cases = [
            # (period1, period2)
            (None, None),
            (1640995200, None),
            (None, 1672531200),
            (1640995200, 1672531200),
        ]
        
        for period1, period2 in test_cases:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.return_value = timeseries_success_response
                
                result = await stonk.get_cash_flow("quarterly", period1, period2)
                
                mock_get_financials.assert_called_once_with("quarterly", "cash_flow", period1, period2)
                assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_financial_methods_error_propagation(self):
        """Test that errors from _get_financials are properly propagated."""
        stonk = Stonk("AAPL")
        
        # Test error propagation for each financial method
        financial_methods = [
            ('get_income_statement', 'annual'),
            ('get_balance_sheet', 'annual'),
            ('get_cash_flow', 'annual'),
        ]
        
        for method_name, frequency in financial_methods:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.side_effect = RuntimeError("API error")
                
                method = getattr(stonk, method_name)
                
                with pytest.raises(RuntimeError, match="API error"):
                    await method(frequency)

    @pytest.mark.asyncio
    async def test_financial_methods_parameter_types(self, timeseries_success_response):
        """Test financial methods accept different parameter types."""
        stonk = Stonk("AAPL")
        
        # Test with int and float period parameters
        test_periods = [
            (1640995200, 1672531200),  # int, int
            (1640995200.0, 1672531200.0),  # float, float
            (1640995200, 1672531200.0),  # int, float
            (1640995200.0, 1672531200),  # float, int
        ]
        
        for period1, period2 in test_periods:
            with patch.object(stonk, '_get_financials', new_callable=AsyncMock) as mock_get_financials:
                mock_get_financials.return_value = timeseries_success_response
                
                result = await stonk.get_income_statement("annual", period1, period2)
                
                mock_get_financials.assert_called_once_with("annual", "income_stmt", period1, period2)
                assert result == timeseries_success_response

    @pytest.mark.asyncio
    async def test_get_financials_with_all_statement_types(self, timeseries_success_response):
        """Test _get_financials works with all statement types."""
        from src.const import TYPES
        
        stonk = Stonk("AAPL")
        
        for statement_type in TYPES.keys():
            with patch.object(stonk._client, 'get_timeseries', new_callable=AsyncMock) as mock_get_timeseries:
                mock_get_timeseries.return_value = timeseries_success_response
                
                result = await stonk._get_financials("annual", statement_type)
                
                # Verify correct types are passed to timeseries
                call_args = mock_get_timeseries.call_args
                types_arg = call_args[0][1]
                expected_types = [f'annual{t}' for t in TYPES[statement_type]]
                assert types_arg == expected_types
                assert result == timeseries_success_response