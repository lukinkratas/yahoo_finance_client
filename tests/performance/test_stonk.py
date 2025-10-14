import pytest

from yfinance import Ticker

from yafin import Stonk

class TestPerformanceStonk:
    """Performance tests for yafin.stonk module."""

    @pytest.fixture
    def ticker(self) -> Ticker:
        """Fixture for Ticker."""
        return Ticker('META')

    @pytest.fixture
    def stonk(self) -> Stonk:
        """Fixture for Stonk."""
        return Stonk('META')

    @pytest.mark.performance
    def test_yfinance_get_chart(self, ticker: Ticker, benchmark) -> None:
        """Test get_chart method."""
        history_df = benchmark(lambda: ticker.history(period='1y', interval='1d'))
        assert not history_df.empty

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_yafin_get_chart(self, stonk: Stonk, benchmark) -> None:
        """Test get_chart method."""
        chart = await benchmark(lambda: stonk.get_chart(period_range='1y', interval='1d'))
        assert chart