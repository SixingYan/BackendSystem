#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from moretime.wrong import error
from typing import Dict


class MoretimeException(Exception):
    pass

# order


class MoretimeOrderException(MoretimeException):
    pass


class NoExistOrder(MoretimeOrderException):

    def __init__(self, order_no):
        self.error = error.NoExistOrder
        self.order_no = order_no


class NoExistOrderPoster(MoretimeOrderException):

    def __init__(self, order_no):
        self.error = error.NoExistOrderPoster
        self.order_no = order_no


class MoretimeOrderPosterCreateFailed(MoretimeOrderException):

    def __init__(self, order_no):
        self.error = error.MoretimeOrderPosterCreateFailed
        self.order_no = order_no

# reply


class MoretimeReplyException(MoretimeException):
    pass


class NoExistReply(MoretimeReplyException):

    def __init__(self, reply_id):
        self.error = error.NoExistReply
        self.reply_id = reply_id


class MoretimeReplySubmitFailed(MoretimeReplyException):

    def __init__(self, poster_id):
        self.error = error.MoretimeReplySubmitFailed
        self.poster_id = poster_id


# poster


class MoretimePosterException(MoretimeException):
    pass


class NoExistPoster(MoretimePosterException):

    def __init__(self, poster_id):
        self.error = error.NoExistPoster
        self.poster_id = poster_id


class MoretimePosterAlreadyExisted(MoretimePosterException):

    def __init__(self, order_no):
        self.error = error.MoretimePosterAlreadyExisted
        self.order_no = order_no


class MoretimePosterSubmitFailed(MoretimePosterException):

    def __init__(self, order_no):
        self.error = error.MoretimePosterSubmitFailed
        self.order_no = order_no


# rate


class MoretimeRateException(MoretimeException):
    pass


class MoretimeRateSubmitFailed(MoretimeRateException):

    def __init__(self, poster_id):
        self.error = error.MoretimeRateSubmitFailed
        self.poster_id = poster_id


class MoretimeRateAlreadyExisted(MoretimeRateException):

    def __init__(self, order_no):
        self.error = error.MoretimeRateAlreadyExisted
        self.order_no = order_no


# others

class InputContentError(MoretimeException):

    def __init__(self, words):
        self.error = error.InputContentError
        self.words = words


class NoExistUser(MoretimeException):

    def __init__(self, user_id):
        self.error = error.NoExistUser
        self.user_id = user_id


class MoretimeAuthorityException(MoretimeException):

    def __init__(self, which: str, where: str, who: str):
        self.error = error.MoretimeAuthorityException
        self.which = which
        self.where = which
        self.who = who


class MoretimeVisibleUpdateFailed(MoretimeException):

    def __init__(self, index_id):
        self.error = error.MoretimeVisibleUpdateFailed
        self.index_id = index_id
