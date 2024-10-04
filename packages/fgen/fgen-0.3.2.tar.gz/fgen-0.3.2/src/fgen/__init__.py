"""
An opinionated framework for wrapping Fortran-based code with Python.
"""
import importlib.metadata

from loguru import logger

logger.disable(__name__)

__version__ = importlib.metadata.version("fgen")
