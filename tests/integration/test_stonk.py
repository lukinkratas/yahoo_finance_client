import pytest

from tests.assertions import assert_contains_keys, assert_keys_are_not_none
from tests.const import (
    INSIGHTS_KEYS,
    OPTIONS_KEYS,
    QUOTE_KEYS,
    SEARCH_KEYS,
)
from yafin import Stonk
from yafin.const import ALL_MODULES
from yafin.utils import get_types_with_frequency


class TestUnitStonk:
    """Tests for yafin.stonk module."""

    @pytest.fixture
    def stonk(self) -> Stonk:
        """Fixture for Stonk."""
        return Stonk('META')

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(self, stonk: Stonk) -> None:
        """Test get_chart method."""
        chart = await stonk.get_chart(period_range='1y', interval='1d')
        assert chart
        assert_keys_are_not_none(chart, ['meta', 'timestamp', 'indicators'])
        assert chart['meta']['symbol'] == stonk.ticker
        assert_keys_are_not_none(
            chart['indicators']['quote'][0], ['open', 'close', 'volume', 'low', 'high']
        )
        assert chart['indicators']['adjclose'][0]['adjclose']

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, stonk: Stonk) -> None:
        """Test get_quote method."""
        quote = await stonk.get_quote()
        assert quote
        assert_contains_keys(quote, QUOTE_KEYS)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(self, stonk: Stonk) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = await stonk.get_quote_summary_all_modules()
        assert quote_summary_all_modules
        assert_keys_are_not_none(quote_summary_all_modules, ALL_MODULES.split(','))

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_income_statement(self, stonk: Stonk) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt = await stonk.get_income_statement(frequency)
        assert annual_income_stmt
        types = get_types_with_frequency(frequency, typ='income_statement')
        types_list = types.split(',')
        income_stmt_types = [field['meta']['type'][0] for field in annual_income_stmt]
        assert sorted(types_list) == sorted(income_stmt_types)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_balance_sheet(self, stonk: Stonk) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheet = await stonk.get_balance_sheet(frequency)
        assert annual_balance_sheet
        types = get_types_with_frequency(frequency, typ='balance_sheet')
        types_list = types.split(',')
        income_stmt_types = [field['meta']['type'][0] for field in annual_balance_sheet]
        assert sorted(types_list) == sorted(income_stmt_types)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_cash_flow(self, stonk: Stonk) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flow = await stonk.get_cash_flow(frequency)
        assert annual_cash_flow
        types = get_types_with_frequency(frequency, typ='cash_flow')
        types_list = types.split(',')
        income_stmt_types = [field['meta']['type'][0] for field in annual_cash_flow]
        assert sorted(types_list) == sorted(income_stmt_types)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, stonk: Stonk) -> None:
        """Test get_options method."""
        options = await stonk.get_options()
        assert options
        assert_contains_keys(options, OPTIONS_KEYS)
        assert options['underlyingSymbol'] == stonk.ticker

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, stonk: Stonk) -> None:
        """Test get_search method."""
        search = await stonk.get_search()
        assert search
        assert_contains_keys(search, SEARCH_KEYS)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, stonk: Stonk) -> None:
        """Test get_recommendations method."""
        recommendations = await stonk.get_recommendations()
        assert recommendations
        assert_contains_keys(recommendations, ['symbol', 'recommendedSymbols'])
        assert recommendations['symbol'] == stonk.ticker

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, stonk: Stonk) -> None:
        """Test get_insights method."""
        insights = await stonk.get_insights()
        assert insights
        assert_contains_keys(insights, INSIGHTS_KEYS)
        assert insights['symbol'] == stonk.ticker
