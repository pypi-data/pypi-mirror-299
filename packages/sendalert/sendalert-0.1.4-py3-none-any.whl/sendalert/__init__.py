from .core import sendalert as _sendalert

def sendalert(*args, **kwargs):
    return _sendalert(*args, **kwargs)

__all__ = ['sendalert']