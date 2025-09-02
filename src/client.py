import datetime
import logging
from typing import Any

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError

from .const import ALL_MODULES, EVENTS, INTERVALS, RANGES
from .utils import error, print_url

logger = logging.getLogger(__name__)


class AsyncClient(object):
    """
    Client for Yahoo Finance Async Stonk API.
    """

    _BASE_URL = r'https://query2.finance.yahoo.com'
    _DEFAULT_PARAMS = {
        'formatted': 'false',
        'region': 'US',
        'lang': 'en-US',
        'corsDomain': 'finance.yahoo.com',
    }

    def __init__(self):
        self._session = AsyncSession(impersonate='chrome')

    @property
    async def _crumb(self) -> str | None:
        logger.debug('Fetching crumb...')

        url = f'{self._BASE_URL}/v1/test/getcrumb'
        response = await self._get_async_request(url=url)

        return response.text if response else None

    async def _get_async_request(
        self, url: str, params: dict[str, str] = None
    ) -> str | None:
        print_url(url, params, print_fn=logger.debug)

        try:
            response = await self._session.get(url, params=params)
            response.raise_for_status()

        except HTTPError as e:
            error(f'HTTP error: {e}', err_cls=HTTPError)

        return response

    async def get_chart(
        self, ticker: str, period_range: str, interval: str, events: str = 'div,split'
    ) -> dict[str, Any]:
        logger.debug(
            f'Getting finance/chart for ticker {ticker}, {period_range=}, {interval=}, {events=}.'  # noqa E501
        )

        if period_range not in RANGES:
            error(f'Invalid {period_range=}. Valid values: {RANGES}')

        if interval not in INTERVALS:
            error(f'Invalid {interval=}. Valid values: {INTERVALS}')

        if events not in EVENTS:
            error(f'Invalid {events=}. Valid values: {EVENTS}')

        url = f'{self._BASE_URL}/v8/finance/chart/{ticker}'
        params = self._DEFAULT_PARAMS | {
            'range': period_range,
            'interval': interval,
            'events': events,
        }
        response = await self._get_async_request(url, params)

        data = response.json()['chart']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_quote(self, tickers: str) -> dict[str, Any]:
        logger.debug(f'Getting finance/quote for ticker {tickers}.')

        url = f'{self._BASE_URL}/v7/finance/quote'
        params = self._DEFAULT_PARAMS | {'symbols': tickers, 'crumb': await self._crumb}
        response = await self._get_async_request(url, params)

        data = response.json()['quoteResponse']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_quote_summary(self, ticker: str, modules: str) -> dict[str, Any]:
        logger.debug(f'Getting finance/quoteSummary for ticker {ticker}.')

        if not all([m in ALL_MODULES for m in modules.split(',')]):
            error(f'Invalid {modules=}. Valid values: {ALL_MODULES}')

        url = f'{self._BASE_URL}/v10/finance/quoteSummary/{ticker}'
        params = self._DEFAULT_PARAMS | {'modules': modules, 'crumb': await self._crumb}
        response = await self._get_async_request(url, params)

        data = response.json()['quoteSummary']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_timeseries(
        self,
        ticker: str,
        types: list[str],
        period1: int | float = None,
        period2: int | float = None,
    ) -> dict[str, Any]:
        logger.debug(
            f'Getting finance/timeseries for ticker {ticker}, {types=}, {period1=}, {period2=}.'  # noqa E501
        )

        if not period1:
            period1 = datetime.datetime(2020, 1, 1).timestamp()

        if not period2:
            period2 = datetime.datetime.now().timestamp()

        url = f'{self._BASE_URL}/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'  # noqa E501
        params = self._DEFAULT_PARAMS | {
            'type': ','.join(types),
            'period1': int(period1),
            'period2': int(period2),
        }
        response = await self._get_async_request(url, params)
        data = response.json()['timeseries']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_options(self, ticker: str) -> dict[str, Any]:
        logger.debug(f'Getting finance/options for ticker {ticker}.')

        url = f'{self._BASE_URL}/v7/finance/options/{ticker}'
        params = self._DEFAULT_PARAMS | {'crumb': await self._crumb}
        response = await self._get_async_request(url, params)

        data = response.json()['optionChain']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_search(self, ticker: str) -> dict[str, Any]:
        logger.debug(f'Getting finance/search for ticker {ticker}.')

        url = f'{self._BASE_URL}/v1/finance/search'
        params = self._DEFAULT_PARAMS | {'q': ticker}
        response = await self._get_async_request(url, params)

        return response.json()

    async def get_recommendations(self, ticker: str) -> dict[str, Any]:
        logger.debug(f'Getting finance/recommendations for ticker {ticker}.')

        url = f'{self._BASE_URL}/v6/finance/recommendationsbysymbol/{ticker}'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)

        data = response.json()['finance']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_insights(self, ticker: str) -> dict[str, Any]:
        logger.debug(f'Getting finance/recommendations for ticker {ticker}.')

        url = f'{self._BASE_URL}/ws/insights/v2/finance/insights'
        params = self._DEFAULT_PARAMS | {'symbol': ticker}
        response = await self._get_async_request(url, params)

        data = response.json()['finance']

        if data['error']:
            error(data['error'])

        return data['result']

    async def get_market_summary(self) -> dict[str, Any]:
        logger.debug('Getting finance/quote/marketSummary.')

        url = f'{self._BASE_URL}/v6/finance/quote/marketSummary'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)

        data = response.json()['marketSummaryResponse']

        if data['error']:
            error(data['error'])

        return data['result']

    async def get_trending(self) -> dict[str, Any]:
        logger.debug('Getting finance/trending.')

        url = f'{self._BASE_URL}/v1/finance/trending/US'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)

        data = response.json()['finance']

        if data['error']:
            error(data['error'])

        return data['result'][0]

    async def get_currencies(self) -> dict[str, Any]:
        logger.debug('Getting finance/currencies.')

        url = f'{self._BASE_URL}/v1/finance/currencies'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)

        data = response.json()['currencies']

        if data['error']:
            error(data['error'])

        return data['result']
