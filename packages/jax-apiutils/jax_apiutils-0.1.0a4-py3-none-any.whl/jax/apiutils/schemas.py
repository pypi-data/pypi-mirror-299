"""JAX API schemas."""

try:
    import fastapi as _
    from jax.apiutils.fastapi.schemas import *
except ImportError:
    pass
