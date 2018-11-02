#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum


class SubmitRate(Enum):
    Passed = -1


class SetVisible(Enum):
    Passed = -1


class RoleVisible(Enum):
    Buyer = 1
    Seller = 1
    Others = -1


class MediaPart(Enum):
    # 这个地方也要调整
    Vframe = 'vframe'
    Picture = 'picture'
    Video = 'video'


class VisibleLevel(Enum):
    Private = 1
    Public = 2
    Others = 3


class VisiblePart(Enum):
    Media = False
    Content = True


class VisibleBucket(Enum):
    Private = 'private'  # "moretime-media-private"
    Public = 'public'  # "moretime-media-public"


class DatabaseStatus(Enum):
    Delete = -1
    Normal = 0


class PublicVisible(Enum):
    Yes = 1
    No = 0


class ChangeVisiblePart(Enum):
    Content = True
    Media = False


class ReplyToPoster(Enum):
    Prior = -1


class MoretimeRate(Enum):
    Default = -1


class ShareCopy(Enum):
    Title = " 在摩尔妈妈度过的美好时光，欢迎大家来看！"
    Description = "多才多艺的妈妈，给孩子不一样的童年"
    ThumbingApi = '?imageView2/1/w/200/h/200'
    DefaultImage = 'https://static.moremom.cn/comImage/default_thumbnail.jpg'

SET_VISIBLE = {True: 1, False: 0}
