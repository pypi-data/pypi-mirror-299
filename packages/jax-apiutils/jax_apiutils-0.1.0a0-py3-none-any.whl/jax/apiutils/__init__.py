"""JAX API Utility Package."""

from importlib import metadata
__version__ = metadata.version("jax-apiutils")

try:
    import fastapi as _
    from jax.apiutils.fastapi import *
except ImportError:
    pass
