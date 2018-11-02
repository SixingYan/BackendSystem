from sqlalchemy.orm import Session
from typing import List

from moretime.util import DictObject
from moretime.entity import Facade
from moretime.api.schema import ObjectInfo
from moretime.api.wapp import logworker
from moretime.config.const import VisibleLevel, VisibleBucket, DatabaseStatus, MediaPart

from moretime.orm import video as video_orm
from moretime.orm.orm_mysql import MoretimeVideoModel

from . import visible as visible_usecase

import moretime.util.qiniu as qiniu


def update_to_public(db: Session, video_id_list: List) -> List:
    """ 将视频更新成公开
        1.取出视频key, 
        1.取出cover_url图片的oss     
        2.进行远程复制后返回公开key, 
        3.存入公开key后返回ids
    """
    if video_id_list == []:
        return []

    # 1. 获取基本信息
    video_key_list = video_ids_to_keys(db, video_id_list)

    # 2.七牛云存储改动
    # 2.1 视频
    public_key_list = visible_usecase.copy_to_public(video_key_list)
    # 2.2 视频封面
    public_key_list = visible_usecase.copy_to_public(video_key_list)

    # 3.数据库改动
    public_id_list = []
    for i in range(len(video_id_list)):
        public_id = video_key_to_id(
            db, video_id_list[i], public_key_list[i])
        public_id_list.append(public_id)

    return public_id_list


def update_to_private(db: Session, video_id_list: List):
    """ 将视频更新成私有
        1.取出key, 
        2.进行远程删除, 
        3.清除(更新)数据库
    """
    if video_id_list == []:
        return

    # 1. 取出key
    video_key_list = video_ids_to_keys(db, video_id_list)

    # 2. 远程删除
    # 2.1 删除视频
    visible_usecase.delete_public(video_key_list)
    # 2.2 删除封面
    visible_usecase.delete_public(video_key_list)

    # 3. 删除数据库相应记录的字段
    for video_id in video_id_list:
        video_orm.delete_video(db, video_id)


def video_ids_to_keys(db: Session, video_id_list: List)-> List:
    """ 给定videoID取出对应视频key（用于远程复制） """
    video_key_list = []

    for video_id in video_id_list:
        m_video = video_orm.find_video_by_id(db, video_id)
        
        key = m_video.key
        video_key_list.append(key)

    return video_key_list


def video_ids_to_objs(
        db: Session, info: DictObject, visible: int)-> List:
    """ 给定videoID取出视频所需的所有数据 """
    # 1. check visible
    if visible == VisibleLevel.Public.value:
        videos_ids = info.video_ids_public
        visible_bucket = VisibleBucket.Public.value

    elif visible == VisibleLevel.Private.value:
        videos_ids = info.video_ids_private
        visible_bucket = VisibleBucket.Private.value

    else:
        videos_ids = ''

    # 2. prepare data
    video_obj_list = []
    if videos_ids != '':
        video_obj_list = preparing(db, videos_ids, visible_bucket)

    return video_obj_list


def preparing(db: Session, obj_list: str, visible_bucket: str):
    """ 尝试准备数据，并根据需求添加filter，允许准备失败返回默认值
        应对 视频id 找不到对应记录而引发的错误 
        视频准备失败不应该引发poster报错
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
        data = [_video_id_to_dict(db, int(i), visible_bucket)
                for i in obj_list.split(',')]
    except Exception as e:
        data = [{} for i in obj_list.split(',')]
        logworker.exception("preparing video")
        logworker.error([obj_list, visible_bucket])

    return data


def _video_id_to_dict(
        db: Session, video_id: int, visible_bucket: str) -> dict:
    """ 给定videoID来取出数据库数据 """
    # 因为 category用于找bucket，而视频表里已经存了bucket信息了
    m_video = video_orm.find_video_by_id(db, video_id)
    return _video_orm_to_dict(m_video, visible_bucket)


def _video_orm_to_dict(v: MoretimeVideoModel, visible_bucket: str) -> dict:
    """ 将数据库的数据包装成前端可用数据 """
    return DictObject(
        key=v.key,
        mime_type=v.mime_type,
        etag=v.etag,
        size=v.size,
        width=v.width,
        height=v.height,
        duration=v.duration,
        cover_url=qiniu.url(Facade.config["qiniu"]["category"][
                            visible_bucket]["bucket"], v.key),
        video_url=qiniu.url(v.bucket, v.key)
    )


def videos_info_to_ids(db: Session, videos_info: List)->List:
    """ 将上传信息存入moretime_video表 """
    if videos_info == [] or videos_info is None:
        return []

    data = [_insert_video(db, VisibleBucket.Private.value, v.media)
            for v in videos_info] if videos_info != [] else []
    return data


def video_key_to_id(db: Session, org_id: int, key: str):
    """ 给出公开key, 将私有视频信息&公开key复制到新的视频对象"""
    m_video = video_orm.find_video_by_id(db, org_id)
    video_id = _insert_video(db, VisibleBucket.Public.value, m_video, key)
    return video_id


def _insert_video(
        db: Session, visible_bucket: str,
        req_video: ObjectInfo, key: str=None) -> int:
    """ 
        1.2.准备存储信息 
        3.查看数据库中是否以后数据 
        4.创建/更新（恢复） 
    """
    # 1.`cloud` 写死 -> qiniu
    cloud = 'qiniu'

    # 2.这里要相应的更改bucket名字
    bucket = Facade.config["qiniu"]["category"][visible_bucket]["bucket"]

    # 3.判断数据库中有没有已存在的记录
    if key is not None:  # 指定了key, 是公开key
        m_video = video_orm.find_video_by_oss_path(
            db, cloud, bucket, key)
        req_key = key

    else:  # 没有指定, 是上传时附带的key
        m_video = video_orm.find_video_by_oss_path(
            db, cloud, bucket, req_video.key)
        req_key = req_video.key

    # 4.创建 视频记录 / 恢复“已删除”的 视频记录
    if not m_video:  # 如果没有则创建
        m_video = video_orm.create_video(
            db, cloud, bucket, req_key,
            etag=req_video.etag, mime_type=req_video.mime_type,
            size=req_video.size, duration=req_video.duration,
            width=req_video.width, height=req_video.height,
            persistent_id=req_video.persistent_id
        )
    else:  # 如果有但是已删除了，恢复成正常
        if m_video.status == DatabaseStatus.Delete.value:  # 将已删除更新为正常
            video_orm.update_video(db, m_video.id, DatabaseStatus.Normal.value)

    return m_video.id
