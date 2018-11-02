"""
    这里是入口，在这里转发具体操作
"""
from . import poster
from . import reply


def poster_toread(*args, **kwargs):
    return poster.toread(*args, **kwargs)


def poster_unread_count(*args, **kwargs):
    return poster.unread_count(*args, **kwargs)


def poster_unread_clean(*args, **kwargs):
    return poster.unread_clean(*args, **kwargs)


def reply_toread(*args, **kwargs):
    return reply.toread(*args, **kwargs)
