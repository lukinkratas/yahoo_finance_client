"""Test data constants and utilities for Yahoo Finance API tests."""

from typing import List, Dict, Any
import datetime


# Valid test data
VALID_TICKERS: List[str] = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA"]
VALID_RANGES: List[str] = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
VALID_INTERVALS: List[str] = ["1m", "5m", "15m", "30m", "1h", "6h", "1d"]
VALID_EVENTS: List[str] = ["div", "split", "div,split", "split,div"]
VALID_FREQUENCIES: List[str] = ["annual", "quarterly", "trailing"]

# Invalid test data
INVALID_TICKERS: List[str] = ["", "INVALID_TICKER_TOO_LONG", "123", "!@#", "invalid"]
INVALID_RANGES: List[str] = ["invalid", "2h", "15y", "1w", "", "2d"]
INVALID_INTERVALS: List[str] = ["invalid", "2m", "45m", "2h", "", "3d"]
INVALID_EVENTS: List[str] = ["invalid", "earnings", "div,earnings", "", "badEvent"]
INVALID_FREQUENCIES: List[str] = ["invalid", "monthly", "daily", "", "weekly"]

# Valid quote summary modules
VALID_MODULES: List[str] = [
    "quoteType",
    "assetProfile", 
    "summaryProfile",
    "summaryDetail",
    "incomeStatementHistory",
    "incomeStatementHistoryQuarterly",
    "balanceSheetHistory",
    "balanceSheetHistoryQuarterly",
    "cashflowStatementHistory",
    "cashflowStatementHistoryQuarterly",
    "esgScores",
    "price",
    "defaultKeyStatistics",
    "financialData",
    "calendarEvents",
    "secFilings",
    "upgradeDowngradeHistory",
    "institutionOwnership",
    "fundOwnership",
    "majorDirectHolders",
    "majorHoldersBreakdown",
    "insiderTransactions",
    "insiderHolders",
    "netSharePurchaseActivity",
    "earnings",
    "earningsHistory",
    "earningsTrend",
    "industryTrend",
    "indexTrend",
    "sectorTrend",
    "recommendationTrend",
    "pageViews"
]

# Invalid quote summary modules
INVALID_MODULES: List[str] = ["invalid", "nonexistent", "badModule", "", "fakeModule"]

# Valid timeseries types for testing
VALID_INCOME_STMT_TYPES: List[str] = [
    "annualTotalRevenue",
    "annualNetIncome", 
    "annualGrossProfit",
    "annualOperatingIncome",
    "quarterlyTotalRevenue",
    "quarterlyNetIncome",
    "quarterlyGrossProfit",
    "quarterlyOperatingIncome",
    "trailingTotalRevenue",
    "trailingNetIncome"
]

VALID_BALANCE_SHEET_TYPES: List[str] = [
    "annualTotalAssets",
    "annualTotalLiabilitiesNetMinorityInterest",
    "annualStockholdersEquity",
    "annualTotalDebt",
    "quarterlyTotalAssets",
    "quarterlyTotalLiabilitiesNetMinorityInterest",
    "quarterlyStockholdersEquity",
    "quarterlyTotalDebt"
]

VALID_CASH_FLOW_TYPES: List[str] = [
    "annualOperatingCashFlow",
    "annualInvestingCashFlow",
    "annualFinancingCashFlow",
    "annualFreeCashFlow",
    "quarterlyOperatingCashFlow",
    "quarterlyInvestingCashFlow",
    "quarterlyFinancingCashFlow",
    "quarterlyFreeCashFlow",
    "trailingOperatingCashFlow",
    "trailingFreeCashFlow"
]

# Test timestamps
TEST_TIMESTAMPS: Dict[str, int] = {
    "start_2020": int(datetime.datetime(2020, 1, 1).timestamp()),
    "start_2021": int(datetime.datetime(2021, 1, 1).timestamp()),
    "start_2022": int(datetime.datetime(2022, 1, 1).timestamp()),
    "end_2021": int(datetime.datetime(2021, 12, 31).timestamp()),
    "end_2022": int(datetime.datetime(2022, 12, 31).timestamp()),
    "current": int(datetime.datetime.now().timestamp())
}

# API endpoint paths for testing
API_ENDPOINTS: Dict[str, str] = {
    "chart": "/v8/finance/chart/{ticker}",
    "quote": "/v7/finance/quote",
    "quote_summary": "/v10/finance/quoteSummary/{ticker}",
    "timeseries": "/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}",
    "options": "/v7/finance/options/{ticker}",
    "search": "/v1/finance/search",
    "recommendations": "/v6/finance/recommendationsbysymbol/{ticker}",
    "insights": "/ws/insights/v2/finance/insights",
    "market_summary": "/v6/finance/quote/marketSummary",
    "trending": "/v1/finance/trending/US",
    "currencies": "/v1/finance/currencies",
    "crumb": "/v1/test/getcrumb"
}

# Default API parameters
DEFAULT_PARAMS: Dict[str, str] = {
    'formatted': 'false',
    'region': 'US',
    'lang': 'en-US',
    'corsDomain': 'finance.yahoo.com',
}

# HTTP status codes for testing
HTTP_STATUS_CODES: Dict[str, int] = {
    "ok": 200,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "method_not_allowed": 405,
    "internal_server_error": 500,
    "bad_gateway": 502,
    "service_unavailable": 503,
    "gateway_timeout": 504
}

# Common error messages for testing
ERROR_MESSAGES: Dict[str, str] = {
    "invalid_ticker": "Invalid ticker symbol",
    "invalid_range": "Invalid range parameter",
    "invalid_interval": "Invalid interval parameter", 
    "invalid_events": "Invalid events parameter",
    "invalid_modules": "Invalid modules parameter",
    "invalid_frequency": "Invalid frequency parameter",
    "not_found": "No data found",
    "unauthorized": "Authentication required",
    "server_error": "Internal server error",
    "service_unavailable": "Service temporarily unavailable"
}

# Mock crumb values for testing
MOCK_CRUMBS: List[str] = [
    "mock_crumb_value_123",
    "test_crumb_456",
    "sample_crumb_789",
    "fake_crumb_abc",
    "demo_crumb_xyz"
]

# Test user agents
TEST_USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

# Sample financial data for testing calculations
SAMPLE_FINANCIAL_DATA: Dict[str, Any] = {
    "revenue": 365817000000,  # $365.82B
    "net_income": 94680000000,  # $94.68B
    "total_assets": 351002000000,  # $351.00B
    "total_debt": 124719000000,  # $124.72B
    "shares_outstanding": 16406400000,  # 16.41B shares
    "market_cap": 2913346560000,  # $2.91T
    "pe_ratio": 30.90,
    "dividend_yield": 0.0049,  # 0.49%
    "beta": 1.19
}

# Test portfolio data
TEST_PORTFOLIO: List[Dict[str, Any]] = [
    {"ticker": "AAPL", "shares": 100, "avg_cost": 150.00},
    {"ticker": "GOOGL", "shares": 50, "avg_cost": 2500.00},
    {"ticker": "MSFT", "shares": 75, "avg_cost": 300.00},
    {"ticker": "TSLA", "shares": 25, "avg_cost": 800.00}
]

# Currency pairs for testing
CURRENCY_PAIRS: List[str] = [
    "EURUSD=X",
    "GBPUSD=X", 
    "USDJPY=X",
    "USDCAD=X",
    "AUDUSD=X",
    "USDCHF=X",
    "NZDUSD=X",
    "EURGBP=X"
]

# Crypto symbols for testing
CRYPTO_SYMBOLS: List[str] = [
    "BTC-USD",
    "ETH-USD",
    "ADA-USD",
    "DOT-USD",
    "LINK-USD",
    "LTC-USD",
    "XRP-USD",
    "BCH-USD"
]

# Index symbols for testing
INDEX_SYMBOLS: List[str] = [
    "^GSPC",  # S&P 500
    "^DJI",   # Dow Jones
    "^IXIC",  # NASDAQ
    "^RUT",   # Russell 2000
    "^VIX",   # VIX
    "^TNX",   # 10-Year Treasury
    "^FTSE",  # FTSE 100
    "^N225"   # Nikkei 225
]

# ETF symbols for testing
ETF_SYMBOLS: List[str] = [
    "SPY",    # SPDR S&P 500
    "QQQ",    # Invesco QQQ
    "IWM",    # iShares Russell 2000
    "VTI",    # Vanguard Total Stock Market
    "VOO",    # Vanguard S&P 500
    "ARKK",   # ARK Innovation
    "GLD",    # SPDR Gold Shares
    "TLT"     # iShares 20+ Year Treasury
]