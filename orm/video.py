#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from moretime.config.const import DatabaseStatus
from moretime.orm.exc import is_duplicate_entry_exception
from moretime.orm.orm_mysql import MoretimeVideoModel
from moretime.util import current_timestamp


def find_video_by_id(db: Session, video_id: int) ->MoretimeVideoModel:
    m = db.query(MoretimeVideoModel).filter(
        MoretimeVideoModel.id == video_id).first()
    return m


def find_video_by_oss_path(
        db: Session,
        cloud: str, bucket: str, key: str) -> MoretimeVideoModel:

    m = db.query(MoretimeVideoModel).filter(
        MoretimeVideoModel.cloud == cloud,
        MoretimeVideoModel.bucket == bucket,
        MoretimeVideoModel.key == key
    ).first()
    return m


def create_video(
        db: Session,
        cloud: str, bucket: str, key: str,
        etag: str = None, mime_type: str = None, size: int = None,
        duration: int = None, width: int = None, height: int = None,
        persistent_id: str = None) ->MoretimeVideoModel:
    """ Create `video` record if not existed.
        Igonre `Duplicate Entry` error.
    """
    video = None
    try:
        video = MoretimeVideoModel(
            cloud=cloud, bucket=bucket, key=key,
            etag=etag, mime_type=mime_type, size=size,
            duration=duration, width=width, height=height,
            persistent_id=persistent_id,
            status=0,
            create_ts=current_timestamp()
        )
        db.add(video)
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        if is_duplicate_entry_exception(exc):
            return video
        else:
            raise
    return video


def update_video(db: Session, video_id: int, status: int=None):
    try:
        video = MoretimeVideoModel(id=video_id)
        if status is not None:
            video.status = status
        db.merge(video)
        db.commit()
    except Exception as e:
        db.rollback()
        print('update_picture', str(e))
        raise


def delete_video(db: Session, video_id: int):
    try:
        video = MoretimeVideoModel(id=video_id)
        video.status = DatabaseStatus.Delete.value
        db.merge(video)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_picture', str(e))
        raise
