import logging
from typing import Any

from typeguard import typechecked

from .client import AsyncClient
from .const import ALL_MODULES
from .exceptions import TrailingBalanceSheetError
from .utils import error, get_types_with_frequency, track_args

logger = logging.getLogger(__name__)


class Symbol(object):
    """Stonk class for a specific ticker."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self._client = AsyncClient()

    @track_args
    @typechecked
    async def get_chart(
        self,
        period_range: str,
        interval: str,
        include_div: bool = True,
        include_split: bool = True,
    ) -> dict[str, Any]:
        """Get chart data for the ticker.

        Args:
            period_range: Range of the period
            interval: Data interval
            include_div: Whether to include dividends
            include_split: Whether to include stock splits

        Returns: Chart data as a dictionary.
        """
        events_list = []

        if include_div:
            events_list.append('div')

        if include_split:
            events_list.append('split')

        events = ','.join(events_list) if events_list else None

        chart_json = await self._client.get_chart(
            self.ticker, period_range, interval, events
        )
        return chart_json['chart']['result'][0]

    @track_args
    async def get_quote(self) -> dict[str, Any]:
        """Get quote for the ticker."""
        quote_json = await self._client.get_quote(self.ticker)
        # client.get_quote can be quiried with multiple tickers, e.g.: 'META,AAPL'
        # from Stonk class we are only querying one ticker
        return quote_json['quoteResponse']['result'][0]

    @track_args
    async def get_quote_summary_all_modules(self) -> dict[str, Any]:
        """Get quote summary for all modules for the ticker."""
        quote_summary_json = await self._client.get_quote_summary(
            self.ticker, ALL_MODULES
        )
        return quote_summary_json['quoteSummary']['result'][0]

    @track_args
    async def _get_quote_summary_single_module(self, module: str) -> dict[str, Any]:
        quote_summary_json = await self._client.get_quote_summary(self.ticker, module)
        return quote_summary_json['quoteSummary']['result'][0][module]

    @track_args
    async def get_quote_type(self) -> dict[str, Any]:
        """Get quote type for the ticker."""
        return await self._get_quote_summary_single_module('quoteType')

    @track_args
    async def get_asset_profile(self) -> dict[str, Any]:
        """Get asset profile for the ticker."""
        return await self._get_quote_summary_single_module('assetProfile')

    @track_args
    async def get_summary_profile(self) -> dict[str, Any]:
        """Get summary profile for the ticker."""
        return await self._get_quote_summary_single_module('summaryProfile')

    @track_args
    async def get_summary_detail(self) -> dict[str, Any]:
        """Get summary detail for the ticker."""
        return await self._get_quote_summary_single_module('summaryDetail')

    @track_args
    async def get_income_statement_history(self) -> list[dict[str, Any]]:
        """Get income statement history for the ticker."""
        result = await self._get_quote_summary_single_module('incomeStatementHistory')
        return result['incomeStatementHistory']

    @track_args
    async def get_income_statement_history_quarterly(self) -> list[dict[str, Any]]:
        """Get income statement history quarterly for the ticker."""
        result = await self._get_quote_summary_single_module(
            'incomeStatementHistoryQuarterly'
        )
        return result['incomeStatementHistory']

    @track_args
    async def get_balance_sheet_history(self) -> list[dict[str, Any]]:
        """Get balance sheet history for the ticker."""
        result = await self._get_quote_summary_single_module('balanceSheetHistory')
        return result['balanceSheetStatements']

    @track_args
    async def get_balance_sheet_history_quarterly(self) -> list[dict[str, Any]]:
        """Get balance sheet history quarterly for the ticker."""
        result = await self._get_quote_summary_single_module(
            'balanceSheetHistoryQuarterly'
        )
        return result['balanceSheetStatements']

    @track_args
    async def get_cashflow_statement_history(self) -> list[dict[str, Any]]:
        """Get cashflow statement history for the ticker."""
        result = await self._get_quote_summary_single_module('cashflowStatementHistory')
        return result['cashflowStatements']

    @track_args
    async def get_cashflow_statement_history_quarterly(self) -> list[dict[str, Any]]:
        """Get cashflow statement history quarterly for the ticker."""
        result = await self._get_quote_summary_single_module(
            'cashflowStatementHistoryQuarterly'
        )
        return result['cashflowStatements']

    @track_args
    async def get_esg_scores(self) -> dict[str, Any]:
        """Get esg scores for the ticker."""
        return await self._get_quote_summary_single_module('esgScores')

    @track_args
    async def get_price(self) -> dict[str, Any]:
        """Get price data for the ticker."""
        return await self._get_quote_summary_single_module('price')

    @track_args
    async def get_default_key_statistics(self) -> dict[str, Any]:
        """Get default key statistics for the ticker."""
        return await self._get_quote_summary_single_module('defaultKeyStatistics')

    @track_args
    async def get_financial_data(self) -> dict[str, Any]:
        """Get financial data for the ticker."""
        return await self._get_quote_summary_single_module('financialData')

    @track_args
    async def get_calendar_events(self) -> dict[str, Any]:
        """Get calendar events for the ticker."""
        return await self._get_quote_summary_single_module('calendarEvents')

    @track_args
    async def get_sec_filings(self) -> dict[str, Any]:
        """Get sec filings for the ticker."""
        return await self._get_quote_summary_single_module('secFilings')

    @track_args
    async def get_upgrade_downgrade_history(self) -> list[dict[str, Any]]:
        """Get upgrade downgrade history for the ticker."""
        result = await self._get_quote_summary_single_module('upgradeDowngradeHistory')
        return result['history']

    @track_args
    async def get_institution_ownership(self) -> list[dict[str, Any]]:
        """Get institution ownership for the ticker."""
        result = await self._get_quote_summary_single_module('institutionOwnership')
        return result['ownershipList']

    @track_args
    async def get_fund_ownership(self) -> list[dict[str, Any]]:
        """Get fund ownership for the ticker."""
        result = await self._get_quote_summary_single_module('fundOwnership')
        return result['ownershipList']

    @track_args
    async def get_major_direct_holders(self) -> dict[str, Any]:
        """Get major direct holders for the ticker."""
        return await self._get_quote_summary_single_module('majorDirectHolders')

    @track_args
    async def get_major_holders_breakdown(self) -> dict[str, Any]:
        """Get major holders breakdown for the ticker."""
        return await self._get_quote_summary_single_module('majorHoldersBreakdown')

    @track_args
    async def get_insider_transactions(self) -> list[dict[str, Any]]:
        """Get insider transactions for the ticker."""
        result = await self._get_quote_summary_single_module('insiderTransactions')
        return result['transactions']

    @track_args
    async def get_insider_holders(self) -> list[dict[str, Any]]:
        """Get insider holders for the ticker."""
        result = await self._get_quote_summary_single_module('insiderHolders')
        return result['holders']

    @track_args
    async def get_net_share_purchase_activity(self) -> dict[str, Any]:
        """Get net share purchase activity for the ticker."""
        return await self._get_quote_summary_single_module('netSharePurchaseActivity')

    @track_args
    async def get_earnings(self) -> dict[str, Any]:
        """Get earnings for the ticker."""
        return await self._get_quote_summary_single_module('earnings')

    @track_args
    async def get_earnings_history(self) -> list[dict[str, Any]]:
        """Get earnings history for the ticker."""
        result = await self._get_quote_summary_single_module('earningsHistory')
        return result['history']

    @track_args
    async def get_earnings_trend(self) -> list[dict[str, Any]]:
        """Get earnings trend for the ticker."""
        result = await self._get_quote_summary_single_module('earningsTrend')
        return result['trend']

    @track_args
    async def get_industry_trend(self) -> dict[str, Any]:
        """Get industry trend for the ticker."""
        return await self._get_quote_summary_single_module('industryTrend')

    @track_args
    async def get_index_trend(self) -> dict[str, Any]:
        """Get index trend for the ticker."""
        return await self._get_quote_summary_single_module('indexTrend')

    @track_args
    async def get_sector_trend(self) -> dict[str, Any]:
        """Get sector trend for the ticker."""
        return await self._get_quote_summary_single_module('sectorTrend')

    @track_args
    async def get_recommendation_trend(self) -> list[dict[str, Any]]:
        """Get recommendation trend for the ticker."""
        result = await self._get_quote_summary_single_module('recommendationTrend')
        return result['trend']

    @track_args
    async def get_page_views(self) -> dict[str, Any]:
        """Get page views for the ticker."""
        return await self._get_quote_summary_single_module('pageViews')

    @track_args
    async def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        types = get_types_with_frequency(frequency, typ)
        timeseries_json = await self._client.get_timeseries(
            self.ticker, types, period1, period2
        )
        return timeseries_json['timeseries']['result']

    @track_args
    async def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get income statement financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Income statement financials as a dictionary.
        """
        return await self._get_financials(
            frequency, 'income_statement', period1, period2
        )

    @track_args
    async def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get balance sheet financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Balance sheet financials as a dictionary.
        """
        if frequency == 'trailing':
            error(
                msg=f'{frequency=} not allowed for balance sheet.',
                err_cls=TrailingBalanceSheetError,
            )

        return await self._get_financials(frequency, 'balance_sheet', period1, period2)

    @track_args
    async def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get cash flow financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Cash flow financials as a dictionary.
        """
        return await self._get_financials(frequency, 'cash_flow', period1, period2)

    @track_args
    async def get_options(self) -> dict[str, Any]:
        """Get options data for the ticker."""
        options_json = await self._client.get_options(self.ticker)
        return options_json['optionChain']['result'][0]

    @track_args
    async def get_search(self) -> dict[str, Any]:
        """Get search results for the ticker."""
        return await self._client.get_search(self.ticker)

    @track_args
    async def get_recommendations(self) -> dict[str, Any]:
        """Get analyst recommendations for the ticker."""
        recommendations_json = await self._client.get_recommendations(self.ticker)
        return recommendations_json['finance']['result'][0]

    @track_args
    async def get_insights(self) -> dict[str, Any]:
        """Get news insights for the ticker."""
        insights_json = await self._client.get_insights(self.ticker)
        return insights_json['finance']['result']
