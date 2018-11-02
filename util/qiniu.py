#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qiniu import Auth
from moretime.entity import Facade
from moretime.config.const import VisibleBucket

URL_DURATION = 7200


def url(bucket: str, key: str) -> str:
    """ 这个是生成video_url的时候使用，指定了bucket & key"""
    return_url = "{}/{}".format(Facade.config["qiniu"]
                                ["bucket"][bucket]["url"], key)

    if bucket == VisibleBucket.Private.value:
        return private_url(return_url)

    return return_url


def private_url(base_url: str, duration_sec: int = URL_DURATION):
    """  """
    q = Auth(Facade.config["qiniu"]["access_key"],
             Facade.config["qiniu"]["secret_key"])
    
    return q.private_download_url(base_url, expires=duration_sec)


def url_from_path(oss_path: str) -> str:
    """  """
    if oss_path == '' or oss_path is None:
        return ''

    splits = oss_path.split(":")
    bucket = splits[1]
    key = splits[2]

    return url(bucket, key)
