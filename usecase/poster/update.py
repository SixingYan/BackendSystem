"""预留：更新内容"""
from sqlalchemy.orm import Session
from typing import List
import moretime.orm.poster as poster_orm


def update(
        db: Session, poster_id: int,
        content: str=None,
        content_visible: int=None, picvid_visible: int=None,
        picture_ids_public: List[int]=None,
        picture_ids_private: List[int]=None,
        video_ids_public: List[int]=None,
        video_ids_private: List[int]=None,
        sort_order: List[int]=None):
    poster_orm.update_poster_by_id(
        db, poster_id, content,
        content_visible, picvid_visible,
        picture_ids_public, picture_ids_private,
        video_ids_public, video_ids_private, sort_order)
