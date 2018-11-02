from sqlalchemy.orm import Session

from . import authority as auth_usecase

from . import order as order_usecase
from flask import request
from moretime.config.const import MoretimeRate
from moretime.api.wapp import logworker
from moretime.wrong import exception
import moretime.orm.rate as rate_orm
import moretime.orm.user as user_orm
import moretime.orm.order as order_orm


def submit_rate(db: Session, order_no: int, rate: int):
    """  """
    # 1. can do or not
    # auth_usecase.has_authority(db, from_user_id, 'submit_rate', poster_id)

    # 2. create a rate
    to_user_id = create_rate(db, order_no, rate)

    # 3. update the user trust 【暂缓】有复杂公式进行计算
    # upsert_user_trust(db, to_user_id)
    return to_user_id


def create_rate(db: Session, order_no: int, rate: int):
    user_id = request.current_user_id
    # 1. order_no & seller_id
    m_order_poster = order_usecase.obtain_order_poster(db, order_no=order_no)
    seller_id = m_order_poster.seller_id

    # 2. has rate ? 【存在则报错】
    m_rate = rate_orm.find_rate_by_order_no(db, order_no)
    if m_rate is not None:
        raise exception.MoretimeRateAlreadyExisted(order_no)

    # 3. create or update
    rate_orm.upsert_rate_transaction(
        db, order_no=order_no, rate=rate,
        buyer_id=user_id, seller_id=seller_id)

    return seller_id


def has_order_rate(db: Session, order_no: int):
    """  """
    result = False
    m_rate = rate_orm.find_rate_by_order_no(db, order_no)
    if m_rate:
        result = True
    return result


def upsert_user_trust(db: Session, to_user_id: int):
    """  """
    rateList = rate_orm.find_rate_by_to_user_id(db, to_user_id)
    if not rateList:  # shold create
        avg_rate = sum(rateList) / len(rateList)  # 简单实现
        user_orm.create_trust_by_user_id(db, to_user_id, avg_rate)
    else:
        avg_rate = sum(rateList) / len(rateList)  # 简单实现
        user_orm.update_trust_by_user_id(db, to_user_id, avg_rate)


def obtain_rate(db, poster_id=None):
    rate = MoretimeRate.Default.value

    if poster_id is not None:
        _rate_ = obtain_rate_by_poster_id(db, poster_id)
        if _rate_ is not None:
            rate = _rate_

    return rate


def obtain_rate_by_poster_id(db, poster_id):
    """  """
    m_order = order_orm.find_order_poster_by_poster_id(db, poster_id)
    if m_order is not None:

        m_rate = rate_orm.find_rate_by_order_no(db, m_order.order_no)
        if m_rate is not None:
            return m_rate.rate
