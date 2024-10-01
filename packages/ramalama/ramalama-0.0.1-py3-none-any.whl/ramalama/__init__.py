"""ramalama client module."""

from ramalama.main import main_cli
import sys

assert sys.version_info >= (3, 6), "Python 3.6 or greater is required."

__all__ = ["main_cli"]
