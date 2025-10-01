from typing import Any
from datetime import datetime

import pytest

from yafin import AsyncClient
from yafin.const import ALL_MODULES, QUOTE_KEYS, TYPES


class TestClient:
    """Tests for yafin.client module."""

    @pytest.fixture
    def client(self) -> AsyncClient:
        """Fixture for AsyncClient."""
        return AsyncClient()

    @pytest.mark.parametrize(
        'kwargs',
        [
            {'ticker': 'META', 'period_range': '1y', 'interval': '1d'},
            {'ticker': 'NVDA', 'period_range': '5y', 'interval': '1wk'},
            {
                'ticker': 'AAPL',
                'period_range': 'ytd',
                'interval': '1d',
                'events': 'div',
            },
            {
                'ticker': 'MSFT',
                'period_range': '1mo',
                'interval': '1d',
                'events': 'split',
            },
            {
                'ticker': 'AMZN',
                'period_range': '5d',
                'interval': '1h',
                'events': 'div,split',
            },
            {
                'ticker': 'GOOGL',
                'period_range': '3mo',
                'interval': '4h',
                'events': 'split,div',
            },
            {
                'ticker': 'TSLA',
                'period_range': '1y',
                'interval': '1d',
                'events': ' div, split ',
            },
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart(self, client: AsyncClient, kwargs: dict[str, Any]) -> None:
        """Test get_chart method."""
        ticker = kwargs['ticker']

        chart = await client.get_chart(**kwargs)
        assert chart, 'Chart data does not exist.'

        assert chart['meta']['symbol'] == ticker, (
            'Ticker does not match symbol in the chart data.'
        )
        assert chart['timestamp'], 'Timestamp not found in the chart data.'

        for key in ['high', 'low', 'close', 'volume', 'open']:
            assert key in chart['indicators']['quote'][0].keys(), (
                f'Key {key} not found in the chart data.'
            )

        if kwargs['interval'] in ['1d', '5d', '1wk', '1mo', '3mo']:
            assert chart['indicators']['adjclose'][0]['adjclose'], (
                'Key adjclose not found in the chart data. (Only valid for interval=1d)'
            )

    @pytest.mark.parametrize(
        'kwargs', [
            {'ticker': 'META', 'period_range': 'xxx', 'interval': '1d', 'events': 'div,split'},
            {'ticker': 'META', 'period_range': '1y', 'interval': 'xxx', 'events': 'div,split'},
            {'ticker': 'META', 'period_range': '1y', 'interval': '1d', 'events': 'xxx'},
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
    async def test_get_quote(self, client: AsyncClient) -> None:
        """Test get_quote method."""
        tickers = 'AAPL,META'

        quotes = await client.get_quote(tickers)
        assert quotes, 'Quote data does not exist.'

        assert len(quotes) == len(tickers.split(',')), (
            'Number of quotes does not match.'
        )

        sorted_quotes = sorted(quotes, key=lambda q: q['symbol'])

        for ticker, quote in zip(sorted(tickers.split(',')), sorted_quotes):
            assert ticker == quote['symbol'], (
                'Ticker does not match symbol in the chart data.'
            )

            for key in QUOTE_KEYS:
                assert key in quotes[0].keys(), (
                    f'Key {key} not found in the {quote["symbol"]} quote data.'
                )

    @pytest.mark.parametrize(
        'kwargs', [
            {'ticker': 'META', 'modules': 'assetProfile'},
            {'ticker': 'META', 'modules': 'assetProfile,price,defaultKeyStatistics,calendarEvents'},
            {'ticker': 'META', 'modules': ALL_MODULES}
        ]
    )
    @pytest.mark.asyncio
    async def test_get_quote_summary(self, client: AsyncClient, kwargs: dict[str, str]) -> None:
        """Test get_quote_summary method."""
        quote_summary = await client.get_quote_summary(**kwargs)
        assert quote_summary, 'Quote summary data does not exist.'

        for module in kwargs['modules'].split(','):
            assert module in quote_summary.keys(), (
                f'Key {module} not found in the quote summary data.'
            )

    @pytest.mark.asyncio
    async def test_get_quote_summary_invalid_args(self, client: AsyncClient) -> None:
        """Test get_quote_summary method with invalid arguments."""
        with pytest.raises(Exception):
            await client.get_timeseries(ticker='META', modules='xxx')

    @pytest.mark.parametrize(
        'kwargs', [
            {'ticker': 'META', 'types': ['trailingNetIncome', 'trailingPretaxIncome', 'trailingEBIT', 'trailingEBITDA', 'trailingGrossProfit'], 'period1': datetime(2020, 1, 1).timestamp(), 'period2': datetime.now().timestamp()},
            {'ticker': 'META', 'types': ['annualNetDebt', 'annualTotalDebt']},
            {'ticker': 'META', 'types': ['quarterlyFreeCashFlow', 'quarterlyOperatingCashFlow']}
        ],
    )
    @pytest.mark.asyncio
    async def test_get_timeseries(self, client: AsyncClient, kwargs: dict[str, Any]) -> None:
        """Test get_timeseries method."""

        timeseries = await client.get_timeseries(**kwargs)
        assert timeseries, f'Timeseries data does not exist.'

        for field in timeseries:
            field['meta']['symbol'][0] == kwargs['ticker'], (
                f'Ticker does not match symbol in the timeseries data.'
            )
        
        field_names = [field['meta']['type'][0] for field in timeseries]
        for typ in kwargs['types']:
            assert typ in field_names, (
                f'Type {typ} not found in the timeseries data.'
            )

    @pytest.mark.parametrize('kwargs', [{'ticker': 'META', 'types': ['trailingNetDebt', 'trailingTotalDebt']}])
    @pytest.mark.asyncio
    async def test_get_timeseries_invalid_args(self, client: AsyncClient, kwargs: dict[str, Any]) -> None:
        """Test get_timeseries method with invalid arguments."""
        with pytest.raises(Exception):
            await client.get_timeseries(**kwargs)


    @pytest.mark.asyncio
    async def test_get_options(self, client: AsyncClient) -> None:
        """Test get_options method."""
        ticker = 'META'

        options = await client.get_options(ticker)
        assert options, 'Options data does not exist.'

    @pytest.mark.asyncio
    async def test_get_search(self, client: AsyncClient) -> None:
        """Test get_search method."""
        ticker = 'META'

        search = await client.get_search(ticker)
        assert search, 'Search data does not exist.'

    @pytest.mark.asyncio
    async def test_get_recommendations(self, client: AsyncClient) -> None:
        """Test get_recommendations method."""
        ticker = 'META'

        recommendations = await client.get_recommendations(ticker)
        assert recommendations, 'Recommendations data does not exist.'

    @pytest.mark.asyncio
    async def test_get_insights(self, client: AsyncClient) -> None:
        """Test get_insights method."""
        ticker = 'META'

        insights = await client.get_insights(ticker)
        assert insights, 'Insights data does not exist.'

    @pytest.mark.asyncio
    async def test_get_market_summary(self, client: AsyncClient) -> None:
        """Test get_market_summary method."""
        market_summary = await client.get_market_summary()
        assert market_summary, 'Market summary data does not exist.'

    @pytest.mark.asyncio
    async def test_get_trending(self, client: AsyncClient) -> None:
        """Test get_trending method."""
        trending = await client.get_trending()
        assert trending, 'Trending data does not exist.'

    @pytest.mark.asyncio
    async def test_get_currencies(self, client: AsyncClient) -> None:
        """Test get_currencies method."""
        currencies = await client.get_currencies()
        assert currencies, 'Currencies data does not exist.'
