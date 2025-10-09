from datetime import datetime
from typing import Any

import pytest
from curl_cffi.requests import Response
from curl_cffi.requests.exceptions import HTTPError
from pytest_mock import MockerFixture

from tests.const import SEARCH_KEYS
from tests.utils import assert_keys_exist
from yafin import AsyncClient
from yafin.const import ALL_MODULES
from yafin.utils import get_types_with_frequency


class TestUnitClient:
    """Tests for yafin.client module."""

    @pytest.fixture
    def client(self) -> AsyncClient:
        """Fixture for AsyncClient."""
        return AsyncClient()

    @pytest.mark.asyncio
    async def test_get_async_request(
        self,
        client: AsyncClient,
        mock_chart_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test _get_async_request method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_chart_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        url = 'https://query2.finance.yahoo.com/v8/finance/chart/META'
        params = {
            'formatted': 'false',
            'region': 'US',
            'lang': 'en-US',
            'corsDomain': 'finance.yahoo.com',
            'range': '1y',
            'interval': '1d',
            'events': 'div,split',
        }
        response = await client._get_async_request(url, params)
        assert response

    @pytest.mark.asyncio
    async def test_get_async_request_http_err(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
    ) -> None:
        """Test _get_async_request method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 404
        mock_response.json.return_value = {
            'quoteSummary': {
                'result': None,
                'error': {
                    'code': 'Not Found',
                    'description': 'Quote not found for symbol: XXXXXXXX',
                },
            }
        }
        mock_response.raise_for_status.side_effect = HTTPError(
            '404 Client Error: Not Found for url'
        )

        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        url = 'https://query2.finance.yahoo.com/v8/finance/chart/xxxxxxxx'
        params = {
            'formatted': 'false',
            'region': 'US',
            'lang': 'en-US',
            'corsDomain': 'finance.yahoo.com',
            'range': '1y',
            'interval': '1d',
            'events': 'div,split',
        }
        with pytest.raises(Exception):
            await client._get_async_request(url, params)

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(ticker='META', period_range='1y', interval='1d'),
            dict(ticker='META', period_range='1y', interval='1d', events='div,split'),
            dict(ticker='META', period_range='1y', interval='1d', events=' div,split '),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart(
        self,
        client: AsyncClient,
        kwargs: dict[str, str],
        mock_chart_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_chart method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_chart_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        chart = await client.get_chart(**kwargs)
        assert chart
        assert chart['chart']
        assert chart['chart']['error'] is None
        assert chart['chart']['result']
        assert chart['chart']['result'][0]['meta']['symbol'] == kwargs['ticker']

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(ticker='META', period_range='xxx', interval='1d', events='div,split'),
            dict(ticker='META', period_range='1y', interval='xxx', events='div,split'),
            dict(ticker='META', period_range='1y', interval='1d', events='xxx'),
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
    async def test_get_quote(
        self,
        client: AsyncClient,
        mock_quote_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_quote method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_quote_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        tickers = 'META'
        quotes = await client.get_quote(tickers)
        assert quotes
        assert quotes['quoteResponse']
        assert quotes['quoteResponse']['result']
        assert quotes['quoteResponse']['error'] is None
        tickers_list = tickers.split(',')
        assert len(quotes['quoteResponse']['result']) == len(tickers_list)
        quotes_tickers_list = [
            result['symbol'] for result in quotes['quoteResponse']['result']
        ]
        assert sorted(tickers_list) == sorted(quotes_tickers_list)

    @pytest.mark.asyncio
    async def test_get_quote_summary(
        self,
        client: AsyncClient,
        mock_quote_summary_all_modules_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_quote_summary method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_quote_summary_all_modules_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        ticker = 'META'
        modules = ALL_MODULES
        quote_summary = await client.get_quote_summary(ticker, modules)
        assert quote_summary
        assert quote_summary['quoteSummary']
        assert quote_summary['quoteSummary']['result']
        assert quote_summary['quoteSummary']['error'] is None
        modules_list = modules.split(',')
        quote_summary_keys = quote_summary['quoteSummary']['result'][0].keys()
        assert sorted(modules_list) == sorted(quote_summary_keys)

    @pytest.mark.asyncio
    async def test_get_quote_summary_invalid_args(self, client: AsyncClient) -> None:
        """Test get_quote_summary method with invalid arguments."""
        with pytest.raises(Exception):
            await client.get_quote_summary(ticker='META', modules='xxx')

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=datetime(2020, 1, 1).timestamp(),
                period2=datetime.now().timestamp(),
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=datetime(2020, 1, 1).timestamp(),
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period2=datetime.now().timestamp(),
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_timeseries(
        self,
        client: AsyncClient,
        kwargs: dict[str, Any],
        mock_timeseries_income_statement_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_timeseries method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_timeseries_income_statement_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        timeseries = await client.get_timeseries(**kwargs)
        assert timeseries
        assert timeseries['timeseries']
        assert timeseries['timeseries']['result']
        assert timeseries['timeseries']['error'] is None
        types_list = kwargs['types'].split(',')
        timeseries_types_list = [
            result['meta']['type'][0] for result in timeseries['timeseries']['result']
        ]
        assert sorted(types_list) == sorted(timeseries_types_list)

    @pytest.mark.asyncio
    async def test_get_timeseries_invalid_args(
        self,
        client: AsyncClient,
        mock_timeseries_income_statement_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_timeseries method with invalid arguments."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_timeseries_income_statement_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        with pytest.raises(Exception):
            await client.get_timeseries(ticker='META', types='xxx')

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        client: AsyncClient,
        mock_options_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_options method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_options_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        ticker = 'META'
        options = await client.get_options(ticker)
        assert options
        assert options['optionChain']
        assert options['optionChain']['result']
        assert options['optionChain']['error'] is None
        assert options['optionChain']['result'][0]['underlyingSymbol'] == ticker
        assert options['optionChain']['result'][0]['quote']['symbol'] == ticker

    @pytest.mark.asyncio
    async def test_get_search(
        self,
        client: AsyncClient,
        mock_search_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_search method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_search_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        search = await client.get_search(tickers='META')
        assert search
        assert_keys_exist(search, SEARCH_KEYS)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        client: AsyncClient,
        mock_recommendations_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_recommendations method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_recommendations_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        ticker = 'META'
        recommendations = await client.get_recommendations(ticker)
        assert recommendations
        assert recommendations['finance']
        assert recommendations['finance']['result']
        assert recommendations['finance']['error'] is None
        assert recommendations['finance']['result'][0]['symbol'] == ticker

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        client: AsyncClient,
        mock_insights_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_insights method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_insights_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        ticker = 'META'
        insights = await client.get_insights(ticker)
        assert insights
        assert insights['finance']
        assert insights['finance']['result']
        assert insights['finance']['error'] is None
        assert insights['finance']['result']['symbol'] == ticker

    @pytest.mark.asyncio
    async def test_get_market_summaries(
        self,
        client: AsyncClient,
        mock_market_summaries_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_market_summaries method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_market_summaries_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        market_summaries = await client.get_market_summaries()
        assert market_summaries
        assert market_summaries['marketSummaryResponse']
        assert market_summaries['marketSummaryResponse']['result']
        assert market_summaries['marketSummaryResponse']['error'] is None

    @pytest.mark.asyncio
    async def test_get_trending(
        self,
        client: AsyncClient,
        mock_trending_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_trending method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_trending_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        trending = await client.get_trending()
        assert trending
        assert trending['finance']
        assert trending['finance']['result']
        assert trending['finance']['error'] is None

    @pytest.mark.asyncio
    async def test_get_currencies(
        self,
        client: AsyncClient,
        mock_currencies_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_currencies method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_currencies_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        currencies = await client.get_currencies()
        assert currencies
        assert currencies['currencies']
        assert currencies['currencies']['result']
        assert currencies['currencies']['error'] is None
