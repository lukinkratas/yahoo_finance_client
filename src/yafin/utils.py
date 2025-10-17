import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, NoReturn, Type

import pandas as pd

from .const import FREQUENCIES, TYPES

logger = logging.getLogger(__name__)


def error(msg: str, err_cls: Type[Exception] = Exception) -> NoReturn:
    """Log error message and raise exception.

    Args:
        msg: error message (hint), that will be logged and raised.
        err_cls: class of the raised error, default Exception.
    """
    logger.error(msg)
    raise err_cls(msg)


def compile_url(url: str, params: dict[str, str] | None = None) -> str:
    """Print URL with parameters.

    Args:
        url: base url, where query param will be added.
        params: http request query parameters.

    Returns: url with params
    """
    url_with_params = url

    if params:
        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        url_with_params += f'?{params_str}'

    return url_with_params


def get_types_with_frequency(frequency: str, typ: str) -> str:
    """Enrich types with frequency.

    Args:
        frequency:
            frequency used for timeseries endpoint, e.g.: annual, quarterly or trailing.
        typ:
            type of types, e.g.: income_statement, balance_sheet or cash_flow,
            which is used for fetching all types for given financial.
            e.g. for income_statement: NetIncome,EBIT,EBITDA,GrossProfit, ...

    Returns:
        types enriched with frequency e.g. for income_statement:
        trailingNetIncome,trailingEBIT,trailingEBITDA,trailingGrossProfit, ...
    """
    if frequency not in FREQUENCIES:
        error(
            msg=f'Invalid {frequency=}. Valid values: {FREQUENCIES}', err_cls=ValueError
        )

    if typ not in TYPES.keys():
        error(msg=f'Invalid {typ=}. Valid values: {TYPES.keys()}', err_cls=ValueError)

    if typ == 'balance_sheet' and frequency == 'trailing':
        error(msg=f'{frequency=} not allowed for balance sheet.', err_cls=ValueError)

    types = TYPES[typ]
    types_with_frequency = [f'{frequency}{t}' for t in types]
    return ','.join(types_with_frequency)


def _get_func_name_and_args(
    func: Callable[..., Any], args: tuple[Any, ...]
) -> tuple[str, tuple[Any, ...]]:
    """Helper function, that takes function and its' arguments.
    It then checks, whether the first argument is a class instance.
    If so, then it returns class_name.method_name and arguments exclusing the first one.
    If not, then it returns function_name and arguments in unchaged form.

    Args:
        func: python function
        args: arguments to the function

    Returns: function name and arguments
    """
    # check if first argument is class instance (self)
    if args and hasattr(args[0], func.__name__):
        func_name = f'{args[0].__class__.__name__}.{func.__name__}'
        return func_name, args[1:]

    return func.__name__, args


def track_args(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for logging functions and its' args, kwargs."""

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name, args_copy = _get_func_name_and_args(func, args)

        logger.debug(f'{func_name}() was called with args={args_copy} and {kwargs=}.')
        result = await func(*args, **kwargs)
        logger.debug(f'{func_name} finished with {result=}.')

        return result

    return async_wrapper


def process_chart_like_yfinance(chart: dict[str, Any]) -> pd.DataFrame:
    """Process chart response json into pandas dataframe, exact as yfinance."""
    dividends = chart['events'].get('dividends')
    dividends_df = pd.DataFrame(
        dividends.values() if dividends else {'date': [], 'amount': []}
    ).rename(columns={'amount': 'dividends'})

    splits = chart['events'].get('splits')
    splits_df = pd.DataFrame(
        splits.values()
        if splits
        else {'date': [], 'numerator': [], 'denominator': [], 'splitRatio': []}
    )
    splits_df['splits'] = splits_df['numerator'] / splits_df['denominator']

    chart_df = (
        pd.DataFrame({'date': chart['timestamp'], **chart['indicators']['quote'][0]})
        .set_index('date')
        .join(dividends_df.set_index('date').loc[:, 'dividends'])
        .join(splits_df.set_index('date').loc[:, 'splits'])
        .fillna(value={'dividends': 0, 'splits': 0})
    )
    chart_df.index = pd.to_datetime(chart_df.index, unit='s')
    chart_df.columns = chart_df.columns.str.capitalize()
    chart_df = chart_df.rename(columns={'Splits': 'Stock Splits'})
    return chart_df.loc[
        :,
        ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
    ]
