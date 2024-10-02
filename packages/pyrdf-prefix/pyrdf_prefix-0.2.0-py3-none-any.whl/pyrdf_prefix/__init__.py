from importlib.metadata import version

from .namespace import PredefinedNamespace, Prefix
from .predefined import *

__version__ = version("pyrdf_prefix")
__all__ = ["Prefix"]
