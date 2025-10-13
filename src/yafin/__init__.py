import importlib.metadata

from .client import AsyncClient
from .stonk import Stonk

__all__ = ['AsyncClient', 'Stonk']
__version__ = importlib.metadata.version(__package__ or __name__)
