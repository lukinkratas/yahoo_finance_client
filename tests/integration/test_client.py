import pytest

from tests.assertions import assert_contains_keys
from tests.const import SEARCH_KEYS
from yafin import AsyncClient
from yafin.const import ALL_MODULES
from yafin.utils import get_types_with_frequency


class TestIntegrationClient:
    """Tests for yafin.client module."""

    @pytest.fixture
    def client(self) -> AsyncClient:
        """Fixture for AsyncClient."""
        return AsyncClient()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(self, client: AsyncClient) -> None:
        """Test get_chart method."""
        ticker = 'META'
        chart = await client.get_chart(ticker, period_range='1y', interval='1d')
        assert chart
        assert chart['chart']
        assert chart['chart']['error'] is None
        assert chart['chart']['result']
        assert chart['chart']['result'][0]['meta']['symbol'] == ticker

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, client: AsyncClient) -> None:
        """Test get_quote method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
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

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary(self, client: AsyncClient) -> None:
        """Test get_quote_summary method."""
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

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_timeseries(self, client: AsyncClient) -> None:
        """Test get_timeseries method."""
        types = get_types_with_frequency(frequency='annual', typ='income_statement')
        timeseries = await client.get_timeseries(ticker='META', types=types)
        assert timeseries
        assert timeseries['timeseries']
        assert timeseries['timeseries']['result']
        assert timeseries['timeseries']['error'] is None
        types_list = types.split(',')
        timeseries_types_list = [
            result['meta']['type'][0] for result in timeseries['timeseries']['result']
        ]
        assert sorted(types_list) == sorted(timeseries_types_list)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, client: AsyncClient) -> None:
        """Test get_options method."""
        ticker = 'META'
        options = await client.get_options(ticker)
        assert options
        assert options['optionChain']
        assert options['optionChain']['result']
        assert options['optionChain']['error'] is None
        assert options['optionChain']['result'][0]['underlyingSymbol'] == ticker
        assert options['optionChain']['result'][0]['quote']['symbol'] == ticker

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, client: AsyncClient) -> None:
        """Test get_search method."""
        search = await client.get_search(tickers='META')
        assert search
        assert_contains_keys(search, SEARCH_KEYS)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, client: AsyncClient) -> None:
        """Test get_recommendations method."""
        ticker = 'META'
        recommendations = await client.get_recommendations(ticker)
        assert recommendations
        assert recommendations['finance']
        assert recommendations['finance']['result']
        assert recommendations['finance']['error'] is None
        assert recommendations['finance']['result'][0]['symbol'] == ticker

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, client: AsyncClient) -> None:
        """Test get_insights method."""
        ticker = 'META'
        insights = await client.get_insights(ticker)
        assert insights
        assert insights['finance']
        assert insights['finance']['result']
        assert insights['finance']['error'] is None
        assert insights['finance']['result']['symbol'] == ticker

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_market_summaries(self, client: AsyncClient) -> None:
        """Test get_market_summaries method."""
        market_summaries = await client.get_market_summaries()
        assert market_summaries
        assert market_summaries['marketSummaryResponse']
        assert market_summaries['marketSummaryResponse']['result']
        assert market_summaries['marketSummaryResponse']['error'] is None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_trending(self, client: AsyncClient) -> None:
        """Test get_trending method."""
        trending = await client.get_trending()
        assert trending
        assert trending['finance']
        assert trending['finance']['result']
        assert trending['finance']['error'] is None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_currencies(self, client: AsyncClient) -> None:
        """Test get_currencies method."""
        currencies = await client.get_currencies()
        assert currencies
        assert currencies['currencies']
        assert currencies['currencies']['result']
        assert currencies['currencies']['error'] is None
