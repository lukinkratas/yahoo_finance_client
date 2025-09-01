import logging

logger = logging.getLogger(__name__)

def error(msg:str, err_cls=Exception) -> None:
    logger.error(msg)
    raise err_cls(msg)

def print_url(url:str, params:dict[str,str]=None, print_fn=print) -> None:

    print_str = url

    if params:
        params_str = '&'.join(f'{key}={value}' for key, value in params.items())
        print_str += f'?{params_str}'
    
    print_fn(print_str)