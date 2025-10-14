from datetime import datetime
from typing import Any

import pytest
from pytest_mock import MockerFixture

from tests.assertions import (
    assert_annual_income_stmt_result,
    assert_chart_result,
    assert_currencies_result,
    assert_insights_result,
    assert_market_summaries_result,
    assert_options_result,
    assert_quote_summary_all_modules_result,
    assert_quotes,
    assert_recommendations_result,
    assert_response_json,
    assert_search,
    assert_trending_result,
)
from tests.utils import mock_200_response, mock_404_response
from yafin import AsyncClient
from yafin.const import ALL_MODULES
from yafin.utils import get_types_with_frequency


class TestUnitClient:
    """Unit tests for yafin.client module."""

    @pytest.fixture
    def client(self) -> AsyncClient:
        """Fixture for AsyncClient."""
        return AsyncClient()

    @pytest.mark.asyncio
    async def test_get_async_request(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
    ) -> None:
        """Test _get_async_request method."""
        mock_200_response(mocker, chart_json_mock)
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
        mock_404_response(
            mocker,
            {
                'quoteSummary': {
                    'result': None,
                    'error': {
                        'code': 'Not Found',
                        'description': 'Quote not found for symbol: XXXXXXXX',
                    },
                }
            },
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
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
    ) -> None:
        """Test get_chart method."""
        mock_200_response(mocker, chart_json_mock)
        chart = await client.get_chart(**kwargs)
        assert_response_json(chart, 'chart')
        assert_chart_result(chart['chart']['result'][0], kwargs['ticker'])

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
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote method."""
        mock_200_response(mocker, quote_json_mock)
        tickers = 'META'
        quotes = await client.get_quote(tickers)
        assert_response_json(quotes, 'quoteResponse')
        assert_quotes(quotes, tickers)

    @pytest.mark.asyncio
    async def test_get_quote_summary(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_summary method."""
        mock_200_response(mocker, quote_summary_all_modules_json_mock)
        ticker = 'META'
        modules = ALL_MODULES
        quote_summary = await client.get_quote_summary(ticker, modules)
        assert_response_json(quote_summary, 'quoteSummary')
        assert_quote_summary_all_modules_result(
            quote_summary['quoteSummary']['result'][0]
        )

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
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
    ) -> None:
        """Test get_timeseries method."""
        mock_200_response(mocker, timeseries_income_statement_json_mock)
        timeseries = await client.get_timeseries(**kwargs)
        assert_response_json(timeseries, 'timeseries')
        assert_annual_income_stmt_result(timeseries['timeseries']['result'])

    @pytest.mark.asyncio
    async def test_get_timeseries_invalid_args(self, client: AsyncClient) -> None:
        """Test get_timeseries method with invalid arguments."""
        with pytest.raises(Exception):
            await client.get_timeseries(ticker='META', types='xxx')

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
    ) -> None:
        """Test get_options method."""
        mock_200_response(mocker, options_json_mock)
        ticker = 'META'
        options = await client.get_options(ticker)
        assert_response_json(options, 'optionChain')
        assert_options_result(options['optionChain']['result'][0], ticker)

    @pytest.mark.asyncio
    async def test_get_search(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
    ) -> None:
        """Test get_search method."""
        mock_200_response(mocker, search_json_mock)
        search = await client.get_search(tickers='META')
        assert_search(search)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        client: AsyncClient,
        recommendations_json_mock: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_recommendations method."""
        mock_200_response(mocker, recommendations_json_mock)
        ticker = 'META'
        recommendations = await client.get_recommendations(ticker)
        assert_response_json(recommendations, 'finance')
        assert_recommendations_result(recommendations['finance']['result'][0], ticker)

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        mock_200_response(mocker, insights_json_mock)
        ticker = 'META'
        insights = await client.get_insights(ticker)
        assert_response_json(insights, 'finance')
        assert_insights_result(insights['finance']['result'], ticker)

    @pytest.mark.asyncio
    async def test_get_market_summaries(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        market_summaries_json_mock: dict[str, Any],
    ) -> None:
        """Test get_market_summaries method."""
        mock_200_response(mocker, market_summaries_json_mock)
        market_summaries = await client.get_market_summaries()
        assert_response_json(market_summaries, 'marketSummaryResponse')
        assert_market_summaries_result(
            market_summaries['marketSummaryResponse']['result']
        )

    @pytest.mark.asyncio
    async def test_get_trending(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        trending_json_mock: dict[str, Any],
    ) -> None:
        """Test get_trending method."""
        mock_200_response(mocker, trending_json_mock)
        trending = await client.get_trending()
        assert_response_json(trending, 'finance')
        assert_trending_result(trending['finance']['result'][0])

    @pytest.mark.asyncio
    async def test_get_currencies(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        currencies_json_mock: dict[str, Any],
    ) -> None:
        """Test get_currencies method."""
        mock_200_response(mocker, currencies_json_mock)
        currencies = await client.get_currencies()
        assert_response_json(currencies, 'currencies')
        assert_currencies_result(currencies['currencies']['result'])
