import asyncio

import pandas as pd
from curl_cffi import requests
from yfinance import Ticker

from yafin import Stonk


def yfinance_main() -> None:  # noqa: D103
    # async session does not work, throws
    #   yfinance.exceptions.YFDataException: Yahoo API requires curl_cffi session
    #   not <class 'curl_cffi.requests.session.AsyncSession'>.
    #   Solution: stop setting session, let YF handle.
    # session = requests.AsyncSession(impersonate="chrome")
    session = requests.Session(impersonate='chrome')
    meta = Ticker('META', session)

    history_df = meta.history(period='1y', interval='1d')
    print(history_df)
    print(history_df.info())


async def yafin_main() -> None:  # noqa: D103
    stonk = Stonk('META')

    chart = await stonk.get_chart(period_range='1y', interval='1d')
    # print(json.dumps(chart, indent=2))

    # print(chart['timestamp'])
    # print(chart['indicators']['quote'][0].keys())
    # print(chart['adjclose']['quote'][0])

    dividends = chart['events'].get('dividends')
    dividends_df = (
        pd.DataFrame(
            list(dividends.values()) if dividends else {'date': [], 'amount': []}
        )
        .set_index('date')
        .rename(columns={'amount': 'dividends'})
    )

    splits = chart['events'].get('splits')
    splits_df = (
        pd.DataFrame(list(splits.values()) if splits else {'date': [], 'numerator': []})
        .set_index('date')
        .rename(columns={'numerator': 'splits'})
    )

    chart_df = (
        pd.DataFrame({'date': chart['timestamp'], **chart['indicators']['quote'][0]})
        .set_index('date')
        .join(dividends_df)
        .join(splits_df)
        .fillna(value={'dividends': 0, 'splits': 0})
    )
    chart_df.index = pd.to_datetime(chart_df.index, unit='s')
    chart_df.columns = chart_df.columns.str.capitalize()
    chart_df = chart_df.rename(columns={'Splits': 'Stock Splits'})
    chart_df = chart_df.loc[
        :, ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    ]
    print(chart_df)
    print(chart_df.info())


if __name__ == '__main__':
    yfinance_main()
    asyncio.run(yafin_main())
