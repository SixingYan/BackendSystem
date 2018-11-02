from typing import List, Dict
from sqlalchemy.orm import Session

from moretime.wrong import exception
from moretime.util import DictObject

# self
import moretime.orm.poster as poster_orm

import moretime.usecase.common as commom_usecase
import moretime.usecase.video as video_usecase
import moretime.usecase.picture as picture_usecase
import moretime.usecase.order as order_usecase

from moretime.api.wapp import logworker

def submit(db: Session, user_id: int, req)->List:
    """
    """
    data = prepare_data(db, user_id, req)

    poster = poster_orm.create_poster_transaction(
        db, req.order_no, data.from_user_id, data.to_user_id,
        data.content, data.picture_id_list, data.video_id_list,
        data.sort_order)

    # 改成 notification 命名
    # notif_usecase.create_poster_user(db, poster_id)

    return poster


def prepare_data(db: Session, user_id: int, req)-> Dict:
    """
        1. from_user
        2. to_user
        3. prepare content
        4. prepare video
        5. prepare picture
        6. sort order
        6. packing object
    """
    # 1. from_user
    from_user_id = user_id

    # 2. to_user
    to_user_id = order_usecase.retrieve_to_user_id(db, req.order_no)
    if to_user_id is None:
        raise exception.NoExistOrder

    # 3. prepare content
    content = commom_usecase.clean_content(req.content)

    # 4. prepare video
    video_id_list = video_usecase.videos_info_to_ids(
        db, req.videos_info_private)
    video_sort = [idx.order_index for idx in req.videos_info_private] \
        if req.videos_info_private is not None else []

    #logworker.warning() 

    # 5. prepare picture
    picture_id_list = picture_usecase.pictures_info_to_ids(
        db, req.pictures_info_private)
    picture_sort = [
        idx.order_index for idx in req.pictures_info_private] \
        if req.pictures_info_private is not None else []

    # 6. prepare sorting order
    sort_order = picture_sort + video_sort

    # 7. packing object
    data = DictObject(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        content=content,
        picture_id_list=picture_id_list,
        video_id_list=video_id_list,
        sort_order=sort_order
    )

    return data
