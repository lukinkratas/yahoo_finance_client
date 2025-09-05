"""Shared test configuration and fixtures."""

import pytest
import respx
from curl_cffi.requests import AsyncSession

from src.client import AsyncClient
from src.stonk import Stonk


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_responses():
    """Fixture that provides a respx mock router for HTTP requests."""
    with respx.mock(base_url="https://query2.finance.yahoo.com") as respx_mock:
        yield respx_mock


@pytest.fixture
async def mock_session():
    """Fixture that provides a mock AsyncSession for testing."""
    session = AsyncSession(impersonate='chrome')
    yield session
    await session.aclose()


@pytest.fixture
async def async_client():
    """Fixture that provides an AsyncClient instance for testing."""
    client = AsyncClient()
    yield client
    # Cleanup if needed
    if hasattr(client, '_session') and client._session:
        await client._session.aclose()


@pytest.fixture
def stonk_instance():
    """Fixture that provides a Stonk instance for testing."""
    return Stonk("AAPL")


@pytest.fixture
def sample_ticker():
    """Fixture that provides a sample ticker for testing."""
    return "AAPL"


@pytest.fixture
def sample_tickers():
    """Fixture that provides multiple sample tickers for testing."""
    return ["AAPL", "GOOGL", "MSFT"]


@pytest.fixture
def valid_tickers():
    """Fixture that provides a list of valid tickers for testing."""
    return ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA"]


@pytest.fixture
def invalid_tickers():
    """Fixture that provides a list of invalid tickers for testing."""
    return ["", "INVALID_TICKER_TOO_LONG", "123", "!@#"]


@pytest.fixture
def valid_ranges():
    """Fixture that provides valid chart ranges for testing."""
    return ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]


@pytest.fixture
def invalid_ranges():
    """Fixture that provides invalid chart ranges for testing."""
    return ["invalid", "2h", "15y", "1w", ""]


@pytest.fixture
def valid_intervals():
    """Fixture that provides valid chart intervals for testing."""
    return ["1m", "5m", "15m", "30m", "1h", "6h", "1d"]


@pytest.fixture
def invalid_intervals():
    """Fixture that provides invalid chart intervals for testing."""
    return ["invalid", "2m", "45m", "2h", ""]


@pytest.fixture
def valid_events():
    """Fixture that provides valid chart events for testing."""
    return ["div", "split", "div,split", "split,div"]


@pytest.fixture
def invalid_events():
    """Fixture that provides invalid chart events for testing."""
    return ["invalid", "earnings", "div,earnings", ""]


@pytest.fixture
def valid_modules():
    """Fixture that provides valid quote summary modules for testing."""
    return [
        "quoteType", "assetProfile", "summaryProfile", "summaryDetail",
        "incomeStatementHistory", "balanceSheetHistory", "cashflowStatementHistory",
        "price", "defaultKeyStatistics", "financialData"
    ]


@pytest.fixture
def invalid_modules():
    """Fixture that provides invalid quote summary modules for testing."""
    return ["invalid", "nonexistent", "badModule", ""]


@pytest.fixture
def valid_frequencies():
    """Fixture that provides valid financial statement frequencies for testing."""
    return ["annual", "quarterly", "trailing"]


@pytest.fixture
def invalid_frequencies():
    """Fixture that provides invalid financial statement frequencies for testing."""
    return ["invalid", "monthly", "daily", ""]


@pytest.fixture
def mock_crumb():
    """Fixture that provides a mock crumb value for testing."""
    return "mock_crumb_value_123"


@pytest.fixture
def base_url():
    """Fixture that provides the base URL for Yahoo Finance API."""
    return "https://query2.finance.yahoo.com"


@pytest.fixture
def default_params():
    """Fixture that provides default API parameters."""
    return {
        'formatted': 'false',
        'region': 'US',
        'lang': 'en-US',
        'corsDomain': 'finance.yahoo.com',
    }
# Import mock response fixtures
from tests.fixtures.api_responses import (
    CHART_SUCCESS_RESPONSE,
    CHART_ERROR_RESPONSE,
    QUOTE_SUCCESS_RESPONSE,
    QUOTE_ERROR_RESPONSE,
    QUOTE_SUMMARY_SUCCESS_RESPONSE,
    QUOTE_SUMMARY_ERROR_RESPONSE,
    TIMESERIES_SUCCESS_RESPONSE,
    TIMESERIES_ERROR_RESPONSE,
    OPTIONS_SUCCESS_RESPONSE,
    OPTIONS_ERROR_RESPONSE,
    SEARCH_SUCCESS_RESPONSE,
    SEARCH_ERROR_RESPONSE,
    RECOMMENDATIONS_SUCCESS_RESPONSE,
    RECOMMENDATIONS_ERROR_RESPONSE,
    INSIGHTS_SUCCESS_RESPONSE,
    INSIGHTS_ERROR_RESPONSE,
    MARKET_SUMMARY_SUCCESS_RESPONSE,
    MARKET_SUMMARY_ERROR_RESPONSE,
    TRENDING_SUCCESS_RESPONSE,
    TRENDING_ERROR_RESPONSE,
    CURRENCIES_SUCCESS_RESPONSE,
    CURRENCIES_ERROR_RESPONSE,
    HTTP_401_ERROR,
    HTTP_404_ERROR,
    HTTP_500_ERROR,
    HTTP_503_ERROR,
    MALFORMED_JSON_RESPONSE,
    MISSING_RESULT_RESPONSE,
    MISSING_ERROR_RESPONSE,
    CRUMB_SUCCESS_RESPONSE,
    CRUMB_ERROR_RESPONSE
)


@pytest.fixture
def chart_success_response():
    """Fixture that provides a successful chart API response."""
    return CHART_SUCCESS_RESPONSE


@pytest.fixture
def chart_error_response():
    """Fixture that provides an error chart API response."""
    return CHART_ERROR_RESPONSE


@pytest.fixture
def quote_success_response():
    """Fixture that provides a successful quote API response."""
    return QUOTE_SUCCESS_RESPONSE


@pytest.fixture
def quote_error_response():
    """Fixture that provides an error quote API response."""
    return QUOTE_ERROR_RESPONSE


@pytest.fixture
def quote_summary_success_response():
    """Fixture that provides a successful quote summary API response."""
    return QUOTE_SUMMARY_SUCCESS_RESPONSE


@pytest.fixture
def quote_summary_error_response():
    """Fixture that provides an error quote summary API response."""
    return QUOTE_SUMMARY_ERROR_RESPONSE


@pytest.fixture
def timeseries_success_response():
    """Fixture that provides a successful timeseries API response."""
    return TIMESERIES_SUCCESS_RESPONSE


@pytest.fixture
def timeseries_error_response():
    """Fixture that provides an error timeseries API response."""
    return TIMESERIES_ERROR_RESPONSE


@pytest.fixture
def options_success_response():
    """Fixture that provides a successful options API response."""
    return OPTIONS_SUCCESS_RESPONSE


@pytest.fixture
def options_error_response():
    """Fixture that provides an error options API response."""
    return OPTIONS_ERROR_RESPONSE


@pytest.fixture
def search_success_response():
    """Fixture that provides a successful search API response."""
    return SEARCH_SUCCESS_RESPONSE


@pytest.fixture
def search_error_response():
    """Fixture that provides an error search API response."""
    return SEARCH_ERROR_RESPONSE


@pytest.fixture
def recommendations_success_response():
    """Fixture that provides a successful recommendations API response."""
    return RECOMMENDATIONS_SUCCESS_RESPONSE


@pytest.fixture
def recommendations_error_response():
    """Fixture that provides an error recommendations API response."""
    return RECOMMENDATIONS_ERROR_RESPONSE


@pytest.fixture
def insights_success_response():
    """Fixture that provides a successful insights API response."""
    return INSIGHTS_SUCCESS_RESPONSE


@pytest.fixture
def insights_error_response():
    """Fixture that provides an error insights API response."""
    return INSIGHTS_ERROR_RESPONSE


@pytest.fixture
def market_summary_success_response():
    """Fixture that provides a successful market summary API response."""
    return MARKET_SUMMARY_SUCCESS_RESPONSE


@pytest.fixture
def market_summary_error_response():
    """Fixture that provides an error market summary API response."""
    return MARKET_SUMMARY_ERROR_RESPONSE


@pytest.fixture
def trending_success_response():
    """Fixture that provides a successful trending API response."""
    return TRENDING_SUCCESS_RESPONSE


@pytest.fixture
def trending_error_response():
    """Fixture that provides an error trending API response."""
    return TRENDING_ERROR_RESPONSE


@pytest.fixture
def currencies_success_response():
    """Fixture that provides a successful currencies API response."""
    return CURRENCIES_SUCCESS_RESPONSE


@pytest.fixture
def currencies_error_response():
    """Fixture that provides an error currencies API response."""
    return CURRENCIES_ERROR_RESPONSE


@pytest.fixture
def http_error_responses():
    """Fixture that provides various HTTP error responses."""
    return {
        401: HTTP_401_ERROR,
        404: HTTP_404_ERROR,
        500: HTTP_500_ERROR,
        503: HTTP_503_ERROR
    }


@pytest.fixture
def malformed_responses():
    """Fixture that provides malformed API responses for testing error handling."""
    return {
        "malformed_json": MALFORMED_JSON_RESPONSE,
        "missing_result": MISSING_RESULT_RESPONSE,
        "missing_error": MISSING_ERROR_RESPONSE
    }


@pytest.fixture
def crumb_responses():
    """Fixture that provides crumb API responses."""
    return {
        "success": CRUMB_SUCCESS_RESPONSE,
        "error": CRUMB_ERROR_RESPONSE
    }


@pytest.fixture
def mock_successful_responses(mock_responses):
    """Fixture that sets up mock responses for all successful API endpoints."""
    # Chart endpoint
    mock_responses.get("/v8/finance/chart/AAPL").mock(
        return_value=respx.Response(200, json=CHART_SUCCESS_RESPONSE)
    )
    
    # Quote endpoint
    mock_responses.get("/v7/finance/quote").mock(
        return_value=respx.Response(200, json=QUOTE_SUCCESS_RESPONSE)
    )
    
    # Quote summary endpoint
    mock_responses.get("/v10/finance/quoteSummary/AAPL").mock(
        return_value=respx.Response(200, json=QUOTE_SUMMARY_SUCCESS_RESPONSE)
    )
    
    # Timeseries endpoint
    mock_responses.get("/ws/fundamentals-timeseries/v1/finance/timeseries/AAPL").mock(
        return_value=respx.Response(200, json=TIMESERIES_SUCCESS_RESPONSE)
    )
    
    # Options endpoint
    mock_responses.get("/v7/finance/options/AAPL").mock(
        return_value=respx.Response(200, json=OPTIONS_SUCCESS_RESPONSE)
    )
    
    # Search endpoint
    mock_responses.get("/v1/finance/search").mock(
        return_value=respx.Response(200, json=SEARCH_SUCCESS_RESPONSE)
    )
    
    # Recommendations endpoint
    mock_responses.get("/v6/finance/recommendationsbysymbol/AAPL").mock(
        return_value=respx.Response(200, json=RECOMMENDATIONS_SUCCESS_RESPONSE)
    )
    
    # Insights endpoint
    mock_responses.get("/ws/insights/v2/finance/insights").mock(
        return_value=respx.Response(200, json=INSIGHTS_SUCCESS_RESPONSE)
    )
    
    # Market summary endpoint
    mock_responses.get("/v6/finance/quote/marketSummary").mock(
        return_value=respx.Response(200, json=MARKET_SUMMARY_SUCCESS_RESPONSE)
    )
    
    # Trending endpoint
    mock_responses.get("/v1/finance/trending/US").mock(
        return_value=respx.Response(200, json=TRENDING_SUCCESS_RESPONSE)
    )
    
    # Currencies endpoint
    mock_responses.get("/v1/finance/currencies").mock(
        return_value=respx.Response(200, json=CURRENCIES_SUCCESS_RESPONSE)
    )
    
    # Crumb endpoint
    mock_responses.get("/v1/test/getcrumb").mock(
        return_value=respx.Response(200, text=CRUMB_SUCCESS_RESPONSE)
    )
    
    return mock_responses


@pytest.fixture
def mock_error_responses(mock_responses):
    """Fixture that sets up mock error responses for all API endpoints."""
    # Chart endpoint errors
    mock_responses.get("/v8/finance/chart/INVALID").mock(
        return_value=respx.Response(200, json=CHART_ERROR_RESPONSE)
    )
    
    # Quote endpoint errors
    mock_responses.get("/v7/finance/quote", params={"symbols": "INVALID"}).mock(
        return_value=respx.Response(200, json=QUOTE_ERROR_RESPONSE)
    )
    
    # Quote summary endpoint errors
    mock_responses.get("/v10/finance/quoteSummary/INVALID").mock(
        return_value=respx.Response(200, json=QUOTE_SUMMARY_ERROR_RESPONSE)
    )
    
    # HTTP error responses
    mock_responses.get("/v8/finance/chart/UNAUTHORIZED").mock(
        return_value=respx.Response(401, json=HTTP_401_ERROR)
    )
    
    mock_responses.get("/v8/finance/chart/NOTFOUND").mock(
        return_value=respx.Response(404, json=HTTP_404_ERROR)
    )
    
    mock_responses.get("/v8/finance/chart/SERVERERROR").mock(
        return_value=respx.Response(500, json=HTTP_500_ERROR)
    )
    
    mock_responses.get("/v8/finance/chart/UNAVAILABLE").mock(
        return_value=respx.Response(503, json=HTTP_503_ERROR)
    )
    
    return mock_responses