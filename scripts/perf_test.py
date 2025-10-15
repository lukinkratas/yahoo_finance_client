import asyncio

from curl_cffi import requests
from yfinance import Ticker

from yafin import Stonk
from yafin.utils import track_performance, process_chart_like_yfinance
import logging
from logging_config import setup_logging

logger = logging.getLogger(__name__)
yfinance_logger = logging.getLogger('yfinance')
yfinance_logger.setLevel(logging.ERROR)

NRUNS = 10

@track_performance(NRUNS)
def main_yfinance() -> None:  # noqa: D103

    # async session does not work, throws
    #   yfinance.exceptions.YFDataException: Yahoo API requires curl_cffi session
    #   not <class 'curl_cffi.requests.session.AsyncSession'>.
    #   Solution: stop setting session, let YF handle.
    # session = requests.AsyncSession(impersonate="chrome")

    session = requests.Session(impersonate='chrome')
    meta = Ticker('META', session)

    history_df = meta.history(period='1y', interval='1d')

    # print(history_df)
    # print(history_df.info())

    session.close()

@track_performance(NRUNS)
async def main() -> None:  # noqa: D103
    stonk = Stonk('META')

    chart = await stonk.get_chart(period_range='1y', interval='1d')
    chart_df = process_chart_like_yfinance(chart)

    # print(chart_df)
    # print(chart_df.info())

if __name__ == '__main__':
    setup_logging()
    main_yfinance()
    asyncio.run(main())
