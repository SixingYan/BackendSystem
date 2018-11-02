# third
from typing import List
from sqlalchemy.orm import Session

from moretime.wrong import exception
from moretime.util import DictObject
from moretime.config.const import PublicVisible, VisiblePart
from moretime.api.wapp import logworker

from . import obtain
from . import update

from moretime.usecase import picture as picture_usecase
from moretime.usecase import video as video_usecase
from moretime.usecase import authority as auth_usecase
from moretime.usecase import reply as reply_usecase


def visible(
        db: Session, poster_id: int,
        is_content: bool, new_visible: int):
    """ """
    # is_content: 是否是更改content_visible字段 --  true: 是，false: 不是
    
    # 1. check authority
    auth_usecase.has_authority(db, 'change_visible', poster_id)

    # 2. get basic
    m_poster = obtain.obtain_simple(db, poster_id=poster_id)
    if m_poster is None:
        raise exception.NoExistPoster(poster_id)

    # 3. update content || update picvid
    if is_content == VisiblePart.Content.value:

        org_visible = m_poster.content_visible
        update_content_visible(db, m_poster, org_visible, new_visible)

    else:
        org_visible = m_poster.picvid_visible
        update_picvid_visible(db, m_poster, org_visible, new_visible)


def update_content_visible(
        db: Session, m_poster: DictObject,
        org_visible: int, new_visible: int):
    """ """
    logworker.info(org_visible)
    logworker.info(new_visible)
    # 1. content
    if org_visible != new_visible:
        update.update(db, m_poster.id, content_visible=new_visible)




    # 2. picvid
    # if not new_visible:  # 【预留】new_visible->false，设置poster整体不可见
    #    update_poster_picvid_visible(db, m_poster, org_visible, new_visible)


def update_picvid_visible(
        db: Session, m_poster: DictObject,
        org_visible: int, new_visible: int):
    """ """
    # 1. prepare raw data
    m_reply_list = reply_usecase.obtain_simple(
        db, poster_id=m_poster.id)

    # 2. change visible
    if org_visible != new_visible:  # need to change

        if org_visible == PublicVisible.Yes.value \
                and new_visible == PublicVisible.No.value:
            # 公众可见->公众不可见
            update_to_private(db, m_poster, m_reply_list)

        else:  # 公众不可见->公众可见
            update_to_public(db, m_poster, m_reply_list)


def update_to_public(
        db: Session, m_poster: DictObject, m_reply_list: List):
    """  """
    # 1. 获取新的public 区 id
    id_list = [int(i) for i in m_poster.picture_ids_private.split(',')] \
        if m_poster.picture_ids_private is not None and m_poster.picture_ids_private != '' else []
    picture_ids_public = picture_usecase.update_to_public(db, id_list)

    # 2. 获取新的public 区 id
    id_list = [int(i) for i in m_poster.video_ids_private.split(',')] \
        if m_poster.video_ids_private is not None and m_poster.video_ids_private != '' else []
    video_ids_public = video_usecase.update_to_public(db, id_list)

    # 3. 更新poster的pictures_ids_public & videos_ids_public 字段
    update.update(
        db, m_poster.id, picture_ids_public=picture_ids_public,
        video_ids_public=video_ids_public,
        picvid_visible=PublicVisible.Yes.value)

    # logworker.info(m_reply_list)

    # 4. 更新reply
    if m_reply_list != []:
        for m_reply in m_reply_list:
            reply_usecase.visible(
                db, PublicVisible.No.value,
                PublicVisible.Yes.value, reply=m_reply)


def update_to_private(
        db: Session, m_poster: DictObject, m_reply_list: List):
    """ """
    # 1. 删除public 区 id
    id_list = [int(i) for i in m_poster.picture_ids_public.split(',')] \
        if m_poster.picture_ids_public is not None and m_poster.picture_ids_public != '' else []
    picture_usecase.update_to_private(db, id_list)

    # 2. 删除public 区 id
    id_list = [int(i) for i in m_poster.video_ids_public.split(',')] \
        if m_poster.video_ids_public is not None and m_poster.video_ids_public != '' else []
    video_usecase.update_to_private(db, id_list)

    # 3. 更新poster的pictures_ids_public & videos_ids_public 字段
    update.update(
        db, m_poster.id, picture_ids_public='',
        video_ids_public='', picvid_visible=PublicVisible.No.value)

    if m_reply_list is not None:
        for m_reply in m_reply_list:
            reply_usecase.visible(
                db, PublicVisible.Yes.value, PublicVisible.No.value, reply=m_reply)


def share(db, poster_id):
    pass
