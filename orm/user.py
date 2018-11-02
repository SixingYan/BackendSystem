from sqlalchemy.orm import Session
from moretime.orm.orm_mysql import UserInfoModel, UserModel


def create_trust_by_user_id(db, user_id, rate):
    pass


def find_user_info_by_user_id(db: Session, user_id: int):
    m_info = db.query(UserInfoModel).filter(
        UserInfoModel.user_id == user_id
    ).first()
    return m_info


def find_user_by_id(db, user_id):
    m_user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()
    return m_user
