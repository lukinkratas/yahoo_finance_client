# Design Document

## Overview

This design document outlines the architecture and implementation strategy for comprehensive unit tests for the Yahoo Finance API client. The testing framework will use pytest with async support, httpx for HTTP mocking, and coverage.py for test coverage reporting. The design emphasizes isolation, maintainability, and comprehensive coverage of both success and error scenarios.

## Architecture

### Testing Framework Stack

- **pytest**: Primary testing framework with excellent async support and fixture management
- **pytest-asyncio**: Plugin for testing async/await code
- **httpx**: Modern HTTP client with built-in mocking capabilities via respx
- **respx**: HTTP request mocking library that integrates well with httpx and async code
- **coverage.py**: Code coverage measurement and reporting
- **pytest-cov**: Coverage plugin for pytest integration
- **uv**: used package manager for the whole repo

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                 # Shared fixtures and configuration
├── test_client.py             # AsyncClient tests
├── test_stonk.py              # Stonk class tests
├── test_utils.py              # Utility function tests
├── fixtures/
│   ├── __init__.py
│   ├── api_responses.py       # Mock API response data
│   └── test_data.py          # Test data constants
└── integration/               # Future integration tests
    └── __init__.py
```

## Components and Interfaces

### Test Configuration (conftest.py)

**Purpose**: Centralized test configuration and shared fixtures

**Key Components**:
- Async event loop fixture for pytest-asyncio
- Mock HTTP client fixtures
- Common test data fixtures
- Response mocking utilities

**Interface**:
```python
@pytest.fixture
async def mock_client() -> AsyncClient

@pytest.fixture
def mock_responses() -> respx.MockRouter

@pytest.fixture
def sample_chart_response() -> dict[str, Any]
```

### AsyncClient Tests (test_client.py)

**Purpose**: Test all AsyncClient methods including HTTP handling, parameter validation, and error scenarios

**Test Categories**:
1. **HTTP Request Tests**: Verify correct URL construction, parameter passing, and request headers
2. **Response Processing Tests**: Verify JSON parsing and result extraction
3. **Error Handling Tests**: Test various HTTP error codes and API error responses
4. **Parameter Validation Tests**: Test invalid parameter handling
5. **Authentication Tests**: Test crumb fetching and caching

**Key Test Methods**:
```python
class TestAsyncClient:
    async def test_get_chart_success()
    async def test_get_chart_invalid_range()
    async def test_get_quote_success()
    async def test_get_quote_summary_invalid_modules()
    async def test_crumb_property_caching()
    async def test_http_error_handling()
    async def test_api_error_response()
```

### Stonk Tests (test_stonk.py)

**Purpose**: Test Stonk class methods, focusing on proper delegation to AsyncClient and parameter handling

**Test Categories**:
1. **Initialization Tests**: Verify ticker assignment and client setup
2. **Delegation Tests**: Verify methods properly call AsyncClient with correct parameters
3. **Data Extraction Tests**: Test quote summary module extraction
4. **Financial Data Tests**: Test frequency and type validation for financial statements
5. **Error Propagation Tests**: Verify errors from AsyncClient are properly propagated

**Key Test Methods**:
```python
class TestStonk:
    def test_initialization()
    async def test_get_chart_delegation()
    async def test_get_quote_type_extraction()
    async def test_get_balance_sheet_trailing_error()
    async def test_financial_frequency_validation()
```

### Utility Tests (test_utils.py)

**Purpose**: Test utility functions for error handling and URL formatting

**Test Categories**:
1. **Error Function Tests**: Test logging and exception raising
2. **URL Formatting Tests**: Test print_url with various parameter combinations

**Key Test Methods**:
```python
class TestUtils:
    def test_error_function_default_exception()
    def test_error_function_custom_exception()
    def test_print_url_no_params()
    def test_print_url_with_params()
```

## Data Models

### Mock Response Structure

Mock responses will follow the actual Yahoo Finance API structure:

```python
CHART_RESPONSE = {
    "chart": {
        "result": [{
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
        }],
        "error": None
    }
}
```

### Test Data Constants

```python
VALID_TICKERS = ["AAPL", "GOOGL", "MSFT", "TSLA"]
INVALID_TICKERS = ["", "INVALID_TICKER_TOO_LONG"]
VALID_RANGES = ["1d", "5d", "1mo", "1y", "max"]
INVALID_RANGES = ["invalid", "2h", "15y"]
```

## Error Handling

### HTTP Error Scenarios

1. **Network Errors**: Connection timeouts, DNS failures
2. **HTTP Status Errors**: 401 Unauthorized, 404 Not Found, 500 Internal Server Error
3. **API Errors**: Yahoo Finance specific error responses
4. **Malformed Responses**: Invalid JSON, missing required fields

### Error Testing Strategy

```python
async def test_http_401_error(mock_responses):
    mock_responses.get("https://query2.finance.yahoo.com/v8/finance/chart/AAPL").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )
    
    client = AsyncClient()
    with pytest.raises(HTTPError):
        await client.get_chart("AAPL", "1d", "1d")
```

## Testing Strategy

### Mocking Strategy

1. **HTTP Level Mocking**: Use respx to mock HTTP requests at the transport level
2. **Response Mocking**: Create realistic mock responses based on actual API responses
3. **Error Injection**: Mock various error conditions to test error handling paths
4. **Async Context**: Ensure all mocks work correctly with async/await patterns

### Coverage Strategy

1. **Line Coverage**: Target 95%+ line coverage across all modules
2. **Branch Coverage**: Ensure all conditional branches are tested
3. **Error Path Coverage**: Comprehensive testing of error handling code paths
4. **Integration Points**: Test interactions between Stonk and AsyncClient

### Test Data Management

1. **Fixtures**: Use pytest fixtures for reusable test data
2. **Parameterized Tests**: Use pytest.mark.parametrize for testing multiple scenarios
3. **Mock Data**: Store complex mock responses in separate fixture files
4. **Data Validation**: Ensure mock data matches real API response structure

## Performance Considerations

### Test Execution Speed

1. **Parallel Execution**: Configure pytest-xdist for parallel test execution
2. **Mock Efficiency**: Use lightweight mocks that don't perform actual HTTP requests
3. **Fixture Scoping**: Optimize fixture scopes to minimize setup/teardown overhead
4. **Selective Testing**: Support running specific test categories during development

### Resource Management

1. **Async Context Management**: Proper cleanup of async resources in tests
2. **Mock Lifecycle**: Ensure mocks are properly reset between tests
3. **Memory Usage**: Monitor memory usage during test execution
4. **Connection Pooling**: Verify HTTP client connection pooling works correctly

## Integration Points

### CI/CD Integration

1. **GitHub Actions**: Configure automated test execution on pull requests
2. **Coverage Reporting**: Integrate with coverage reporting services
3. **Test Results**: Generate JUnit XML reports for CI systems
4. **Quality Gates**: Fail builds if coverage drops below threshold

### Development Workflow

1. **Pre-commit Hooks**: Run tests before commits
2. **IDE Integration**: Support for running tests from development environments
3. **Debug Support**: Enable debugging of failing tests
4. **Watch Mode**: Support for continuous test execution during development