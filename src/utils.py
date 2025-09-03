import logging

logger = logging.getLogger(__name__)


def error(msg: str, err_cls=Exception) -> None:
    """Log error message and raise exception."""
    logger.error(msg)
    raise err_cls(msg)


def print_url(url: str, params: dict[str, str] | None = None, print_fn=print) -> None:
    """Print URL with parameters."""
    print_str = url

    if params:
        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        print_str += f'?{params_str}'

    print_fn(print_str)
