from typing import Any, Generator
import pytest

from yafin import Stonk
from yafin.const import FREQUENCIES

class TestStonk:
    """Tests for yafin.stonk module."""

    def test(self) -> None:
        pass

    @pytest.fixture
    def stonk(self) -> Generator[Stonk, None, None]:
        """Fixture for Stonk."""
        return Stonk('META')

    @pytest.mark.parametrize(
        'kwargs',
        [
            {'period_range': '1y', 'interval': '1d'},
            {'period_range': '5y', 'interval': '1wk'},
            {'period_range': 'ytd', 'interval': '1d', 'include_div': True, 'include_split': False},
            {'period_range': '1mo', 'interval': '1d', 'include_div': False, 'include_split': True},
            {'period_range': '5d', 'interval': '1h', 'include_div': True, 'include_split': True},
            {'period_range': '3mo', 'interval': '4h', 'include_div': True, 'include_split': True},
            {'period_range': '1y', 'interval': '1d', 'include_div': True, 'include_split': True},
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart(self, stonk: Stonk, kwargs: dict[str, Any]) -> None:
        """Test get_chart method."""
        chart = await stonk.get_chart(**kwargs)
        assert chart, 'Chart data does not exist.'

    @pytest.mark.asyncio
    async def test_get_quote(self, stonk: Stonk) -> None:
        """Test get_quote method."""
        quote = await stonk.get_quote()
        assert quote, 'Quote data does not exist.'

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(self, stonk: Stonk) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = await stonk.get_quote_summary_all_modules()
        assert quote_summary_all_modules, 'Quote summary with all modules data does not exist.'

    @pytest.mark.asyncio
    async def test_get_quote_type(self, stonk: Stonk) -> None:
        """Test get_quote_type method."""
        quote_type = await stonk.get_quote_type()
        assert quote_type, 'Quote type data does not exist.'

    @pytest.mark.asyncio
    async def test_get_asset_profile(self, stonk: Stonk) -> None:
        """Test get_asset_profile method."""
        asset_profile = await stonk.get_asset_profile()
        assert asset_profile, 'Asset profile data does not exist.'

    @pytest.mark.asyncio
    async def test_get_summary_profile(self, stonk: Stonk) -> None:
        """Test get_summary_profile method."""
        summary_profile = await stonk.get_summary_profile()
        assert summary_profile, 'Summary profile data does not exist.'

    @pytest.mark.asyncio
    async def test_get_summary_detail(self, stonk: Stonk) -> None:
        """Test get_summary_detail method."""
        summary_detail = await stonk.get_summary_detail()
        assert summary_detail, 'Summary detail data does not exist.'

    @pytest.mark.asyncio
    async def test_get_income_statement_history(self, stonk: Stonk) -> None:
        """Test get_income_statement_history method."""
        income_statement_history = await stonk.get_income_statement_history()
        assert income_statement_history, 'Income statement history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_income_statement_history_quarterly(self, stonk: Stonk) -> None:
        """Test get_income_statement_history_quarterly method."""
        income_statement_history_quarterly = await stonk.get_income_statement_history_quarterly()
        assert income_statement_history_quarterly, 'Income statement quarterly history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_balance_sheet_history(self, stonk: Stonk) -> None:
        """Test get_balance_sheet_history method."""
        balance_sheet_history = await stonk.get_balance_sheet_history()
        assert balance_sheet_history, 'Balance sheet history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_balance_sheet_history_quarterly(self, stonk: Stonk) -> None:
        """Test get_balance_sheet_history_quarterly method."""
        balance_sheet_history_quarterly = await stonk.get_balance_sheet_history_quarterly()
        assert balance_sheet_history_quarterly, 'Balance sheet quarterly history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_cashflow_statement_history(self, stonk: Stonk) -> None:
        """Test get_cashflow_statement_history method."""
        cashflow_statement_history = await stonk.get_cashflow_statement_history()
        assert cashflow_statement_history, 'Cash flow history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_cashflow_statement_history_quarterly(self, stonk: Stonk) -> None:
        """Test get_cashflow_statement_history_quarterly method."""
        cashflow_statement_history_quarterly = await stonk.get_cashflow_statement_history_quarterly()
        assert cashflow_statement_history_quarterly, 'Cash flow quarterly history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_esg_scores(self, stonk: Stonk) -> None:
        """Test get_esg_scores method."""
        esg_scores = await stonk.get_esg_scores()
        assert esg_scores, 'ESG scores does not exist.'

    @pytest.mark.asyncio
    async def test_get_price(self, stonk: Stonk) -> None:
        """Test get_price method."""
        price = await stonk.get_price()
        assert price, 'Price data does not exist.'

    @pytest.mark.asyncio
    async def test_get_default_key_statistics(self, stonk: Stonk) -> None:
        """Test get_default_key_statistics method."""
        default_key_statistics = await stonk.get_default_key_statistics()
        assert default_key_statistics, 'Default key statistics data does not exist.'

    @pytest.mark.asyncio
    async def test_get_financial_data(self, stonk: Stonk) -> None:
        """Test get_financial_data method."""
        financial_data = await stonk.get_financial_data()
        assert financial_data, 'Financial data does not exist.'

    @pytest.mark.asyncio
    async def test_get_calendar_events(self, stonk: Stonk) -> None:
        """Test get_calendar_events method."""
        calendar_events = await stonk.get_calendar_events()
        assert calendar_events, 'Calendat events does not exist.'

    @pytest.mark.asyncio
    async def test_get_sec_filings(self, stonk: Stonk) -> None:
        """Test get_sec_filings method."""
        sec_filings = await stonk.get_sec_filings()
        assert sec_filings, 'SEC filings does not exist.'

    @pytest.mark.asyncio
    async def test_get_upgrade_downgrade_history(self, stonk: Stonk) -> None:
        """Test get_upgrade_downgrade_history method."""
        upgrade_downgrade_history = await stonk.get_upgrade_downgrade_history()
        assert upgrade_downgrade_history, 'Upgrade downgrade history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_institution_ownership(self, stonk: Stonk) -> None:
        """Test get_institution_ownership method."""
        institution_ownership = await stonk.get_institution_ownership()
        assert institution_ownership, 'Institution ownership data does not exist.'

    @pytest.mark.asyncio
    async def test_get_fund_ownership(self, stonk: Stonk) -> None:
        """Test get_fund_ownership method."""
        fund_ownership = await stonk.get_fund_ownership()
        assert fund_ownership, 'Fund ownership data does not exist.'

    @pytest.mark.asyncio
    async def test_get_major_direct_holders(self, stonk: Stonk) -> None:
        """Test get_major_direct_holders method."""
        major_direct_holders = await stonk.get_major_direct_holders()
        assert major_direct_holders, 'Major direct holders data does not exist.'

    @pytest.mark.asyncio
    async def test_get_major_holders_breakdown(self, stonk: Stonk) -> None:
        """Test get_major_holders_breakdown method."""
        major_holders_breakdown = await stonk.get_major_holders_breakdown()
        assert major_holders_breakdown, 'Major holders breakdown data does not exist.'

    @pytest.mark.asyncio
    async def test_get_insider_transactions(self, stonk: Stonk) -> None:
        """Test get_insider_transactions method."""
        insider_transactions = await stonk.get_insider_transactions()
        assert insider_transactions, 'Insider transactions data does not exist.'

    @pytest.mark.asyncio
    async def test_get_insider_holders(self, stonk: Stonk) -> None:
        """Test get_insider_holders method."""
        insider_holders = await stonk.get_insider_holders()
        assert insider_holders, 'Insider holders data does not exist.'

    @pytest.mark.asyncio
    async def test_get_net_share_purchase_activity(self, stonk: Stonk) -> None:
        """Test get_net_share_purchase_activity method."""
        net_share_purchase_activity = await stonk.get_net_share_purchase_activity()
        assert net_share_purchase_activity, 'Net share purchase activity data does not exist.'

    @pytest.mark.asyncio
    async def test_get_earnings(self, stonk: Stonk) -> None:
        """Test get_earnings method."""
        earnings = await stonk.get_earnings()
        assert earnings, 'Earnings data does not exist.'

    @pytest.mark.asyncio
    async def test_get_earnings_history(self, stonk: Stonk) -> None:
        """Test get_earnings_history method."""
        earnings_history = await stonk.get_earnings_history()
        assert earnings_history, 'Earnings history data does not exist.'

    @pytest.mark.asyncio
    async def test_get_earnings_trend(self, stonk: Stonk) -> None:
        """Test get_earnings_trend method."""
        earnings_trend = await stonk.get_earnings_trend()
        assert earnings_trend, 'Earnings trend data does not exist.'

    @pytest.mark.asyncio
    async def test_get_industry_trend(self, stonk: Stonk) -> None:
        """Test get_industry_trend method."""
        industry_trend = await stonk.get_industry_trend()
        assert industry_trend, 'Industry trend data does not exist.'

    @pytest.mark.asyncio
    async def test_get_index_trend(self, stonk: Stonk) -> None:
        """Test get_index_trend method."""
        index_trend = await stonk.get_index_trend()
        assert index_trend, 'Index trend data does not exist.'

    @pytest.mark.asyncio
    async def test_get_sector_trend(self, stonk: Stonk) -> None:
        """Test get_sector_trend method."""
        sector_trend = await stonk.get_sector_trend()
        assert sector_trend, 'Sector trend data does not exist.'

    @pytest.mark.asyncio
    async def test_get_recommendation_trend(self, stonk: Stonk) -> None:
        """Test get_recommendation_trend method."""
        recommendation_trend = await stonk.get_recommendation_trend()
        assert recommendation_trend, 'Recommendation trend data does not exist.'

    @pytest.mark.asyncio
    async def test_get_page_views(self, stonk: Stonk) -> None:
        """Test get_page_views method."""
        page_views = await stonk.get_page_views()
        assert page_views, 'Page views data does not exist.'

    @pytest.mark.parametrize('frequency', FREQUENCIES)
    @pytest.mark.asyncio
    async def test_get_income_statement(self, stonk: Stonk, frequency: str, start_ts: float, end_ts: float) -> None:
        """Test get_income_statement method."""
        ttm_income_stmt = await stonk.get_income_statement(frequency, period1=start_ts, period2=end_ts)
        assert ttm_income_stmt, f'Income statement {frequency} data does not exist.'

    @pytest.mark.parametrize('frequency', ['annual', 'quarterly'])
    @pytest.mark.asyncio
    async def test_get_balance_sheet(self, stonk: Stonk, frequency: str) -> None:
        """Test get_balance_sheet method."""
        annual_balance_sheet = await stonk.get_balance_sheet(frequency)
        assert annual_balance_sheet, f'Balance sheet {frequency} data does not exist.'

    @pytest.mark.parametrize('frequency', FREQUENCIES)
    @pytest.mark.asyncio
    async def test_get_cash_flow(self, stonk: Stonk, frequency: str) -> None:
        """Test get_cash_flow method."""
        quarterly_cash_flow = await stonk.get_cash_flow(frequency)
        assert quarterly_cash_flow, f'Cash flow {frequency} data does not exist.'

    @pytest.mark.asyncio
    async def test_get_options(self, stonk: Stonk) -> None:
        """Test get_options method."""
        options = await stonk.get_options()
        assert options, 'Options data does not exist.'

    @pytest.mark.asyncio
    async def test_get_search(self, stonk: Stonk) -> None:
        """Test get_search method."""
        search = await stonk.get_search()
        assert search, 'Search data does not exist.'

    @pytest.mark.asyncio
    async def test_get_recommendations(self, stonk: Stonk) -> None:
        """Test get_recommendations method."""
        recommendations = await stonk.get_recommendations()
        assert recommendations, 'Recommendations data does not exist.'

    @pytest.mark.asyncio
    async def test_get_insights(self, stonk: Stonk) -> None:
        """Test get_insights method."""
        insights = await stonk.get_insights()
        assert insights, 'Insights data does not exist.'

