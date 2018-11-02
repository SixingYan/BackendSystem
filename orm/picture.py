#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from moretime.orm.exc import is_duplicate_entry_exception
from moretime.orm.orm_mysql import MoretimePictureModel
from moretime.util import current_timestamp


def find_picture_by_id(db: Session, picture_id: int):
    m = db.query(MoretimePictureModel).filter(
        MoretimePictureModel.id == picture_id).first()
    return m


def find_picture_by_oss_path(
        db: Session, cloud: str, bucket: str,
        key: str) -> MoretimePictureModel:

    m = db.query(MoretimePictureModel).filter(
        MoretimePictureModel.cloud == cloud,
        MoretimePictureModel.bucket == bucket,
        MoretimePictureModel.key == key
    ).first()
    return m


def create_picture(
        db: Session,
        cloud: str, bucket: str, key: str,
        etag: str = None, mime_type: str = None, size: int = None,
        duration: int = None, width: int = None, height: int = None,
        persistent_id: str = None) ->MoretimePictureModel:
    """ Create `video` record if not existed.
        Igonre `Duplicate Entry` error.
    """
    m = None
    try:
        m = MoretimePictureModel(
            cloud=cloud, bucket=bucket, key=key,
            etag=etag, mime_type=mime_type, size=size,
            duration=duration, width=width, height=height,
            persistent_id=persistent_id,
            status=0,
            create_ts=current_timestamp()
        )
        db.add(m)
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        if is_duplicate_entry_exception(exc):
            return m
        else:
            print('create_video', str(e))
            raise
    return m


def update_picture(db: Session, picture_id: int, status: int=None):
    try:
        m = MoretimePictureModel(id=picture_id)
        if status is not None:
            m.status = status

        db.merge(m)
        db.commit()
    except Exception as e:
        db.rollback()
        print('update_picture', str(e))
        raise


def delete_picture(db: Session, picture_id: int):
    try:
        picture = MoretimePictureModel(id=picture_id)
        picture.status = -1

        db.merge(picture)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_picture', str(e))
        raise
