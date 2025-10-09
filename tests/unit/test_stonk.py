from datetime import datetime
from typing import Any

import pytest
from curl_cffi.requests import Response
from pytest_mock import MockerFixture

from tests.const import (
    ASSET_PROFILE_KEYS,
    CALENDAR_EVENTS_EARNING_KEYS,
    DEFAULT_KEY_STATISTICS_KEYS,
    EARNINGS_HISTORY_KEYS,
    EARNINGS_TREND_KEYS,
    ESG_SCORES_KEYS,
    FINANCIAL_DATA_KEYS,
    HOLDER_KEYS,
    INCOME_STATEMENT_HISTORY_KEYS,
    INSIGHTS_KEYS,
    MAJOR_HOLDERS_BREAKDOWN_KEYS,
    NET_SHARE_PURCHASE_ACIVITY_KEYS,
    OPTIONS_KEYS,
    OWNERSHIP_KEYS,
    PRICE_KEYS,
    QUOTE_KEYS,
    QUOTE_TYPE_KEYS,
    RECOMMENDATIONS_TREND_KEYS,
    SEARCH_KEYS,
    SEC_FILING_KEYS,
    SUMMARY_DETAIL_KEYS,
    SUMMARY_PROFILE_KEYS,
    TRANSACTION_KEYS,
    UPGRADE_DOWNGRADE_HISTORY_KEYS,
)
from tests.utils import assert_keys_are_not_none, assert_keys_exist
from yafin import Stonk
from yafin.const import ALL_MODULES
from yafin.utils import get_types_with_frequency


class TestUnitStonk:
    """Tests for yafin.stonk module."""

    @pytest.fixture
    def stonk(self) -> Stonk:
        """Fixture for Stonk."""
        return Stonk('META')

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
        stonk: Stonk,
        kwargs: dict[str, Any],
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

        chart = await stonk.get_chart(**kwargs)
        assert chart
        assert_keys_are_not_none(chart, ['meta', 'timestamp', 'indicators'])
        assert chart['meta']['symbol'] == stonk.ticker
        assert_keys_are_not_none(
            chart['indicators']['quote'][0], ['open', 'close', 'volume', 'low', 'high']
        )
        assert chart['indicators']['adjclose'][0]['adjclose']

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
        self, stonk: Stonk, kwargs: dict[str, Any]
    ) -> None:
        """Test get_chart method with invalid arguments."""
        with pytest.raises(Exception):
            await stonk.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(
        self, stonk: Stonk, mock_quote_json: dict[str, Any], mocker: MockerFixture
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

        quote = await stonk.get_quote()
        assert quote
        assert_keys_exist(quote, QUOTE_KEYS)

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(
        self,
        stonk: Stonk,
        mock_quote_summary_all_modules_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_quote_summary_all_modules_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        quote_summary_all_modules = await stonk.get_quote_summary_all_modules()
        assert quote_summary_all_modules
        assert_keys_are_not_none(quote_summary_all_modules, ALL_MODULES.split(','))

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module(
        self,
        stonk: Stonk,
        mock_asset_profile_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test _get_quote_summary_single_module method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_asset_profile_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        asset_profile = await stonk._get_quote_summary_single_module(
            module='assetProfile'
        )
        assert asset_profile
        assert_keys_exist(asset_profile, ASSET_PROFILE_KEYS)

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module_invalid_args(
        self, stonk: Stonk
    ) -> None:
        """Test _get_quote_summary_single_module method with invalid arguments."""
        with pytest.raises(Exception):
            await stonk._get_quote_summary_single_module(module='xxx')

    @pytest.mark.asyncio
    async def test_get_quote_type(
        self,
        stonk: Stonk,
        mock_quote_type_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_quote_type method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_quote_type_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        quote_type = await stonk.get_quote_type()
        assert quote_type
        assert_keys_exist(quote_type, QUOTE_TYPE_KEYS)

    @pytest.mark.asyncio
    async def test_get_asset_profile(
        self,
        stonk: Stonk,
        mock_asset_profile_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_asset_profile method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_asset_profile_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        asset_profile = await stonk.get_asset_profile()
        assert asset_profile
        assert_keys_exist(asset_profile, ASSET_PROFILE_KEYS)

    @pytest.mark.asyncio
    async def test_get_summary_profile(
        self,
        stonk: Stonk,
        mock_summary_profile_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_summary_profile method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_summary_profile_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        summary_profile = await stonk.get_summary_profile()
        assert summary_profile
        assert_keys_exist(summary_profile, SUMMARY_PROFILE_KEYS)

    @pytest.mark.asyncio
    async def test_get_summary_detail(
        self,
        stonk: Stonk,
        mock_summary_detail_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_summary_detail method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_summary_detail_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        summary_detail = await stonk.get_summary_detail()
        assert summary_detail
        assert_keys_exist(summary_detail, SUMMARY_DETAIL_KEYS)

    @pytest.mark.asyncio
    async def test_get_income_statement_history(
        self,
        stonk: Stonk,
        mock_income_statement_history_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_income_statement_history method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_income_statement_history_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        income_statement_history = await stonk.get_income_statement_history()
        assert income_statement_history
        for period in income_statement_history:
            assert_keys_exist(period, INCOME_STATEMENT_HISTORY_KEYS)

    @pytest.mark.asyncio
    async def test_get_income_statement_history_quarterly(
        self,
        stonk: Stonk,
        mock_income_statement_history_quarterly_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_income_statement_history_quarterly method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_income_statement_history_quarterly_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        income_statement_history_quarterly = (
            await stonk.get_income_statement_history_quarterly()
        )
        assert income_statement_history_quarterly
        for period in income_statement_history_quarterly:
            assert_keys_exist(period, INCOME_STATEMENT_HISTORY_KEYS)

    @pytest.mark.asyncio
    async def test_get_balance_sheet_history(
        self,
        stonk: Stonk,
        mock_balance_sheet_history_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_balance_sheet_history method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_balance_sheet_history_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        balance_sheet_history = await stonk.get_balance_sheet_history()
        assert balance_sheet_history
        for period in balance_sheet_history:
            assert_keys_exist(period, ['maxAge', 'endDate'])

    @pytest.mark.asyncio
    async def test_get_balance_sheet_history_quarterly(
        self,
        stonk: Stonk,
        mock_balance_sheet_history_quarterly_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_balance_sheet_history_quarterly method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_balance_sheet_history_quarterly_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        balance_sheet_history_quarterly = (
            await stonk.get_balance_sheet_history_quarterly()
        )
        assert balance_sheet_history_quarterly
        for period in balance_sheet_history_quarterly:
            assert_keys_exist(period, ['maxAge', 'endDate'])

    @pytest.mark.asyncio
    async def test_get_cashflow_statement_history(
        self,
        stonk: Stonk,
        mock_cashflow_statement_history_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_cashflow_statement_history method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_cashflow_statement_history_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        cashflow_statement_history = await stonk.get_cashflow_statement_history()
        assert cashflow_statement_history
        for period in cashflow_statement_history:
            assert_keys_exist(period, ['maxAge', 'endDate', 'netIncome'])

    @pytest.mark.asyncio
    async def test_get_cashflow_statement_history_quarterly(
        self,
        stonk: Stonk,
        mock_cashflow_statement_history_quarterly_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_cashflow_statement_history_quarterly method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_cashflow_statement_history_quarterly_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        cashflow_statement_history_quarterly = (
            await stonk.get_cashflow_statement_history_quarterly()
        )
        assert cashflow_statement_history_quarterly
        for period in cashflow_statement_history_quarterly:
            assert_keys_exist(period, ['maxAge', 'endDate', 'netIncome'])

    @pytest.mark.asyncio
    async def test_get_esg_scores(
        self,
        stonk: Stonk,
        mock_esg_scores_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_esg_scores method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_esg_scores_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        esg_scores = await stonk.get_esg_scores()
        assert esg_scores
        assert_keys_exist(esg_scores, ESG_SCORES_KEYS)

    @pytest.mark.asyncio
    async def test_get_price(
        self,
        stonk: Stonk,
        mock_price_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_price method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_price_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        price = await stonk.get_price()
        assert price
        assert_keys_exist(price, PRICE_KEYS)

    @pytest.mark.asyncio
    async def test_get_default_key_statistics(
        self,
        stonk: Stonk,
        mock_default_key_statistics_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_default_key_statistics method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_default_key_statistics_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        default_key_statistics = await stonk.get_default_key_statistics()
        assert default_key_statistics
        assert_keys_exist(default_key_statistics, DEFAULT_KEY_STATISTICS_KEYS)

    @pytest.mark.asyncio
    async def test_get_financial_data(
        self,
        stonk: Stonk,
        mock_financial_data_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_financial_data method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_financial_data_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        financial_data = await stonk.get_financial_data()
        assert financial_data
        assert_keys_exist(financial_data, FINANCIAL_DATA_KEYS)

    @pytest.mark.asyncio
    async def test_get_calendar_events(
        self,
        stonk: Stonk,
        mock_calendar_events_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_calendar_events method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_calendar_events_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        calendar_events = await stonk.get_calendar_events()
        assert calendar_events
        assert_keys_exist(
            calendar_events, ['maxAge', 'earnings', 'exDividendDate', 'dividendDate']
        )
        assert_keys_exist(calendar_events['earnings'], CALENDAR_EVENTS_EARNING_KEYS)

    @pytest.mark.asyncio
    async def test_get_sec_filings(
        self,
        stonk: Stonk,
        mock_sec_filings_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_sec_filings method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_sec_filings_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        sec_filings = await stonk.get_sec_filings()
        assert sec_filings
        assert_keys_exist(sec_filings, ['maxAge', 'filings'])
        for sec_filing in sec_filings['filings']:
            assert_keys_exist(sec_filing, SEC_FILING_KEYS)

    @pytest.mark.asyncio
    async def test_get_upgrade_downgrade_history(
        self,
        stonk: Stonk,
        mock_upgrade_downgrade_history_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_upgrade_downgrade_history method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_upgrade_downgrade_history_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        upgrade_downgrade_history = await stonk.get_upgrade_downgrade_history()
        assert upgrade_downgrade_history
        for upgrade_downgrade in upgrade_downgrade_history:
            assert_keys_exist(upgrade_downgrade, UPGRADE_DOWNGRADE_HISTORY_KEYS)

    @pytest.mark.asyncio
    async def test_get_institution_ownership(
        self,
        stonk: Stonk,
        mock_institution_ownership_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_institution_ownership method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_institution_ownership_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        institution_ownership = await stonk.get_institution_ownership()
        assert institution_ownership
        for ownership in institution_ownership:
            assert_keys_exist(ownership, OWNERSHIP_KEYS)

    @pytest.mark.asyncio
    async def test_get_fund_ownership(
        self,
        stonk: Stonk,
        mock_fund_ownership_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_fund_ownership method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_fund_ownership_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        fund_ownership = await stonk.get_fund_ownership()
        assert fund_ownership
        for ownership in fund_ownership:
            assert_keys_exist(ownership, OWNERSHIP_KEYS)

    @pytest.mark.asyncio
    async def test_get_major_direct_holders(
        self,
        stonk: Stonk,
        mock_major_direct_holders_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_major_direct_holders method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_major_direct_holders_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        major_direct_holders = await stonk.get_major_direct_holders()
        assert major_direct_holders
        assert_keys_exist(major_direct_holders, ['holders', 'maxAge'])

    @pytest.mark.asyncio
    async def test_get_major_holders_breakdown(
        self,
        stonk: Stonk,
        mock_major_holders_breakdown_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_major_holders_breakdown method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_major_holders_breakdown_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        major_holders_breakdown = await stonk.get_major_holders_breakdown()
        assert major_holders_breakdown
        assert_keys_exist(major_holders_breakdown, MAJOR_HOLDERS_BREAKDOWN_KEYS)

    @pytest.mark.asyncio
    async def test_get_insider_transactions(
        self,
        stonk: Stonk,
        mock_insider_transactions_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_insider_transactions method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_insider_transactions_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        insider_transactions = await stonk.get_insider_transactions()
        assert insider_transactions
        for transaction in insider_transactions:
            assert_keys_exist(transaction, TRANSACTION_KEYS)

    @pytest.mark.asyncio
    async def test_get_insider_holders(
        self,
        stonk: Stonk,
        mock_insider_holders_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_insider_holders method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_insider_holders_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        insider_holders = await stonk.get_insider_holders()
        assert insider_holders
        for holder in insider_holders:
            assert_keys_exist(holder, HOLDER_KEYS)

    @pytest.mark.asyncio
    async def test_get_net_share_purchase_activity(
        self,
        stonk: Stonk,
        mock_net_share_purchase_activity_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_net_share_purchase_activity method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_net_share_purchase_activity_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        net_share_purchase_activity = await stonk.get_net_share_purchase_activity()
        assert net_share_purchase_activity
        assert_keys_exist(net_share_purchase_activity, NET_SHARE_PURCHASE_ACIVITY_KEYS)

    @pytest.mark.asyncio
    async def test_get_earnings(
        self,
        stonk: Stonk,
        mock_earnings_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_earnings method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_earnings_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        earnings = await stonk.get_earnings()
        assert earnings
        assert_keys_exist(
            earnings,
            ['maxAge', 'earningsChart', 'financialsChart', 'financialCurrency'],
        )

    @pytest.mark.asyncio
    async def test_get_earnings_history(
        self,
        stonk: Stonk,
        mock_earnings_history_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_earnings_history method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_earnings_history_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        earnings_history = await stonk.get_earnings_history()
        assert earnings_history
        for period in earnings_history:
            assert_keys_exist(period, EARNINGS_HISTORY_KEYS)

    @pytest.mark.asyncio
    async def test_get_earnings_trend(
        self,
        stonk: Stonk,
        mock_earnings_trend_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_earnings_trend method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_earnings_trend_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        earnings_trend = await stonk.get_earnings_trend()
        assert earnings_trend
        for trend in earnings_trend:
            assert_keys_exist(trend, EARNINGS_TREND_KEYS)

    @pytest.mark.asyncio
    async def test_get_industry_trend(
        self,
        stonk: Stonk,
        mock_industry_trend_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_industry_trend method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_industry_trend_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        industry_trend = await stonk.get_industry_trend()
        assert industry_trend
        assert_keys_exist(industry_trend, ['maxAge', 'symbol', 'estimates'])

    @pytest.mark.asyncio
    async def test_get_index_trend(
        self,
        stonk: Stonk,
        mock_index_trend_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_index_trend method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_index_trend_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        index_trend = await stonk.get_index_trend()
        assert index_trend
        assert_keys_exist(index_trend, ['maxAge', 'symbol', 'estimates'])

    @pytest.mark.asyncio
    async def test_get_sector_trend(
        self,
        stonk: Stonk,
        mock_sector_trend_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_sector_trend method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_sector_trend_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        sector_trend = await stonk.get_sector_trend()
        assert sector_trend
        assert_keys_exist(sector_trend, ['maxAge', 'symbol', 'estimates'])

    @pytest.mark.asyncio
    async def test_get_recommendation_trend(
        self,
        stonk: Stonk,
        mock_recommendation_trend_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_recommendation_trend method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_recommendation_trend_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        recommendation_trend = await stonk.get_recommendation_trend()
        assert recommendation_trend
        for trend in recommendation_trend:
            assert_keys_exist(trend, RECOMMENDATIONS_TREND_KEYS)

    @pytest.mark.asyncio
    async def test_get_page_views(
        self,
        stonk: Stonk,
        mock_page_views_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_page_views method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_page_views_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        page_views = await stonk.get_page_views()
        assert page_views
        assert_keys_exist(
            page_views, ['shortTermTrend', 'midTermTrend', 'longTermTrend', 'maxAge']
        )

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
        stonk: Stonk,
        kwargs: dict[str, Any],
        mock_timeseries_income_statement_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_income_statement method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_timeseries_income_statement_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        annual_income_stmt = await stonk.get_income_statement(**kwargs)
        assert annual_income_stmt
        types = get_types_with_frequency(
            frequency=kwargs['frequency'], typ='income_statement'
        )
        types_list = types.split(',')
        income_stmt_types = [field['meta']['type'][0] for field in annual_income_stmt]
        assert sorted(types_list) == sorted(income_stmt_types)

    @pytest.mark.asyncio
    async def test_get_income_statement_invalid_args(
        self,
        stonk: Stonk,
        mock_timeseries_income_statement_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_income_statement method with invalid arguments.."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_timeseries_income_statement_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        with pytest.raises(Exception):
            await stonk.get_income_statement(frequency='xxx')

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
        stonk: Stonk,
        kwargs: dict[str, Any],
        mock_timeseries_balance_sheet_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_balance_sheet method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_timeseries_balance_sheet_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        annual_balance_sheet = await stonk.get_balance_sheet(**kwargs)
        assert annual_balance_sheet
        types = get_types_with_frequency(
            frequency=kwargs['frequency'], typ='balance_sheet'
        )
        types_list = types.split(',')
        income_stmt_types = [field['meta']['type'][0] for field in annual_balance_sheet]
        assert sorted(types_list) == sorted(income_stmt_types)

    @pytest.mark.asyncio
    async def test_get_balance_sheet_invalid_args(
        self,
        stonk: Stonk,
        mock_timeseries_balance_sheet_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_balance_sheet method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_timeseries_balance_sheet_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        with pytest.raises(Exception):
            await stonk.get_balance_sheet(frequency='trailing')

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
        stonk: Stonk,
        kwargs: dict[str, Any],
        mock_timeseries_cash_flow_json: dict[str, Any],
        mocker: MockerFixture,
    ) -> None:
        """Test get_cash_flow method."""
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_timeseries_cash_flow_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        annual_cash_flow = await stonk.get_cash_flow(**kwargs)
        assert annual_cash_flow
        types = get_types_with_frequency(frequency=kwargs['frequency'], typ='cash_flow')
        types_list = types.split(',')
        income_stmt_types = [field['meta']['type'][0] for field in annual_cash_flow]
        assert sorted(types_list) == sorted(income_stmt_types)

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        stonk: Stonk,
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

        options = await stonk.get_options()
        assert options
        assert_keys_exist(options, OPTIONS_KEYS)
        assert options['underlyingSymbol'] == stonk.ticker

    @pytest.mark.asyncio
    async def test_get_search(
        self, stonk: Stonk, mock_search_json: dict[str, Any], mocker: MockerFixture
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

        search = await stonk.get_search()
        assert search
        assert_keys_exist(search, SEARCH_KEYS)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        stonk: Stonk,
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

        recommendations = await stonk.get_recommendations()
        assert recommendations
        assert_keys_exist(recommendations, ['symbol', 'recommendedSymbols'])
        assert recommendations['symbol'] == stonk.ticker

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        stonk: Stonk,
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

        insights = await stonk.get_insights()
        assert insights
        assert_keys_exist(insights, INSIGHTS_KEYS)
        assert insights['symbol'] == stonk.ticker
