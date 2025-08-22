# from pprint import pprint
import json
from pathlib import Path
import datetime

import asyncio
from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError

import logging

from const import INCOME_STMT_TYPES, BALANCE_SHEET_TYPE, CASH_FLOW_TYPES

logger = logging.getLogger(__name__)

def json_dump(d:dict[str,str], filename:str) -> None:
    path = Path("output").joinpath(filename)
    with open(path, "w") as outfile:
        json.dump(d, outfile, indent=2)
    
class AsyncClient(object):
    """
    Client for Yahoo Finance Async Stonk API.
    """

    _BASE_URL_ = r'https://query2.finance.yahoo.com'
    _ROOT_URL_ = r'https://finance.yahoo.com'

    def __init__(self):
        self._session = AsyncSession(impersonate='chrome')

    @property
    async def _crumb(self) -> str | None:

        logger.debug('Fetching crumb...')

        url = f'{self._BASE_URL_}/v1/test/getcrumb'
        response = await self._get_async_request(url=url)

        return response.text if response else None

    async def _get_async_request(self, url: str, **kwargs) -> str | None:

        try:
            response = await self._session.get(url, **kwargs)
            response.raise_for_status()

        except HTTPError as e:
            logger.error(e)
            raise e

        return response
    
    async def _post_async_request(self, url: str, payload: dict[str, str], **kwargs) -> str | None:

        try:
            response = await self._session.post(url, data=payload, **kwargs)
            response.raise_for_status()

        except HTTPError as e:
            logger.error(e)
            raise e

        return response

    async def get_finance_chart(self, ticker:str, range: str, interval: str) -> dict[str, str]:

        logger.debug(f'Getting finance/chart for ticker {ticker}, {range=}, {interval=}')

        url = f'{self._BASE_URL_}/v8/finance/chart/{ticker}'
        params = {'range': range, 'interval': interval}

        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        print(f'{url}?{params_str}')

        response = await self._get_async_request(url=url, params=params)

        return response.json()['chart']['result'][0] if response else None

    async def get_finance_quote_summary(self, ticker: str, modules: list[str], **kwargs) -> dict[str, str] | None:

        logger.debug(f'Getting finance/quoteSummary for ticker {ticker}, {modules=}')

        url = f'{self._BASE_URL_}/v10/finance/quoteSummary/{ticker}'
        modules_str = ','.join(modules)
        params = kwargs | {'modules': modules_str, 'crumb': await self._crumb}

        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        print(f'{url}?{params_str}')

        response = await self._get_async_request(url=url, params=params)

        if response.json()['quoteSummary']['error']:
            msg = f'Error in response: {response.json()["quoteSummary"]["error"]}'
            logger.error(msg)
            raise Exception(msg)

        return response.json()['quoteSummary']['result'][0] if response else None
    
    async def get_finance_timeseries(self, ticker:str, types:list[str], period1:int|float=None, period2:int|float=None, **kwargs) -> dict[str, str] | None:
        
        logger.debug(f'Getting finance/timeseries for ticker {ticker}, {types=}')

        url = f'{self._BASE_URL_}/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'
        types_str = ','.join(types)

        if not period1:
            period1 = datetime.datetime(2020, 1, 1).timestamp()

        if not period2:
            period2 = datetime.datetime.now().timestamp()

        params = kwargs | {'type': types_str, 'period1': int(period1), 'period2': int(period2)}

        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        print(f'{url}?{params_str}')

        response = await self._get_async_request(url=url, params=params)

        if response.json()['timeseries']['error']:
            msg = f'Error in response: {response.json()["quoteSummary"]["error"]}'
            logger.error(msg)
            raise Exception(msg)

        return response.json()['timeseries']['result'] if response else None
    
    async def get_news(self, ticker:str) -> dict[str, str] | None:

        logger.debug(f'Getting news for ticker {ticker}')

        count = 10
        url = f"{self._ROOT_URL_}/xhr/ncp"
        params = {
            'queryRef': 'latestNews',
            'serviceKey': 'ncp_fin'
        }
        payload = {
            "serviceConfig": {
                "snippetCount": count,
                "s": [ticker]
            }
        }

        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        print(f'{url}?{params_str} with {payload=}')

        response = await self._post_async_request(url=url, payload=payload, params=params)

        return response.json() if response else None

class Stonk(object):

    _client = AsyncClient()

    def __init__(self, ticker: str):
        self.ticker = ticker

    async def get_history(self, range: str, interval: str) -> dict[str, str]:

        logger.debug(f'Getting history for ticker {self.ticker}, {range=}, {interval=}')

        response_json = await self._client.get_finance_chart(ticker=self.ticker, range=range, interval=interval)

        # fetch data from http response json
        timestamps = response_json['timestamp']
        ohlcvs = response_json['indicators']['quote'][0]
        adjclose = response_json['indicators']['adjclose'][0]

        # merge dicts
        history_data = {'timestamp': timestamps} | ohlcvs | adjclose

        return history_data
    
    async def _get_finance_quote_summary_single_module(self, module:str, **kwargs) -> dict[str, str] | None:

        # convert camelCase to text with spaces
        module_str = ''.join(' ' + char.lower() if char.isupper() else char for char in module)
        logger.debug(f'Getting {module_str} for ticker {self.ticker}.')
        response_json = await self._client.get_finance_quote_summary(ticker=self.ticker, modules=[module], **kwargs)
        return response_json[module] if response_json else None
    
    async def get_quote_type(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='quoteType')

    async def get_asset_profile(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='assetProfile')
    
    async def get_summary_profile(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='summaryProfile')
    
    async def get_summary_detail(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='summaryDetail')
    
    async def get_calendar_events(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='calendarEvents')
    
    async def get_default_key_statistics(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='defaultKeyStatistics')
    
    # async def get_details(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='details')
    
    async def get_earnings(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='earnings')
    
    async def get_esg_scores(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='esgScores')
    
    async def get_sec_fillings(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='secFilings')
    
    async def get_upgrades_downgrades_history(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='upgradeDowngradeHistory')
    
    async def get_institution_ownership(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='institutionOwnership')
    
    async def get_fund_ownership(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='fundOwnership')
    
    async def get_major_direct_holders(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='majorDirectHolders')
    
    async def get_major_holders_breakdown(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='majorHoldersBreakdown')
    
    async def get_insider_holders(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='insiderHolders')
    
    async def get_insider_transactions(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='insiderTransactions')
    
    async def get_net_share_purchase_activity(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='netSharePurchaseActivity')
    
    async def get_earnings_history(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='earningsHistory')
    
    async def get_earnings_trend(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='earningsTrend')
    
    async def get_industry_trend(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='industryTrend')
    
    async def get_index_trend(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='indexTrend')
    
    async def get_sector_trend(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='sectorTrend')
    
    async def get_recommendation_trend(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='recommendationTrend')
    
    async def get_financial_data(self) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(module='financialData')
    
    # async def get_top_holdings(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='topHoldings')
    
    # async def get_fund_profile(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='fundProfile')
        
    # async def get_futures_chain(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='futuresChain')

    async def _get_finance_timeseries(self, types:list[str], frequency:str=None) -> dict[str, str] | None:

        logger.debug(f'Getting finance timeseries for ticker {self.ticker} with {frequency=} and {types=}.')

        if not frequency:
            frequency = 'annual'
            
        if not frequency in ['annual', 'quarterly', 'trailing']:
            msg = f'{frequency=} is not allowed. annual, quarterly, trailing are the only allowed options.'
            logger.error(msg)
            raise Exception(msg)

        frequency_types_combined = [f'{frequency}{t}' for t in types]

        response_json = await self._client.get_finance_timeseries(ticker=self.ticker, types=frequency_types_combined)
        return response_json if response_json else None
    
    async def get_income_statement_history(self, frequency:str=None) -> dict[str, str] | None:
        return await self._get_finance_timeseries(INCOME_STMT_TYPES, frequency)

    async def get_balance_sheet_history(self, frequency:str=None) -> dict[str, str] | None:

        if frequency == 'trailing':
            msg = f'{frequency=} is not allowed for balance sheet.'
            logger.error(msg)
            raise Exception(msg)
        
        return await self._get_finance_timeseries(BALANCE_SHEET_TYPE, frequency)
    
    async def get_cash_flow_history(self, frequency:str=None) -> dict[str, str] | None:
        return await self._get_finance_timeseries(CASH_FLOW_TYPES, frequency)
        

async def main() -> None:

    yf_client = AsyncClient()

    aapl_history_data = await yf_client.get_finance_chart(ticker='AAPL', range='1mo', interval='1d')
    json_dump(aapl_history_data, 'history_data_client_aapl.json')

    aapl_info_data = await yf_client.get_finance_quote_summary(
        ticker='AAPL',
        modules=[
            'financialData',
            'quoteType',
            'defaultKeyStatistics',
            'assetProfile',
            'summaryDetail'
        ]
    )
    json_dump(aapl_info_data, 'info_data_client_aapl.json')

    aapl_net_income_data = await yf_client.get_finance_timeseries(ticker='AAPL', types=['annualNetIncome', 'quarterlyNetIncome', 'trailingNetIncome'])
    json_dump(aapl_net_income_data, 'net_income_client_aapl.json')

    aapl_news = await yf_client.get_news(ticker='AAPL')
    json_dump(aapl_news, 'news_client_aapl.json')

    aapl = Stonk('AAPL')

    history_data = await aapl.get_history(range='1mo', interval='1d')
    json_dump(history_data, 'history_data.json')

    quote_type = await aapl.get_quote_type()
    json_dump(quote_type, 'quote_type.json')

    asset_profile = await aapl.get_asset_profile()
    json_dump(asset_profile, 'asset_profile.json')

    summary_profile = await aapl.get_summary_profile()
    json_dump(summary_profile, 'summary_profile.json')

    summary_detail = await aapl.get_summary_detail()
    json_dump(summary_detail, 'summary_detail.json')

    calendar_events = await aapl.get_calendar_events()
    json_dump(calendar_events, 'calendar_events.json')
    
    default_key_statistics = await aapl.get_default_key_statistics()
    json_dump(default_key_statistics, 'default_key_statistics.json')
    
    # details = await aapl.get_details()
    # json_dump(details, 'details.json')
    
    earnings = await aapl.get_earnings()
    json_dump(earnings, 'earnings.json')
    
    esg_scores = await aapl.get_esg_scores()
    json_dump(esg_scores, 'esg_scores.json')

    sec_fillings = await aapl.get_sec_fillings()
    json_dump(sec_fillings, 'sec_fillings.json')
    
    upgrades_downgrades_history = await aapl.get_upgrades_downgrades_history()
    json_dump(upgrades_downgrades_history, 'upgrades_downgrades_history.json')

    institution_ownership = await aapl.get_institution_ownership()
    json_dump(institution_ownership, 'institution_ownership.json')
    
    fund_ownership = await aapl.get_fund_ownership()
    json_dump(fund_ownership, 'fund_ownership.json')

    major_direct_holders = await aapl.get_major_direct_holders()
    json_dump(major_direct_holders, 'major_direct_holders.json')
    
    major_holders_breakdown = await aapl.get_major_holders_breakdown()
    json_dump(major_holders_breakdown, 'major_holders_breakdown.json')

    insider_holders = await aapl.get_insider_holders()
    json_dump(insider_holders, 'insider_holders.json')
    
    insider_transactions = await aapl.get_insider_transactions()
    json_dump(insider_transactions, 'insider_transactions.json')

    net_share_purchase_activity = await aapl.get_net_share_purchase_activity()
    json_dump(net_share_purchase_activity, 'net_share_purchase_activity.json')

    earnings_history = await aapl.get_earnings_history()
    json_dump(earnings_history, 'earnings_history.json')
    
    earnings_trend = await aapl.get_earnings_trend()
    json_dump(earnings_trend, 'earnings_trend.json')
    
    industry_trend = await aapl.get_industry_trend()
    json_dump(industry_trend, 'industry_trend.json')

    index_trend = await aapl.get_index_trend()
    json_dump(index_trend, 'index_trend.json')
    
    sector_trend = await aapl.get_sector_trend()
    json_dump(sector_trend, 'sector_trend.json')
    
    recommendation_trend = await aapl.get_recommendation_trend()
    json_dump(recommendation_trend, 'recommendation_trend.json')
    
    # futures_chain = await aapl.get_futures_chain()
    # json_dump(futures_chain, 'futures_chain.json')

    financial_data = await aapl.get_financial_data()
    json_dump(financial_data, 'financial_data.json')

    # top_holdings = await aapl.get_top_holdings()
    # json_dump(top_holdings, 'top_holdings.json')
    
    # fund_profile = await aapl.get_fund_profile()
    # json_dump(fund_profile, 'fund_profile.json')

    income_statement_history = await aapl.get_income_statement_history()
    json_dump(income_statement_history, 'income_statement_history.json')

    income_statement_history = await aapl.get_income_statement_history(frequency='quarterly')
    json_dump(income_statement_history, 'income_statement_quarterly_history.json')

    income_statement_history = await aapl.get_income_statement_history(frequency='trailing')
    json_dump(income_statement_history, 'income_statement_trailing_history.json')

    balance_sheet_history = await aapl.get_balance_sheet_history()
    json_dump(balance_sheet_history, 'balance_sheet_history.json')

    balance_sheet_history = await aapl.get_balance_sheet_history(frequency='quarterly')
    json_dump(balance_sheet_history, 'balance_sheet_quarterly_history.json')

    cash_flow_history = await aapl.get_cash_flow_history()
    json_dump(cash_flow_history, 'cash_flow_history.json')

    cash_flow_history = await aapl.get_cash_flow_history(frequency='quarterly')
    json_dump(cash_flow_history, 'cash_flow_quarterly_history.json')

    cash_flow_history = await aapl.get_cash_flow_history(frequency='trailing')
    json_dump(cash_flow_history, 'cash_flow_trailing_history.json')

if __name__ == '__main__':
    asyncio.run(main())