from typing import List
from sqlalchemy.orm import Session
from moretime.util import current_timestamp
from moretime.orm.orm_mysql import MoretimeRateModel
from moretime.orm import poster as poster_orm
from moretime.orm import order as order_orm


def create_rate(
        db: Session, order_no: int, rate: int,
        buyer_id: int, seller_id: int) ->int:
    order_rate = MoretimeRateModel(
        order_no=order_no,
        rate=rate,
        update_ts=current_timestamp(),
        buyer_id=buyer_id,
        seller_id=seller_id
    )
    return order_rate


def upsert_rate_transaction(
        db: Session, order_no: int, rate: int,
        buyer_id: int, seller_id: int) ->int:
    order_rate = None
    try:
        order_rate = create_rate(
            db, order_no, rate, buyer_id, seller_id)

        db.merge(order_rate)
        db.commit()
    except Exception as e:
        db.rollback()
        print('upsert_rate_transaction', str(e))
        raise

    return order_rate


def find_rate_by_order_no(
        db: Session, order_no: int):
    rate = db.query(MoretimeRateModel).filter(
        MoretimeRateModel.order_no == order_no
    ).first()
    return rate


def find_rate_by_from_user_id(
        db: Session, from_user_id: int):
    rate = db.query(MoretimeRateModel).filter(
        MoretimeRateModel.from_user_id == from_user_id
    ).all()
    return rate


def find_rate_by_to_user_id(
        db: Session, to_user_id: int):
    rate = db.query(MoretimeRateModel).filter(
        MoretimeRateModel.seller_id == to_user_id
    ).all()
    return rate


def find_rate_by_poster_id(
        db: Session, poster_id: int):
    rate = db.query(MoretimeRateModel).filter(
        MoretimeRateModel.poster_id == poster_id
    ).first()
    return rate


def update_rate_by_order_no(
        db: Session,
        order_no: int):
    # 【预留】
    pass


def delete_rate_by_order_no(
        db: Session, order_no: int):
    try:
        m_rate = MoretimeRateModel(order_no=order_no)
        m_rate.status = -1,
        m_rate.update_ts = current_timestamp()

        db.merge(m_rate)
        db.commit()
    except Exception as e:
        db.rollback()
        print('delete_rate_by_order_no', str(e))
        raise
