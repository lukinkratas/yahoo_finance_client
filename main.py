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

    
    async def _get_finance_quote_summary_single_module(self, ticker:str, module:str, **kwargs) -> dict[str, str] | None:

        response_json = await self.get_finance_quote_summary(ticker=ticker, modules=[module], **kwargs)
        return response_json[module] if response_json else None
    
    async def get_quote_type(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='quoteType')

    async def get_asset_profile(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='assetProfile')
    
    async def get_summary_profile(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='summaryProfile')
    
    async def get_summary_detail(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='summaryDetail')
    
    async def get_calendar_events(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='calendarEvents')
    
    async def get_default_key_statistics(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='defaultKeyStatistics')
    
    # async def get_details(self, ticker:str) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='details')
    
    async def get_earnings(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='earnings')
    
    async def get_esg_scores(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='esgScores')
    
    async def get_sec_fillings(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='secFilings')
    
    async def get_upgrades_downgrades_history(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='upgradeDowngradeHistory')
    
    async def get_institution_ownership(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='institutionOwnership')
    
    async def get_fund_ownership(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='fundOwnership')
    
    async def get_major_direct_holders(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='majorDirectHolders')
    
    async def get_major_holders_breakdown(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='majorHoldersBreakdown')
    
    async def get_insider_holders(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='insiderHolders')
    
    async def get_insider_transactions(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='insiderTransactions')
    
    async def get_net_share_purchase_activity(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='netSharePurchaseActivity')
    
    async def get_earnings_history(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='earningsHistory')
    
    async def get_earnings_trend(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='earningsTrend')
    
    async def get_industry_trend(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='industryTrend')
    
    async def get_index_trend(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='indexTrend')
    
    async def get_sector_trend(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='sectorTrend')
    
    async def get_recommendation_trend(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='recommendationTrend')
    
    async def get_financial_data(self, ticker:str) -> dict[str, str] | None:
        return await self._get_finance_quote_summary_single_module(ticker=ticker, module='financialData')
    
    # async def get_top_holdings(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='topHoldings')
    
    # async def get_fund_profile(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='fundProfile')
        
    # async def get_futures_chain(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='futuresChain')

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
    
    async def get_quote_type(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)

    async def get_asset_profile(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_summary_profile(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_summary_detail(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_calendar_events(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_default_key_statistics(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    # async def get_details(self) -> dict[str, str] | None:
    #     return await self._get_finance_quote_summary_single_module(module='details')
    
    async def get_earnings(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_esg_scores(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_sec_fillings(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_upgrades_downgrades_history(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_institution_ownership(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_fund_ownership(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_major_direct_holders(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_major_holders_breakdown(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_insider_holders(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_insider_transactions(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_net_share_purchase_activity(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_earnings_history(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_earnings_trend(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_industry_trend(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_index_trend(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_sector_trend(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_recommendation_trend(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
    async def get_financial_data(self) -> dict[str, str] | None:
        return await self._client._get_finance_quote_summary_single_module(ticker=self.ticker)
    
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
    json_dump(aapl_history_data, 'aapl_history_data_via_client.json')

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
    json_dump(aapl_info_data, 'aapl_info_data_via_client.json')

    aapl_quote_type = await yf_client.get_quote_type(ticker='AAPL')
    json_dump(aapl_quote_type, 'aapl_quote_type_via_client.json')

    aapl_asset_profile = await yf_client.get_asset_profile(ticker='AAPL')
    json_dump(aapl_asset_profile, 'aapl_asset_profile_via_client.json')

    aapl_summary_profile = await yf_client.get_summary_profile(ticker='AAPL')
    json_dump(aapl_summary_profile, 'aapl_summary_profile_via_client.json')

    aapl_summary_detail = await yf_client.get_summary_detail(ticker='AAPL')
    json_dump(aapl_summary_detail, 'aapl_summary_detail_via_client.json')

    aapl_calendar_events = await yf_client.get_calendar_events(ticker='AAPL')
    json_dump(aapl_calendar_events, 'aapl_calendar_events_via_client.json')
    
    aapl_default_key_statistics = await yf_client.get_default_key_statistics(ticker='AAPL')
    json_dump(aapl_default_key_statistics, 'aapl_default_key_statistics_via_client.json')
    
    # details = await aapl.get_details()
    # json_dump(details, 'details.json')
    
    aapl_earnings = await yf_client.get_earnings(ticker='AAPL')
    json_dump(aapl_earnings, 'aapl_earnings_via_client.json')
    
    aapl_esg_scores = await yf_client.get_esg_scores(ticker='AAPL')
    json_dump(aapl_esg_scores, 'aapl_esg_scores_via_client.json')

    aapl_sec_fillings = await yf_client.get_sec_fillings(ticker='AAPL')
    json_dump(aapl_sec_fillings, 'aapl_sec_fillings_via_client.json')
    
    aapl_upgrades_downgrades_history = await yf_client.get_upgrades_downgrades_history(ticker='AAPL')
    json_dump(aapl_upgrades_downgrades_history, 'aapl_upgrades_downgrades_history_via_client.json')

    aapl_institution_ownership = await yf_client.get_institution_ownership(ticker='AAPL')
    json_dump(aapl_institution_ownership, 'aapl_institution_ownership_via_client.json')
    
    aapl_fund_ownership = await yf_client.get_fund_ownership(ticker='AAPL')
    json_dump(aapl_fund_ownership, 'aapl_fund_ownership_via_client.json')

    aapl_major_direct_holders = await yf_client.get_major_direct_holders(ticker='AAPL')
    json_dump(aapl_major_direct_holders, 'aapl_major_direct_holders_via_client.json')
    
    aapl_major_holders_breakdown = await yf_client.get_major_holders_breakdown(ticker='AAPL')
    json_dump(aapl_major_holders_breakdown, 'aapl_major_holders_breakdown_via_client.json')

    aapl_insider_holders = await yf_client.get_insider_holders(ticker='AAPL')
    json_dump(aapl_insider_holders, 'aapl_insider_holders_via_client.json')
    
    aapl_insider_transactions = await yf_client.get_insider_transactions(ticker='AAPL')
    json_dump(aapl_insider_transactions, 'aapl_insider_transactions_via_client.json')

    aapl_net_share_purchase_activity = await yf_client.get_net_share_purchase_activity(ticker='AAPL')
    json_dump(aapl_net_share_purchase_activity, 'aapl_net_share_purchase_activity_via_client.json')

    aapl_earnings_history = await yf_client.get_earnings_history(ticker='AAPL')
    json_dump(aapl_earnings_history, 'aapl_earnings_history_via_client.json')
    
    aapl_earnings_trend = await yf_client.get_earnings_trend(ticker='AAPL')
    json_dump(aapl_earnings_trend, 'aapl_earnings_trend_via_client.json')
    
    aapl_industry_trend = await yf_client.get_industry_trend(ticker='AAPL')
    json_dump(aapl_industry_trend, 'aapl_industry_trend_via_client.json')

    aapl_index_trend = await yf_client.get_index_trend(ticker='AAPL')
    json_dump(aapl_index_trend, 'aapl_index_trend_via_client.json')
    
    aapl_sector_trend = await yf_client.get_sector_trend(ticker='AAPL')
    json_dump(aapl_sector_trend, 'aapl_sector_trend_via_client.json')
    
    aapl_recommendation_trend = await yf_client.get_recommendation_trend(ticker='AAPL')
    json_dump(aapl_recommendation_trend, 'aapl_recommendation_trend_via_client.json')
    
    # futures_chain = await aapl.get_futures_chain()
    # json_dump(futures_chain, 'futures_chain.json')

    aapl_financial_data = await yf_client.get_financial_data(ticker='AAPL')
    json_dump(aapl_financial_data, 'aapl_financial_data_via_client.json')

    # top_holdings = await aapl.get_top_holdings()
    # json_dump(top_holdings, 'top_holdings.json')
    
    # fund_profile = await aapl.get_fund_profile()
    # json_dump(fund_profile, 'fund_profile.json')

    aapl_net_income_data = await yf_client.get_finance_timeseries(ticker='AAPL', types=['annualNetIncome', 'quarterlyNetIncome', 'trailingNetIncome'])
    json_dump(aapl_net_income_data, 'aapl_net_income_data_via_client.json')

    aapl_news = await yf_client.get_news(ticker='AAPL')
    json_dump(aapl_news, 'aapl_news_via_client.json')

    aapl = Stonk('AAPL')

    aapl_history_data = await aapl.get_history(range='1mo', interval='1d')
    json_dump(aapl_history_data, 'aapl_history_data_via_stonk.json')

    aapl_quote_type = await aapl.get_quote_type()
    json_dump(aapl_quote_type, 'aapl_quote_type_via_stonk.json')

    aapl_asset_profile = await aapl.get_asset_profile()
    json_dump(aapl_asset_profile, 'aapl_asset_profile_via_stonk.json')

    aapl_summary_profile = await aapl.get_summary_profile()
    json_dump(aapl_summary_profile, 'aapl_summary_profile_via_stonk.json')

    aapl_summary_detail = await aapl.get_summary_detail()
    json_dump(aapl_summary_detail, 'aapl_summary_detail_via_stonk.json')

    aapl_calendar_events = await aapl.get_calendar_events()
    json_dump(aapl_calendar_events, 'aapl_calendar_events_via_stonk.json')
    
    aapl_default_key_statistics = await aapl.get_default_key_statistics()
    json_dump(aapl_default_key_statistics, 'aapl_default_key_statistics_via_stonk.json')
    
    # details = await aapl.get_details()
    # json_dump(details, 'details.json')
    
    aapl_earnings = await aapl.get_earnings()
    json_dump(aapl_earnings, 'aapl_earnings_via_stonk.json')
    
    aapl_esg_scores = await aapl.get_esg_scores()
    json_dump(aapl_esg_scores, 'aapl_esg_scores_via_stonk.json')

    aapl_sec_fillings = await aapl.get_sec_fillings()
    json_dump(aapl_sec_fillings, 'aapl_sec_fillings_via_stonk.json')
    
    aapl_upgrades_downgrades_history = await aapl.get_upgrades_downgrades_history()
    json_dump(aapl_upgrades_downgrades_history, 'aapl_upgrades_downgrades_history_via_stonk.json')

    aapl_institution_ownership = await aapl.get_institution_ownership()
    json_dump(aapl_institution_ownership, 'aapl_institution_ownership_via_stonk.json')
    
    aapl_fund_ownership = await aapl.get_fund_ownership()
    json_dump(aapl_fund_ownership, 'aapl_fund_ownership_via_stonk.json')

    aapl_major_direct_holders = await aapl.get_major_direct_holders()
    json_dump(aapl_major_direct_holders, 'aapl_major_direct_holders_via_stonk.json')
    
    aapl_major_holders_breakdown = await aapl.get_major_holders_breakdown()
    json_dump(aapl_major_holders_breakdown, 'aapl_major_holders_breakdown_via_stonk.json')

    aapl_insider_holders = await aapl.get_insider_holders()
    json_dump(aapl_insider_holders, 'aapl_insider_holders_via_stonk.json')
    
    aapl_insider_transactions = await aapl.get_insider_transactions()
    json_dump(aapl_insider_transactions, 'aapl_insider_transactions_via_stonk.json')

    aapl_net_share_purchase_activity = await aapl.get_net_share_purchase_activity()
    json_dump(aapl_net_share_purchase_activity, 'aapl_net_share_purchase_activity_via_stonk.json')

    aapl_earnings_history = await aapl.get_earnings_history()
    json_dump(aapl_earnings_history, 'aapl_earnings_history_via_stonk.json')
    
    aapl_earnings_trend = await aapl.get_earnings_trend()
    json_dump(aapl_earnings_trend, 'aapl_earnings_trend_via_stonk.json')
    
    aapl_industry_trend = await aapl.get_industry_trend()
    json_dump(aapl_industry_trend, 'aapl_industry_trend_via_stonk.json')

    aapl_index_trend = await aapl.get_index_trend()
    json_dump(aapl_index_trend, 'aapl_index_trend_via_stonk.json')
    
    aapl_sector_trend = await aapl.get_sector_trend()
    json_dump(aapl_sector_trend, 'aapl_sector_trend_via_stonk.json')
    
    aapl_recommendation_trend = await aapl.get_recommendation_trend()
    json_dump(aapl_recommendation_trend, 'aapl_recommendation_trend_via_stonk.json')
    
    # futures_chain = await aapl.get_futures_chain()
    # json_dump(futures_chain, 'futures_chain.json')

    aapl_financial_data = await aapl.get_financial_data()
    json_dump(aapl_financial_data, 'aapl_financial_data_via_stonk.json')

    # top_holdings = await aapl.get_top_holdings()
    # json_dump(top_holdings, 'top_holdings.json')
    
    # fund_profile = await aapl.get_fund_profile()
    # json_dump(fund_profile, 'fund_profile.json')

    aapl_annual_income_statement_history = await aapl.get_income_statement_history()
    json_dump(aapl_annual_income_statement_history, 'aapl_annual_income_statement_history_via_stonk.json')

    aapl_quarterly_income_statement_history = await aapl.get_income_statement_history(frequency='quarterly')
    json_dump(aapl_quarterly_income_statement_history, 'aapl_quarterly_income_statement_history_via_stonk.json')

    aapl_trailing_income_statement_history = await aapl.get_income_statement_history(frequency='trailing')
    json_dump(aapl_trailing_income_statement_history, 'aapl_trailing_income_statement_history_via_stonk.json')

    aapl_annual_balance_sheet_history = await aapl.get_balance_sheet_history()
    json_dump(aapl_annual_balance_sheet_history, 'aapl_annual_balance_sheet_history_via_stonk.json')

    aapl_quarterly_balance_sheet_history = await aapl.get_balance_sheet_history(frequency='quarterly')
    json_dump(aapl_quarterly_balance_sheet_history, 'aapl_quarterly_balance_sheet_history_via_stonk.json')

    aapl_annual_cash_flow_history = await aapl.get_cash_flow_history()
    json_dump(aapl_annual_cash_flow_history, 'aapl_annual_cash_flow_history_via_stonk.json')

    aapl_quarterly_cash_flow_history = await aapl.get_cash_flow_history(frequency='quarterly')
    json_dump(aapl_quarterly_cash_flow_history, 'aapl_quarterly_cash_flow_history_via_stonk.json')

    aapl_trailing_cash_flow_history = await aapl.get_cash_flow_history(frequency='trailing')
    json_dump(aapl_trailing_cash_flow_history, 'aapl_trailing_cash_flow_history_via_stonk.json')

if __name__ == '__main__':
    asyncio.run(main())