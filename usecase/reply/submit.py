from sqlalchemy.orm import Session

from moretime.util import DictObject

from moretime.config.const import ReplyToPoster
from moretime.orm import reply as reply_orm

from moretime.usecase import common as common_usecase
from moretime.usecase import picture as picture_usecase
from moretime.usecase import video as video_usecase
from moretime.usecase import poster as poster_usecase

from moretime.wrong import exception

from . import obtain


def submit(
        db: Session, from_user_id: int, req: DictObject)->int:
    """
    """
    # 1. prepare data
    data = prepare_data(db, req)

    # 2. create reply
    reply = reply_orm.create_reply_transaction(
        db, req.poster_id, from_user_id, data.to_user_id,
        data.parent_ids, data.prior_id,
        data.content, data.picture_id_list, data.video_id_list,
        data.sort_order)

    # 3. create reply-notif 【暂缓】
    # notif_usercase.create_reply_info(
    #    db, poster_id, reply_id, from_user_id, to_user_id)

    return reply


def prepare_data(db: Session, req: DictObject)->DictObject:
    """ """
    # 1. content
    content = common_usecase.clean_content(req.content)

    # 2. video
    video_id_list = video_usecase.videos_info_to_ids(
        db, req.videos_info_private)
    video_sort = [idx.order_index for idx in req.videos_info_private] \
        if req.videos_info_private is not None else []

    # 3. picture
    picture_id_list = picture_usecase.pictures_info_to_ids(
        db, req.pictures_info_private)
    picture_sort = [idx.order_index for idx in req.pictures_info_private] \
        if req.pictures_info_private is not None else []

    # 4. parent_ids
    parent_ids = generate_parent_reply_id(db, req.prior_id)

    # 5. prepare sorting order
    sort_order = picture_sort + video_sort

    # 6. to_user_id
    if req.prior_id == ReplyToPoster.Prior.value:
        m_poster = poster_usecase.obtain_simple(db, poster_id=req.poster_id)

        if m_poster is None:
            raise exception.NoExistPoster(req.poster_id)
            #logworker.error(exception.NoExistPoster.error + " " + str(req.poster_id))

        to_user_id = m_poster.from_user_id  # 评论给poster的发布者

    else:
        m_reply = obtain.obtain_simple(db, reply_id=req.prior_id)

        if m_reply is None:
            raise exception.NoExistReply(req.prior_id)

        to_user_id = m_reply.from_user_id  # 评论给上一条reply的发布者

    # 7. packing
    data = DictObject(
        content=content,
        video_id_list=video_id_list,
        picture_id_list=picture_id_list,
        sort_order=sort_order,
        prior_id=req.prior_id,
        parent_ids=parent_ids,
        to_user_id=to_user_id
    )
    return data


def generate_parent_reply_id(db: Session, prior_id: int=None)->str:
    """  """
    parent_ids = ''
    if prior_id is not None and prior_id != ReplyToPoster.Prior.value:
        # not the first reply, then it may have the its parent reply
        m_reply = obtain.obtain_simple(db, reply_id=prior_id)

        if m_reply is None:
            parent_ids = str(prior_id)

        else:
            parent_ids = m_reply.parent_ids + ',' + str(prior_id)

    return parent_ids
