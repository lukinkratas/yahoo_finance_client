from typing import Generator

import pytest
from curl_cffi.requests import Response
from pytest_mock import MockerFixture

from yafin import AsyncClient


class TestClient:
    """Tests for yafin.client module."""

    @pytest.fixture
    def client(self) -> Generator[AsyncClient, None, None]:
        """Fixture for AsyncClient."""
        yield AsyncClient()

    @pytest.mark.asyncio
    async def test_get_chart(self, client: AsyncClient, mocker: MockerFixture) -> None:
        """Test get_chart method."""
        ticker = 'META'
        mock_response_json = {
            'chart': {
                'result': [
                    {
                        'meta': {
                            'currency': 'USD',
                            'symbol': ticker,
                            'exchangeName': 'NMS',
                            'fullExchangeName': 'NasdaqGS',
                            'instrumentType': 'EQUITY',
                            'firstTradeDate': 1337347800,
                            'regularMarketTime': 1757098884,
                            'hasPrePostMarketData': True,
                            'gmtoffset': -14400,
                            'timezone': 'EDT',
                            'exchangeTimezoneName': 'America/New_York',
                            'regularMarketPrice': 752.93,
                            'fiftyTwoWeekHigh': 796.25,
                            'fiftyTwoWeekLow': 479.8,
                            'regularMarketDayHigh': 757.92,
                            'regularMarketDayLow': 745.03,
                            'regularMarketVolume': 6966814,
                            'longName': 'Meta Platforms, Inc.',
                            'shortName': 'Meta Platforms, Inc.',
                            'chartPreviousClose': 763.46,
                            'priceHint': 2,
                            'currentTradingPeriod': {
                                'pre': {
                                    'timezone': 'EDT',
                                    'start': 1757059200,
                                    'end': 1757079000,
                                    'gmtoffset': -14400,
                                },
                                'regular': {
                                    'timezone': 'EDT',
                                    'start': 1757079000,
                                    'end': 1757102400,
                                    'gmtoffset': -14400,
                                },
                                'post': {
                                    'timezone': 'EDT',
                                    'start': 1757102400,
                                    'end': 1757116800,
                                    'gmtoffset': -14400,
                                },
                            },
                            'dataGranularity': '1d',
                            'range': '1mo',
                            'validRanges': [
                                '1d',
                                '5d',
                                '1mo',
                                '3mo',
                                '6mo',
                                '1y',
                                '2y',
                                '5y',
                                '10y',
                                'ytd',
                                'max',
                            ],
                        },
                        'timestamp': [
                            1754400600,
                            1754487000,
                            1754573400,
                            1754659800,
                            1754919000,
                            1755005400,
                            1755091800,
                            1755178200,
                            1755264600,
                            1755523800,
                            1755610200,
                            1755696600,
                            1755783000,
                            1755869400,
                            1756128600,
                            1756215000,
                            1756301400,
                            1756387800,
                            1756474200,
                            1756819800,
                            1756906200,
                            1756992600,
                            1757098884,
                        ],
                        'indicators': {
                            'quote': [
                                {
                                    'high': [
                                        783.1300048828125,
                                        773.6400146484375,
                                        775.0,
                                        769.9000244140625,
                                        773.4600219726562,
                                        793.6699829101562,
                                        795.4600219726562,
                                        787.8099975585938,
                                        796.25,
                                        775.8099975585938,
                                        767.1699829101562,
                                        750.2000122070312,
                                        745.5,
                                        756.9000244140625,
                                        758.8800048828125,
                                        754.8699951171875,
                                        754.1500244140625,
                                        753.0499877929688,
                                        747.1400146484375,
                                        736.0,
                                        740.25,
                                        761.1599731445312,
                                        757.9199829101562,
                                    ],
                                    'close': [
                                        763.4600219726562,
                                        771.989990234375,
                                        761.8300170898438,
                                        769.2999877929688,
                                        765.8699951171875,
                                        790.0,
                                        780.0800170898438,
                                        782.1300048828125,
                                        785.22998046875,
                                        767.3699951171875,
                                        751.47998046875,
                                        747.719970703125,
                                        739.0999755859375,
                                        754.7899780273438,
                                        753.2999877929688,
                                        754.0999755859375,
                                        747.3800048828125,
                                        751.1099853515625,
                                        738.7000122070312,
                                        735.1099853515625,
                                        737.0499877929688,
                                        748.6500244140625,
                                        752.9299926757812,
                                    ],
                                    'volume': [
                                        11640300,
                                        9733900,
                                        9019700,
                                        7320800,
                                        7612000,
                                        14563100,
                                        8811800,
                                        8116200,
                                        13375400,
                                        16513700,
                                        12286700,
                                        11898200,
                                        8876300,
                                        10612700,
                                        6861200,
                                        7601800,
                                        8315400,
                                        7468000,
                                        9070500,
                                        9350900,
                                        7699300,
                                        11421700,
                                        6966814,
                                    ],
                                    'low': [
                                        763.0,
                                        760.4600219726562,
                                        759.5499877929688,
                                        758.5800170898438,
                                        764.6699829101562,
                                        772.4299926757812,
                                        778.22998046875,
                                        772.510009765625,
                                        780.8200073242188,
                                        756.5599975585938,
                                        749.3599853515625,
                                        731.0,
                                        733.1099853515625,
                                        734.3900146484375,
                                        750.1300048828125,
                                        747.9400024414062,
                                        742.8400268554688,
                                        740.7999877929688,
                                        735.3499755859375,
                                        721.72998046875,
                                        733.989990234375,
                                        745.8200073242188,
                                        745.030029296875,
                                    ],
                                    'open': [
                                        776.4500122070312,
                                        770.0,
                                        773.489990234375,
                                        762.75,
                                        770.0800170898438,
                                        773.0,
                                        791.1500244140625,
                                        777.8800048828125,
                                        784.1500244140625,
                                        775.0900268554688,
                                        767.1199951171875,
                                        747.5700073242188,
                                        744.7100219726562,
                                        739.22998046875,
                                        754.8200073242188,
                                        750.7999877929688,
                                        752.2999877929688,
                                        744.0,
                                        745.280029296875,
                                        726.0399780273438,
                                        736.0,
                                        748.5700073242188,
                                        752.614990234375,
                                    ],
                                }
                            ],
                            'adjclose': [
                                {
                                    'adjclose': [
                                        763.4600219726562,
                                        771.989990234375,
                                        761.8300170898438,
                                        769.2999877929688,
                                        765.8699951171875,
                                        790.0,
                                        780.0800170898438,
                                        782.1300048828125,
                                        785.22998046875,
                                        767.3699951171875,
                                        751.47998046875,
                                        747.719970703125,
                                        739.0999755859375,
                                        754.7899780273438,
                                        753.2999877929688,
                                        754.0999755859375,
                                        747.3800048828125,
                                        751.1099853515625,
                                        738.7000122070312,
                                        735.1099853515625,
                                        737.0499877929688,
                                        748.6500244140625,
                                        752.9299926757812,
                                    ]
                                }
                            ],
                        },
                    }
                ],
                'error': None,
            }
        }
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        chart = await client.get_chart(
            ticker='AAPL', period_range='1y', interval='1d', events='div,split'
        )

        assert chart, 'Chart does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

        assert chart[ticker.lower()], 'Ticker data does not exist.'
        assert chart[ticker.lower()]['symbol'] == ticker, (
            'Ticker symbol does not match.'
        )
        assert chart['timestamp'], 'Timestamp data does not exist.'
        assert chart['indicators']['quote'][0]['high'], 'High data does not exist.'
        assert chart['indicators']['quote'][0]['low'], 'Low data does not exist.'
        assert chart['indicators']['quote'][0]['close'], 'Close data does not exist.'
        assert chart['indicators']['quote'][0]['volume'], 'Volume data does not exist.'
        assert chart['indicators']['quote'][0]['open'], 'Open data does not exist.'
        assert chart['indicators']['adjclose'][0]['adjclose'], (
            'Adjclose data does not exist.'
        )

    @pytest.mark.parametrize(
        'kwargs',
        [
            {
                'ticker': 'META',
                'period_range': 'xxx',
                'interval': '1d',
                'events': 'div,split',
            },
            {
                'ticker': 'META',
                'period_range': '1y',
                'interval': 'xxx',
                'events': 'div,split',
            },
            {'ticker': 'META', 'period_range': '1y', 'interval': '7d', 'events': 'xxx'},
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self, client: AsyncClient, kwargs: dict[str, str]
    ) -> None:
        """Test get_chart method with invalid arguments."""
        with pytest.raises(Exception):
            await client.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(self, client: AsyncClient, mocker: MockerFixture) -> None:
        """Test get_quote method."""
        tickers = 'AAPL,META'
        mock_response_json = {
            'quoteResponse': {
                'result': [
                    {
                        'language': 'en-US',
                        'region': 'US',
                        'quoteType': 'EQUITY',
                        'typeDisp': 'Equity',
                        'quoteSourceName': 'Nasdaq Real Time Price',
                        'triggerable': True,
                        'customPriceAlertConfidence': 'HIGH',
                        'currency': 'USD',
                        'corporateActions': [],
                        'exchange': 'NMS',
                        'messageBoardId': 'finmb_20765463',
                        'exchangeTimezoneName': 'America/New_York',
                        'exchangeTimezoneShortName': 'EDT',
                        'gmtOffSetMilliseconds': -14400000,
                        'market': 'us_market',
                        'esgPopulated': False,
                        'priceHint': 2,
                        'postMarketChangePercent': 0.226071,
                        'postMarketTime': 1757548792,
                        'regularMarketTime': 1757534401,
                        'shortName': 'Meta Platforms, Inc.',
                        'longName': 'Meta Platforms, Inc.',
                        'hasPrePostMarketData': True,
                        'firstTradeDateMilliseconds': 1337347800000,
                        'postMarketPrice': 753.68,
                        'postMarketChange': 1.70001,
                        'regularMarketChange': -13.72,
                        'regularMarketDayHigh': 765.7,
                        'regularMarketDayRange': '751.0 - 765.7',
                        'regularMarketDayLow': 751.0,
                        'regularMarketVolume': 11675543,
                        'regularMarketPreviousClose': 765.7,
                        'bid': 751.9,
                        'ask': 790.02,
                        'bidSize': 1,
                        'askSize': 1,
                        'fullExchangeName': 'NasdaqGS',
                        'financialCurrency': 'USD',
                        'regularMarketOpen': 765.01,
                        'averageDailyVolume3Month': 11736962,
                        'averageDailyVolume10Day': 9955760,
                        'fiftyTwoWeekLowChange': 272.18,
                        'fiftyTwoWeekLowChangePercent': 0.567278,
                        'fiftyTwoWeekRange': '479.8 - 796.25',
                        'fiftyTwoWeekHighChange': -44.27002,
                        'fiftyTwoWeekHighChangePercent': -0.05559814,
                        'fiftyTwoWeekLow': 479.8,
                        'fiftyTwoWeekHigh': 796.25,
                        'fiftyTwoWeekChangePercent': 43.07078,
                        'dividendDate': 1750896000,
                        'earningsTimestamp': 1753905600,
                        'earningsTimestampStart': 1761768000,
                        'earningsTimestampEnd': 1761768000,
                        'earningsCallTimestampStart': 1753909200,
                        'earningsCallTimestampEnd': 1753909200,
                        'isEarningsDateEstimate': True,
                        'trailingAnnualDividendRate': 2.05,
                        'trailingPE': 27.324854,
                        'dividendRate': 2.1,
                        'trailingAnnualDividendYield': 0.0026772886,
                        'dividendYield': 0.28,
                        'epsTrailingTwelveMonths': 27.52,
                        'epsForward': 25.3,
                        'epsCurrentYear': 27.851,
                        'marketState': 'PREPRE',
                        'regularMarketChangePercent': -1.79183,
                        'regularMarketPrice': 751.98,
                        'priceEpsCurrentYear': 27.000107,
                        'sharesOutstanding': 2168960000,
                        'bookValue': 77.532,
                        'fiftyDayAverage': 739.9588,
                        'fiftyDayAverageChange': 12.021179,
                        'fiftyDayAverageChangePercent': 0.016245741,
                        'twoHundredDayAverage': 653.8399,
                        'twoHundredDayAverageChange': 98.140076,
                        'twoHundredDayAverageChangePercent': 0.15009803,
                        'marketCap': 1889079001088,
                        'forwardPE': 29.72253,
                        'priceToBook': 9.698963,
                        'sourceInterval': 15,
                        'exchangeDataDelayedBy': 0,
                        'ipoExpectedDate': '2022-06-09',
                        'averageAnalystRating': '1.4 - Strong Buy',
                        'tradeable': False,
                        'cryptoTradeable': False,
                        'displayName': 'Meta Platforms',
                        'symbol': 'META',
                    },
                    {
                        'language': 'en-US',
                        'region': 'US',
                        'quoteType': 'EQUITY',
                        'typeDisp': 'Equity',
                        'quoteSourceName': 'Nasdaq Real Time Price',
                        'triggerable': True,
                        'customPriceAlertConfidence': 'HIGH',
                        'currency': 'USD',
                        'corporateActions': [],
                        'exchange': 'NMS',
                        'messageBoardId': 'finmb_24937',
                        'exchangeTimezoneName': 'America/New_York',
                        'exchangeTimezoneShortName': 'EDT',
                        'gmtOffSetMilliseconds': -14400000,
                        'market': 'us_market',
                        'esgPopulated': False,
                        'priceHint': 2,
                        'postMarketChangePercent': 0.101945,
                        'postMarketTime': 1757548798,
                        'regularMarketTime': 1757534401,
                        'shortName': 'Apple Inc.',
                        'longName': 'Apple Inc.',
                        'hasPrePostMarketData': True,
                        'firstTradeDateMilliseconds': 345479400000,
                        'postMarketPrice': 227.021,
                        'postMarketChange': 0.231201,
                        'regularMarketChange': -7.56001,
                        'regularMarketDayHigh': 232.34,
                        'regularMarketDayRange': '225.9522 - 232.34',
                        'regularMarketDayLow': 225.9522,
                        'regularMarketVolume': 80814115,
                        'regularMarketPreviousClose': 234.35,
                        'bid': 226.71,
                        'ask': 226.85,
                        'bidSize': 2,
                        'askSize': 2,
                        'fullExchangeName': 'NasdaqGS',
                        'financialCurrency': 'USD',
                        'regularMarketOpen': 232.025,
                        'averageDailyVolume3Month': 54747006,
                        'averageDailyVolume10Day': 52031080,
                        'fiftyTwoWeekLowChange': 57.579987,
                        'fiftyTwoWeekLowChangePercent': 0.34028712,
                        'fiftyTwoWeekRange': '169.21 - 260.1',
                        'fiftyTwoWeekHighChange': -33.310013,
                        'fiftyTwoWeekHighChangePercent': -0.12806617,
                        'fiftyTwoWeekLow': 169.21,
                        'fiftyTwoWeekHigh': 260.1,
                        'fiftyTwoWeekChangePercent': 1.8045545,
                        'dividendDate': 1755129600,
                        'earningsTimestamp': 1753992000,
                        'earningsTimestampStart': 1761854400,
                        'earningsTimestampEnd': 1761854400,
                        'earningsCallTimestampStart': 1753995600,
                        'earningsCallTimestampEnd': 1753995600,
                        'isEarningsDateEstimate': True,
                        'trailingAnnualDividendRate': 1.01,
                        'trailingPE': 34.36212,
                        'dividendRate': 1.04,
                        'trailingAnnualDividendYield': 0.004309793,
                        'dividendYield': 0.46,
                        'epsTrailingTwelveMonths': 6.6,
                        'epsForward': 8.31,
                        'epsCurrentYear': 7.38411,
                        'marketState': 'PREPRE',
                        'regularMarketChangePercent': -3.22595,
                        'regularMarketPrice': 226.79,
                        'priceEpsCurrentYear': 30.713247,
                        'sharesOutstanding': 14840399872,
                        'bookValue': 4.431,
                        'fiftyDayAverage': 220.249,
                        'fiftyDayAverageChange': 6.5410004,
                        'fiftyDayAverageChangePercent': 0.029698208,
                        'twoHundredDayAverage': 221.4848,
                        'twoHundredDayAverageChange': 5.305191,
                        'twoHundredDayAverageChangePercent': 0.023952845,
                        'marketCap': 3365654233088,
                        'forwardPE': 27.291214,
                        'priceToBook': 51.18257,
                        'sourceInterval': 15,
                        'exchangeDataDelayedBy': 0,
                        'averageAnalystRating': '2.0 - Buy',
                        'tradeable': False,
                        'cryptoTradeable': False,
                        'displayName': 'Apple',
                        'symbol': 'AAPL',
                    },
                ],
                'error': None,
            }
        }

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        finance_quote = await client.get_quote(tickers)

        assert finance_quote, 'Finance quote does not exist.'
        assert len(finance_quote) == len(tickers.split(',')), (
            'Number of quotes does not match.'
        )

        symbols = [quote['symbol'] for quote in finance_quote]
        for ticker in tickers.split(','):
            assert ticker in symbols, f'Ticker {ticker} not found in quotes.'
