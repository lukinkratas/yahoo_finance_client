from typing import Generator
import datetime
from typing import Any

import pytest
from curl_cffi.requests import Response
from pytest_mock import MockerFixture

from yafin import AsyncClient
from yafin.const import ALL_MODULES, TYPES


class TestClient:
    """Tests for yafin.client module."""

    @pytest.fixture
    def client(self) -> Generator[AsyncClient, None, None]:
        """Fixture for AsyncClient."""
        yield AsyncClient()

    @pytest.mark.asyncio
    async def test_get_chart(self, client: AsyncClient, mock_chart_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_chart method."""
        ticker = 'META'

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_chart_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        chart = await client.get_chart(
            ticker, period_range='1y', interval='1d', events='div,split'
        )
        assert chart, 'Chart data does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

        assert chart[ticker.lower()], 'Ticker data does not exist.'
        assert chart[ticker.lower()]['symbol'] == ticker, (
            'Ticker symbol does not match.'
        )
        assert chart['timestamp'], 'Timestamp data does not exist.'
        for key in ['high', 'low', 'close', 'volume', 'open']:
            assert key in chart['indicators']['quote'][0].keys(), f'{key.capitalize()} data does not exist.'
        assert chart['indicators']['adjclose'][0]['adjclose'], (
            'Adjclose data does not exist.'
        )

    @pytest.mark.parametrize(
        'kwargs',
        [
            {
                'ticker': 'META',
                'period_range': 'xxx',
                'interval': '1d',
                'events': 'div,split',
            },
            {
                'ticker': 'META',
                'period_range': '1y',
                'interval': 'xxx',
                'events': 'div,split',
            },
            {'ticker': 'META', 'period_range': '1y', 'interval': '7d', 'events': 'xxx'},
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self, client: AsyncClient, kwargs: dict[str, str]
    ) -> None:
        """Test get_chart method with invalid arguments."""
        with pytest.raises(Exception):
            await client.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(self, client: AsyncClient, mock_quote_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_quote method."""
        tickers = 'AAPL,META'

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_quote_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        quotes = await client.get_quote(tickers)
        assert quotes, 'Quote data does not exist.'

        assert len(quotes) == len(tickers.split(',')), (
            'Number of quotes does not match.'
        )

        symbols = [quote['symbol'] for quote in quotes]
        for ticker in tickers.split(','):
            assert ticker in symbols, f'Ticker {ticker} not found in quotes.'

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(self, client: AsyncClient, mock_quote_summary_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_quote_summary method."""

        ticker = 'META'

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_quote_summary_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        quote_summary = await client.get_quote_summary(ticker, modules=ALL_MODULES)
        assert quote_summary, 'Quote summary data does not exist.'

        for module in ALL_MODULES.split(','):
            assert module in quote_summary.keys(), f'Module {module} not found in quote summary.'

    @pytest.mark.asyncio
    async def test_get_timeseries_income_stmt_types(self, client: AsyncClient, mock_annual_income_stmt_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_timeseries method with annual income statement types."""
        start_ts = datetime.datetime(2020, 1, 1).timestamp()
        now_ts = datetime.datetime.now().timestamp()
        ticker = 'META'
        frequency = 'annual'
        income_stmt_types = TYPES['income_stmt']
        types_with_frequency = [f'{frequency}{t}' for t in income_stmt_types]

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_annual_income_stmt_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        annual_income_stmt = await client.get_timeseries(ticker, types=types_with_frequency, period1=start_ts, period2=now_ts)
        assert annual_income_stmt, 'Annual income statement data does not exist.'

    @pytest.mark.asyncio
    async def test_get_timeseries_balance_sheet_types(self, client: AsyncClient, mock_annual_balance_sheet_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_timeseries method with annual balance sheet types."""

        start_ts = datetime.datetime(2020, 1, 1).timestamp()
        now_ts = datetime.datetime.now().timestamp()
        ticker = 'META'
        frequency = 'annual'
        balance_sheet_types = TYPES['balance_sheet']
        types_with_frequency = [f'{frequency}{t}' for t in balance_sheet_types]

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_annual_balance_sheet_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        annual_balance_sheet = await client.get_timeseries(ticker, types=types_with_frequency, period1=start_ts, period2=now_ts)
        assert annual_balance_sheet, 'Annual balance sheet data does not exist.'

    @pytest.mark.asyncio
    async def test_get_timeseries_cash_flow_types(self, client: AsyncClient, mock_annual_cash_flow_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_timeseries method with annual cash flow types."""

        start_ts = datetime.datetime(2020, 1, 1).timestamp()
        now_ts = datetime.datetime.now().timestamp()
        ticker = 'META'
        frequency = 'annual'
        cash_flow_types = TYPES['cash_flow']
        types_with_frequency = [f'{frequency}{t}' for t in cash_flow_types]

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_annual_cash_flow_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        annual_cash_flow = await client.get_timeseries(ticker, types=types_with_frequency, period1=start_ts, period2=now_ts)
        assert annual_cash_flow, 'Annual cash flow data does not exist.'
    
    @pytest.mark.asyncio
    async def test_get_options(self, client: AsyncClient, mock_options_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_options method."""
        ticker = 'META'

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_options_json
        mock_response.raise_for_status = mocker.Mock()
        mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )

        options = await client.get_options(ticker)
        assert options, 'Options data does not exist.'

    @pytest.mark.asyncio
    async def test_get_search(self, client: AsyncClient, mock_options_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_search method."""
        ticker = 'META'
        
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_options_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        
        search = await client.get_search(ticker)
        assert search, 'Search data does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_recommendations(self, client: AsyncClient, mock_recommendations_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_recommendations method."""
        ticker = 'META'
        
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_recommendations_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        
        recommendations = await client.get_recommendations(ticker)
        assert recommendations, 'Recommendations data does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_insights(self, client: AsyncClient, mock_insights_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_insights method."""
        ticker = 'META'
        
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_insights_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        
        insights = await client.get_insights(ticker)
        assert insights, 'Insights data does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_market_summary(self, client: AsyncClient, mock_market_summary_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_market_summary method."""
       
        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_market_summary_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        
        market_summary = await client.get_market_summary()
        assert market_summary, 'Market summary data does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_trending(self, client: AsyncClient, mock_trending_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_trending method."""

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_trending_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        
        trending = await client.get_trending()
        assert trending, 'Trending data does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_currencies(self, client: AsyncClient, mock_currencies_json: dict[str, Any], mocker: MockerFixture) -> None:
        """Test get_currencies method."""

        mock_response = mocker.Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_currencies_json
        mock_response.raise_for_status = mocker.Mock()
        get_patch = mocker.patch(
            'yafin.client.AsyncSession.get',
            new=mocker.AsyncMock(return_value=mock_response),
        )
        
        currencies = await client.get_currencies()
        assert currencies, 'Currencies data does not exist.'

        # no crumb fetching -> just one get call
        get_patch.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
