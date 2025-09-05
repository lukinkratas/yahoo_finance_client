"""Mock API response data for Yahoo Finance endpoints."""

from typing import Any, Dict, List


# Chart endpoint responses
CHART_SUCCESS_RESPONSE: Dict[str, Any] = {
    "chart": {
        "result": [{
            "meta": {
                "currency": "USD",
                "symbol": "AAPL",
                "exchangeName": "NMS",
                "instrumentType": "EQUITY",
                "firstTradeDate": 345479400,
                "regularMarketTime": 1640995200,
                "gmtoffset": -18000,
                "timezone": "EST",
                "exchangeTimezoneName": "America/New_York",
                "regularMarketPrice": 177.57,
                "chartPreviousClose": 179.38,
                "previousClose": 179.38,
                "scale": 3,
                "priceHint": 2,
                "dataGranularity": "1d",
                "range": "1d",
                "validRanges": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
            },
            "timestamp": [1640970000, 1640973600, 1640977200, 1640980800],
            "indicators": {
                "quote": [{
                    "open": [182.01, 181.50, 180.25, 179.00],
                    "high": [182.88, 182.00, 181.00, 180.50],
                    "low": [177.71, 179.50, 178.75, 177.50],
                    "close": [177.57, 180.00, 179.25, 178.00],
                    "volume": [59773000, 45000000, 38000000, 42000000]
                }],
                "adjclose": [{
                    "adjclose": [177.57, 180.00, 179.25, 178.00]
                }]
            },
            "events": {
                "dividends": {
                    "1635422400": {
                        "amount": 0.22,
                        "date": 1635422400
                    }
                },
                "splits": {
                    "1598284800": {
                        "date": 1598284800,
                        "numerator": 4,
                        "denominator": 1,
                        "splitRatio": "4:1"
                    }
                }
            }
        }],
        "error": None
    }
}

CHART_ERROR_RESPONSE: Dict[str, Any] = {
    "chart": {
        "result": None,
        "error": {
            "code": "Not Found",
            "description": "No data found, symbol may be delisted"
        }
    }
}

# Quote endpoint responses
QUOTE_SUCCESS_RESPONSE: Dict[str, Any] = {
    "quoteResponse": {
        "result": [{
            "language": "en-US",
            "region": "US",
            "quoteType": "EQUITY",
            "typeDisp": "Equity",
            "quoteSourceName": "Nasdaq Real Time Price",
            "triggerable": True,
            "customPriceAlertConfidence": "HIGH",
            "currency": "USD",
            "marketState": "CLOSED",
            "regularMarketChangePercent": -1.0089464,
            "regularMarketPrice": 177.57,
            "exchange": "NMS",
            "shortName": "Apple Inc.",
            "longName": "Apple Inc.",
            "messageBoardId": "finmb_24937",
            "exchangeTimezoneName": "America/New_York",
            "exchangeTimezoneShortName": "EST",
            "gmtOffSetMilliseconds": -18000000,
            "market": "us_market",
            "esgPopulated": False,
            "firstTradeDateMilliseconds": 345479400000,
            "priceHint": 2,
            "regularMarketChange": -1.8099976,
            "regularMarketTime": 1640995200,
            "regularMarketDayHigh": 182.88,
            "regularMarketDayRange": "177.71 - 182.88",
            "regularMarketDayLow": 177.71,
            "regularMarketVolume": 59773000,
            "regularMarketPreviousClose": 179.38,
            "bid": 177.50,
            "ask": 177.60,
            "bidSize": 8,
            "askSize": 12,
            "fullExchangeName": "NasdaqGS",
            "financialCurrency": "USD",
            "regularMarketOpen": 182.01,
            "averageDailyVolume3Month": 85589533,
            "averageDailyVolume10Day": 88071540,
            "fiftyTwoWeekLowChange": 58.57001,
            "fiftyTwoWeekLowChangePercent": 0.49218756,
            "fiftyTwoWeekRange": "119.0 - 182.94",
            "fiftyTwoWeekHighChange": -5.3699951,
            "fiftyTwoWeekHighChangePercent": -0.029350281,
            "fiftyTwoWeekLow": 119.0,
            "fiftyTwoWeekHigh": 182.94,
            "dividendDate": 1636588800,
            "earningsTimestamp": 1635451200,
            "earningsTimestampStart": 1643659200,
            "earningsTimestampEnd": 1644004800,
            "trailingAnnualDividendRate": 0.88,
            "trailingAnnualDividendYield": 0.004906542,
            "trailingPE": 30.901785,
            "dividendRate": 0.88,
            "dividendYield": 0.004906542,
            "epsTrailingTwelveMonths": 5.745,
            "epsForward": 6.56,
            "epsCurrentYear": 5.67,
            "priceEpsCurrentYear": 31.322751,
            "sharesOutstanding": 16406400000,
            "bookValue": 4.146,
            "fiftyDayAverage": 156.69,
            "fiftyDayAverageChange": 20.880005,
            "fiftyDayAverageChangePercent": 0.13327394,
            "twoHundredDayAverage": 147.76,
            "twoHundredDayAverageChange": 29.809998,
            "twoHundredDayAverageChangePercent": 0.20175438,
            "marketCap": 2913346560000,
            "forwardPE": 27.073475,
            "priceToBook": 42.83524,
            "sourceInterval": 15,
            "exchangeDataDelayedBy": 0,
            "averageAnalystRating": "2.0 - Buy",
            "tradeable": False,
            "cryptoTradeable": False,
            "symbol": "AAPL"
        }],
        "error": None
    }
}

QUOTE_ERROR_RESPONSE: Dict[str, Any] = {
    "quoteResponse": {
        "result": [],
        "error": {
            "code": "Not Found",
            "description": "No data found for symbols"
        }
    }
}
# Quote Summary endpoint responses
QUOTE_SUMMARY_SUCCESS_RESPONSE: Dict[str, Any] = {
    "quoteSummary": {
        "result": [{
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
            },
            "assetProfile": {
                "address1": "One Apple Park Way",
                "city": "Cupertino",
                "state": "CA",
                "zip": "95014",
                "country": "United States",
                "phone": "408 996 1010",
                "website": "https://www.apple.com",
                "industry": "Consumer Electronics",
                "industryKey": "consumer-electronics",
                "industryDisp": "Consumer Electronics",
                "sector": "Technology",
                "sectorKey": "technology",
                "sectorDisp": "Technology",
                "longBusinessSummary": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.",
                "fullTimeEmployees": 154000,
                "auditRisk": 4,
                "boardRisk": 1,
                "compensationRisk": 5,
                "shareHolderRightsRisk": 1,
                "overallRisk": 1,
                "governanceEpochDate": 1640995200,
                "compensationAsOfEpochDate": 1640995200,
                "maxAge": 86400
            },
            "summaryDetail": {
                "priceHint": {"raw": 2, "fmt": "2", "longFmt": "2"},
                "previousClose": {"raw": 179.38, "fmt": "179.38"},
                "open": {"raw": 182.01, "fmt": "182.01"},
                "dayLow": {"raw": 177.71, "fmt": "177.71"},
                "dayHigh": {"raw": 182.88, "fmt": "182.88"},
                "regularMarketPreviousClose": {"raw": 179.38, "fmt": "179.38"},
                "regularMarketOpen": {"raw": 182.01, "fmt": "182.01"},
                "regularMarketDayLow": {"raw": 177.71, "fmt": "177.71"},
                "regularMarketDayHigh": {"raw": 182.88, "fmt": "182.88"},
                "dividendRate": {"raw": 0.88, "fmt": "0.88"},
                "dividendYield": {"raw": 0.004906542, "fmt": "0.49%"},
                "exDividendDate": {"raw": 1636588800, "fmt": "2021-11-11"},
                "payoutRatio": {"raw": 0.1531, "fmt": "15.31%"},
                "fiveYearAvgDividendYield": {"raw": 1.30, "fmt": "1.30"},
                "beta": {"raw": 1.185463, "fmt": "1.19"},
                "trailingPE": {"raw": 30.901785, "fmt": "30.90"},
                "forwardPE": {"raw": 27.073475, "fmt": "27.07"},
                "volume": {"raw": 59773000, "fmt": "59.77M", "longFmt": "59,773,000"},
                "regularMarketVolume": {"raw": 59773000, "fmt": "59.77M", "longFmt": "59,773,000"},
                "averageVolume": {"raw": 85589533, "fmt": "85.59M", "longFmt": "85,589,533"},
                "averageVolume10days": {"raw": 88071540, "fmt": "88.07M", "longFmt": "88,071,540"},
                "averageDailyVolume10Day": {"raw": 88071540, "fmt": "88.07M", "longFmt": "88,071,540"},
                "bid": {"raw": 177.50, "fmt": "177.50"},
                "ask": {"raw": 177.60, "fmt": "177.60"},
                "bidSize": {"raw": 800, "fmt": "800", "longFmt": "800"},
                "askSize": {"raw": 1200, "fmt": "1.2k", "longFmt": "1,200"},
                "marketCap": {"raw": 2913346560000, "fmt": "2.91T", "longFmt": "2,913,346,560,000"},
                "fiftyTwoWeekLow": {"raw": 119.0, "fmt": "119.00"},
                "fiftyTwoWeekHigh": {"raw": 182.94, "fmt": "182.94"},
                "priceToSalesTrailing12Months": {"raw": 7.9, "fmt": "7.90"},
                "fiftyDayAverage": {"raw": 156.69, "fmt": "156.69"},
                "twoHundredDayAverage": {"raw": 147.76, "fmt": "147.76"},
                "currency": "USD",
                "fromCurrency": None,
                "toCurrency": None,
                "lastMarket": None,
                "algorithm": None,
                "tradeable": False
            }
        }],
        "error": None
    }
}

QUOTE_SUMMARY_ERROR_RESPONSE: Dict[str, Any] = {
    "quoteSummary": {
        "result": None,
        "error": {
            "code": "Not Found",
            "description": "Quote not found for ticker symbol"
        }
    }
}

# Timeseries endpoint responses
TIMESERIES_SUCCESS_RESPONSE: Dict[str, Any] = {
    "timeseries": {
        "result": [{
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
                },
                {
                    "asOfDate": "2020-09-26",
                    "periodType": "12M",
                    "currencyCode": "USD",
                    "reportedValue": {"raw": 57411000000, "fmt": "57.41B"}
                }
            ]
        }],
        "error": None
    }
}

TIMESERIES_ERROR_RESPONSE: Dict[str, Any] = {
    "timeseries": {
        "result": None,
        "error": {
            "code": "Not Found",
            "description": "No timeseries data found"
        }
    }
}

# Options endpoint responses
OPTIONS_SUCCESS_RESPONSE: Dict[str, Any] = {
    "optionChain": {
        "result": [{
            "underlyingSymbol": "AAPL",
            "expirationDates": [1642204800, 1642809600, 1643414400],
            "strikes": [170.0, 175.0, 180.0, 185.0, 190.0],
            "hasMiniOptions": False,
            "quote": {
                "language": "en-US",
                "region": "US",
                "quoteType": "EQUITY",
                "typeDisp": "Equity",
                "quoteSourceName": "Nasdaq Real Time Price",
                "triggerable": True,
                "currency": "USD",
                "regularMarketPrice": 177.57,
                "exchange": "NMS",
                "shortName": "Apple Inc.",
                "longName": "Apple Inc.",
                "symbol": "AAPL"
            },
            "options": [{
                "expirationDate": 1642204800,
                "hasMiniOptions": False,
                "calls": [{
                    "contractSymbol": "AAPL220114C00170000",
                    "strike": 170.0,
                    "currency": "USD",
                    "lastPrice": 8.25,
                    "change": 0.15,
                    "percentChange": 1.85,
                    "volume": 1250,
                    "openInterest": 5432,
                    "bid": 8.20,
                    "ask": 8.30,
                    "contractSize": "REGULAR",
                    "expiration": 1642204800,
                    "lastTradeDate": 1640995200,
                    "impliedVolatility": 0.28,
                    "inTheMoney": True
                }],
                "puts": [{
                    "contractSymbol": "AAPL220114P00170000",
                    "strike": 170.0,
                    "currency": "USD",
                    "lastPrice": 1.25,
                    "change": -0.05,
                    "percentChange": -3.85,
                    "volume": 850,
                    "openInterest": 3210,
                    "bid": 1.20,
                    "ask": 1.30,
                    "contractSize": "REGULAR",
                    "expiration": 1642204800,
                    "lastTradeDate": 1640995200,
                    "impliedVolatility": 0.25,
                    "inTheMoney": False
                }]
            }]
        }],
        "error": None
    }
}

OPTIONS_ERROR_RESPONSE: Dict[str, Any] = {
    "optionChain": {
        "result": None,
        "error": {
            "code": "Not Found",
            "description": "No options data found"
        }
    }
}

# Search endpoint responses
SEARCH_SUCCESS_RESPONSE: Dict[str, Any] = {
    "explains": [],
    "count": 1,
    "quotes": [{
        "exchange": "NMS",
        "shortname": "Apple Inc.",
        "quoteType": "EQUITY",
        "symbol": "AAPL",
        "index": "quotes",
        "score": 1000000.0,
        "typeDisp": "Equity",
        "longname": "Apple Inc.",
        "exchDisp": "NASDAQ",
        "sector": "Technology",
        "sectorDisp": "Technology",
        "industry": "Consumer Electronics",
        "industryDisp": "Consumer Electronics",
        "isYahooFinance": True
    }],
    "news": [],
    "nav": [],
    "lists": [],
    "researchReports": [],
    "screenerFieldResults": [],
    "totalTime": 12,
    "timeTakenForQuotes": 400,
    "timeTakenForNews": 0,
    "timeTakenForAlgowatchlist": 400,
    "timeTakenForPredefinedScreener": 400,
    "timeTakenForCrunchbase": 400,
    "timeTakenForNav": 400,
    "timeTakenForResearchReports": 0,
    "timeTakenForScreenerField": 400,
    "timeTakenForCulturalAssets": 400
}

SEARCH_ERROR_RESPONSE: Dict[str, Any] = {
    "explains": [],
    "count": 0,
    "quotes": [],
    "news": [],
    "nav": [],
    "lists": [],
    "researchReports": [],
    "screenerFieldResults": [],
    "totalTime": 8,
    "timeTakenForQuotes": 400,
    "timeTakenForNews": 0,
    "timeTakenForAlgowatchlist": 400,
    "timeTakenForPredefinedScreener": 400,
    "timeTakenForCrunchbase": 400,
    "timeTakenForNav": 400,
    "timeTakenForResearchReports": 0,
    "timeTakenForScreenerField": 400,
    "timeTakenForCulturalAssets": 400
}

# Recommendations endpoint responses
RECOMMENDATIONS_SUCCESS_RESPONSE: Dict[str, Any] = {
    "finance": {
        "result": [{
            "symbol": "AAPL",
            "recommendedSymbols": [
                {"symbol": "MSFT", "score": 0.234567},
                {"symbol": "GOOGL", "score": 0.198765},
                {"symbol": "AMZN", "score": 0.187654}
            ]
        }],
        "error": None
    }
}

RECOMMENDATIONS_ERROR_RESPONSE: Dict[str, Any] = {
    "finance": {
        "result": None,
        "error": {
            "code": "Not Found",
            "description": "No recommendations found"
        }
    }
}

# Insights endpoint responses
INSIGHTS_SUCCESS_RESPONSE: Dict[str, Any] = {
    "finance": {
        "result": {
            "symbol": "AAPL",
            "instrumentInfo": {
                "technicalEvents": {
                    "provider": "Trading Central",
                    "sector": "Technology",
                    "shortTermOutlook": {
                        "stateDescription": "Strong Bullish",
                        "direction": "Bullish",
                        "score": 4,
                        "scoreDescription": "Strong Bullish signals based on technical analysis",
                        "indexTimestamp": 1640995200,
                        "stateExpiry": 1641081600
                    },
                    "intermediateTermOutlook": {
                        "stateDescription": "Bullish",
                        "direction": "Bullish",
                        "score": 3,
                        "scoreDescription": "Bullish signals based on technical analysis",
                        "indexTimestamp": 1640995200,
                        "stateExpiry": 1641686400
                    }
                },
                "keyTechnicals": {
                    "provider": "Trading Central",
                    "support": 175.50,
                    "resistance": 185.00,
                    "stopLoss": 170.00
                },
                "valuation": {
                    "provider": "Trading Central",
                    "description": "Overvalued",
                    "discount": "-15%",
                    "relativeValue": "Premium"
                }
            },
            "companySnapshot": {
                "sectorInfo": "Technology",
                "company": {
                    "innovativeness": 0.9990,
                    "sustainability": 0.7234,
                    "insiderSentiments": 0.6543,
                    "earningsReports": {
                        "earningsDate": 1643659200,
                        "epsActual": 2.10,
                        "epsEstimate": 1.89,
                        "epsSurprise": 0.21,
                        "epsSurprisePercent": 11.11
                    }
                }
            }
        },
        "error": None
    }
}

INSIGHTS_ERROR_RESPONSE: Dict[str, Any] = {
    "finance": {
        "result": None,
        "error": {
            "code": "Not Found",
            "description": "No insights found"
        }
    }
}

# Market Summary endpoint responses
MARKET_SUMMARY_SUCCESS_RESPONSE: Dict[str, Any] = {
    "marketSummaryResponse": {
        "result": [{
            "language": "en-US",
            "region": "US",
            "quoteType": "INDEX",
            "typeDisp": "Index",
            "quoteSourceName": "Delayed Quote",
            "triggerable": False,
            "currency": "USD",
            "exchange": "SNP",
            "shortName": "S&P 500",
            "longName": "S&P 500",
            "messageBoardId": "finmb_5563713",
            "exchangeTimezoneName": "America/New_York",
            "exchangeTimezoneShortName": "EST",
            "gmtOffSetMilliseconds": -18000000,
            "market": "us_market",
            "esgPopulated": False,
            "firstTradeDateMilliseconds": -252322200000,
            "priceHint": 2,
            "regularMarketChange": 65.64001,
            "regularMarketChangePercent": 1.3848957,
            "regularMarketTime": 1640995200,
            "regularMarketPrice": 4808.93,
            "regularMarketDayHigh": 4818.62,
            "regularMarketDayRange": "4783.35 - 4818.62",
            "regularMarketDayLow": 4783.35,
            "regularMarketVolume": 0,
            "regularMarketPreviousClose": 4743.29,
            "fullExchangeName": "SNP",
            "regularMarketOpen": 4791.19,
            "sourceInterval": 15,
            "exchangeDataDelayedBy": 0,
            "tradeable": False,
            "cryptoTradeable": False,
            "symbol": "^GSPC"
        }],
        "error": None
    }
}

MARKET_SUMMARY_ERROR_RESPONSE: Dict[str, Any] = {
    "marketSummaryResponse": {
        "result": [],
        "error": {
            "code": "Internal Error",
            "description": "Market summary data unavailable"
        }
    }
}

# Trending endpoint responses
TRENDING_SUCCESS_RESPONSE: Dict[str, Any] = {
    "finance": {
        "result": [{
            "count": 5,
            "quotes": [
                {"symbol": "AAPL"},
                {"symbol": "TSLA"},
                {"symbol": "MSFT"},
                {"symbol": "GOOGL"},
                {"symbol": "AMZN"}
            ],
            "jobTimestamp": 1640995200,
            "startInterval": 1640995200
        }],
        "error": None
    }
}

TRENDING_ERROR_RESPONSE: Dict[str, Any] = {
    "finance": {
        "result": None,
        "error": {
            "code": "Internal Error",
            "description": "Trending data unavailable"
        }
    }
}

# Currencies endpoint responses
CURRENCIES_SUCCESS_RESPONSE: Dict[str, Any] = {
    "currencies": {
        "result": [
            {"id": "USD=X", "fullName": "USD/USD", "symbol": "USD=X"},
            {"id": "EURUSD=X", "fullName": "EUR/USD", "symbol": "EURUSD=X"},
            {"id": "GBPUSD=X", "fullName": "GBP/USD", "symbol": "GBPUSD=X"}
        ],
        "error": None
    }
}

CURRENCIES_ERROR_RESPONSE: Dict[str, Any] = {
    "currencies": {
        "result": [],
        "error": {
            "code": "Internal Error",
            "description": "Currency data unavailable"
        }
    }
}

# HTTP Error responses
HTTP_401_ERROR: Dict[str, Any] = {
    "error": {
        "code": "Unauthorized",
        "description": "Authentication required"
    }
}

HTTP_404_ERROR: Dict[str, Any] = {
    "error": {
        "code": "Not Found",
        "description": "The requested resource was not found"
    }
}

HTTP_500_ERROR: Dict[str, Any] = {
    "error": {
        "code": "Internal Server Error",
        "description": "An internal server error occurred"
    }
}

HTTP_503_ERROR: Dict[str, Any] = {
    "error": {
        "code": "Service Unavailable",
        "description": "Service temporarily unavailable"
    }
}

# Malformed response examples
MALFORMED_JSON_RESPONSE: str = '{"chart": {"result": [{"meta": {"symbol": "AAPL"'  # Incomplete JSON

MISSING_RESULT_RESPONSE: Dict[str, Any] = {
    "chart": {
        "error": None
        # Missing "result" key
    }
}

MISSING_ERROR_RESPONSE: Dict[str, Any] = {
    "chart": {
        "result": None
        # Missing "error" key
    }
}

# Crumb response
CRUMB_SUCCESS_RESPONSE: str = "mock_crumb_value_123"
CRUMB_ERROR_RESPONSE: str = ""
