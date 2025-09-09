from typing import Generator

import pytest
from pytest_mock import MockerFixture
from curl_cffi.requests import Response

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
        mock_response_json = {
            'chart': {
                'result': [
                    {
                        'meta': {
                            'currency': 'USD',
                            'symbol': 'META',
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
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        chart = await client.get_chart(
            ticker='AAPL', period_range='1y', interval='1d', events='div,split'
        )

        assert chart, 'Chart does not exist.'
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
        # mock_get.assert_awaited_once_with(expected_url, params=expected_params)
        # assert chart['meta']['symbol'] == 'META'
        # assert isinstance(chart['timestamp'], list) and len(chart['timestamp']) > 0
        # test invalid options
