#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import marshmallow
from flask import jsonify, g, request


from moretime.wrong import error, exception
from moretime.api.wapp import logworker
from moretime.api.decorator import authenticated
from moretime.api.response import OKResponse, ErrorResponse, DataResponse
from moretime.api.schema import OrderGetSchema, RatePostSchema

from moretime.usecase import authority as auth_usecase
from moretime.usecase import order as order_usecase
from moretime.usecase import rate as rate_usecase
from moretime.usecase import poster as poster_usecase

from . import blueprint as bp


@bp.route('/order', methods=['GET'])
@authenticated
def order_get():
    # 1. check data
    try:
        req = OrderGetSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.error(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'obtain_order', req.order_no)
    except exception.AuthorityException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. querying
    result = order_usecase.has_order_poster(g.db, req.order_no)

    return jsonify(OKResponse(result))


@bp.route('/order/poster', methods=['GET'])
@authenticated
def order_poster_get():
    # 1. check data
    try:
        req = OrderGetSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.error(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'obtain_order_poster', req.order_no)
    except exception.AuthorityException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. querying
    data = poster_usecase.obtain(g.db, order_no=req.order_no)

    return jsonify(DataResponse(data))


@bp.route('/order/rate', methods=['POST'])
@authenticated
def rate_post():
    # 1. check data
    try:
        req = RatePostSchema().load(request.json)
    except marshmallow.ValidationError as err:
        logworker.error(request.json)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'submit_rate', req.order_no)
    except exception.AuthorityException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. create rate
    try:
        rate_usecase.submit_rate(
            g.db, req.order_no, req.rate)
    except exception.MoretimeOrderException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    return jsonify(OKResponse(True))
