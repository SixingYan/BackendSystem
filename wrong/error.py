#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Define API Errors

    An API error object is an instance of `namedtuple`.
"""

from collections import namedtuple

APIError = namedtuple("APIError", ["code", "msg", "wording"])

UnknownError = APIError(1, "Unknown Error", "服务器开小差了")
InvalidParameter = APIError(1001, "Invalid Parameter", "服务器开小差了")
InvalidSignature = APIError(1002, "Invalid Signature", "服务器开小差了")
Unauthorized = APIError(2001, "Unauthorized", "请先登录")
NoExistOrder = APIError(8001, "No Exist Order", "该订单号对应的订单不存在哦")
NoExistOrderPoster = APIError(8002, "No Existent Order-Poster", "该订单号对应的摩尔时光不存在哦")
NoExistPoster = APIError(8003, "No Exist Poster", "对应的摩尔时光不存在哦")
NoExistReply = APIError(8004, "NoExistReply", "对应的回复不存在哦")
MoretimePosterAlreadyExisted = APIError(8005, "Moretime Poster Already Existed", "相应的摩尔时光已经存在了哦")
MoretimePosterSubmitFailed = APIError(8006, "Moretime Poster Submit Failed", "提交的摩尔时光失败了哦")
MoretimeReplySubmitFailed = APIError(8007, "Moretime Reply Submit Failed", "回复评论失败了哦")
MoretimeRateSubmitFailed = APIError(8008, "Moretime Rate Submit Failed", "评分失败了哦")
MoretimeRateAlreadyExisted = APIError(8009, "Moretime Rate Already Existed", "评分已经存在了哦")
InputContentError = APIError(8010, "Input Content Error", "输入的内容不能少于9个字哦")
MoretimeOrderPosterCreateFailed = APIError(8011, "Moretime Order-Poster Create Failed", "订单-摩尔时光 对应关系创建失败，管理员正在处理，请勿重复提交摩尔时光哦")
NoExistUser = APIError(8012, "No Exist User", "对应的用户信息不存在呢")
MoretimeVisibleUpdateFailed = APIError(8013, "Moretime Visible Update Failed", "摩尔时光 可见性更改失败，请在反馈中给管理员留言哦")
NoExistTimeSharing = APIError(8013, "No Exist Time Sharing", "对应的时间共享信息不存在哦")
MoretimeReplyOnlyOnce = APIError(8014, "MoretimeReplyOnlyOnce", "只能回复一次哦")
MoretimeAuthorityException = APIError(8500, "Moretime Authority Limit", "似乎没有权限访问这里哦")
