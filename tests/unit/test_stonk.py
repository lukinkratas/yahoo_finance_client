from datetime import datetime
from typing import Any

import pytest
from pytest_mock import MockerFixture

from tests.assertions import (
    assert_annual_balance_sheet_result,
    assert_annual_cash_flow_result,
    assert_annual_income_stmt_result,
    assert_asset_profile,
    assert_balance_sheet_history,
    assert_balance_sheet_history_quarterly,
    assert_calendar_events,
    assert_cashflow_statement_history,
    assert_cashflow_statement_history_quarterly,
    assert_chart_result,
    assert_default_key_statistics,
    assert_earnings,
    assert_earnings_history,
    assert_earnings_trend,
    assert_esg_scores,
    assert_financial_data,
    assert_fund_ownership,
    assert_income_statement_history,
    assert_income_statement_history_quarterly,
    assert_index_trend,
    assert_industry_trend,
    assert_insider_holders,
    assert_insider_transactions,
    assert_insights_result,
    assert_institution_ownership,
    assert_major_direct_holders,
    assert_major_holders_breakdown,
    assert_net_share_purchase_activity,
    assert_options_result,
    assert_page_views,
    assert_price,
    assert_quote_result,
    assert_quote_summary_all_modules_result,
    assert_quote_type,
    assert_recommendation_trend,
    assert_recommendations_result,
    assert_search,
    assert_sec_filings,
    assert_sector_trend,
    assert_summary_detail,
    assert_summary_profile,
    assert_upgrade_downgrade_history,
)
from tests.utils import mock_200_response
from yafin import Symbol


class TestUnitSymbol:
    """Unit tests for yafin.symbol module."""

    @pytest.fixture
    def symbol(self) -> Symbol:
        """Fixture for Symbol."""
        return Symbol('META')

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(period_range='1y', interval='1d'),
            dict(
                period_range='1y', interval='1d', include_div=True, include_split=True
            ),
            dict(period_range='1y', interval='1d', include_div=True),
            dict(period_range='1y', interval='1d', include_split=True),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart(
        self,
        symbol: Symbol,
        kwargs: dict[str, Any],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
    ) -> None:
        """Test get_chart method."""
        mock_200_response(mocker, chart_json_mock)
        chart = await symbol.get_chart(**kwargs)
        assert_chart_result(chart, symbol.ticker)

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(period_range='xxx', interval='1d', events='div,split'),
            dict(period_range='1y', interval='xxx', events='div,split'),
            dict(period_range='1y', interval='1d', events='xxx'),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self, symbol: Symbol, kwargs: dict[str, Any]
    ) -> None:
        """Test get_chart method with invalid arguments."""
        with pytest.raises(Exception):
            await symbol.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(
        self, symbol: Symbol, mocker: MockerFixture, quote_json_mock: dict[str, Any]
    ) -> None:
        """Test get_quote method."""
        mock_200_response(mocker, quote_json_mock)
        quote = await symbol.get_quote()
        assert_quote_result(quote, symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        mock_200_response(mocker, quote_summary_all_modules_json_mock)
        quote_summary_all_modules = await symbol.get_quote_summary_all_modules()
        assert_quote_summary_all_modules_result(quote_summary_all_modules)

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test _get_quote_summary_single_module method."""
        mock_200_response(mocker, asset_profile_json_mock)
        asset_profile = await symbol._get_quote_summary_single_module(
            module='assetProfile'
        )
        assert_asset_profile(asset_profile)

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module_invalid_args(
        self, symbol: Symbol
    ) -> None:
        """Test _get_quote_summary_single_module method with invalid arguments."""
        with pytest.raises(Exception):
            await symbol._get_quote_summary_single_module(module='xxx')

    @pytest.mark.asyncio
    async def test_get_quote_type(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_type method."""
        mock_200_response(mocker, quote_type_json_mock)
        quote_type = await symbol.get_quote_type()
        assert_quote_type(quote_type)

    @pytest.mark.asyncio
    async def test_get_asset_profile(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_asset_profile method."""
        mock_200_response(mocker, asset_profile_json_mock)
        asset_profile = await symbol.get_asset_profile()
        assert_asset_profile(asset_profile)

    @pytest.mark.asyncio
    async def test_get_summary_profile(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        summary_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_summary_profile method."""
        mock_200_response(mocker, summary_profile_json_mock)
        summary_profile = await symbol.get_summary_profile()
        assert_summary_profile(summary_profile)

    @pytest.mark.asyncio
    async def test_get_summary_detail(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        summary_detail_json_mock: dict[str, Any],
    ) -> None:
        """Test get_summary_detail method."""
        mock_200_response(mocker, summary_detail_json_mock)
        summary_detail = await symbol.get_summary_detail()
        assert_summary_detail(summary_detail)

    @pytest.mark.asyncio
    async def test_get_income_statement_history(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        income_statement_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_income_statement_history method."""
        mock_200_response(mocker, income_statement_history_json_mock)
        income_statement_history = await symbol.get_income_statement_history()
        assert_income_statement_history(income_statement_history)

    @pytest.mark.asyncio
    async def test_get_income_statement_history_quarterly(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        income_statement_history_quarterly_json_mock: dict[str, Any],
    ) -> None:
        """Test get_income_statement_history_quarterly method."""
        mock_200_response(mocker, income_statement_history_quarterly_json_mock)
        income_statement_history_quarterly = (
            await symbol.get_income_statement_history_quarterly()
        )
        assert_income_statement_history_quarterly(income_statement_history_quarterly)

    @pytest.mark.asyncio
    async def test_get_balance_sheet_history(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        balance_sheet_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_balance_sheet_history method."""
        mock_200_response(mocker, balance_sheet_history_json_mock)
        balance_sheet_history = await symbol.get_balance_sheet_history()
        assert_balance_sheet_history(balance_sheet_history)

    @pytest.mark.asyncio
    async def test_get_balance_sheet_history_quarterly(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        balance_sheet_history_quarterly_json_mock: dict[str, Any],
    ) -> None:
        """Test get_balance_sheet_history_quarterly method."""
        mock_200_response(mocker, balance_sheet_history_quarterly_json_mock)
        balance_sheet_history_quarterly = (
            await symbol.get_balance_sheet_history_quarterly()
        )
        assert_balance_sheet_history_quarterly(balance_sheet_history_quarterly)

    @pytest.mark.asyncio
    async def test_get_cashflow_statement_history(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        cashflow_statement_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_cashflow_statement_history method."""
        mock_200_response(mocker, cashflow_statement_history_json_mock)
        cashflow_statement_history = await symbol.get_cashflow_statement_history()
        assert_cashflow_statement_history(cashflow_statement_history)

    @pytest.mark.asyncio
    async def test_get_cashflow_statement_history_quarterly(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        cashflow_statement_history_quarterly_json_mock: dict[str, Any],
    ) -> None:
        """Test get_cashflow_statement_history_quarterly method."""
        mock_200_response(mocker, cashflow_statement_history_quarterly_json_mock)
        cashflow_statement_history_quarterly = (
            await symbol.get_cashflow_statement_history_quarterly()
        )
        assert_cashflow_statement_history_quarterly(
            cashflow_statement_history_quarterly
        )

    @pytest.mark.asyncio
    async def test_get_esg_scores(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        esg_scores_json_mock: dict[str, Any],
    ) -> None:
        """Test get_esg_scores method."""
        mock_200_response(mocker, esg_scores_json_mock)
        esg_scores = await symbol.get_esg_scores()
        assert_esg_scores(esg_scores)

    @pytest.mark.asyncio
    async def test_get_price(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        price_json_mock: dict[str, Any],
    ) -> None:
        """Test get_price method."""
        mock_200_response(mocker, price_json_mock)
        price = await symbol.get_price()
        assert_price(price)

    @pytest.mark.asyncio
    async def test_get_default_key_statistics(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        default_key_statistics_json_mock: dict[str, Any],
    ) -> None:
        """Test get_default_key_statistics method."""
        mock_200_response(mocker, default_key_statistics_json_mock)
        default_key_statistics = await symbol.get_default_key_statistics()
        assert_default_key_statistics(default_key_statistics)

    @pytest.mark.asyncio
    async def test_get_financial_data(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        financial_data_json_mock: dict[str, Any],
    ) -> None:
        """Test get_financial_data method."""
        mock_200_response(mocker, financial_data_json_mock)
        financial_data = await symbol.get_financial_data()
        assert_financial_data(financial_data)

    @pytest.mark.asyncio
    async def test_get_calendar_events(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        calendar_events_json_mock: dict[str, Any],
    ) -> None:
        """Test get_calendar_events method."""
        mock_200_response(mocker, calendar_events_json_mock)
        calendar_events = await symbol.get_calendar_events()
        assert_calendar_events(calendar_events)

    @pytest.mark.asyncio
    async def test_get_sec_filings(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        sec_filings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_sec_filings method."""
        mock_200_response(mocker, sec_filings_json_mock)
        sec_filings = await symbol.get_sec_filings()
        assert_sec_filings(sec_filings)

    @pytest.mark.asyncio
    async def test_get_upgrade_downgrade_history(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        upgrade_downgrade_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_upgrade_downgrade_history method."""
        mock_200_response(mocker, upgrade_downgrade_history_json_mock)
        upgrade_downgrade_history = await symbol.get_upgrade_downgrade_history()
        assert_upgrade_downgrade_history(upgrade_downgrade_history)

    @pytest.mark.asyncio
    async def test_get_institution_ownership(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        institution_ownership_json_mock: dict[str, Any],
    ) -> None:
        """Test get_institution_ownership method."""
        mock_200_response(mocker, institution_ownership_json_mock)
        institution_ownership = await symbol.get_institution_ownership()
        assert_institution_ownership(institution_ownership)

    @pytest.mark.asyncio
    async def test_get_fund_ownership(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        fund_ownership_json_mock: dict[str, Any],
    ) -> None:
        """Test get_fund_ownership method."""
        mock_200_response(mocker, fund_ownership_json_mock)
        fund_ownership = await symbol.get_fund_ownership()
        assert_fund_ownership(fund_ownership)

    @pytest.mark.asyncio
    async def test_get_major_direct_holders(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        major_direct_holders_json_mock: dict[str, Any],
    ) -> None:
        """Test get_major_direct_holders method."""
        mock_200_response(mocker, major_direct_holders_json_mock)
        major_direct_holders = await symbol.get_major_direct_holders()
        assert_major_direct_holders(major_direct_holders)

    @pytest.mark.asyncio
    async def test_get_major_holders_breakdown(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        major_holders_breakdown_json_mock: dict[str, Any],
    ) -> None:
        """Test get_major_holders_breakdown method."""
        mock_200_response(mocker, major_holders_breakdown_json_mock)
        major_holders_breakdown = await symbol.get_major_holders_breakdown()
        assert_major_holders_breakdown(major_holders_breakdown)

    @pytest.mark.asyncio
    async def test_get_insider_transactions(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        insider_transactions_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insider_transactions method."""
        mock_200_response(mocker, insider_transactions_json_mock)
        insider_transactions = await symbol.get_insider_transactions()
        assert_insider_transactions(insider_transactions)

    @pytest.mark.asyncio
    async def test_get_insider_holders(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        insider_holders_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insider_holders method."""
        mock_200_response(mocker, insider_holders_json_mock)
        insider_holders = await symbol.get_insider_holders()
        assert_insider_holders(insider_holders)

    @pytest.mark.asyncio
    async def test_get_net_share_purchase_activity(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        net_share_purchase_activity_json_mock: dict[str, Any],
    ) -> None:
        """Test get_net_share_purchase_activity method."""
        mock_200_response(mocker, net_share_purchase_activity_json_mock)
        net_share_purchase_activity = await symbol.get_net_share_purchase_activity()
        assert_net_share_purchase_activity(net_share_purchase_activity)

    @pytest.mark.asyncio
    async def test_get_earnings(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        earnings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings method."""
        mock_200_response(mocker, earnings_json_mock)
        earnings = await symbol.get_earnings()
        assert_earnings(earnings)

    @pytest.mark.asyncio
    async def test_get_earnings_history(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        earnings_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings_history method."""
        mock_200_response(mocker, earnings_history_json_mock)
        earnings_history = await symbol.get_earnings_history()
        assert_earnings_history(earnings_history)

    @pytest.mark.asyncio
    async def test_get_earnings_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        earnings_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings_trend method."""
        mock_200_response(mocker, earnings_trend_json_mock)
        earnings_trend = await symbol.get_earnings_trend()
        assert_earnings_trend(earnings_trend)

    @pytest.mark.asyncio
    async def test_get_industry_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        industry_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_industry_trend method."""
        mock_200_response(mocker, industry_trend_json_mock)
        industry_trend = await symbol.get_industry_trend()
        assert_industry_trend(industry_trend)

    @pytest.mark.asyncio
    async def test_get_index_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        index_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_index_trend method."""
        mock_200_response(mocker, index_trend_json_mock)
        index_trend = await symbol.get_index_trend()
        assert_index_trend(index_trend)

    @pytest.mark.asyncio
    async def test_get_sector_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        sector_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_sector_trend method."""
        mock_200_response(mocker, sector_trend_json_mock)
        sector_trend = await symbol.get_sector_trend()
        assert_sector_trend(sector_trend)

    @pytest.mark.asyncio
    async def test_get_recommendation_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        recommendation_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendation_trend method."""
        mock_200_response(mocker, recommendation_trend_json_mock)
        recommendation_trend = await symbol.get_recommendation_trend()
        assert_recommendation_trend(recommendation_trend)

    @pytest.mark.asyncio
    async def test_get_page_views(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        page_views_json_mock: dict[str, Any],
    ) -> None:
        """Test get_page_views method."""
        mock_200_response(mocker, page_views_json_mock)
        page_views = await symbol.get_page_views()
        assert_page_views(page_views)

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(frequency='annual'),
            dict(
                frequency='annual',
                period1=datetime(2020, 1, 1).timestamp(),
                period2=datetime.now().timestamp(),
            ),
            dict(frequency='annual', period1=datetime(2020, 1, 1).timestamp()),
            dict(frequency='annual', period2=datetime.now().timestamp()),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_income_statement(
        self,
        symbol: Symbol,
        kwargs: dict[str, Any],
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
    ) -> None:
        """Test get_income_statement method."""
        mock_200_response(mocker, timeseries_income_statement_json_mock)
        annual_income_stmt = await symbol.get_income_statement(**kwargs)
        assert_annual_income_stmt_result(annual_income_stmt)

    @pytest.mark.asyncio
    async def test_get_income_statement_invalid_args(self, symbol: Symbol) -> None:
        """Test get_income_statement method with invalid arguments.."""
        with pytest.raises(Exception):
            await symbol.get_income_statement(frequency='xxx')

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(frequency='annual'),
            dict(
                frequency='annual',
                period1=datetime(2020, 1, 1).timestamp(),
                period2=datetime.now().timestamp(),
            ),
            dict(frequency='annual', period1=datetime(2020, 1, 1).timestamp()),
            dict(frequency='annual', period2=datetime.now().timestamp()),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_balance_sheet(
        self,
        symbol: Symbol,
        kwargs: dict[str, Any],
        mocker: MockerFixture,
        timeseries_balance_sheet_json_mock: dict[str, Any],
    ) -> None:
        """Test get_balance_sheet method."""
        mock_200_response(mocker, timeseries_balance_sheet_json_mock)
        annual_balance_sheet = await symbol.get_balance_sheet(**kwargs)
        assert_annual_balance_sheet_result(annual_balance_sheet)

    @pytest.mark.asyncio
    async def test_get_balance_sheet_invalid_args(self, symbol: Symbol) -> None:
        """Test get_balance_sheet method."""
        with pytest.raises(Exception):
            await symbol.get_balance_sheet(frequency='trailing')

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(frequency='annual'),
            dict(
                frequency='annual',
                period1=datetime(2020, 1, 1).timestamp(),
                period2=datetime.now().timestamp(),
            ),
            dict(frequency='annual', period1=datetime(2020, 1, 1).timestamp()),
            dict(frequency='annual', period2=datetime.now().timestamp()),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_cash_flow(
        self,
        symbol: Symbol,
        kwargs: dict[str, Any],
        mocker: MockerFixture,
        timeseries_cash_flow_json_mock: dict[str, Any],
    ) -> None:
        """Test get_cash_flow method."""
        mock_200_response(mocker, timeseries_cash_flow_json_mock)
        annual_cash_flow = await symbol.get_cash_flow(**kwargs)
        assert_annual_cash_flow_result(annual_cash_flow)

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
    ) -> None:
        """Test get_options method."""
        mock_200_response(mocker, options_json_mock)
        options = await symbol.get_options()
        assert_options_result(options, symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_search(
        self, symbol: Symbol, mocker: MockerFixture, search_json_mock: dict[str, Any]
    ) -> None:
        """Test get_search method."""
        mock_200_response(mocker, search_json_mock)
        search = await symbol.get_search()
        assert_search(search)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        recommendations_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendations method."""
        mock_200_response(mocker, recommendations_json_mock)
        recommendations = await symbol.get_recommendations()
        assert_recommendations_result(recommendations, symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        mock_200_response(mocker, insights_json_mock)
        insights = await symbol.get_insights()
        assert_insights_result(insights, symbol.ticker)
