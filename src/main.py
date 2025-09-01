import json
from pathlib import Path

import asyncio
from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError
import datetime

import logging

from typing import Any

from const import INTERVALS, RANGES, EVENTS, ALL_MODULES, FREQUENCIES, TYPES

logger = logging.getLogger(__name__)

def json_dump(d:dict[str,str], filename:str) -> None:
    path = Path("output").joinpath(filename)
    with open(path, "w") as outfile:
        json.dump(d, outfile, indent=2)

def error(msg:str, err_cls=Exception) -> None:
    logger.error(msg)
    raise err_cls(msg)

def print_url(url:str, params:dict[str,str]=None, print_fn=print) -> None:

    print_str = url

    if params:
        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        print_str += f'?{params_str}'
    
    print_fn(print_str)
    
class AsyncClient(object):
    """
    Client for Yahoo Finance Async Stonk API.
    """

    _BASE_URL = r'https://query2.finance.yahoo.com'
    _DEFAULT_PARAMS = {
        'formatted': 'false', 'region': 'US', 'lang': 'en-US', 'corsDomain': 'finance.yahoo.com'
    }

    def __init__(self):
        self._session = AsyncSession(impersonate='chrome')

    @property
    async def _crumb(self) -> str | None:

        logger.debug('Fetching crumb...')   

        url = f'{self._BASE_URL}/v1/test/getcrumb'
        response = await self._get_async_request(url=url)

        return response.text if response else None

    async def _get_async_request(self, url:str, params:dict[str,str]=None) -> str | None:

        print_url(url, params, print_fn=logger.debug)

        try:
            response = await self._session.get(url, params=params)
            response.raise_for_status()

        except HTTPError as e:
            error(f'HTTP error: {e}', err_cls=HTTPError)

        return response
    
    async def get_finance_chart(self, ticker:str, period_range:str, interval:str, events:str='div,split') -> dict[str, Any]:

        logger.debug(f'Getting finance/chart for ticker {ticker}, {period_range=}, {interval=}, {events=}.')

        if period_range not in RANGES:
            error(f'Invalid {period_range=}. Valid values: {RANGES}')
        
        if interval not in INTERVALS:
            error(f'Invalid {interval=}. Valid values: {INTERVALS}')
        
        if events not in EVENTS:
            error(f'Invalid {events=}. Valid values: {EVENTS}')

        url = f'{self._BASE_URL}/v8/finance/chart/{ticker}'
        params = self._DEFAULT_PARAMS | {'range': period_range, 'interval': interval, 'events': events}
        response = await self._get_async_request(url, params)

        data = response.json()['chart']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_finance_quote_summary_all_modules(self, ticker:str) -> dict[str, Any]:

        logger.debug(f'Getting finance/quoteSummary for ticker {ticker}.')

        url = f'{self._BASE_URL}/v10/finance/quoteSummary/{ticker}'
        params = self._DEFAULT_PARAMS | {'modules': ','.join(ALL_MODULES), 'crumb': await self._crumb}
        response = await self._get_async_request(url, params)

        data = response.json()['quoteSummary']

        if data['error']:
            error(data['error'])

        return data['result'][0]
    
    async def get_finance_timeseries(
        self, ticker:str, types:list[str], period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:
        
        logger.debug(f'Getting finance/timeseries for ticker {ticker}, {types=}, {period1=}, {period2=}.')

        if not period1:
            period1 = datetime.datetime(2020, 1, 1).timestamp()

        if not period2:
            period2 = datetime.datetime.now().timestamp()

        url = f'{self._BASE_URL}/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'
        params = self._DEFAULT_PARAMS | {
            'type': ','.join(types), 'period1': int(period1), 'period2': int(period2)
        }
        response = await self._get_async_request(url, params)
        data = response.json()['timeseries']

        if data['error']:
            error(data['error'])

        return data['result'][0]
       
    async def _get_financials(
        self, ticker:str, frequency:str, typ:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:
        
        logger.debug(f'Getting {typ.replace('_', ' ')} for ticker {ticker}, {frequency=}, {period1=}, {period2=}.')

        if frequency not in FREQUENCIES:
            error(f'Invalid {frequency=}. Valid values: {FREQUENCIES}')

        if typ not in TYPES.keys():
            error(f'Invalid {typ=}. Valid values: {TYPES.keys()}')

        types = TYPES[typ]
        types_with_frequency = [f'{frequency}{t}' for t in types]
        return await self.get_finance_timeseries(ticker, types_with_frequency, period1, period2)
    
    async def get_income_statement(
        self, ticker:str, frequency:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:
        return await self._get_financials(ticker, frequency, 'income_stmt', period1, period2)
    
    async def get_balance_sheet(
        self, ticker:str, frequency:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:

        if frequency == 'trailing':
            error(f'{frequency=} not allowed for balance sheet.')

        return await self._get_financials(ticker, frequency, 'balance_sheet', period1, period2)
    
    async def get_cash_flow(
        self, ticker:str, frequency:str, period1:int|float=None, period2:int|float=None
    ) -> dict[str, Any]:
        return await self._get_financials(ticker, frequency, 'cash_flow', period1, period2)

    async def get_finance_search(self, ticker:str) -> dict[str, Any]:

        logger.debug(f'Getting finance/search for ticker {ticker}.')

        url = f'{self._BASE_URL}/v1/finance/search'
        params = self._DEFAULT_PARAMS | {'q': ticker}
        response = await self._get_async_request(url, params)

        return response.json()

class Stonk(object):

    _client = AsyncClient()

    def __init__(self, ticker: str):
        self.ticker = ticker

async def main() -> None:

    aapl = Stonk('AAPL')

    yf_client = AsyncClient()

    aapl_finance_chart_1y = await yf_client.get_finance_chart(ticker='AAPL', period_range='1y', interval='1d', events='div,split')
    print(aapl_finance_chart_1y)
    aapl_finance_chart_ytd = await yf_client.get_finance_chart(ticker='AAPL', period_range='ytd', interval='1d', events='div')
    print(aapl_finance_chart_ytd)
    meta_finance_chart_1mo = await yf_client.get_finance_chart(ticker='META', period_range='1mo', interval='1d')
    print(meta_finance_chart_1mo)
    meta_finance_chart_5d = await yf_client.get_finance_chart(ticker='META', period_range='5d', interval='1h')
    print(meta_finance_chart_5d)

    aapl_finance_quote_summary_all_modules = await yf_client.get_finance_quote_summary_all_modules(ticker='AAPL')
    print(aapl_finance_quote_summary_all_modules)

    import datetime

    start_ts = datetime.datetime(2020, 1, 1).timestamp()
    now_ts = datetime.datetime.now().timestamp()
    aapl_ttm_income_stmt = await yf_client.get_finance_timeseries(
        ticker='AAPL',
        types=['trailingNetIncome', 'trailingPretaxIncome', 'trailingEBIT', 'trailingEBITDA', 'trailingGrossProfit'],
        period1=start_ts,
        period2=now_ts
    )
    print(aapl_ttm_income_stmt)

    meta_annual_balance_sheet = await yf_client.get_finance_timeseries(ticker='META', types=['annualNetDebt', 'annualTotalDebt'])
    print(meta_annual_balance_sheet)
    
    aapl_quarterly_cash_flow = await yf_client.get_finance_timeseries(ticker='AAPL', types=['quarterlyFreeCashFlow', 'quarterlyOperatingCashFlow'])
    print(aapl_quarterly_cash_flow)

    aapl_ttm_income_stmt = await yf_client.get_income_statement(
        ticker='AAPL',
        frequency='trailing',
        period1=start_ts,
        period2=now_ts
    )
    print(aapl_ttm_income_stmt)
    
    meta_annual_balance_sheet = await yf_client.get_balance_sheet(ticker='META', frequency='annual')
    print(meta_annual_balance_sheet)
    
    aapl_quarterly_cash_flow = await yf_client.get_cash_flow(ticker='AAPL', frequency='quarterly')
    print(aapl_quarterly_cash_flow)

    aapl_finance_search = await yf_client.get_finance_search(ticker='AAPL')
    print(aapl_finance_search)

if __name__ == '__main__':
    asyncio.run(main())