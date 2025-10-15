from typing import Generator

import pytest
from curl_cffi import requests
from pytest_benchmark.fixture import BenchmarkFixture
from yfinance import Ticker


class TestPerformanceBaseline:
    """Performance tests for yafin.stonk module."""

    @pytest.fixture
    def ticker(self) -> Generator[Ticker, None, None]:
        """Fixture for Ticker."""
        session = requests.Session(impersonate='chrome')
        yield Ticker('META', session=session)
        session.close()

    @pytest.mark.baseline
    @pytest.mark.performance
    def test_get_chart(self, ticker: Ticker, benchmark: BenchmarkFixture) -> None:
        """Test get_chart method."""
        benchmark.pedantic(
            lambda: ticker.history(period='1y', interval='1d'),
            rounds=20,
            iterations=1,
            warmup_rounds=0,
        )
