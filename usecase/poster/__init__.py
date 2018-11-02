"""
	这里是入口，在这里转发具体操作
"""
from . import obtain as o
from . import submit as s
from . import update as u
from . import visible as v
from . import delete as d

def obtain(*args, **kwargs):
    return o.obtain(*args, **kwargs)


def obtain_simple(*args, **kwargs):
    return o.obtain_simple(*args, **kwargs)


def submit(*args, **kwargs):
    return s.submit(*args, **kwargs)


def update(*args, **kwargs):
    return u.update(*args, **kwargs)


def visible(*args, **kwargs):
    return v.visible(*args, **kwargs)


def delete(*args, **kwargs):
    return d.delete(*args, **kwargs)
