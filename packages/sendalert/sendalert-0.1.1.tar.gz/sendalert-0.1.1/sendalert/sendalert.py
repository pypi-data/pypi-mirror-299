from . import sendalert as _sendalert

def sendalert(text, project="default", mode="default"):
    return _sendalert(text, project, mode)