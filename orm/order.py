#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from moretime.orm.orm_mysql import TimeSharingOrderModel, TimeSharingModel
from moretime.orm.orm_mysql import OrderPosterModel
from moretime.util import current_timestamp


def find_order_by_order_no(db: Session, order_no: int):
    m = db.query(TimeSharingOrderModel).filter(
        TimeSharingOrderModel.order_no == order_no).first()
    return m


def find_time_sharing_by_id(db: Session, id: int):
    m = db.query(TimeSharingModel).filter(
        TimeSharingModel.id == id).first()
    return m


def find_order_poster_by_order_no(db: Session, order_no: int):
    m = db.query(OrderPosterModel).filter(
        OrderPosterModel.order_no == order_no).first()
    return m


def find_order_poster_by_poster_id(db: Session, poster_id: int):
    m = db.query(OrderPosterModel).filter(
        OrderPosterModel.poster_id == poster_id).first()
    return m


def create_order_poster_transaction(
        db: Session, order_no: int,
        user_id: int, poster_id: int, to_user_id: int)->int:
    try:
        order_poster = OrderPosterModel(
            order_no=order_no,
            poster_id=poster_id,
            create_ts=current_timestamp(),
            seller_id=user_id,
            buyer_id=to_user_id
        )

        db.add(order_poster)
        db.commit()
    except Exception as e:
        # TODO: LOG
        db.rollback()
        print('create_order_poster_transaction', str(e))
        raise

    return order_poster
