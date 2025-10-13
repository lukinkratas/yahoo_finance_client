import logging
from datetime import datetime
from typing import Any

from curl_cffi.requests import AsyncSession, Response
from curl_cffi.requests.exceptions import HTTPError

from .const import ALL_MODULES, ALL_TYPES_WITH_FREQUENCIES, EVENTS, INTERVALS, RANGES
from .utils import compile_url, error, track_args

logger = logging.getLogger(__name__)


class AsyncClient(object):
    """Client for Yahoo Finance API."""

    _BASE_URL = r'https://query2.finance.yahoo.com'
    _DEFAULT_PARAMS = {
        'formatted': 'false',
        'region': 'US',
        'lang': 'en-US',
        'corsDomain': 'finance.yahoo.com',
    }

    def __init__(self) -> None:
        self._session: AsyncSession[Any] = AsyncSession(impersonate='chrome')

    async def __aenter__(self) -> self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._session.close()

    @property
    async def _crumb(self) -> str | None:
        logger.debug('Fetching crumb...')

        url = f'{self._BASE_URL}/v1/test/getcrumb'
        response = await self._get_async_request(url=url)
        return response.text if response else None

    @track_args
    async def _get_async_request(
        self, url: str, params: dict[str, Any] | None = None
    ) -> Response:
        logger.debug(compile_url(url, params))

        try:
            response = await self._session.get(url, params=params)
            response.raise_for_status()

        except HTTPError as e:
            error(f'HTTP error: {e}', err_cls=HTTPError)

        return response

    @track_args
    async def get_chart(
        self,
        ticker: str,
        period_range: str,
        interval: str,
        events: str | None = 'div,split',
    ) -> dict[str, Any]:
        """Get chart data for the ticker.

        Args:
            ticker: Ticker symbol.
            period_range: Range of the period.
            interval: Data interval.
            events: Events to include.

        Returns: Chart data as a dictionary.
        """
        logger.debug(
            f'Getting finance/chart for ticker {ticker}, {period_range=}, {interval=}, {events=}.'  # noqa E501
        )

        if period_range not in RANGES:
            error(f'Invalid {period_range=}. Valid values: {RANGES}')

        if interval not in INTERVALS:
            error(f'Invalid {interval=}. Valid values: {INTERVALS}')

        events = events.replace(' ', '') if events else None

        if events not in EVENTS:
            error(f'Invalid {events=}. Valid values: {EVENTS}')

        url = f'{self._BASE_URL}/v8/finance/chart/{ticker}'
        params = (
            self._DEFAULT_PARAMS
            | {
                'range': period_range,
                'interval': interval,
            }
            | {'events': events}
            if events
            else {}
        )

        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_quote(self, tickers: str) -> dict[str, Any]:
        """Get quote for the ticker(s).

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Quote data as a dictionary.
        """
        logger.debug(f'Getting finance/quote for ticker {tickers}.')

        url = f'{self._BASE_URL}/v7/finance/quote'
        params = self._DEFAULT_PARAMS | {'symbols': tickers, 'crumb': await self._crumb}
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_quote_summary(self, ticker: str, modules: str) -> dict[str, Any]:
        """Get quote summary for the ticker.

        Args:
            ticker: Ticker symbol.
            modules: Comma-separated modules to include.

        Returns: Quote summary data as a dictionary.
        """
        logger.debug(f'Getting finance/quoteSummary for ticker {ticker}.')

        if not all([m in ALL_MODULES for m in modules.split(',')]):
            error(f'Invalid {modules=}. Valid values: {ALL_MODULES}')

        url = f'{self._BASE_URL}/v10/finance/quoteSummary/{ticker}'
        params = self._DEFAULT_PARAMS | {'modules': modules, 'crumb': await self._crumb}
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_timeseries(
        self,
        ticker: str,
        types: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> dict[str, Any]:
        """Get timeseries for the ticker.

        Args:
            ticker: Ticker symbol.
            types: Timeseries types (incl. frequency) to include.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Timeseries data as a dictionary.
        """
        logger.debug(
            f'Getting finance/timeseries for ticker {ticker}, {types=}, {period1=}, {period2=}.'  # noqa E501
        )

        if not all([t in ALL_TYPES_WITH_FREQUENCIES for t in types.split(',')]):
            error(f'Invalid {types=}. Valid values: {ALL_TYPES_WITH_FREQUENCIES}')

        if not period1:
            period1 = datetime(2020, 1, 1).timestamp()

        if not period2:
            period2 = datetime.now().timestamp()

        url = f'{self._BASE_URL}/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'  # noqa E501
        params = self._DEFAULT_PARAMS | {
            'type': types,
            'period1': int(period1),
            'period2': int(period2),
        }

        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_options(self, ticker: str) -> dict[str, Any]:
        """Get options for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Options as a dictionary.
        """
        logger.debug(f'Getting finance/options for ticker {ticker}.')

        url = f'{self._BASE_URL}/v7/finance/options/{ticker}'
        params = self._DEFAULT_PARAMS | {'crumb': await self._crumb}
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_search(self, tickers: str) -> dict[str, Any]:
        """Get search results for the ticker.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Search results as a dictionary.
        """
        logger.debug(f'Getting finance/search for ticker {tickers}.')

        url = f'{self._BASE_URL}/v1/finance/search'
        params = self._DEFAULT_PARAMS | {'q': tickers}
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_recommendations(self, ticker: str) -> dict[str, Any]:
        """Get analyst recommendations for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Recommendations as a dictionary.
        """
        logger.debug(f'Getting finance/recommendations for ticker {ticker}.')

        url = f'{self._BASE_URL}/v6/finance/recommendationsbysymbol/{ticker}'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_insights(self, ticker: str) -> dict[str, Any]:
        """Get insights for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Insights as a dictionary.
        """
        logger.debug(f'Getting finance/insights for ticker {ticker}.')

        url = f'{self._BASE_URL}/ws/insights/v2/finance/insights'
        params = self._DEFAULT_PARAMS | {'symbol': ticker}
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_market_summaries(self) -> dict[str, Any]:
        """Get market summaries.

        Returns: Market summaries as a list of dictionaries.
        """
        logger.debug('Getting finance/quote/marketSummary.')

        url = f'{self._BASE_URL}/v6/finance/quote/marketSummary'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_trending(self) -> dict[str, Any]:
        """Get trending tickers.

        Returns: Trending tickers as a dictionary.
        """
        logger.debug('Getting finance/trending.')

        url = f'{self._BASE_URL}/v1/finance/trending/US'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @track_args
    async def get_currencies(self) -> dict[str, Any]:
        """Get currency exchange rates.

        Returns: Currency exchange rates as a list of dictionaries.
        """
        logger.debug('Getting finance/currencies.')

        url = f'{self._BASE_URL}/v1/finance/currencies'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()
