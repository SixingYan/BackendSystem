import moretime.usecase.poster as poster_usecase


def toread(db, poster_id: int):
    m_poster = poster_usecase.obtain_simple(db, poster_id)
    m_poster.to_user_id
    pass


def unread_count(user_id: int):
    pass


def unread_clean(user_id: int):
    pass
