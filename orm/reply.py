from sqlalchemy.orm import Session
from typing import List
from moretime.util import current_timestamp, DictObject
from moretime.orm.orm_mysql import ReplyModel
from moretime.config.const import DatabaseStatus
#from orm.rate import create_rate
#from orm.poster import find_poster_by_id
from moretime.api.wapp import logworker


def create_reply(
        db: Session, poster_id: int,
        from_user_id: int, to_user_id: int,
        parent_ids: str, prior_id: int, content: str,
        picture_id_list: List[int]=None,
        video_id_list: List[int]=None,
        sort_order: List[int]=None)-> DictObject:

    reply = ReplyModel(
        poster_id=poster_id,
        prior_id=prior_id, parent_ids=parent_ids,
        create_ts=current_timestamp(),
        content=content,
        from_user_id=from_user_id, to_user_id=to_user_id
    )
    if picture_id_list:
        reply.picture_ids_private = ','.join(
            [str(i) for i in picture_id_list])

    if video_id_list:
        reply.video_ids_private = ','.join(
            [str(i) for i in video_id_list])

    if sort_order is not None:
        reply.sort_order = ','.join(
            [str(i) for i in sort_order])
    return reply


def create_reply_transaction(
        db: Session, poster_id: int,
        from_user_id: int, to_user_id: int,
        parent_ids: str, prior_id: int, content: str,
        picture_id_list: List[int]=None,
        video_id_list: List[int]=None,
        sort_order: List[int]=None)-> DictObject:
    reply = None
    try:
        reply = create_reply(
            db,
            poster_id,
            from_user_id, to_user_id,
            parent_ids, prior_id,
            content,
            picture_id_list, video_id_list, sort_order)

        db.add(reply)
        db.commit()
    except Exception as e:
        db.rollback()
        print('create_reply_transaction', str(e))
        raise e
    return reply


def find_reply_by_id(db: Session, reply_id: int):
    m_reply = db.query(ReplyModel).filter(
        ReplyModel.id == reply_id
    ).first()
    return m_reply


def find_reply_by_poster_id(
        db: Session, poster_id: int,
        offset: int=None, limit: int=None) -> List[ReplyModel]:
    m_reply = db.query(ReplyModel).filter(
        ReplyModel.poster_id == poster_id)

    if offset is not None and offset != -1:
        m_reply = m_reply.offset(offset)

    if limit is not None and limit != -1:
        m_reply = m_reply.limit(limit)
    return m_reply.all()


def find_reply_by_from_user_id(db: Session, from_user_id: int):
    m_reply = db.query(ReplyModel).filter(
        ReplyModel.from_user_id == from_user_id
    ).all()
    return m_reply


def find_reply_by_to_user_id(
        db: Session, to_user_id: int, offset: int=None, limit: int=None):
    m_reply = db.query(ReplyModel).filter(
        ReplyModel.to_user_id == to_user_id,
        ReplyModel.status == DatabaseStatus.Normal.value
    )

    if offset is not None and offset != -1:
        m_reply = m_reply.offset(offset)

    if limit is not None and limit != -1:
        m_reply = m_reply.limit(limit)

    return m_reply.all()


def update_reply_by_id(
        db: Session, reply_id: int, content: str=None,
        picture_ids_public: List=None, picture_ids_private: List=None,
        video_ids_public: List=None, video_ids_private: List=None,
        sort_order: List=None):
    try:
        m_reply = ReplyModel(id=reply_id)

        if content is not None:
            m_reply.content = content

        if picture_ids_public is not None:
            m_reply.picture_ids_public = ','.join(
                [str(i) for i in picture_ids_public])

        if picture_ids_private is not None:
            m_reply.picture_ids_private = picture_ids_private

        if video_ids_public is not None:
            m_reply.video_ids_public = ','.join(
                [str(i) for i in video_ids_public])

        if video_ids_private is not None:
            m_reply.video_ids_private = video_ids_private

        if sort_order is not None:
            m_reply.sort_order = ','.join(
                [str(i) for i in sort_order])

        m_reply.update_ts = current_timestamp()

        db.merge(m_reply)
        db.commit()
    except Exception as e:
        db.rollback()
        print('update_reply_by_reply_id', str(e))
        raise


def delete_poster_picvide_public_by_reply_id(
        db: Session, reply_id: int)->None:
    """ """
    try:
        m_reply = ReplyModel(reply_id=reply_id)
        m_reply.picture_ids_public = ''
        m_reply.video_ids_public = ''
        m_reply.update_ts = current_timestamp()

        db.merge(m_reply)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_poster_by_poster_id', str(e))
        raise


def delete_reply_by_poster_id(db: Session, poster_id: int)->None:
    try:
        m_reply = ReplyModel(poster_id=poster_id)
        m_reply.status = -1
        m_reply.update_ts = current_timestamp()

        db.merge(m_reply)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_reply_by_poster_id', str(e))
        raise


def delete_reply_by_id(db: Session, reply_id: int)->None:
    try:
        m_reply = ReplyModel(reply_id=reply_id)
        m_reply.status = -1
        m_reply.update_ts = current_timestamp()

        db.merge(m_reply)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_reply_by_reply_id', str(e))
        raise
