from sqlalchemy.orm import Session

from moretime.util import DictObject
import moretime.orm.reply as reply_orm
import moretime.usecase.video as video_usecase
import moretime.usecase.picture as picture_usecase
from moretime.config.const import PublicVisible
from moretime.api.wapp import logworker


def visible(
        db: Session, org_visible: int, new_visible: int,
        reply_id: int=None, reply=None):
    """ """
    if reply is not None:
        update_visible_by_object(db, org_visible, new_visible, reply)

    if reply_id is not None:
        # 【预留】设置单条评论可见性
        pass


def update_visible_by_object(
        db: Session,
        org_visible: int, new_visible: int, m_reply: DictObject):
    """ """
    if org_visible != new_visible:  # need to change

        if org_visible == PublicVisible.Yes.value \
                and new_visible == PublicVisible.No.value:  # 公众可见->公众不可见
            update_to_private(db, m_reply)

        else:  # 公众不可见->公众可见
            #logworker.info('m_reply')
            #logworker.info(m_reply)
            update_to_public(db, m_reply)


def update_to_public(db: Session, m_reply: DictObject):
    # 1. 获取新的public 区 id

    id_list = [int(i) for i in m_reply.picture_ids_private.split(',')] \
        if m_reply.picture_ids_private is not None and m_reply.picture_ids_private != '' else []
    picture_ids_public = picture_usecase.update_to_public(db, id_list)

    # 2. 获取新的public 区 id
    id_list = [int(i) for i in m_reply.video_ids_private.split(',')] \
        if m_reply.video_ids_private is not None and m_reply.video_ids_private != '' else []
    video_ids_public = video_usecase.update_to_public(db, id_list)

    # 3. 更新poster的pictures_ids_public & videos_ids_public 字段
    reply_orm.update_reply_by_id(
        db, m_reply.id, picture_ids_public=picture_ids_public,
        video_ids_public=video_ids_public)


def update_to_private(db: Session, m_reply: DictObject):
    # 1. 删除public 区 id
    id_list = [int(i) for i in m_reply.picture_ids_public.split(',')] \
        if m_reply.picture_ids_public is not None and m_reply.picture_ids_public != '' else []
    picture_usecase.update_to_private(db, id_list)

    # 2. 删除public 区 id
    id_list = [int(i) for i in m_reply.video_ids_public.split(',')] \
        if m_reply.video_ids_public is not None and m_reply.video_ids_public != '' else []
    video_usecase.update_to_private(db, id_list)

    # 3. 清空reply的pictures_ids_public & videos_ids_public 字段
    reply_orm.update_reply_by_id(
        db, m_reply.id, picture_ids_public='', video_ids_public='')


def update_visible_by_reply_id():
    # 【预留】指定reply_id更改可见性
    pass
