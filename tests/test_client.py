import pytest

from yahoo_finance import AsyncClient

class TestClient:

    @pytest.fixture
    def client(self) -> AsyncClient:
        return AsyncClient()

    @pytest.mark.asyncio
    async def test_get_chart(self, client: AsyncClient):

        chart = await client.get_chart(
            ticker='AAPL', period_range='1y', interval='1d', events='div,split'
        )

        assert chart, 'Chart does not exist.'
