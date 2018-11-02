from sqlalchemy.orm import Session
from typing import List

from moretime.util import DictObject
from moretime.config.const import MoretimeRate, ReplyToPoster
from moretime.usecase import picture as picture_usecase
from moretime.usecase import video as video_usecase
from moretime.usecase import visible as visible_usecase
from moretime.usecase import common as common_usecase
import moretime.usecase.user as user_usecase
import moretime.usecase.rate as rate_usecase
from moretime.usecase import poster as poster_usecase
from moretime.api.wapp import logworker
from moretime.orm import reply as reply_orm
from moretime.orm import rate as rate_orm
from moretime.orm.orm_mysql import (
    ReplyModel
)


def obtain(
        db: Session, reply_id: int=None,
        from_user_id: int=None, to_user_id: int=None,
        poster_id: int=None, visible: int=None,
        offset: int=None, limit: int=None, count: bool=False) -> List or DictObject:
    """ 外部调用的方法 """
    data = []

    if reply_id is not None:
        data = obtain_by_id(db, reply_id, visible)

    if poster_id is not None:
        data = obtain_by_poster_id(db, poster_id, visible, offset, limit)

    if from_user_id is not None:
        data = obtain_by_from_user_id(db, from_user_id, visible)

    if to_user_id is not None and count is False:
        # logworker.info(to_user_id)
        # logworker.info(visible)
        data = obtain_by_to_user_id(db, to_user_id, visible, offset, limit)

    if to_user_id is not None and count is True:
        data = obtain_count_by_to_user_id(db, to_user_id, visible)

    return data


def obtain_count_by_to_user_id(db: Session, to_user_id: int, visible: int):
    """ """
    data = 0
    reply_list = obtain_by_to_user_id(db, to_user_id, visible)

    if reply_list is not None:
        data = len(reply_list)
    return data


def obtain_by_id(
        db: Session, reply_id: int,
        visible_choose: int=None, m_poster: DictObject=None,
        m_reply: DictObject=None)-> DictObject:
    """
        1. get raw data, if no exist, stop and return
    """
    # 1. get raw data
    if m_reply is None:
        m_reply = obtain_simple(db, reply_id=reply_id)
    if m_reply is None:
        return None

    # 2. filter visible
    if visible_choose is None:
        visible_choose = visible_usecase.obtain_visible_choose(m_reply)

    # 3. packing video
    video_obj_list = video_usecase.video_ids_to_objs(
        db, m_reply, visible_choose)

    # 4. packing picture
    picture_obj_list = picture_usecase.picture_ids_to_objs(
        db, m_reply, visible_choose)

    # 5. sort media
    media_obj_list = None
    if m_reply.sort_order != '' or m_reply.sort_order is not None:

        order_list = [int (i) for i in m_reply.sort_order.split(',')] \
            if m_reply.sort_order is not None and m_reply.sort_order != '' else []

        media_obj_list = common_usecase.prepare_sort_object(
            order_list, picture_obj_list, video_obj_list)

    # 6. rate
    # rate = MoretimeRate.Default.value
    # if m_poster is not None:
    #    if m_reply.prior_id == ReplyToPoster.Prior.value and m_reply.from_user_id == m_poster.to_user_id:
    #        m_rate = rate_orm.find_rate_by_order_no(db, m_poster.index_id)
    #        if m_rate is not None:
    #            rate = m_rate.rate

    user = user_usecase.obtain_user(db, m_reply.from_user_id)

    # packing reply
    reply = packing(m_reply, media_obj_list, user)

    return reply


def obtain_by_from_user_id(
        db: Session, from_user_id: int, visible_choose: int=None):
    # 【预留】 用户发出的所有评论
    pass


def obtain_by_to_user_id(
        db: Session, to_user_id: int, visible_choose: int=None,
        offset: int=None, limit: int=None):
    """ 指定用户收到的所有评论 """
    reply_list = []

    # 1. raw data
    m_reply_list = reply_orm.find_reply_by_to_user_id(
        db, to_user_id=to_user_id, offset=offset)

    # 2. obtain
    #data = packing_reply_list(db, m_reply_list, visible_choose)
    data = []
    # logworker.info("12342341234123423423423423423412341234")
    for m_reply in m_reply_list:

        if m_reply.prior_id == ReplyToPoster.Prior.value:
            # logworker.info(m_reply.id)
            reply = DictObject(
                poster_id=m_reply.poster_id,
                reply=obtain_by_id(
                    db, m_reply.id, visible_choose, m_reply=m_reply),
                rate=rate_usecase.obtain_rate(db, m_reply.poster_id)
            )
            data.append(reply)

    # 3. limit that is not rate reply
    data = [d for d in data if d.rate != MoretimeRate.Default.value]

    if limit is not None and len(data) > limit:
        data = data[:limit]
    
    logworker.info("12342341234123423423423423423412341234")
    logworker.info(len(data))
    
    return data


def obtain_by_poster_id(
        db: Session, poster_id: int, visible_choose: int=None,
        offset: int=None, limit: int=None):
    """  """
    data = []

    # 1. raw data
    m_reply_list = obtain_simple(
        db, poster_id=poster_id, offset=offset, limit=limit)

    if m_reply_list is None or m_reply_list == []:
        return data

    # 2. filter visible (special)
    if visible_choose is None:  # 未指定了使用的可见性
        m_poster = poster_usecase.obtain_simple(
            db, poster_id=poster_id)
        visible_choose = visible_usecase.obtain_visible_choose(m_poster)

    # 3. obtain
    data = packing_reply_list(db, m_reply_list, visible_choose)

    # logworker.info(data)
    return data


def packing_reply_list(
        db: Session, m_reply_list: List[ReplyModel],
        visible_choose: int=None)->List[DictObject]:
    """ 装载reply_list """
    reply_obj_list = []
    tryNum = 0
    # 1. 形成 {reply, follow_reply_list} 的 object
    while m_reply_list != [] and tryNum <= 2 * len(m_reply_list):
        add_or_not = False
        m_reply = m_reply_list.pop(0)  # 提取出一个

        logworker.info(m_reply.id)

        if m_reply.prior_id == ReplyToPoster.Prior.value:  # 指向poster
            reply_obj = DictObject(
                poster_id=m_reply.poster_id,
                reply=obtain_by_id(
                    db, m_reply.id, visible_choose, m_reply=m_reply),
                follow_reply_list=[],
                rate=rate_usecase.obtain_rate(db, m_reply.poster_id)
            )
            reply_obj_list.append(reply_obj)
            add_or_not = True

        else:  # follow reply
            flag = False

            for i in range(len(reply_obj_list)):  # 找到哪个前置
                reply_obj = reply_obj_list[i]

                if reply_obj.reply.reply_id == m_reply.prior_id:
                    reply_obj.follow_reply_list.append(obtain_by_id(
                        db, m_reply.id, visible_choose, m_reply=m_reply))
                    flag = True  # 已添加
                    break

            if flag is False:  # 没找到它的前置，说明前置还没出现
                m_reply_list.append(m_reply)  # 放回

            else:
                add_or_not = True  # 说明已经使用了

        if add_or_not is True:
            tryNum += 1  # 计数循环次数，防止无限循环

    # 2. 排序
    reply_obj_list = common_usecase.sort_reply(reply_obj_list)

    return reply_obj_list


def packing(
        m_reply: ReplyModel, media_obj_list: List,
        user: DictObject)->DictObject:
    """ """
    d_reply = DictObject(
        user=user,
        reply_id=m_reply.id,
        from_user_id=m_reply.from_user_id,
        to_user_id=m_reply.to_user_id,
        content=m_reply.content,
        media_obj_list=media_obj_list,
        create_ts=m_reply.create_ts
    )
    return d_reply


def obtain_simple(
        db: Session, reply_id: int=None, user_id: int=None,
        from_user_id: int=None, to_user_id: int=None,
        poster_id: int=None, offset: int=None, limit: int=None)->DictObject:
    """ 内部调用的接口 """
    m_reply = None

    if reply_id is not None:
        m_reply = obtain_simple_by_id(db, reply_id)

    if poster_id is not None:
        m_reply = obtain_simple_by_poster_id(
            db, poster_id, offset=offset, limit=limit)

    if to_user_id is not None:
        m_reply = obtain_simple_by_to_user_id(db, to_user_id)

    return m_reply


def obtain_simple_by_id(db: Session, reply_id: int):
    """ """
    m_reply = reply_orm.find_reply_by_id(db, reply_id=reply_id)

    return m_reply


def obtain_simple_by_poster_id(db: Session, poster_id: int, offset: int=None, limit: int=None):
    """ """
    m_reply_list = reply_orm.find_reply_by_poster_id(
        db, poster_id=poster_id, offset=offset, limit=limit)

    return m_reply_list


def obtain_simple_by_to_user_id(db: Session, to_user_id: int):
    m_reply_list = reply_orm.find_reply_by_to_user_id(
        db, to_user_id=to_user_id)

    return m_reply_list
