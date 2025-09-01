import logging

from typing import Any

from .client import AsyncClient
from .const import ALL_MODULES, FREQUENCIES, TYPES
from .utils import error

logger = logging.getLogger(__name__)
    
class Stonk(object):

    _client = AsyncClient()

    def __init__(self, ticker: str):
        self.ticker = ticker

    async def get_finance_chart(self, period_range:str, interval:str, events:str='div,split') -> dict[str, Any]:
        return await self._client.get_finance_chart(self.ticker, period_range, interval, events)
    
    async def get_finance_quote_summary_all_modules(self) -> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, ALL_MODULES)
    
    async def _get_finance_quote_summary_single_module(self, module:str) -> dict[str, Any]:

        data = await self._client.get_finance_quote_summary(self.ticker, module)
        return data[module]
    
    async def get_quote_type(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'quoteType')

    async def get_asset_profile(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'assetProfile')

    async def get_summary_profile(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'summaryProfile')

    async def get_summary_detail(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'summaryDetail')

    async def get_income_statement_history(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'incomeStatementHistory')

    async def get_income_statement_history_quarterly(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'incomeStatementHistoryQuarterly')

    async def get_balance_sheet_history(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'balanceSheetHistory')

    async def get_balance_sheet_history_quarterly(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'balanceSheetHistoryQuarterly')

    async def get_cashflow_statement_history(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'cashflowStatementHistory')

    async def get_cashflow_statement_history_quarterly(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'cashflowStatementHistoryQuarterly')

    async def get_esg_scores(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'esgScores')

    async def get_price(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'price')

    async def get_default_key_statistics(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'defaultKeyStatistics')

    async def get_financial_data(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'financialData')

    async def get_calendar_events(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'calendarEvents')

    async def get_sec_filings(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'secFilings')

    async def get_upgrade_downgrade_history(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'upgradeDowngradeHistory')

    async def get_institution_ownership(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'institutionOwnership')

    async def get_fund_ownership(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'fundOwnership')

    async def get_major_direct_holders(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'majorDirectHolders')

    async def get_major_holders_breakdown(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'majorHoldersBreakdown')

    async def get_insider_transactions(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'insiderTransactions')

    async def get_insider_holders(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'insiderHolders')

    async def get_net_share_purchase_activity(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'netSharePurchaseActivity')

    async def get_earnings(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'earnings')

    async def get_earnings_history(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'earningsHistory')

    async def get_earnings_trend(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'earningsTrend')

    async def get_industry_trend(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'industryTrend')

    async def get_index_trend(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'indexTrend')

    async def get_sector_trend(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'sectorTrend')

    async def get_recommendation_trend(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'recommendationTrend')

    async def get_page_views(self)-> dict[str, Any]:
        return await self._client.get_finance_quote_summary(self.ticker, 'pageViews')

    async def _get_financials(
        self, frequency:str, typ:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:

        if not frequency in FREQUENCIES:
            error(f'Invalid {frequency=}. Valid values: {FREQUENCIES}')

        if not typ in TYPES.keys():
            error(f'Invalid {typ=}. Valid values: {TYPES.keys()}')

        types = TYPES[typ]
        types_with_frequency = [f'{frequency}{t}' for t in types]
        return await self._client.get_finance_timeseries(self.ticker, types_with_frequency, period1, period2)
    
    async def get_income_statement(
        self, frequency:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:
        return await self._get_financials(frequency, 'income_stmt', period1, period2)
    
    async def get_balance_sheet(
        self, frequency:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:

        if frequency == 'trailing':
            error(f'{frequency=} not allowed for balance sheet.')

        return await self._get_financials(frequency, 'balance_sheet', period1, period2)
    
    async def get_cash_flow(
        self, frequency:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:
        return await self._get_financials(frequency, 'cash_flow', period1, period2)
    
    async def get_finance_options(self) -> dict[str, Any]:
        return await self._client.get_finance_options(self.ticker)

    async def get_finance_search(self) -> dict[str, Any]:
        return await self._client.get_finance_search(self.ticker)