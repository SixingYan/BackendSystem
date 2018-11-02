import moretime.orm.reply as reply_orm


def update(db, reply_id: int, status: int=None):
    reply_orm.update_reply_by_id(db, reply_id, status)
