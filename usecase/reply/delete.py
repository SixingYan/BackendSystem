#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from . import update

from moretime.config.const import DatabaseStatus


def delete(db: Session, reply_id: int):
    """  """
    update.update(db, reply_id, status=DatabaseStatus.Delete.value)


def clean(db: Session, reply_id):
    '''【预留】 消息界面不再显示 '''
    pass
