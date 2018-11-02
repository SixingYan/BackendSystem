"""
	这里是入口，在这里转发具体操作
"""
from sqlalchemy.orm import Session
from moretime.api.wapp import logworker
from flask import request
from . import obtain as o
from . import submit as s
from . import update as u
from . import visible as v
from . import delete as d


def obtain(*args, **kwargs):
    return o.obtain(*args, **kwargs)


def obtain_simple(*args, **kwargs):
    return o.obtain_simple(*args, **kwargs)


def submit(*args, **kwargs):
    return s.submit(*args, **kwargs)


def update(*args, **kwargs):  # 【预留】
    return u.update(*args, **kwargs)


def visible(*args, **kwargs):
    return v.visible(*args, **kwargs)


def delete(*args, **kwargs):
    return d.delete(*args, **kwargs)


def is_first_submit(db: Session, poster_id: int)->bool:
    result = False
    m_reply_list = o.obtain(db, poster_id=poster_id)
    if len(m_reply_list) == 1:  # 说明之前没有,只有刚刚评论的一条
        result = True

    return result


def has_already_submit(db: Session, poster_id: int, ):
    user_id = request.current_user_id
    result = False
    m_reply_list = o.obtain(db, poster_id=poster_id)
    
    for m_reply in m_reply_list:
        if m_reply.reply.from_user_id == user_id:
            result = True
            break
        else:
            flag = False
            for rep in m_reply.follow_reply_list:
                if rep.from_user_id == user_id:
                    result = True
                    flag = True
                    break
            if flag is True:
                break

    return result
