import pandas as pd
import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from yafin import Stonk
from yafin.utils import process_chart_like_yfinance


class TestPerformanceStonk:
    """Performance tests for yafin.stonk module."""

    @pytest.fixture
    def stonk(self) -> Stonk:
        """Fixture for Stonk."""
        return Stonk('META')

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_get_chart_pandas(
        self, stonk: Stonk, benchmark: BenchmarkFixture
    ) -> None:
        """Test get_chart method."""

        async def run_get_chart() -> pd.DataFrame:
            chart = await stonk.get_chart(period_range='1y', interval='1d')
            return process_chart_like_yfinance(chart)

        await benchmark.pedantic(
            run_get_chart, rounds=20, iterations=1, warmup_rounds=0
        )
