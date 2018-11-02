from sqlalchemy.orm import Session
from moretime.api.wapp import logworker
from moretime.util import qiniu, DictObject
from moretime.orm import user as user_orm


def obtain_user(db: Session, user_id: int):
    """   """
    # 1. basic
    m_user_info = user_orm.find_user_info_by_user_id(db, user_id)
    if m_user_info is None:
        raise exception.NoExistUserInfo(user_id)

    # 2. information
    nickname = m_user_info.nickname

    try:
        avatar_url = qiniu.url_from_path(m_user_info.avatar_oss)
    except Exception as e:
        avatar_url = ''
        logworker.exception("obtain_user url_from_path")
        logworker.error([user_id])

    # packing
    data = DictObject(user_id=user_id, nickname=nickname,
                      avatar_url=avatar_url)

    return data
