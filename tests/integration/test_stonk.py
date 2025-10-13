import pytest

from tests.assertions import (
    assert_annual_balance_sheet_result,
    assert_annual_cash_flow_result,
    assert_annual_income_stmt_result,
    assert_chart_result,
    assert_insights_result,
    assert_options_result,
    assert_quote_result,
    assert_quote_summary_all_modules_result,
    assert_recommendations_result,
    assert_search,
)
from yafin import Stonk


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
        assert_chart_result(chart, stonk.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, stonk: Stonk) -> None:
        """Test get_quote method."""
        quote = await stonk.get_quote()
        assert_quote_result(quote, stonk.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(self, stonk: Stonk) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = await stonk.get_quote_summary_all_modules()
        assert_quote_summary_all_modules_result(quote_summary_all_modules)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_income_statement(self, stonk: Stonk) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt = await stonk.get_income_statement(frequency)
        assert_annual_income_stmt_result(annual_income_stmt)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_balance_sheet(self, stonk: Stonk) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheet = await stonk.get_balance_sheet(frequency)
        assert_annual_balance_sheet_result(annual_balance_sheet)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_cash_flow(self, stonk: Stonk) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flow = await stonk.get_cash_flow(frequency)
        assert_annual_cash_flow_result(annual_cash_flow)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, stonk: Stonk) -> None:
        """Test get_options method."""
        options = await stonk.get_options()
        assert_options_result(options, stonk.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, stonk: Stonk) -> None:
        """Test get_search method."""
        search = await stonk.get_search()
        assert_search(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, stonk: Stonk) -> None:
        """Test get_recommendations method."""
        recommendations = await stonk.get_recommendations()
        assert_recommendations_result(recommendations, stonk.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, stonk: Stonk) -> None:
        """Test get_insights method."""
        insights = await stonk.get_insights()
        assert_insights_result(insights, stonk.ticker)
