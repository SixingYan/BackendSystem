# third
from typing import List
from sqlalchemy.orm import Session

from moretime.orm import order as order_orm
from moretime.wrong import exception


def has_order_poster(db: Session, order_no: int) -> bool:
    """
    """
    result = False

    m_order_poster = obtain_order_poster(db, order_no=order_no)

    if m_order_poster is not None:
        result = True

    return result


def obtain_order(db: Session, order_no: int):
    """   """
    m_order = order_orm.find_order_by_order_no(db, order_no)

    return m_order


def obtain_order_poster(
        db: Session, order_no: int=None, poster_id: int=None):
    """   """
    data = None

    if order_no is not None:
        data = obtain_order_poster_by_order_no(db, order_no)

    if poster_id is not None:
        data = obtain_order_poster_by_poster_id(db, poster_id)

    return data


def obtain_order_poster_by_order_no(db: Session, order_no: int):
    """   """
    m_order_poster = order_orm.find_order_poster_by_order_no(db, order_no)

    return m_order_poster


def obtain_order_poster_by_poster_id(db: Session, poster_id: int):
    """   """
    m_order_poster = order_orm.find_order_poster_by_poster_id(db, poster_id)

    return m_order_poster


def submit(
        db: Session, order_no: int, poster_id: int,
        from_user_id: int, to_user_id: int)->int:
    """ """
    m_order_poster = order_orm.create_order_poster_transaction(
        db, order_no,
        from_user_id,
        poster_id,
        to_user_id
    )

    return m_order_poster


def retrieve_to_user_id(db, order_no: int)->int:
    """   """
    m_order = order_orm.find_order_by_order_no(db, order_no)

    if m_order is None:
        raise exception.NoExistOrder(order_no)

    return m_order.buyer_id


def retrieve_order(db: Session, order_no: int):
    """  """
    m_order = order_orm.find_order_by_order_no(db, order_no)

    return m_order


def retrieve_timeshare(db: Session, time_sharing_id: int):
    """  """
    m_timeshare = order_orm.find_time_sharing_by_id(db, time_sharing_id)

    return m_timeshare
