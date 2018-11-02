#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import marshmallow
from flask import jsonify, g, request

from moretime.wrong import error, exception
from moretime.api.schema import (
    PosterGetSchema,
    PosterPostSchema,
    PosterSchema,
    PosterVisibleSchema,
    PosterDeleteSchema,
    PosterShareSchema,
    PageRequestSchema,
    PosterAndReplySchema,
    AppDownloadRecordSchema
)

from moretime.api.decorator import authenticated
from moretime.api.response import OKResponse, DataResponse, ErrorResponse
from moretime.api.wapp import logworker
import moretime.usecase.authority as auth_usecase
import moretime.usecase.poster as poster_usecase
import moretime.usecase.order as order_usecase

from moretime.config.const import RoleVisible, VisibleLevel, VisiblePart, PublicVisible, SET_VISIBLE

from . import blueprint as bp


@bp.route('/poster', methods=['GET'])
@authenticated
def poster_get():
    # 1. check data - poster id
    try:
        req = PosterGetSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.error(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'obtain_poster', req.poster_id)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. querying
    poster = poster_usecase.obtain(g.db, poster_id=req.poster_id)

    # 4. prepare return data
    data = PosterSchema().dump(poster)

    return jsonify(DataResponse(data))


@bp.route('/poster', methods=['POST'])
@authenticated
def poster_post():

    # 1. check data
    try:
        req = PosterPostSchema().load(request.json)
    except marshmallow.ValidationError as err:
        logworker.error(request.json)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'submit_poster', req.order_no)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. create querying
    try:
        poster = poster_usecase.submit(g.db, request.current_user_id, req)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 4. create querying    #【这里尝试使用异步的方式调用】【去除】 此时可以返回了
    try:
        order_usecase.submit(
            g.db, req.order_no, poster.id,
            request.current_user_id, poster.to_user_id)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    #result = PosterCreateSchema().dump(poster.id)

    return jsonify(DataResponse({"posterID": poster.id}))


@bp.route('/poster/delete', methods=['POST'])
@authenticated
def poster_delete():
    # 1. check data - poster id
    try:
        req = PosterDeleteSchema().load(request.json)
    except marshmallow.ValidationError as err:
        logworker.error(request.json)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authorty
    try:
        auth_usecase.has_authority(
            g.db, 'delete_poster', req.poster_id)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # querying
    try:
        poster_usecase.delete(g.db, req.poster_id)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    return jsonify(OKResponse(True))


@bp.route('/poster/visible', methods=['POST'])
@authenticated
def poster_visible():
    # 1. check data - poster id
    try:
        req = PosterVisibleSchema().load(request.json)
    except marshmallow.ValidationError as err:
        logworker.error(request.json)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authorty
    # None 由visible控制是否可以操作

    # 3. update querying
    try:
        poster_usecase.visible(
            g.db, req.poster_id, req.is_content, SET_VISIBLE[req.set_visible])
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    return jsonify(OKResponse(True))


@bp.route('/poster/user', methods=['GET'])
@authenticated
def poster_user_get():

    # 1. check data - offset limit
    try:
        req = PageRequestSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.exception(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    # None 查看自己的 不用验证

    # 3. querying
    try:
        data = poster_usecase.obtain(
            g.db, to_user_id=request.current_user_id,
            visible=RoleVisible.Buyer.value, offset=req.offset, limit=req.limit)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 4. prepare return data
    data = PosterSchema(many=True).dump(data)

    return jsonify(DataResponse(data))


@bp.route('/poster/share', methods=['GET'])
@authenticated
def poster_share():
    """ """
    # 1. check data
    try:
        req = PosterGetSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.exception(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority 使用[更改可见性]权限
    try:
        auth_usecase.has_authority(
            g.db, 'change_visible', req.poster_id)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. change visible
    try:
        poster_usecase.visible(
            g.db, req.poster_id,
            VisiblePart.Media.value, PublicVisible.Yes.value)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 4. query share information
    try:
        data = poster_usecase.obtain(
            g.db, poster_id=req.poster_id, share=True,
            visible=VisibleLevel.Private.value)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    data = PosterShareSchema().dump(data)

    return jsonify(DataResponse(data))


@bp.route('/poster/reply', methods=['GET'])
# @authenticated 公众访问，不用登陆 H5 分享页
def poster_reply():
    """summary: 同时获得指定poster内容和它的所有回复 分享页H5"""
    # 1. check data
    try:
        req = PosterGetSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.exception(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority 目前是否可查看
    try:
        auth_usecase.has_authority(
            g.db, 'obtain_poster_public', req.poster_id)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. query
    try:
        data = poster_usecase.obtain(
            g.db, poster_id=req.poster_id,
            visible=VisibleLevel.Public.value, share=True, wechat=True)
    except exception.MoretimeException as exc:
        logworker.exception(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    data = PosterAndReplySchema().dump(data)

    return jsonify(DataResponse(data))


@bp.route('/poster/reply/download', methods=['GET'])
# @authenticated 公众下载统计，不用登陆
def poster_reply_download():
    """【预留】目前不实现"""
    """
    # 1. check data
    try:
        req = AppDownloadRecordSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.exception(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    # None

    # 3. query
    # 【预留】:记录点击下载的poster_id
    """
    return jsonify(OKResponse(True))
