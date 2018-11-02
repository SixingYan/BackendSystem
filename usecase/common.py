#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict
from urllib.parse import quote

from moretime.wrong import exception
from moretime.util import DictObject

from moretime.api.wapp import logworker


def clean_content(words: str):
    """ 内容清理 """
    if words is None:
        raise exception.InputContentError(words)
    w = words.strip()
    if len(w) < 9:
        raise exception.InputContentError(words)
    return words


def prepare_sort_object(
        order_list: List[str], picture_objs: List[DictObject]=None,
        video_objs: List[DictObject]=None)->List[DictObject]:
    """ 将obj取出返回前端时 """
    
    # 0. 如果都是空的就直接返回
    if (picture_objs is None or picture_objs == []) and (video_objs is None or video_objs == []):
        return []

    result = [0 for _ in range(len(order_list))]

    # 1. 先排图片
    idx = 0
    if picture_objs is not None and picture_objs != []:
        for i in range(len(picture_objs)):
            result[int(order_list[idx])] = picture_objs[i]
            idx += 1

    # 2. 排视频
    idx = len(picture_objs)  # 从图片后开始排
    if video_objs is not None and video_objs != []:
        for i in range(len(video_objs)):
            result[int(order_list[idx])] = video_objs[i]
            idx += 1

    return result  # [video, picture, video, video, picture...]


def sort_reply(reply_obj_list: List[DictObject]):
    """ 个人主页-评论-评论排序 目前使用 时间戳 排序"""
    return sorted(reply_obj_list, key=lambda r: r.reply.create_ts, reverse=True)

    """
    score_list = []
    for i in range(len(reply_obj_list)):
        reply = reply_obj_list[i]
        score = 0
        if reply.content:
            pass
        if reply.media_obj_list:
            pass
        if reply.create_ts:
            pass
        score_list.append(score)
    """


def cosort(ref_list, data_list):
    """ 联合排序 """
    pass


def change_CN_url(url: str):
    """
    进行编码的url
    """
    cn_url = quote(url, 'utf-8')
    return cn_url
