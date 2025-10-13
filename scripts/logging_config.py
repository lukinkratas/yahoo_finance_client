from logging.config import dictConfig


def setup_logging() -> None:
    """Setup logging config."""
    cfg = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': (
                    '%(asctime)s | %(levelname)-8s | %(name)-12s | '
                    '%(filename)s:%(lineno)d | %(funcName)s | %(message)s'
                ),
            },
            'simple': {
                'format': '%(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': 'DEBUG',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'main.log',
                'formatter': 'default',
                'level': 'DEBUG',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
            },
        },
    }
    dictConfig(cfg)
