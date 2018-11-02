#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from moretime.config.const import ChangeVisiblePart, DatabaseStatus, PublicVisible

import moretime.usecase.visible as visible_usecase
from moretime.usecase import reply as reply_usecase
import moretime.orm.reply as reply_orm

from . import update


def delete(db: Session, user_id: int, poster_id: int):
    """
        1. update poster content public
        2. update&clean poster+reply picurevideo public
        3. update status = -1
        4. update reply status = -1
    """
    # 1. update poster content public
    visible_usecase.update_visible(
        db, user_id, poster_id,
        ChangeVisiblePart.Media.value, PublicVisible.No.value)

    # 2. update&clean poster+reply picurevideo public
    visible_usecase.update_visible(
        db, user_id, poster_id,
        ChangeVisiblePart.Content.value, PublicVisible.No.value)

    # 3. update status = -1
    update.update(db, poster_id, status=DatabaseStatus.Delete.value)

    # 4. update reply status = -1
    m_reply_list = reply_orm.find_reply_by_poster_id(db, poster_id)
    if m_reply_list is None:
        for m in m_reply_list:
            reply_usecase.delete(db, m.id)
