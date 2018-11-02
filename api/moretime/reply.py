import marshmallow
from flask import jsonify, g, request

from moretime.wrong import error, exception
from moretime.api.wapp import logworker
from moretime.config.const import (
    SubmitRate, SetVisible,
    VisiblePart, ReplyToPoster, VisibleLevel, SET_VISIBLE, PublicVisible)

from moretime.api.schema import (
    PosterReplySchema,
    PosterReplyRateSchema,
    ReplyPostSchema,
    ReplyGetSchema,
    ReplyCreateSchema,
    ReplyDeleteSchema,
    ReplyToUserGetSchema,
    PosterGetSchema,
    ReplySchema
)
from moretime.api.decorator import authenticated
from moretime.api.response import OKResponse, DataResponse, ErrorResponse

import moretime.usecase.authority as auth_usecase
import moretime.usecase.reply as reply_usecase
import moretime.usecase.rate as rate_usecase
import moretime.usecase.poster as poster_usecase

from . import blueprint as bp


@bp.route('/reply', methods=['GET'])
@authenticated
def reply_get():
    ''' obtain by reply id'''
    # 1. check data
    try:
        req = ReplyGetSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.error(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'obtain_reply', req.poster_id)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. querying
    try:
        data = reply_usecase.obtain(
            g.db, reply_id=req.reply_id)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(error.MoretimeReplySubmitFailed, data=str(exc)))

    # 4. prepare return data
    data = ReplySchema(many=True).dump(data)

    return jsonify(DataResponse(data))


@bp.route('/reply', methods=['POST'])
@authenticated
def reply_post():
    # 1. check data
    try:
        req = ReplyPostSchema().load(request.json)
    except marshmallow.ValidationError as err:
        logworker.error(request.json)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'submit_reply', req.poster_id)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # temp!?. can it reply again?
    if reply_usecase.has_already_submit(g.db, req.poster_id) is True:
        return jsonify(ErrorResponse(error.MoretimeReplyOnlyOnce))

    # 3. querying
    try:
        reply = reply_usecase.submit(
            g.db, request.current_user_id, req)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 5. set content visible [force!] 第一条评论更新文字可见性
    if req.prior_id == ReplyToPoster.Prior.value:
        # 有可能是第一条评论
        if reply_usecase.is_first_submit(g.db, req.poster_id) is True:
            try:
                poster_usecase.visible(
                    g.db, req.poster_id,
                    VisiblePart.Content.value, PublicVisible.Yes.value,)
            except exception.MoretimeException as exc:
                logworker.error(req)
                return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 6. set picvid visible    异步
    if req.set_visible is not None:
        try:
            poster_usecase.visible(
                g.db, req.poster_id,
                VisiblePart.Media.value, SET_VISIBLE[req.set_visible])
        except exception.MoretimeException as exc:
            logworker.error(req)
            return jsonify(ErrorResponse(exc.error, data=str(exc)))

    result = ReplyCreateSchema().dump(
        {'reply_id': reply.id, 'to_user_id': reply.to_user_id})

    return jsonify(DataResponse(result))


@bp.route('/reply/delete', methods=['POST'])
@authenticated
def reply_delete():
    # 1. check data
    try:
        req = ReplyDeleteSchema().load(request.args)
    except marshmallow.ValidationError as err:
        logworker.error(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    try:
        auth_usecase.has_authority(
            g.db, 'delete_reply', req.reply_id)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 3. querying
    try:
        reply_usecase.delete(g.db, req.reply_id)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    return jsonify(OKResponse(True))


@bp.route('/reply/poster', methods=['GET'])
@authenticated
def reply_poster_get():
    # 1. check data
    try:
        req = PosterGetSchema().load(request.args)  # 涉及公众
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
    try:
        data = reply_usecase.obtain(
            g.db, poster_id=req.poster_id,
            offset=req.offset, limit=req.limit)  # 检查
        # visible=VisibleLevel.Private.value)
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 4. prepare return data
    data = PosterReplyRateSchema(many=True).dump(data)

    return jsonify(DataResponse(data))


@bp.route('/reply/user', methods=['GET'])
#@authenticated
def reply_user_get():
    # 1. check data
    try:
        req = ReplyToUserGetSchema().load(request.args)  # 涉及公众
    except marshmallow.ValidationError as err:
        logworker.error(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    # None  任何身份都可以尝试访问

    # 3. querying
    try:
        data = reply_usecase.obtain(
            g.db, to_user_id=req.user_id,
            visible=VisibleLevel.Public.value,
            offset=req.offset, limit=req.limit)  # 检查
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 4. prepare return data
    data = PosterReplyRateSchema(many=True).dump(data)

    return jsonify(DataResponse(data))


@bp.route('/reply/user/count', methods=['GET'])
#@authenticated
def reply_user_count_get():
    # 1. check data
    try:
        req = ReplyToUserGetSchema().load(request.args)  # 涉及公众
    except marshmallow.ValidationError as err:
        logworker.error(request.args)
        return jsonify(ErrorResponse(error.InvalidParameter, data=err.messages))

    # 2. check authority
    # None  任何身份都可以尝试访问

    # 3. querying
    try:
        data = reply_usecase.obtain(
            g.db, to_user_id=req.user_id,
            visible=VisibleLevel.Public.value, count=True)  # 检查
    except exception.MoretimeException as exc:
        logworker.error(req)
        return jsonify(ErrorResponse(exc.error, data=str(exc)))

    # 4. prepare return data
    #data = PosterReplySchema(many=True).dump(data)

    return jsonify(DataResponse({'count': data}))
