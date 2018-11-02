#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy.orm import Session
from moretime.entity import Facade
from moretime.api.schema import ObjectInfo
from moretime.api.wapp import logworker
from moretime.util import DictObject, qiniu
from moretime.config.const import DatabaseStatus, VisibleBucket, VisibleLevel, MediaPart
import moretime.usecase.visible as visible_usecase

import moretime.orm.picture as picture_orm
from moretime.orm.orm_mysql import MoretimePictureModel


def picture_ids_to_objs(db: Session, info: DictObject, visible: int)-> List:
    """ 给定pictureID取出视频所需的所有数据 """
    # 1. check visible
    if visible == VisibleLevel.Public.value:
        picture_ids = info.picture_ids_public

    elif visible == VisibleLevel.Private.value:
        picture_ids = info.picture_ids_private

    else:
        picture_ids = ''

    # 2. prepare data
    picture_info_list = []
    if picture_ids != '':
        picture_info_list = preparing(db, picture_ids)

    return picture_info_list


def preparing(db, obj_list):
    """ 尝试准备数据，并根据需求添加filter，允许准备失败返回默认值
        应对 图片id 找不到对应记录而引发的错误 
        图片准备失败不应该引发poster报错
        1. add the filter 
        2. try dealing
    """
    data = []
    # 1. filter
    if obj_list is None:
        return data

    if obj_list == '':
        return data

    # 2. try dealing the data
    try:
        data = [_picture_id_to_dict(db, int(i)) for i in obj_list.split(',')]
    except Exception as e:
        data = [{} for i in obj_list.split(',')]
        logworker.exception("preparing picture")
        logworker.error([obj_list])

    return data


def pictures_info_to_ids(
        db: Session, pictures_info: List[DictObject]) -> List:
    """ 将上传信息存入moretime_picture表 """
    if pictures_info is None or pictures_info == []:
        return []

    data = [_insert_picture(db, VisibleBucket.Private.value, p.media)
            for p in pictures_info] if pictures_info != [] else []
    return data


def picture_key_to_id(db: Session, org_id: int, key: str):
    """ 给出公开key, 将私有图片信息&公开key复制到新的图片对象"""
    m_picture = picture_orm.find_picture_by_id(db, org_id)

    picture_id = _insert_picture(
        db, VisibleBucket.Public.value, m_picture, key)

    return picture_id


def picture_ids_to_keys(db: Session, picture_id_list: List) -> List:
    """ 给定pictureID取出对应视频key（用于远程复制） """
    picture_key_list = []

    for picture_id in picture_id_list:
        m_picture = picture_orm.find_picture_by_id(db, picture_id)
        key = m_picture.key.split(':')[2]
        picture_key_list.append(key)

    return picture_key_list


def update_to_private(db: Session, picture_id_list: List):
    """ 将视频更新成私有
        1.取出key, 
        2.进行远程删除, 
        3.清除(更新)数据库
    """
    if picture_id_list == []:
        return
    # 1. 取出key,
    picture_key_list = picture_ids_to_keys(db, picture_id_list)

    # 2. 进行远程删除,
    visible_usecase.delete_public(picture_key_list)

    # 3. 删除数据库相应记录
    for picture_id in picture_id_list:
        picture_orm.delete_picture(db, picture_id)


def update_to_public(db: Session, picture_id_list: List)->List:
    """ 将图片更新成公开
        1.取出图片key,   
        2.进行远程复制后返回公开key, 
        3.存入公开key后返回ids
    """
    if picture_id_list == []:
        return []
    # 1.取出图片key,
    private_key_list = picture_ids_to_keys(db, picture_id_list)

    # 2.进行远程复制后返回公开key,
    public_key_list = visible_usecase.copy_to_public(private_key_list)

    # 3.存入公开key后返回ids
    public_id_list = []
    for i in range(len(picture_id_list)):
        public_id = picture_key_to_id(
            db, picture_id_list[i], public_key_list[i])
        public_id_list.append(public_id)

    return public_id_list


def _insert_picture(
        db: Session, visible_bucket: str,
        req_picture: ObjectInfo, key: str=None) -> int:
    """ 
        1.2.准备存储信息 
        3.查看数据库中是否以后数据 
        4.创建/更新（恢复） 
    """
    # 1. `cloud` 写死 -> qiniu
    cloud = 'qiniu'

    # 2.这里要相应的更改bucket名字
    bucket = Facade.config["qiniu"]["category"][visible_bucket]["bucket"]
    # logworker.info('111111111111')
    # logworker.info(bucket)

    # 3.判断数据库中有没有已存在的记录

    # req_picture.key = ':'.join(
    #    ['qiniu', bucket, req_picture.key])

    # m_picture = picture_orm.find_picture_by_oss_path(
    #    db, cloud, bucket, req_picture.key)

    # 3.判断数据库中有没有已存在的记录
    if key is not None:  # 指定了key, 是公开key
        req_key = ':'.join(['qiniu', bucket, key])  # 拼接qiniu:bucket:key
        # 查找数据库中是否已存在
        m_picture = picture_orm.find_picture_by_oss_path(
            db, cloud, bucket, req_key)

    else:  # 没有指定, 是上传时附带的key
        req_key = ':'.join(['qiniu', bucket, req_picture.key])
        m_picture = picture_orm.find_picture_by_oss_path(
            db, cloud, bucket, req_key)

    # 4.创建 视频记录 / 恢复“已删除”的 视频记录
    if not m_picture:
        m_picture = picture_orm.create_picture(
            db, cloud, bucket, req_key,
            etag=req_picture.etag, mime_type=req_picture.mime_type,
            size=req_picture.size, duration=req_picture.duration,
            width=req_picture.width, height=req_picture.height,
            persistent_id=req_picture.persistent_id
        )
    else:
        if m_picture.status == DatabaseStatus.Delete.value:
            picture_orm.update_picture(
                db, m_picture.id, DatabaseStatus.Normal.value)
    return m_picture.id


def _picture_id_to_dict(db, picture_id):
    """ 给定pictureID来取出数据库数据 """
    m_picture = picture_orm.find_picture_by_id(db, picture_id)
    return _picture_orm_to_dict(m_picture)


def _picture_orm_to_dict(p: MoretimePictureModel) -> dict:
    """ 将数据库的数据包装成前端可用数据 """
    return DictObject(
        key=p.key,
        mime_type=p.mime_type,
        etag=p.etag,
        size=p.size,
        width=p.width,
        height=p.height,
        cover_url=qiniu.url_from_path(p.key)
    )
