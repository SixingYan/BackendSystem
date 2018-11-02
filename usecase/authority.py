#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
无权操作，直接raise！
注意：visible_usecase都是 第三者本位的，所有的查询逻辑都是 公众可见？是公众吗？
'''
from sqlalchemy.orm import Session
from flask import request
from . import order as order_usecase
from . import reply as reply_usecase
from . import visible as visible_usecase
from . import poster as poster_usecase

from moretime.config.const import PublicVisible

from moretime.wrong import exception


def has_authority(db: Session, action: str, index_id: int) -> bool:
    """  """
    if action != 'obtain_poster_public': 
        user_id = request.current_user_id

    if action == 'obtain_order':
        has_auth_obtain_order_poster(db, user_id, index_id)

    if action == 'submit_rate':
        has_auth_submit_rate(db, user_id, index_id)

    if action == 'obtain_reply':
        has_auth_obtain_reply(db, user_id, index_id)

    if action == 'submit_reply':
        has_auth_submit_reply(db, user_id, index_id)

    if action == 'obtain_poster':
        has_auth_obtain_poster(db, user_id, index_id)

    if action == 'obtain_order_poster':
        has_auth_obtain_order_poster(db, user_id, index_id)

    if action == 'obtain_poster_public':
        has_auth_obtain_poster_public(db, index_id)

    if action == 'submit_poster':
        has_auth_submit_poster(db, user_id, index_id)

    if action == 'change_visible':
        has_auth_change_visible(db, user_id, index_id)


def has_auth_obtain_order_poster(
        db: Session, user_id: int, order_no: int)->None:
    """
    是否有权限查看当前order是否有poster
    -> 他是order的seller
    """
    result = False
    #---------
    m_order = order_usecase.obtain_order(db, order_no=order_no)
    if m_order is None:
        raise exception.NoExistOrder(order_no)

    if m_order.seller_id == user_id:
        result = True
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_obtain_order_poster',
            which=str(order_no),
            who=str(user_id))


def has_auth_submit_rate(db: Session, user_id: int, order_no: int):
    """
    是否有权限对poster对应的order进行评分
    -> 他是order的buyer
    """
    result = False
    #---------
    m_order = order_usecase.obtain_order(
        db, order_no=order_no)
    if m_order is None:
        raise exception.NoExistOrder(order_no)

    if m_order.buyer_id == user_id:
        result = True
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_submit_rate',
            which=str(order_no),
            who=str(user_id))


def has_auth_obtain_reply(db: Session, user_id: int, reply_id: int):
    """
    是否有权限查看这条评论
    -> 是否是卖家/买家  还是 公众
    -> poster属于公开状态
    """
    result = False
    #---------
    m_reply = reply_usecase.obtain_simple(
        db, reply_id=reply_id)
    if m_reply is None:
        raise exception.NoExistReply(reply_id)

    m_poster = poster_usecase.obtain_simple(db, poster_id=m_reply.poster_id)
    if m_poster is None:
        raise exception.NoExistPoster(m_reply.poster_id)

    result = visible_usecase.check_visible(
        m_poster, role=True, content=True)
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_obtain_reply',
            which=str(reply_id),
            who=str(user_id))


def has_auth_submit_reply(db: Session, user_id: int, poster_id: int):
    """
    这地方没改完，把具体逻辑移到这儿，别在其他地方实现
    是否有权限提交评论
    ->  只有卖家/家长可以评论 当role=False(非公众)
    -> 【预留】【公开状态】第三者可以评论
    -> 家长没回复之前不能卖家不能回复
    """
    result = False
    #---------
    m_poster = poster_usecase.obtain_simple(
        db, poster_id=poster_id)
    if m_poster is None:
        raise exception.NoExistPoster(poster_id)

    if user_id == m_poster.from_user_id:  # 卖家不能第一次评论
        reply_list = reply_usecase.obtain_simple(db, poster_id=poster_id)
        if reply_list is not None and reply_list != []:
            result = True

    elif user_id == m_poster.to_user_id:   # 买家直接评论
        result = True

    else:
        if m_poster.content_visible == PublicVisible.Yes.value:
            result = True
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_submit_reply',
            which=str(poster_id),
            who=str(user_id))


def has_auth_delete_reply(db: Session, user_id: int, reply_id: int):
    pass


def has_auth_obtain_poster(db: Session, user_id: int, poster_id: int):
    """
    是否有权限查看poster
    -> 卖家直接看不能公开部分
    -> #买家需要先评分才能看不能公开部分
    -> 公众能看公开，需要检查content是否已公开
    """
    result = False
    #---------
    m_poster = poster_usecase.obtain_simple(
        db, poster_id=poster_id)
    if m_poster is None:
        raise exception.NoExistPoster(poster_id)

    if m_poster.from_user_id == user_id:  # 卖家
        result = True

    elif m_poster.to_user_id == user_id:  # 买家
        # m_rate = rate_usecase.obtain_simple(
        #    db, order_no=m_poster.index_id)
        # if m_rate is not None:  # 已评分
        #    result = True
        result = True

    elif m_poster.content_visible == PublicVisible.Yes.value:  # 公众可见
        result = True

    else:
        pass
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_obtain_poster',
            which=str(poster_id),
            who=str(user_id))


def has_auth_obtain_poster_public(
        db: Session, poster_id: int):
    """
    是否有权限查看poster
    -> 需要检查content是否已公开
    """
    result = False
    #---------
    m_poster = poster_usecase.obtain_simple(
        db, poster_id=poster_id)
    if m_poster is None:
        raise exception.NoExistPoster(poster_id)

    if m_poster.content_visible == PublicVisible.Yes.value:
        result = True
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_obtain_poster_public',
            which=str(poster_id),
            who='')


def has_auth_submit_poster(db: Session, user_id: int, order_no: int):
    """
    是否有权限对order_no提交poster
    -> 他是order的seller
    """
    result = False
    #---------
    m_order = order_usecase.obtain_order(db, order_no=order_no)
    if m_order is None:
        raise exception.NoExistOrder(order_no)
    
    if m_order.seller_id == user_id:
        result = True
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_submit_poster',
            which=str(order_no),
            who=str(user_id))


def has_auth_change_visible(db, user_id: int, poster_id: int):
    """
    是否有权限改变poster可见性
    -> 家长能改变可见性
    """
    result = False
    #---------
    m_poster = poster_usecase.obtain_simple(
        db, poster_id=poster_id)
    
    if m_poster is None:
        raise exception.NoExistPoster(poster_id)

    if m_poster.to_user_id == user_id:
        result = True
    #---------
    if not result:
        raise exception.MoretimeAuthorityException(
            where='has_auth_change_visible',
            which=str(poster_id),
            who=str(user_id))
