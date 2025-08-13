# from enum import Enum

import asyncio
from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError

import logging
import logging.config
from logging_conf import LOGGING_CONFIG

# YFAS = Yahoo Finance Async Stonk (Api Client?)
# todo: more efficient, when one AsyncSession per multiple Stonks is used.
# TODO
# - [ ] (Sync) client
# - [ ] AsyncClient - get crumb only once
# - [?] modules as enum

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# class Module(Enum):
#     QUOTE_TYPE = "quoteType"
#     ASSET_PROFILE = "assetProfile"
#     SUMMARY_DETAIL = 'summaryDetail'
    
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

        else:
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

        return response

    async def get_finance_quote_summary(self, ticker: str, modules: list[str]) -> dict[str, str] | None:

        logger.debug(f'Getting finance/quoteSummary for ticker {ticker}, {modules=}')

        url = f'{self._BASE_URL_}/v10/finance/quoteSummary/{ticker}'
        params = {'modules': ','.join(modules), 'formatted': False, 'crumb': await self._crumb}
        print(f'{url=}, {params=}')
        response = await self._get_async_request(url=url, params=params)

        if response.json()['quoteSummary']['error']:
            logger.error(f'Error in response: {response.json()["quoteSummary"]["error"]}')

        return response.json()['quoteSummary']['result'][0] if response else None

class Stonk(object):

    _client = AsyncClient()

    def __init__(self, ticker: str):
        self.ticker = ticker

    async def get_history(self, range: str, interval: str) -> dict[str, str]:

        logger.debug(f'Getting history for ticker {self.ticker}, {range=}, {interval=}')

        response = await self._client.get_finance_chart(ticker=self.ticker, range=range, interval=interval)

        # fetch data from http response json
        timestamps = response.json()['chart']['result'][0]['timestamp']
        ohlcvs = response.json()['chart']['result'][0]['indicators']['quote'][0]

        # merge dicts
        history_data = {'timestamp': timestamps} | ohlcvs

        return history_data
    
    async def _get_finance_quote_summary_single_module(self, module:str) -> dict[str, str] | None:

        response = await self._client.get_finance_quote_summary(ticker=self.ticker, modules=[module])
        return response[module] if response else None
    
    async def get_quote_type(self) -> dict[str, str] | None:
        
        logger.debug(f'Getting quote type for ticker {self.ticker}.')
        response = await self._get_finance_quote_summary_single_module(module="quoteType")
        return response

    async def get_asset_profile(self) -> dict[str, str] | None:

        logger.debug(f'Getting asset profile for ticker {self.ticker}.')
        response = await self._get_finance_quote_summary_single_module(module="assetProfile")
        return response
    
    async def get_summary_detail(self) -> dict[str, str] | None:

        logger.debug(f'Getting symmary detail for ticker {self.ticker}.')
        response = await self._get_finance_quote_summary_single_module(module="summaryDetail")
        return response
    
async def main() -> None:

    yf_client = AsyncClient()

    aapl_history_data = await yf_client.get_finance_chart(ticker='AAPL', range='1mo', interval='1d')
    print(f'{aapl_history_data=}')

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
    print(f'{aapl_info_data=}')

    aapl = Stonk('AAPL')

    history_data = await aapl.get_history(range='1mo', interval='1d')
    print(f'{history_data=}')

    quote_type = await aapl.get_quote_type()
    print(f'{quote_type=}')

    asset_rofile = await aapl.get_asset_profile()
    print(f'{asset_rofile=}')

    summary_detail = await aapl.get_summary_detail()
    print(f'{summary_detail=}')

if __name__ == '__main__':
    asyncio.run(main())