import logging
from typing import Any

from .client import AsyncClient
from .const import ALL_MODULES, FREQUENCIES, TYPES
from .utils import error

logger = logging.getLogger(__name__)


class Stonk(object):
    """Stonk class for a specific ticker."""

    _client = AsyncClient()

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    async def get_chart(
        self, period_range: str, interval: str, events: str = 'div,split'
    ) -> dict[str, Any]:
        """Get chart data for the ticker.

        Args:
            period_range: Range of the period
            interval: Data interval
            events: Events to include

        Returns: Chart data as a dictionary.
        """
        return await self._client.get_chart(self.ticker, period_range, interval, events)

    async def get_quote(self) -> dict[str, Any]:
        """Get quote for the ticker."""
        return await self._client.get_quote(self.ticker)

    async def get_quote_summary_all_modules(self) -> dict[str, Any]:
        """Get quote summary for all modules for the ticker."""
        return await self._client.get_quote_summary(self.ticker, ALL_MODULES)

    async def _get_quote_summary_single_module(self, module: str) -> dict[str, Any]:
        data = await self._client.get_quote_summary(self.ticker, module)
        return data[module]

    async def get_quote_type(self) -> dict[str, Any]:
        """Get quote type for the ticker."""
        return await self._get_quote_summary_single_module('quoteType')

    async def get_asset_profile(self) -> dict[str, Any]:
        """Get asset profile for the ticker."""
        return await self._get_quote_summary_single_module('assetProfile')

    async def get_summary_profile(self) -> dict[str, Any]:
        """Get summary profile for the ticker."""
        return await self._get_quote_summary_single_module('summaryProfile')

    async def get_summary_detail(self) -> dict[str, Any]:
        """Get summary detail for the ticker."""
        return await self._get_quote_summary_single_module('summaryDetail')

    async def get_income_statement_history(self) -> dict[str, Any]:
        """Get income statement history for the ticker."""
        return await self._get_quote_summary_single_module('incomeStatementHistory')

    async def get_income_statement_history_quarterly(self) -> dict[str, Any]:
        """Get income statement history quarterly for the ticker."""
        return await self._get_quote_summary_single_module(
            'incomeStatementHistoryQuarterly'
        )

    async def get_balance_sheet_history(self) -> dict[str, Any]:
        """Get balance sheet history for the ticker."""
        return await self._get_quote_summary_single_module('balanceSheetHistory')

    async def get_balance_sheet_history_quarterly(self) -> dict[str, Any]:
        """Get balance sheet history quarterly for the ticker."""
        return await self._get_quote_summary_single_module(
            'balanceSheetHistoryQuarterly'
        )

    async def get_cashflow_statement_history(self) -> dict[str, Any]:
        """Get cashflow statement history for the ticker."""
        return await self._get_quote_summary_single_module('cashflowStatementHistory')

    async def get_cashflow_statement_history_quarterly(self) -> dict[str, Any]:
        """Get cashflow statement history quarterly for the ticker."""
        return await self._get_quote_summary_single_module(
            'cashflowStatementHistoryQuarterly'
        )

    async def get_esg_scores(self) -> dict[str, Any]:
        """Get esg scores for the ticker."""
        return await self._get_quote_summary_single_module('esgScores')

    async def get_price(self) -> dict[str, Any]:
        """Get price data for the ticker."""
        return await self._get_quote_summary_single_module('price')

    async def get_default_key_statistics(self) -> dict[str, Any]:
        """Get default key statistics for the ticker."""
        return await self._get_quote_summary_single_module('defaultKeyStatistics')

    async def get_financial_data(self) -> dict[str, Any]:
        """Get financial data for the ticker."""
        return await self._get_quote_summary_single_module('financialData')

    async def get_calendar_events(self) -> dict[str, Any]:
        """Get calendar events for the ticker."""
        return await self._get_quote_summary_single_module('calendarEvents')

    async def get_sec_filings(self) -> dict[str, Any]:
        """Get sec filings for the ticker."""
        return await self._get_quote_summary_single_module('secFilings')

    async def get_upgrade_downgrade_history(self) -> dict[str, Any]:
        """Get upgrade downgrade history for the ticker."""
        return await self._get_quote_summary_single_module('upgradeDowngradeHistory')

    async def get_institution_ownership(self) -> dict[str, Any]:
        """Get institution ownership for the ticker."""
        return await self._get_quote_summary_single_module('institutionOwnership')

    async def get_fund_ownership(self) -> dict[str, Any]:
        """Get fund ownership for the ticker."""
        return await self._get_quote_summary_single_module('fundOwnership')

    async def get_major_direct_holders(self) -> dict[str, Any]:
        """Get major direct holders for the ticker."""
        return await self._get_quote_summary_single_module('majorDirectHolders')

    async def get_major_holders_breakdown(self) -> dict[str, Any]:
        """Get major holders breakdown for the ticker."""
        return await self._get_quote_summary_single_module('majorHoldersBreakdown')

    async def get_insider_transactions(self) -> dict[str, Any]:
        """Get insider transactions for the ticker."""
        return await self._get_quote_summary_single_module('insiderTransactions')

    async def get_insider_holders(self) -> dict[str, Any]:
        """Get insider holders for the ticker."""
        return await self._get_quote_summary_single_module('insiderHolders')

    async def get_net_share_purchase_activity(self) -> dict[str, Any]:
        """Get net share purchase activity for the ticker."""
        return await self._get_quote_summary_single_module('netSharePurchaseActivity')

    async def get_earnings(self) -> dict[str, Any]:
        """Get earnings for the ticker."""
        return await self._get_quote_summary_single_module('earnings')

    async def get_earnings_history(self) -> dict[str, Any]:
        """Get earnings history for the ticker."""
        return await self._get_quote_summary_single_module('earningsHistory')

    async def get_earnings_trend(self) -> dict[str, Any]:
        """Get earnings trend for the ticker."""
        return await self._get_quote_summary_single_module('earningsTrend')

    async def get_industry_trend(self) -> dict[str, Any]:
        """Get industry trend for the ticker."""
        return await self._get_quote_summary_single_module('industryTrend')

    async def get_index_trend(self) -> dict[str, Any]:
        """Get index trend for the ticker."""
        return await self._get_quote_summary_single_module('indexTrend')

    async def get_sector_trend(self) -> dict[str, Any]:
        """Get sector trend for the ticker."""
        return await self._get_quote_summary_single_module('sectorTrend')

    async def get_recommendation_trend(self) -> dict[str, Any]:
        """Get recommendation trend for the ticker."""
        return await self._get_quote_summary_single_module('recommendationTrend')

    async def get_page_views(self) -> dict[str, Any]:
        """Get page views for the ticker."""
        return await self._get_quote_summary_single_module('pageViews')

    async def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> dict[str, Any]:
        if frequency not in FREQUENCIES:
            error(f'Invalid {frequency=}. Valid values: {FREQUENCIES}')

        if typ not in TYPES.keys():
            error(f'Invalid {typ=}. Valid values: {TYPES.keys()}')

        types = TYPES[typ]
        types_with_frequency = [f'{frequency}{t}' for t in types]
        return await self._client.get_timeseries(
            self.ticker, types_with_frequency, period1, period2
        )

    async def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> dict[str, Any]:
        """Get income statement financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Income statement financials as a dictionary.
        """
        return await self._get_financials(frequency, 'income_stmt', period1, period2)

    async def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> dict[str, Any]:
        """Get balance sheet financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Balance sheet financials as a dictionary.
        """
        if frequency == 'trailing':
            error(f'{frequency=} not allowed for balance sheet.')

        return await self._get_financials(frequency, 'balance_sheet', period1, period2)

    async def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> dict[str, Any]:
        """Get cash flow financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Cash flow financials as a dictionary.
        """
        return await self._get_financials(frequency, 'cash_flow', period1, period2)

    async def get_options(self) -> dict[str, Any]:
        """Get options data for the ticker."""
        return await self._client.get_options(self.ticker)

    async def get_search(self) -> dict[str, Any]:
        """Get search results for the ticker."""
        return await self._client.get_search(self.ticker)

    async def get_recommendations(self) -> dict[str, Any]:
        """Get analyst recommendations for the ticker."""
        return await self._client.get_recommendations(self.ticker)

    async def get_insights(self) -> dict[str, Any]:
        """Get news insights for the ticker."""
        return await self._client.get_insights(self.ticker)
