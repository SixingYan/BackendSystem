from typing import List
from sqlalchemy.orm import Session
from moretime.util import current_timestamp
from moretime.orm.orm_mysql import PosterModel


def create_poster_transaction(
        db: Session, order_no: int,
        from_user_id: int, to_user_id: int,
        content: str,
        picture_id_list: List[int]=None,
        video_id_list: List[int]=None,
        sort_order: List[int]=None) -> int:
    poster = None
    try:
        poster = PosterModel(
            index_id=order_no,
            create_ts=current_timestamp(),
            content=content,
            from_user_id=from_user_id,
            to_user_id=to_user_id
        )
        if picture_id_list is not None:
            poster.picture_ids_private = ','.join(
                [str(i) for i in picture_id_list])

        if video_id_list is not None:
            poster.video_ids_private = ','.join(
                [str(i) for i in video_id_list])

        if sort_order is not None:
            poster.sort_order = ','.join(
                [str(i) for i in sort_order])

        db.add(poster)
        db.commit()
    except Exception as e:
        # TODO: LOG
        db.rollback()
        print('create_poster_transaction', str(e))
        raise
        
    return poster


def find_poster_by_id(
        db: Session, poster_id: int):
    poster = db.query(PosterModel).filter(
        PosterModel.id == poster_id
    ).first()
    return poster


def find_poster_by_from_user_id(
        db: Session, from_user_id: int):
    poster = db.query(PosterModel).filter(
        PosterModel.from_user_id == from_user_id).all()
    return poster


def find_poster_by_to_user_id(
        db: Session, to_user_id: int, offset: int=None, limit: int=None):
    poster = db.query(PosterModel).filter(
        PosterModel.to_user_id == to_user_id)
    
    if offset is not None and offset != -1:
        poster = poster.offset(offset)
    if limit is not None and limit != -1:
        poster = poster.limit(limit)

    return poster.all()


def update_poster_by_id(
        db: Session, poster_id: int,
        content: str=None,
        content_visible: int=None, picvid_visible: int=None,
        picture_ids_public: List[int]=None,
        picture_ids_private: List[int]=None,
        video_ids_public: List[int]=None,
        video_ids_private: List[int]=None,
        sort_order: List[int]=None):
    try:
        m_poster = PosterModel(id=poster_id)
        if content is not None:
            m_poster.content = content

        if content_visible is not None:
            m_poster.content_visible = content_visible

        if picvid_visible is not None:
            m_poster.picvid_visible = picvid_visible

        if picture_ids_public is not None:
            m_poster.picture_ids_public = ','.join(
                [str(i) for i in picture_ids_public])

        if picture_ids_private is not None:
            m_poster.picture_ids_private = ','.join(
                [str(i) for i in picture_ids_private])

        if video_ids_public is not None:
            m_poster.video_ids_public = ','.join(
                [str(i) for i in video_ids_public])

        if video_ids_private is not None:
            m_poster.video_ids_private = ','.join(
                [str(i) for i in video_ids_private])

        if sort_order is not None:
            poster.sort_order = ','.join(
                [str(i) for i in sort_order])

        m_poster.update_ts = current_timestamp()

        db.merge(m_poster)
        db.commit()
    except Exception as e:
        db.rollback()
        print('update_poster_by_id', str(e))
        raise


def delete_poster_picvide_public_by_poster_id(
        db: Session, poster_id: int):
    try:
        m_poster = PosterModel(id=poster_id)
        m_poster.picture_ids_public = ''
        m_poster.video_ids_public = ''
        m_poster.update_ts = current_timestamp()

        db.merge(m_poster)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_poster_picvide_public_by_poster_id', str(e))
        raise


def delete_poster_by_id(
        db: Session, poster_id: int):
    try:
        m_poster = PosterModel(id=poster_id)
        m_poster.status = -1,
        m_poster.update_ts = current_timestamp()

        db.merge(m_poster)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_poster_by_poster_id', str(e))
        raise
