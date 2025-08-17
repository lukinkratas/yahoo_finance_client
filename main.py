# from pprint import pprint
import json
from pathlib import Path
import datetime

import asyncio
from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError

import logging

from const import INCOME_STMT_TYPES

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

    def __init__(self):
        self._session = AsyncSession(impersonate='chrome')

    async def _get_async_request(self, url: str, **kwargs) -> str | None:

        try:
            response = await self._session.get(url, **kwargs)
            response.raise_for_status()

        except HTTPError as e:
            logger.error(e)
            raise e

        return response
    
    @property
    async def _crumb(self) -> str | None:

        logger.debug('Fetching crumb...')

        url = f'{self._BASE_URL_}/v1/test/getcrumb'
        response = await self._get_async_request(url=url)

        return response.text if response else None

    async def get_finance_chart(self, ticker:str, range: str, interval: str) -> dict[str, str]:

        logger.debug(f'Getting finance/chart for ticker {ticker}, {range=}, {interval=}')

        url = f'{self._BASE_URL_}/v8/finance/chart/{ticker}'
        params = {'range': range, 'interval': interval}
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

    async def get_income_statement_history(self, frequency:str=None) -> dict[str, str] | None:

        if not frequency:
            frequency = 'annual'
            
        if not frequency in ['annual', 'quarterly', 'trailing']:
            msg = f'{frequency=} is not allowed'
            logger.error(msg)
            raise Exception(msg)

        types = [f'{frequency}{typ}' for typ in INCOME_STMT_TYPES]

        response_json = await self._client.get_finance_timeseries(ticker=self.ticker, types=types)
        return response_json if response_json else None

async def main() -> None:

    display = print

    yf_client = AsyncClient()

    aapl_history_data = await yf_client.get_finance_chart(ticker='AAPL', range='1mo', interval='1d')
    display(f'{aapl_history_data=}\n')
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
    display(f'{aapl_info_data=}')
    json_dump(aapl_info_data, 'info_data_client_aapl.json')

    aapl = Stonk('AAPL')

    history_data = await aapl.get_history(range='1mo', interval='1d')
    display(f'{history_data=}\n')
    json_dump(history_data, 'history_data.json')

    quote_type = await aapl.get_quote_type()
    display(f'{quote_type.keys()=}\n')
    json_dump(quote_type, 'quote_type.json')

    asset_profile = await aapl.get_asset_profile()
    display(f'{asset_profile.keys()=}\n')
    json_dump(asset_profile, 'asset_profile.json')

    summary_profile = await aapl.get_summary_profile()
    display(f'{summary_profile.keys()=}\n')
    json_dump(summary_profile, 'summary_profile.json')

    summary_detail = await aapl.get_summary_detail()
    display(f'{summary_detail.keys()=}\n')
    json_dump(summary_detail, 'summary_detail.json')

    income_statement_history = await aapl.get_income_statement_history()
    json_dump(income_statement_history, 'income_statement_history.json')

    income_statement_history = await aapl.get_income_statement_history(frequency='quarterly')
    json_dump(income_statement_history, 'income_statement_quarterly_history.json')

    income_statement_history = await aapl.get_income_statement_history(frequency='trailing')
    json_dump(income_statement_history, 'income_statement_trailing_history.json')

if __name__ == '__main__':
    asyncio.run(main())