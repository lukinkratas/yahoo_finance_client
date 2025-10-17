import asyncio
import statistics
from collections.abc import Callable
from datetime import timedelta
from functools import wraps
from time import perf_counter
from typing import Any

from curl_cffi import requests
from yfinance import Ticker

from yafin import AsyncSymbol
from yafin.utils import _get_func_name_and_args, process_chart_like_yfinance

NRUNS = 1


def log_performance(n: int = 1) -> Callable[..., Any]:
    """Decorator for logging functions and its' performance."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name, _ = _get_func_name_and_args(func, args)
            run_times = []

            print(f'{func_name} running {n} time(s) started.')
            total_start_time = perf_counter()

            for idx in range(1, n + 1):
                print(f'  {func_name} run no.{idx} started.')
                run_start_time = perf_counter()

                result = func(*args, **kwargs)

                run_elapsed_time = perf_counter() - run_start_time
                run_times.append(run_elapsed_time)
                run_elapsed_time_td = timedelta(seconds=run_elapsed_time)
                print(
                    f'  {func_name} run no.{idx} finished with '
                    f'elapsed_time={run_elapsed_time_td}.'
                )

            total_elapsed_time = perf_counter() - total_start_time
            total_elapsed_time_td = timedelta(seconds=total_elapsed_time)
            avg_elapsed_time_td = timedelta(seconds=statistics.mean(run_times))
            print(
                f'{func_name} running {n} time(s) finished with '
                f'total={total_elapsed_time_td} and average={avg_elapsed_time_td}.'
            )

            return result

        return wrapper

    return decorator


@log_performance(NRUNS)
def main_yfinance() -> None:  # noqa: D103
    # async session does not work, throws
    #   yfinance.exceptions.YFDataException: Yahoo API requires curl_cffi session
    #   not <class 'curl_cffi.requests.session.AsyncSession'>.
    #   Solution: stop setting session, let YF handle.
    # session = requests.AsyncSession(impersonate="chrome")

    with requests.Session(impersonate='chrome') as session:
        meta = Ticker('META', session=session)
        history_df = meta.history(period='1y', interval='1d')

    print(history_df)
    print(history_df.info())

    session.close()


@log_performance(NRUNS)
async def main() -> None:  # noqa: D103
    async with AsyncSymbol('META') as symbol:
        chart = await symbol.get_chart(period_range='1y', interval='1d')
        chart_df = process_chart_like_yfinance(chart)

    print(chart_df)
    print(chart_df.info())


if __name__ == '__main__':
    main_yfinance()
    asyncio.run(main())
