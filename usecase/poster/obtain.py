from typing import List, Dict
from sqlalchemy.orm import Session

from moretime.entity import Facade
from moretime.wrong import exception
from moretime.util import DictObject
from moretime.api.wapp import logworker

from moretime.orm import poster as poster_orm
from moretime.orm import rate as rate_orm
from moretime.orm import order as order_orm

from moretime.config.const import VisibleLevel, MoretimeRate, ShareCopy

import moretime.usecase.video as video_usecase
import moretime.usecase.picture as picture_usecase
import moretime.usecase.order as order_usecase
import moretime.usecase.visible as visible_usecase
import moretime.usecase.common as common_usecase
import moretime.usecase.user as user_usecase
from moretime.usecase import reply as reply_usecase


def obtain(
        db: Session, from_user_id: int=None, to_user_id: int=None,
        poster_id: int=None, visible: int=None,
        share: bool=False, wechat: bool=False, order_no: int=None, offset: int=None, limit: int=None)->List:
    """
        1. 指定poster
        2. 用户发出的poster
        3. 用户收到的poster
    """
    data = []

    if order_no is not None:
        data = obtian_by_order_no(db, order_no)

    if poster_id is not None:  # 有人访问了指定的poster
        data = obtain_by_id(db, poster_id, visible)

    if to_user_id is not None:  # 访问自己的poster
        data = obtain_by_to_user_id(db, to_user_id, visible, offset, limit)

    if poster_id is not None and share is True and wechat is True:  # 从分享页访问
        data = obtian_poster_reply_by_id(db, poster_id, visible)

    if poster_id is not None and share is True and wechat is False:  # 分享信息
        data = obtain_share(db, poster_id, visible)

    if from_user_id is not None:  # 【预留】
        data = obtain_by_from_user_id(db, from_user_id, visible)

    return data


def obtain_share(db, poster_id, visible):
    """ 点击分享时，返回分享所需信息，信息体只包含：
    """
    # 0. raw data
    m_poster = obtain_by_id(db, poster_id, visible)

    # 1. title
    m_order = order_usecase.retrieve_order(db, m_poster.order_no)
    if m_order is None:
        raise exception.NoExistOrder(m_poster.order_no)
    title = m_order.child_nickname + ShareCopy.Title.value

    description = ShareCopy.Description.value
    webpage_url = Facade.config["wechat"][
        "url"] + str(poster_id) + '&child=' + common_usecase.change_CN_url(m_poster.child_nickname)
    #webpage_url = common_usecase.change_CN_url(m_poster.child_nickname)

    thumb_image_url = ''
    if m_poster.media_obj_list != []:
        media = m_poster.media_obj_list[0]
        thumb_image_url = media.cover_url + ShareCopy.ThumbingApi.value
    else:
        thumb_image_url = ShareCopy.DefaultImage.value

    data = DictObject(
        title=title,
        description=description,
        webpage_url=webpage_url,
        thumb_image_url=thumb_image_url
    )

    return data


def obtain_by_id(
        db: Session,
        poster_id: int, visible_choose: int=None)->Dict:
    """ 通过poster的id来找到并包装poster
        0. basic information
        1. child_nickname & start_ts
        2. 
    """
    # 0. basic information
    m_poster = obtain_simple(db, poster_id=poster_id)
    if m_poster is None:
        raise exception.NoExistPoster(poster_id)

    # 1. child_nickname
    m_order = order_usecase.retrieve_order(db, m_poster.index_id)
    if m_order is None:
        raise exception.NoExistOrder(m_poster.index_id)
    child_nickname = m_order.child_nickname

    # 1. 订单时间
    m_timeshare = order_usecase.retrieve_timeshare(db, m_order.time_sharing_id)
    if m_timeshare is None:
        raise exception.NoExistTimeSharing(m_order.time_sharing_id)
    start_ts = m_timeshare.start_ts

    # 2. visible
    if visible_choose is None:
        visible_choose = visible_usecase.obtain_visible_choose(
            m_poster)

    # 3. packing video
    video_obj_list = video_usecase.video_ids_to_objs(
        db, m_poster, visible_choose)

    # 4. packing picture
    picture_obj_list = picture_usecase.picture_ids_to_objs(
        db, m_poster, visible_choose)

    # 5. sort media
    media_obj_list = []
    if m_poster.sort_order != '' or m_poster.sort_order is not None and (video_obj_list is not None or picture_obj_list is not None):

        order_list = [int(i) for i in m_poster.sort_order.split(',')] \
            if m_poster.sort_order is not None and m_poster.sort_order != '' else []

        media_obj_list = common_usecase.prepare_sort_object(
            order_list, picture_obj_list, video_obj_list)

    # 6. user 头像信息
    user = user_usecase.obtain_user(db, m_poster.from_user_id)
    if user is None:
        raise exception.NoExistUser(m_poster.from_user_id)

    # 7. 评分
    rate = MoretimeRate.Default.value
    m_rate = rate_orm.find_rate_by_order_no(db, m_poster.index_id)
    if m_rate is not None:
        rate = m_rate.rate

    # 8. packing poster
    poster = packing(m_poster, child_nickname, start_ts,
                     media_obj_list, user, rate)

    return poster


def obtian_by_order_no(db: Session, order_no: int):
    """  """
    m_order_poster = order_orm.find_order_poster_by_order_no(db, order_no)
    if m_order_poster is None:
        raise exception.NoExistOrderPoster(order_no)

    return obtain_by_id(db, m_order_poster.poster_id)


def obtain_by_user_id(db, user_id):
    """ 这个是什么时候会使用？ """
    data = []

    m_poster_list = poster_orm.find_poster_by_to_user_id(
        db, to_user_id=user_id)

    for m_poster in m_poster_list:
        poster = obtain_by_id(
            db, m_poster.id, VisibleLevel.Private.value)

        data.append(poster)

    return data


def obtain_by_from_user_id(
        db: Session, from_user_id: int, visible: int=None)->List:
    """ 获取指定用户发出的所有poster """
    data = []
    m_poster_list = poster_orm.find_poster_by_from_user_id(
        db, from_user_id=from_user_id)

    for m_poster in m_poster_list:
        poster = obtain_by_id(db, m_poster.id, visible)
        data.append(poster)

    return data


def obtain_by_to_user_id(
        db: Session, to_user_id: int, visible: int=None,
        offset: int=None, limit: int=None)->List:
    """ 获取指定用户收到的所有poster """
    data = []
    m_poster_list = poster_orm.find_poster_by_to_user_id(
        db, to_user_id=to_user_id, offset=offset, limit=limit)

    for m_poster in m_poster_list:
        poster = obtain_by_id(db, m_poster.id, visible)
        data.append(poster)

    return data


def packing(
        m_data: DictObject,
        child_nickname: str, start_ts: int, media_obj_list: List=None,
        user: DictObject=None, rate: int=-1)->Dict:
    """ """

    package = DictObject(
        start_ts=start_ts,
        user=user,
        poster_id=m_data.id,
        order_no=m_data.index_id,
        from_user_id=m_data.from_user_id,
        to_user_id=m_data.to_user_id,
        content=m_data.content,
        media_obj_list=media_obj_list,
        child_nickname=child_nickname,
        is_media_public=m_data.picvid_visible,
        create_ts=m_data.create_ts,
        rate=rate
    )
    return package


def obtian_poster_reply_by_id(db, poster_id, visible):
    """ 加入reply_list """
    poster = obtain_by_id(db, poster_id, visible)

    reply_list = reply_usecase.obtain(
        db, poster_id=poster_id, visible=visible)

    data = DictObject(poster=poster, reply_list=reply_list)
    return data


def obtain_simple(db: Session, poster_id: int=None, user_id: int=None):
    data = None
    if poster_id is not None:
        data = obtain_simple_by_id(db, poster_id)

    if user_id is not None:  # 【预留】
        pass

    return data


def obtain_simple_by_id(db: Session, poster_id: int)->DictObject:
    m_poster = poster_orm.find_poster_by_id(db, poster_id=poster_id)
    return m_poster
