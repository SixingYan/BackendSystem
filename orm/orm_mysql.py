#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Index
from sqlalchemy.dialects.mysql import \
    TINYINT, SMALLINT, INTEGER, BIGINT, \
    VARCHAR, TEXT, \
    DECIMAL, NUMERIC, \
    TIMESTAMP, DATE, DATETIME
from sqlalchemy.sql.schema import DefaultClause
from sqlalchemy.sql.elements import TextClause


_ = TINYINT
_ = SMALLINT
_ = INTEGER
_ = BIGINT
_ = VARCHAR
_ = TEXT
_ = DECIMAL
_ = NUMERIC
_ = TIMESTAMP
_ = DATE
_ = DATETIME


from sqlalchemy.ext.declarative import as_declarative
import ast
import time

@as_declarative()
class Base(object):

    def fields(self):
        fields = dict()
        for column in self.__table__.columns:
            fields[column.name] = getattr(self, column.name)
        return fields

    def keys(self):
        columns = self.__table__.columns
        return tuple([c.name for c in columns])

    def add(self, session_):
        return session_.add(self)

    def update(self, fields):
        for column in self.__table__.columns:
            if column.name in fields:
                setattr(self, column.name, fields[column.name])

    def to_dict(self):
        d = {k: v for k, v in vars(self).items() if not k.startswith('_')}
        return str(d)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            data = ast.literal_eval(data)
        id = None
        if "id" in data:
            id = data.pop("id")

        o = cls(**data)
        o.id = id
        return o

    @classmethod
    def get(cls, id_, session_):
        return session_.query(cls).get(id_)

    @classmethod
    def query(cls, session_):
        return session_.query(cls)

    @classmethod
    def query_id(cls, session_):
        return session_.query(cls.id)

    @classmethod
    def local_ts(cs):
        return int(time.mktime(time.localtime()))


class AbuseReportModel(Base):
    __tablename__ = 'abuse_report'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1), comment='0 未处理  1  已处理')
    to_user_id = Column('to_user_id', INTEGER(display_width=11), comment=' 内容发布这的user_id\\n\\n')
    user_id = Column('user_id', INTEGER(display_width=11), comment='举报人')
    remark = Column('remark', VARCHAR(length=255), comment='管理员备注')
    target_id = Column('target_id', VARCHAR(length=32), comment='内容的id ， target_id\\n\\n')
    target_type = Column('target_type', VARCHAR(length=32), comment='内容归类， target_type    视频/评论/摩尔时光等\\n\\n')
    reason = Column('reason', VARCHAR(length=255), comment='举报原因， reason, 涉黄，恐怖，谣言等\\n\\n')
    create_ts = Column('create_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('search_order_index', Column('create_ts', INTEGER(display_width=10)), Column('status', TINYINT(display_width=1), comment='0 未处理  1  已处理')),
    )


class AddressModel(Base):
    __tablename__ = 'address'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    lng = Column('lng', DECIMAL(precision=10, scale=6), comment='经度')
    lat = Column('lat', DECIMAL(precision=10, scale=6), comment='纬度')
    province = Column('province', VARCHAR(length=8), comment='省份(包括自治区和直辖市)')
    city = Column('city', VARCHAR(length=12), comment='城市')
    district = Column('district', VARCHAR(length=8), comment='区')
    street = Column('street', VARCHAR(length=32), comment='街道地址 具体到街道号,小区,单位等 如: 张自忠路3号段祺瑞执政府旧址')
    room = Column('room', VARCHAR(length=32), comment='具体门牌号 如: 16号楼3单元202室')
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='0: 正常 -1: 删除')
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class AdminRoleModel(Base):
    __tablename__ = 'admin_role'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(length=45), nullable=False)
    auth = Column('auth', VARCHAR(length=255), nullable=False)
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))


class AdviseReportModel(Base):
    __tablename__ = 'advise_report'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    url = Column('url', VARCHAR(length=255))
    cat = Column('cat', TINYINT(display_width=1))
    status = Column('status', TINYINT(display_width=1))
    remark = Column('remark', VARCHAR(length=255))
    img = Column('img', VARCHAR(length=255))
    user_id = Column('user_id', INTEGER(display_width=11))
    contact = Column('contact', VARCHAR(length=255))
    create_ts = Column('create_ts', INTEGER(display_width=10))


class AppAdModel(Base):
    __tablename__ = 'app_ad'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1))
    adsrc = Column('adsrc', VARCHAR(length=255))
    adurl = Column('adurl', VARCHAR(length=255))
    comment = Column('comment', VARCHAR(length=64))
    interval = Column('interval', TINYINT(display_width=1))
    creator = Column('creator', INTEGER(display_width=11))
    update_ts = Column('update_ts', INTEGER(display_width=10), nullable=False)
    __table_args__ = (
        Index('status_update_ts', Column('status', TINYINT(display_width=1)), Column('update_ts', INTEGER(display_width=10), nullable=False)),
    )


class AppConfigModel(Base):
    __tablename__ = 'app_config'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1))
    app_version = Column('app_version', SMALLINT(display_width=5))
    content = Column('content', TEXT(collation='utf8mb4_unicode_ci'))
    comment = Column('comment', VARCHAR(length=64))
    creator = Column('creator', INTEGER(display_width=11))
    update_ts = Column('update_ts', INTEGER(display_width=10), nullable=False)
    __table_args__ = (
        Index('status_update_ts', Column('status', TINYINT(display_width=1)), Column('update_ts', INTEGER(display_width=10), nullable=False)),
    )


class AuthGroupModel(Base):
    __tablename__ = 'auth_group'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(length=80), nullable=False)
    __table_args__ = (
        Index('name', Column('name', VARCHAR(length=80), nullable=False), unique=True),
    )


class AuthUserModel(Base):
    __tablename__ = 'auth_user'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    password = Column('password', VARCHAR(length=128), nullable=False)
    last_login = Column('last_login', DATETIME(fsp=6))
    is_superuser = Column('is_superuser', TINYINT(display_width=1), nullable=False)
    username = Column('username', VARCHAR(length=150), nullable=False)
    first_name = Column('first_name', VARCHAR(length=30), nullable=False)
    last_name = Column('last_name', VARCHAR(length=150), nullable=False)
    email = Column('email', VARCHAR(length=254), nullable=False)
    is_staff = Column('is_staff', TINYINT(display_width=1), nullable=False)
    is_active = Column('is_active', TINYINT(display_width=1), nullable=False)
    date_joined = Column('date_joined', DATETIME(fsp=6), nullable=False)
    __table_args__ = (
        Index('username', Column('username', VARCHAR(length=150), nullable=False), unique=True),
    )


class CarerApplicationModel(Base):
    __tablename__ = 'carer_application'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    intro_video_id = Column('intro_video_id', INTEGER(display_width=11, unsigned=True), comment='个人视频 id')
    playground_video_id = Column('playground_video_id', INTEGER(display_width=11, unsigned=True), comment='场地视频 id')
    extra_video_ids = Column('extra_video_ids', VARCHAR(length=64), server_default=DefaultClause(TextClause("''")), comment='其他视频 id 逗号分割的字符列表 如 1,2,3')
    address_id = Column('address_id', INTEGER(display_width=11, unsigned=True), comment='地址 id')
    birth_certificate_oss = Column('birth_certificate_oss', VARCHAR(length=255), comment='出生证明文件 OSS 路径')
    care_exp = Column('care_exp', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')), comment='带娃经验(年)')
    degree = Column('degree', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='学历 0 无 1 专科 2 本科 3 硕士 4 博士')
    child_count_max = Column('child_count_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='最多接待多少孩子')
    child_age_min = Column('child_age_min', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最小年龄')
    child_age_max = Column('child_age_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最大年龄')
    result = Column('result', TINYINT(display_width=1), comment='不通过原因 | 0 审核通过 | 1 视频涉黄 | 2 视频涉政 | 3 视频涉暴恐 | 4 经验认证未通过 | 5 介绍视频没有看护人 | 6 介绍内容不符合要求 | 7 场地不符合要求 ')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='-1 删除 0 审核中 1 通过 2 拒绝 3 失效')
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class ChildModel(Base):
    __tablename__ = 'child'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    id_card_no = Column('id_card_no', VARCHAR(length=18))
    gender = Column('gender', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    birth_ts = Column('birth_ts', INTEGER(display_width=10))
    nickname = Column('nickname', VARCHAR(length=16))
    realname = Column('realname', VARCHAR(length=16))
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class CityModel(Base):
    __tablename__ = 'city'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(length=16), nullable=False)
    pinyin = Column('pinyin', VARCHAR(length=64))


class CouponModel(Base):
    __tablename__ = 'coupon'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    amount = Column('amount', VARCHAR(length=45), nullable=False)
    is_fixed = Column('is_fixed', VARCHAR(length=45), nullable=False)
    money_id = Column('money_id', VARCHAR(length=45))
    content_id = Column('content_id', VARCHAR(length=45))
    usage_id = Column('usage_id', VARCHAR(length=45))
    transaction_ids = Column('transaction_ids', VARCHAR(length=45))
    others_ids = Column('others_ids', VARCHAR(length=45))
    status = Column('status', VARCHAR(length=45), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', VARCHAR(length=45))


class CouponContentModel(Base):
    __tablename__ = 'coupon_content'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    title = Column('title', VARCHAR(length=125), nullable=False)
    content = Column('content', VARCHAR(length=255))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10))


class CouponMoneyModel(Base):
    __tablename__ = 'coupon_money'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    valid_min = Column('valid_min', TINYINT(display_width=1))
    valid_max = Column('valid_max', TINYINT(display_width=1))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10))


class CouponTransactionModel(Base):
    __tablename__ = 'coupon_transaction'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(length=45))
    description = Column('description', VARCHAR(length=45))
    status = Column('status', VARCHAR(length=45))
    create_ts = Column('create_ts', VARCHAR(length=45))


class CouponUsageModel(Base):
    __tablename__ = 'coupon_usage'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    max_uses = Column('max_uses', TINYINT(display_width=1))
    min_items = Column('min_items', TINYINT(display_width=1))
    max_items = Column('max_items', TINYINT(display_width=1))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False)


class DbluatestModel(Base):
    __tablename__ = 'dbluatest'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    name = Column('name', VARCHAR(length=16))
    age = Column('age', TINYINT(display_width=1))


class DeviceModel(Base):
    __tablename__ = 'device'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    uuid = Column('uuid', VARCHAR(length=64))
    device_id = Column('device_id', VARCHAR(length=64))
    device_manufacturer = Column('device_manufacturer', VARCHAR(length=64))
    device_platform = Column('device_platform', VARCHAR(length=16))
    device_brand = Column('device_brand', VARCHAR(length=45))
    device_type = Column('device_type', VARCHAR(length=32))
    app_version = Column('app_version', VARCHAR(length=16))
    os_version = Column('os_version', VARCHAR(length=24))
    os_lang = Column('os_lang', VARCHAR(length=16))
    channel = Column('channel', VARCHAR(length=32))
    resolution = Column('resolution', VARCHAR(length=32))
    create_ts = Column('create_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('uuid_index', Column('uuid', VARCHAR(length=64))),
        Index('device_id_index', Column('device_id', VARCHAR(length=64))),
    )


class DjangoContentTypeModel(Base):
    __tablename__ = 'django_content_type'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    app_label = Column('app_label', VARCHAR(length=100), nullable=False)
    model = Column('model', VARCHAR(length=100), nullable=False)
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', Column('app_label', VARCHAR(length=100), nullable=False), Column('model', VARCHAR(length=100), nullable=False), unique=True),
    )


class InsuranceModel(Base):
    __tablename__ = 'insurance'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    company = Column('company', VARCHAR(length=16))
    insurer_name = Column('insurer_name', VARCHAR(length=8))
    insurer_id_no = Column('insurer_id_no', VARCHAR(length=18))
    insurer_mobile = Column('insurer_mobile', VARCHAR(length=11))
    insured_name = Column('insured_name', VARCHAR(length=8))
    insured_id_no = Column('insured_id_no', VARCHAR(length=18))
    info = Column('info', TEXT())
    status = Column('status', TINYINT(display_width=1))
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class InviteModel(Base):
    __tablename__ = 'invite'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    from_user_id = Column('from_user_id', INTEGER(display_width=11), nullable=False)
    to_user_id = Column('to_user_id', INTEGER(display_width=11), nullable=False)
    invite_chain = Column('invite_chain', VARCHAR(length=255), comment='之前邀请关系链 ","分隔')
    reward_login = Column('reward_login', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='奖励首次登录 0 未奖励 1 已奖励')
    reward_pay_order = Column('reward_pay_order', INTEGER(display_width=12), server_default=DefaultClause(TextClause('0')), comment='奖励首次完成订单')
    channel = Column('channel', VARCHAR(length=64))
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False, server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('to_user_id', Column('to_user_id', INTEGER(display_width=11), nullable=False), unique=True),
    )


class InvitePictureModel(Base):
    __tablename__ = 'invite_picture'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11), nullable=False, comment='创建图片用户id, 0 为系统创建')
    pic_type = Column('pic_type', INTEGER(display_width=3), nullable=False, comment='图片类型 0 海报')
    cloud = Column('cloud', VARCHAR(length=16), nullable=False)
    bucket = Column('bucket', VARCHAR(length=64), nullable=False)
    oss = Column('oss', VARCHAR(length=255), nullable=False)
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))


class MessageModel(Base):
    __tablename__ = 'message'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    parent_id = Column('parent_id', INTEGER(display_width=11))
    from_user_id = Column('from_user_id', INTEGER(display_width=11), nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    subject = Column('subject', VARCHAR(length=64))
    content = Column('content', VARCHAR(length=255))
    expire_ts = Column('expire_ts', INTEGER(display_width=10), nullable=False)
    create_ts = Column('create_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('expire_ts_status', Column('expire_ts', INTEGER(display_width=10), nullable=False), Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))),
    )


class MessageRecipientModel(Base):
    __tablename__ = 'message_recipient'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    to_user_id = Column('to_user_id', INTEGER(display_width=11))
    status = Column('status', TINYINT(display_width=1))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class MidModel(Base):
    __tablename__ = 'mid'
    auto = Column('auto', INTEGER(display_width=11), primary_key=True, nullable=False)
    base = Column('base', INTEGER(display_width=11), primary_key=True, nullable=False)
    random = Column('random', INTEGER(display_width=11), primary_key=True, nullable=False)
    tag = Column('tag', VARCHAR(length=16))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    ts = Column('ts', TIMESTAMP(), server_default=DefaultClause(TextClause('CURRENT_TIMESTAMP')))
    __table_args__ = (
        Index('mid_auto_base_random', Column('auto', INTEGER(display_width=11), primary_key=True, nullable=False), Column('base', INTEGER(display_width=11), primary_key=True, nullable=False), Column('random', INTEGER(display_width=11), primary_key=True, nullable=False), unique=True),
    )


class MoretimePictureModel(Base):
    __tablename__ = 'moretime_picture'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    cloud = Column('cloud', VARCHAR(length=16), nullable=False)
    bucket = Column('bucket', VARCHAR(length=64), nullable=False)
    key = Column('key', VARCHAR(length=128), nullable=False)
    etag = Column('etag', VARCHAR(length=32))
    mime_type = Column('mime_type', VARCHAR(length=125))
    size = Column('size', INTEGER(display_width=10, unsigned=True))
    duration = Column('duration', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    width = Column('width', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    height = Column('height', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    persistent_id = Column('persistent_id', VARCHAR(length=32))
    pfop_vframe_status = Column('pfop_vframe_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    pfop_transcode_status = Column('pfop_transcode_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))


class MoretimeRateModel(Base):
    __tablename__ = 'moretime_rate'
    order_no = Column('order_no', INTEGER(display_width=10), primary_key=True, nullable=False)
    buyer_id = Column('buyer_id', INTEGER(display_width=11), nullable=False)
    seller_id = Column('seller_id', INTEGER(display_width=11), nullable=False)
    rate = Column('rate', TINYINT(display_width=4), nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=10), nullable=False)


class MoretimeVideoModel(Base):
    __tablename__ = 'moretime_video'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    cloud = Column('cloud', VARCHAR(length=16), nullable=False)
    bucket = Column('bucket', VARCHAR(length=64), nullable=False)
    key = Column('key', VARCHAR(length=128), nullable=False)
    etag = Column('etag', VARCHAR(length=32))
    mime_type = Column('mime_type', VARCHAR(length=125))
    size = Column('size', INTEGER(display_width=10, unsigned=True))
    duration = Column('duration', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    width = Column('width', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    height = Column('height', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    persistent_id = Column('persistent_id', VARCHAR(length=32))
    pfop_vframe_status = Column('pfop_vframe_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    pfop_transcode_status = Column('pfop_transcode_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))


class OrderModel(Base):
    __tablename__ = 'order'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11), comment='下单用户')
    service_item_id = Column('service_item_id', INTEGER(display_width=11), comment='订单所属服务实例')
    price = Column('price', INTEGER(display_width=11), comment='订单金额 单位: 摩尔豆')
    remark = Column('remark', VARCHAR(length=32), server_default=DefaultClause(TextClause("''")), comment='下单时用户的留言')
    insurance_id = Column('insurance_id', INTEGER(display_width=11), comment='订单保险')
    status = Column('status', TINYINT(display_width=1), comment='订单状态 0: 待支付 1: 已支付 2: 完成 3: 取消 4: 关闭')
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class OrderChildModel(Base):
    __tablename__ = 'order_child'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    order_id = Column('order_id', INTEGER(display_width=11))
    child_id = Column('child_id', INTEGER(display_width=11))
    status = Column('status', TINYINT(display_width=1))
    create_ts = Column('create_ts', INTEGER(display_width=10))


class OrderPosterModel(Base):
    __tablename__ = 'order_poster'
    order_no = Column('order_no', INTEGER(display_width=11), primary_key=True, nullable=False, comment='订单号')
    poster_id = Column('poster_id', INTEGER(display_width=11), nullable=False, comment='摩尔时光号')
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False, comment='创建时间')
    seller_id = Column('seller_id', INTEGER(display_width=11), nullable=False, comment='看护人id')
    buyer_id = Column('buyer_id', INTEGER(display_width=11), nullable=False, comment='监护人id')
    update_ts = Column('update_ts', INTEGER(display_width=10), comment='更新时间(预留)')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))


class OssModel(Base):
    __tablename__ = 'oss'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    cloud = Column('cloud', VARCHAR(length=8), nullable=False)
    bucket = Column('bucket', VARCHAR(length=64), nullable=False)
    key = Column('key', VARCHAR(length=128), nullable=False)
    etag = Column('etag', VARCHAR(length=32))
    mime_type = Column('mime_type', VARCHAR(length=16))
    size = Column('size', INTEGER(display_width=10, unsigned=True))
    status = Column('status', TINYINT(display_width=1), nullable=False)
    created_time = Column('created_time', TIMESTAMP(), nullable=False, server_default=DefaultClause(TextClause('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))
    __table_args__ = (
        Index('objcet_cloud_bucket_key_unique', Column('cloud', VARCHAR(length=8), nullable=False), Column('bucket', VARCHAR(length=64), nullable=False), Column('key', VARCHAR(length=128), nullable=False), unique=True),
    )


class OssRefModel(Base):
    __tablename__ = 'oss_ref'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=10, unsigned=True))
    object_id = Column('object_id', INTEGER(display_width=10, unsigned=True))
    tag = Column('tag', VARCHAR(length=32))
    created_time = Column('created_time', TIMESTAMP())
    status = Column('status', TINYINT(display_width=1))


class PlaygroundModel(Base):
    __tablename__ = 'playground'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True))
    address_id = Column('address_id', INTEGER(display_width=11, unsigned=True))
    type = Column('type', TINYINT(display_width=4))
    capacity = Column('capacity', SMALLINT(display_width=6))
    space = Column('space', SMALLINT(display_width=6))
    equip = Column('equip', VARCHAR(length=32))
    status = Column('status', TINYINT(display_width=4), server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=11))
    update_ts = Column('update_ts', INTEGER(display_width=11))


class PointModel(Base):
    __tablename__ = 'point'
    user_id = Column('user_id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False, server_default=DefaultClause(TextClause('0')))
    point = Column('point', INTEGER(display_width=11))
    total_grant = Column('total_grant', INTEGER(display_width=11))
    total_deposit = Column('total_deposit', INTEGER(display_width=11))
    total_withdraw = Column('total_withdraw', INTEGER(display_width=11))


class PointDepositModel(Base):
    __tablename__ = 'point_deposit'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False, comment='积分 - 购买')
    tx_id = Column('tx_id', INTEGER(display_width=11))
    customer_id = Column('customer_id', INTEGER(display_width=10, unsigned=True), nullable=False)
    point = Column('point', INTEGER(display_width=11), nullable=False, server_default=DefaultClause(TextClause('0')), comment='购买积分数量\\n')
    amount = Column('amount', INTEGER(display_width=10), nullable=False, server_default=DefaultClause(TextClause('0')), comment='花费的法币金额，单位为分')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='状态  -1 人工删除  -2 过期删除   0 等待支付  1 已支付  2 已对账 ')
    trade_no = Column('trade_no', VARCHAR(length=32), nullable=False, comment='内部交易流水号')
    out_trade_no = Column('out_trade_no', VARCHAR(length=32), comment='外部订单号 -  第三方支付返回的支付订单流水号，以方便和第三方对账。')
    payment_channel = Column('payment_channel', TINYINT(display_width=1), nullable=False, comment='0 微信官方渠道  1  阿里官方渠道  2  银联官方渠道   3  现在支付  4 pingxx支付')
    payment_method = Column('payment_method', TINYINT(display_width=1, unsigned=True), nullable=False, comment='支付类型 APP_WXPAY     =  0, -- 微信官方渠道AP\\n    WAP_WXPAY     =  1, -- 微信官方渠道WAP\\n    APP_ALIPAY    =  2, -- 支付宝官方渠道\\n    WAP_ALIPAY    =  3, -- 支付宝官方渠道\\n    UNIPAY        =  4, -- 银联官方渠道\\n    BACCOUNT      =  5, -- 银行账号转账\\n')
    notify_body = Column('notify_body', TEXT(), comment='第三方通知')
    payload_body = Column('payload_body', TEXT(), comment='订单相关数据')
    do_after_paid = Column('do_after_paid', VARCHAR(length=16))
    client_ip = Column('client_ip', VARCHAR(length=16), comment='客户ip地址')
    paied_ts = Column('paied_ts', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')), comment='支付时间')
    expire_ts = Column('expire_ts', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')), comment='如果订单在expire_ts之前未支付，那么删除订单。')
    create_ts = Column('create_ts', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    create_ym = Column('create_ym', INTEGER(display_width=6))
    __table_args__ = (
        Index('customer_id', Column('customer_id', INTEGER(display_width=10, unsigned=True), nullable=False)),
        Index('create_ym', Column('create_ym', INTEGER(display_width=6))),
        Index('created_ts_status', Column('create_ts', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0'))), Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='状态  -1 人工删除  -2 过期删除   0 等待支付  1 已支付  2 已对账 ')),
        Index('trade_no', Column('trade_no', VARCHAR(length=32), nullable=False, comment='内部交易流水号')),
        Index('out_trade_no', Column('out_trade_no', VARCHAR(length=32), comment='外部订单号 -  第三方支付返回的支付订单流水号，以方便和第三方对账。')),
    )


class PointGrantModel(Base):
    __tablename__ = 'point_grant'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False, comment='积分 - 奖励')
    tx_id = Column('tx_id', INTEGER(display_width=11))
    customer_id = Column('customer_id', INTEGER(display_width=11, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    point = Column('point', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')), comment='摩尔积分数量， 可正可负\\n')
    cashable = Column('cashable', INTEGER(display_width=11))
    uncashable = Column('uncashable', INTEGER(display_width=11))
    channel = Column('channel', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='积分奖励渠道：0 注册奖励   1 推荐注册  2 充值激励  3 订单取消-处罚金  4 订单被取消-补偿金')
    remark = Column('remark', VARCHAR(length=64), comment='原因 | 依据')
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    create_ym = Column('create_ym', INTEGER(display_width=6))
    __table_args__ = (
        Index('customer_id', Column('customer_id', INTEGER(display_width=11, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))),
        Index('created_ts_status', Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))),
    )


class PointGrantConstraintTimeModel(Base):
    __tablename__ = 'point_grant_constraint_time'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    grant_id = Column('grant_id', INTEGER(display_width=10))
    status = Column('status', TINYINT(display_width=1), comment='0 表示未check ， \\n1 表示已check，符合条件\\n2 表示已check，不符合条件，已撤回推用户的point奖励')
    minimum = Column('minimum', INTEGER(display_width=10), comment='最低消费')
    start_ts = Column('start_ts', INTEGER(display_width=10))
    end_ts = Column('end_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('end_ts_status', Column('end_ts', INTEGER(display_width=10)), Column('status', TINYINT(display_width=1), comment='0 表示未check ， \\n1 表示已check，符合条件\\n2 表示已check，不符合条件，已撤回推用户的point奖励')),
    )


class PointOrderModel(Base):
    __tablename__ = 'point_order'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False, comment='积分 - 购买')
    tx_id = Column('tx_id', INTEGER(display_width=11))
    from_customer_id = Column('from_customer_id', INTEGER(display_width=10, unsigned=True), nullable=False)
    to_customer_id = Column('to_customer_id', INTEGER(display_width=11), nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='0 买方已付款  1  卖方已收款  2  异常交易，挂起，管理员介入  3  买方违约，导致退款  4  卖方违约，导致退款')
    point = Column('point', INTEGER(display_width=11), nullable=False, server_default=DefaultClause(TextClause('0')), comment='积分\\npoint = cashable_point + uncashable_point')
    cashable = Column('cashable', INTEGER(display_width=11))
    uncashable = Column('uncashable', INTEGER(display_width=11))
    trade_no = Column('trade_no', VARCHAR(length=32), nullable=False, comment='内部交易流水号')
    order_no = Column('order_no', VARCHAR(length=32), comment='外部订单号')
    refund_status = Column('refund_status', TINYINT(display_width=1), comment='0 正常状态  3  买方违约，导致退款  4  卖方违约，导致退款 ')
    remark = Column('remark', VARCHAR(length=128))
    client_ip = Column('client_ip', VARCHAR(length=16))
    create_ts = Column('create_ts', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    create_ym = Column('create_ym', INTEGER(display_width=6))
    __table_args__ = (
        Index('created_ts_status', Column('create_ts', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0'))), Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='0 买方已付款  1  卖方已收款  2  异常交易，挂起，管理员介入  3  买方违约，导致退款  4  卖方违约，导致退款')),
        Index('order_no', Column('order_no', VARCHAR(length=32), comment='外部订单号')),
        Index('trade_no', Column('trade_no', VARCHAR(length=32), nullable=False, comment='内部交易流水号')),
        Index('from_customer_id', Column('from_customer_id', INTEGER(display_width=10, unsigned=True), nullable=False)),
        Index('to_customer_id', Column('to_customer_id', INTEGER(display_width=11), nullable=False)),
        Index('create_ym', Column('create_ym', INTEGER(display_width=6))),
    )


class PointTxModel(Base):
    __tablename__ = 'point_tx'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    from_customer_id = Column('from_customer_id', INTEGER(display_width=10), comment='0 为系统用户')
    to_customer_id = Column('to_customer_id', INTEGER(display_width=10), comment='0 为系统用户')
    type = Column('type', TINYINT(display_width=1), comment='    ORDER_PREPAID       = 0,  -- 预付摩尔豆   - 订单交易\\n    ORDER_PAID          = 1,  -- 实付摩尔豆   - 订单交易 ( 和 0 互斥，更改状态)\\n    ORDER_REFUND        = 2,  -- 摩尔豆退还   - 订单交易 ( 订单取消 )\\n    ORDER_CANCEL_FINE   = 3,  -- 违约金-罚款  - 订单交易 ( 订单取消，罚违约方)\\n    ORDER_CANCEL_REWARD = 4,  -- 违约金-补偿  - 订单交易 ( 订单取消，罚违约方)\\n    SYS_REWARD          = 5,  -- 平台奖励\\n    SYS_FINE            = 6,  -- 平台处罚\\n    DEPOSIT             = 7,  -- 摩尔豆充值\\n    WITHDRAW_PREPAID    = 8,  -- 摩尔豆提现 申请\\n    WITHDRAW_PAID       = 9,  -- 摩尔豆提现 成功\\n    WITHDRAW_DENIED     = 10, -- 摩尔豆提现 拒绝\\n')
    point = Column('point', INTEGER(display_width=10))
    cashable = Column('cashable', INTEGER(display_width=10))
    uncashable = Column('uncashable', INTEGER(display_width=10))
    remark = Column('remark', VARCHAR(length=255))
    order_no = Column('order_no', VARCHAR(length=32))
    create_ts = Column('create_ts', INTEGER(display_width=10))
    create_ym = Column('create_ym', INTEGER(display_width=6))
    __table_args__ = (
        Index('create_ts', Column('create_ts', INTEGER(display_width=10))),
        Index('create_ym', Column('create_ym', INTEGER(display_width=6)), Column('type', TINYINT(display_width=1), comment='    ORDER_PREPAID       = 0,  -- 预付摩尔豆   - 订单交易\\n    ORDER_PAID          = 1,  -- 实付摩尔豆   - 订单交易 ( 和 0 互斥，更改状态)\\n    ORDER_REFUND        = 2,  -- 摩尔豆退还   - 订单交易 ( 订单取消 )\\n    ORDER_CANCEL_FINE   = 3,  -- 违约金-罚款  - 订单交易 ( 订单取消，罚违约方)\\n    ORDER_CANCEL_REWARD = 4,  -- 违约金-补偿  - 订单交易 ( 订单取消，罚违约方)\\n    SYS_REWARD          = 5,  -- 平台奖励\\n    SYS_FINE            = 6,  -- 平台处罚\\n    DEPOSIT             = 7,  -- 摩尔豆充值\\n    WITHDRAW_PREPAID    = 8,  -- 摩尔豆提现 申请\\n    WITHDRAW_PAID       = 9,  -- 摩尔豆提现 成功\\n    WITHDRAW_DENIED     = 10, -- 摩尔豆提现 拒绝\\n')),
        Index('type', Column('type', TINYINT(display_width=1), comment='    ORDER_PREPAID       = 0,  -- 预付摩尔豆   - 订单交易\\n    ORDER_PAID          = 1,  -- 实付摩尔豆   - 订单交易 ( 和 0 互斥，更改状态)\\n    ORDER_REFUND        = 2,  -- 摩尔豆退还   - 订单交易 ( 订单取消 )\\n    ORDER_CANCEL_FINE   = 3,  -- 违约金-罚款  - 订单交易 ( 订单取消，罚违约方)\\n    ORDER_CANCEL_REWARD = 4,  -- 违约金-补偿  - 订单交易 ( 订单取消，罚违约方)\\n    SYS_REWARD          = 5,  -- 平台奖励\\n    SYS_FINE            = 6,  -- 平台处罚\\n    DEPOSIT             = 7,  -- 摩尔豆充值\\n    WITHDRAW_PREPAID    = 8,  -- 摩尔豆提现 申请\\n    WITHDRAW_PAID       = 9,  -- 摩尔豆提现 成功\\n    WITHDRAW_DENIED     = 10, -- 摩尔豆提现 拒绝\\n')),
        Index('from_user_id', Column('from_customer_id', INTEGER(display_width=10), comment='0 为系统用户')),
        Index('order_no', Column('order_no', VARCHAR(length=32))),
        Index('to_user_id', Column('to_customer_id', INTEGER(display_width=10), comment='0 为系统用户')),
    )


class PointWithdrawModel(Base):
    __tablename__ = 'point_withdraw'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    tx_id = Column('tx_id', INTEGER(display_width=11))
    customer_id = Column('customer_id', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    amount = Column('amount', DECIMAL(precision=8, scale=2), nullable=False, server_default=DefaultClause(TextClause('0.00')), comment='提现的法币金额\\n')
    point = Column('point', INTEGER(display_width=11), nullable=False, server_default=DefaultClause(TextClause('0')), comment='消耗的积分')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='状态  -1 人工删除  -2 过期删除   0 等待人民币汇出  1 已汇出人民币  2 已人工确认汇出人民币')
    payment_channel = Column('payment_channel', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='0 微信官方渠道  1  阿里官方渠道  2  银联官方渠道   3  现在支付  4 pingxx支付  5  银行转账汇款  \\n10 云账户')
    payment_method = Column('payment_method', TINYINT(display_width=1), comment='支付方式')
    trade_no = Column('trade_no', VARCHAR(length=32), nullable=False, comment='内部交易流水号')
    out_trade_no = Column('out_trade_no', VARCHAR(length=32), comment='外部订单号 -  第三方支付返回的支付订单流水号，以方便和第三方对账。')
    paied_ts = Column('paied_ts', INTEGER(display_width=10), nullable=False, server_default=DefaultClause(TextClause('0')), comment='支付时间')
    account_no = Column('account_no', VARCHAR(length=16), nullable=False, comment='用户的 微信号/ 支付宝号/ 银行卡号')
    account_bank = Column('account_bank', VARCHAR(length=10), nullable=False, comment='银行')
    account_name = Column('account_name', VARCHAR(length=5), comment='姓名')
    account_real_name = Column('account_real_name', VARCHAR(length=32), comment='真实姓名\\n')
    account_id_no = Column('account_id_no', VARCHAR(length=18), comment='身份证号码')
    account_mobile = Column('account_mobile', VARCHAR(length=16), comment='收款通知手机号')
    remark = Column('remark', VARCHAR(length=255))
    operator_id = Column('operator_id', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')), comment='操作人 id')
    create_ts = Column('create_ts', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ym = Column('create_ym', INTEGER(display_width=6))
    __table_args__ = (
        Index('create_ts_status', Column('create_ts', INTEGER(display_width=10, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0'))), Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='状态  -1 人工删除  -2 过期删除   0 等待人民币汇出  1 已汇出人民币  2 已人工确认汇出人民币')),
    )


class PosterModel(Base):
    __tablename__ = 'poster'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    index_id = Column('index_id', INTEGER(display_width=11), nullable=False)
    update_ts = Column('update_ts', INTEGER(display_width=10))
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False)
    content = Column('content', VARCHAR(length=255))
    video_ids_public = Column('video_ids_public', VARCHAR(length=255), comment='example: 1,2,3,4,5,6')
    video_ids_private = Column('video_ids_private', VARCHAR(length=255), comment='example: 1,2,3,4,5,6')
    picture_ids_public = Column('picture_ids_public', VARCHAR(length=255), comment='example: 1,2,3,4,5,6')
    picture_ids_private = Column('picture_ids_private', VARCHAR(length=255), comment='example: 1,2,3,4,5,6')
    sort_order = Column('sort_order', VARCHAR(length=255))
    content_visible = Column('content_visible', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='0不可见 1 可见')
    picvid_visible = Column('picvid_visible', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='0不可见 1 可见')
    from_user_id = Column('from_user_id', INTEGER(display_width=10), nullable=False, comment='发送摩尔时光的人')
    to_user_id = Column('to_user_id', INTEGER(display_width=10), nullable=False, comment='接受摩尔时光的人')


class ReplyModel(Base):
    __tablename__ = 'reply'
    poster_id = Column('poster_id', INTEGER(display_width=11), nullable=False)
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False)
    update_ts = Column('update_ts', INTEGER(display_width=10))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    content = Column('content', VARCHAR(length=255), nullable=False)
    video_ids_public = Column('video_ids_public', VARCHAR(length=255))
    video_ids_private = Column('video_ids_private', VARCHAR(length=255))
    picture_ids_public = Column('picture_ids_public', VARCHAR(length=255))
    picture_ids_private = Column('picture_ids_private', VARCHAR(length=255))
    sort_order = Column('sort_order', VARCHAR(length=255))
    prior_id = Column('prior_id', INTEGER(display_width=11))
    parent_ids = Column('parent_ids', VARCHAR(length=255))
    from_user_id = Column('from_user_id', INTEGER(display_width=11), nullable=False)
    to_user_id = Column('to_user_id', INTEGER(display_width=11), nullable=False)


class ServiceModel(Base):
    __tablename__ = 'service'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11), comment='提供服务的用户id')
    provider_name = Column('provider_name', VARCHAR(length=32), comment='服务提供者\x08的名字 如: 小番茄的妈妈')
    playground_id = Column('playground_id', INTEGER(display_width=11), comment='活动场所 目前只支持一个')
    child_count_max = Column('child_count_max', SMALLINT(display_width=5), comment='孩子数量上限')
    child_age_max = Column('child_age_max', TINYINT(display_width=1), comment='孩子年龄上限 0则不限')
    child_age_min = Column('child_age_min', TINYINT(display_width=1), comment='孩子年龄下限 0则不限')
    content_id = Column('content_id', INTEGER(display_width=11), comment='内容介绍模版')
    status = Column('status', TINYINT(display_width=1), comment='0: 正常 -1: 删除')
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10), nullable=False)
    __table_args__ = (
        Index('carer_user_id_uindex', Column('user_id', INTEGER(display_width=11), comment='提供服务的用户id'), unique=True),
    )


class ServiceItemModel(Base):
    __tablename__ = 'service_item'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    service_id = Column('service_id', INTEGER(display_width=11))
    start_ts = Column('start_ts', INTEGER(display_width=10))
    end_ts = Column('end_ts', INTEGER(display_width=10))
    price = Column('price', INTEGER(display_width=11), comment='服务价格 单位: 摩尔豆')
    child_count = Column('child_count', SMALLINT(display_width=5), server_default=DefaultClause(TextClause('0')), comment='已报名孩子数量')
    description = Column('description', VARCHAR(length=64))
    repeat = Column('repeat', VARCHAR(length=5), comment='重复周期 None: 不重复 Day: 每天 Week: 每周 Month: 每月 Year: 每年')
    status = Column('status', TINYINT(display_width=1), comment='0: 正常 1 审核中 2 审核失败 -1: 删除')
    create_ts = Column('create_ts', INTEGER(display_width=10))
    update_ts = Column('update_ts', INTEGER(display_width=10))


class TestModel(Base):
    __tablename__ = 'test'
    user_id = Column('user_id', INTEGER(display_width=11), primary_key=True, nullable=False)
    nickname = Column('nickname', VARCHAR(length=45))


class TimeSharingModel(Base):
    __tablename__ = 'time_sharing'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11), nullable=False)
    child_age_min = Column('child_age_min', INTEGER(display_width=11), nullable=False, comment='接待孩子最小年龄')
    child_age_max = Column('child_age_max', INTEGER(display_width=11), nullable=False, comment='接待孩子最大年龄')
    child_count_max = Column('child_count_max', INTEGER(display_width=11), nullable=False, comment='最多接待多少孩子')
    address_id = Column('address_id', INTEGER(display_width=11), nullable=False, comment='活动地址 id')
    city_id = Column('city_id', INTEGER(display_width=11), comment='共享时间发布者所在城市id')
    start_ts = Column('start_ts', INTEGER(display_width=10), nullable=False)
    end_ts = Column('end_ts', INTEGER(display_width=10), nullable=False)
    price = Column('price', INTEGER(display_width=11), nullable=False)
    activity = Column('activity', VARCHAR(length=64), server_default=DefaultClause(TextClause("''")), comment='活动内容标签')
    description = Column('description', TEXT(), comment='详细描述')
    accompany_required = Column('accompany_required', TINYINT(display_width=4), nullable=False, server_default=DefaultClause(TextClause('1')), comment='是否必须家人陪同')
    child_count = Column('child_count', INTEGER(display_width=11), nullable=False, comment='已报名孩子数量')
    status = Column('status', TINYINT(display_width=4), server_default=DefaultClause(TextClause('0')), comment='0 正常 -1 删除')
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))


class TimeSharingOrderModel(Base):
    __tablename__ = 'time_sharing_order'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    order_no = Column('order_no', INTEGER(display_width=10), comment='订单号')
    buyer_id = Column('buyer_id', INTEGER(display_width=11), nullable=False, comment='下单user_id')
    guardian_id = Column('guardian_id', INTEGER(display_width=11), comment='guardian的 user_id')
    guardian_name = Column('guardian_name', VARCHAR(length=16), nullable=False)
    guardian_id_card_no = Column('guardian_id_card_no', VARCHAR(length=18), nullable=False)
    guardian_mobile = Column('guardian_mobile', VARCHAR(length=11), nullable=False)
    child_id = Column('child_id', INTEGER(display_width=11), comment='参加活动的child_id')
    child_nickname = Column('child_nickname', VARCHAR(length=16), nullable=False)
    child_name = Column('child_name', VARCHAR(length=16), nullable=False)
    child_id_card_no = Column('child_id_card_no', VARCHAR(length=18), nullable=False)
    time_sharing_id = Column('time_sharing_id', INTEGER(display_width=20), nullable=False)
    start_ts = Column('start_ts', INTEGER(display_width=10), nullable=False, comment='活动开始ts')
    end_ts = Column('end_ts', INTEGER(display_width=10), nullable=False, comment='活动结束ts')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='订单状态 1 待支付 2 进行中（已支付） 3 已取消 4 已完成 5 已关闭 ')
    refund_status = Column('refund_status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='退款状态 0 无退款 1 退款中 2 已退款 ')
    fund_status = Column('fund_status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='退款状态 0 无放款 1 放款中 2 已放款')
    seller_id = Column('seller_id', INTEGER(display_width=11), nullable=False)
    address_id = Column('address_id', INTEGER(display_width=11), nullable=False)
    city_id = Column('city_id', INTEGER(display_width=11))
    insurance_id = Column('insurance_id', INTEGER(display_width=11))
    remark = Column('remark', VARCHAR(length=100))
    cancel_reason = Column('cancel_reason', INTEGER(display_width=3), server_default=DefaultClause(TextClause('0')), comment='取消原因 家长：100 订单有误 101 已和看护人沟通 102 计划有变 103 其他 看护人：200')
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False, server_default=DefaultClause(TextClause('0')))
    payment_ts = Column('payment_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    cancel_ts = Column('cancel_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    finish_ts = Column('finish_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    close_ts = Column('close_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('order_no', Column('order_no', INTEGER(display_width=10), comment='订单号'), unique=True),
    )


class UserModel(Base):
    __tablename__ = 'user'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    code = Column('code', VARCHAR(length=8), nullable=False)
    mobile = Column('mobile', VARCHAR(length=11), nullable=False, server_default=DefaultClause(TextClause('0')))
    password = Column('password', VARCHAR(length=64), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=11, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('create_ts_status', Column('create_ts', INTEGER(display_width=11, unsigned=True), nullable=False, server_default=DefaultClause(TextClause('0'))), Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))),
        Index('mobile_UNIQUE', Column('mobile', VARCHAR(length=11), nullable=False, server_default=DefaultClause(TextClause('0'))), Column('code', VARCHAR(length=8), nullable=False), unique=True),
    )


class UserActionLogModel(Base):
    __tablename__ = 'user_action_log'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11))
    action = Column('action', VARCHAR(length=64))
    create_ts = Column('create_ts', INTEGER(display_width=10))


class UserAddressModel(Base):
    __tablename__ = 'user_address'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11), comment='用户 id')
    lng = Column('lng', DECIMAL(precision=10, scale=6), comment='经度')
    lat = Column('lat', DECIMAL(precision=10, scale=6), comment='纬度')
    province = Column('province', VARCHAR(length=8), comment='省/直辖市 如:北京市')
    city = Column('city', VARCHAR(length=12), comment='城市 如:北京市')
    city_id = Column('city_id', INTEGER(display_width=11))
    district = Column('district', VARCHAR(length=8), comment='区 如:海淀区')
    address = Column('address', VARCHAR(length=64), comment='街道地址 如:亮马桥路27号院1903号')
    name = Column('name', VARCHAR(length=32), comment='住宅、建筑、公司等名称 如:大鱼公司')
    room = Column('room', VARCHAR(length=32), comment='用户填写的房间号 如:2楼2018室')
    poi = Column('poi', VARCHAR(length=32), comment='第三方 SDK 给的 Point of Interest')
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('user_address_city', Column('city', VARCHAR(length=12), comment='城市 如:北京市')),
        Index('user_address_lng_lat', Column('lng', DECIMAL(precision=10, scale=6), comment='经度'), Column('lat', DECIMAL(precision=10, scale=6), comment='纬度')),
    )


class UserAdminModel(Base):
    __tablename__ = 'user_admin'
    user_id = Column('user_id', INTEGER(display_width=11), primary_key=True, nullable=False)
    role_id = Column('role_id', INTEGER(display_width=11), nullable=False)
    name = Column('name', VARCHAR(length=45), nullable=False)
    password = Column('password', VARCHAR(length=255))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False)


class UserCarerInfoModel(Base):
    __tablename__ = 'user_carer_info'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    intro_video_id = Column('intro_video_id', INTEGER(display_width=11, unsigned=True), comment='个人视频 id')
    playground_video_id = Column('playground_video_id', INTEGER(display_width=11, unsigned=True), comment='场地视频 id')
    extra_video_ids = Column('extra_video_ids', VARCHAR(length=64), nullable=False, server_default=DefaultClause(TextClause("''")), comment='其他视频 id 逗号分割的字符列表 如 1,2,3')
    address_id = Column('address_id', INTEGER(display_width=11, unsigned=True), comment='地址 id')
    city_id = Column('city_id', INTEGER(display_width=11), comment='城市id')
    lat = Column('lat', DECIMAL(precision=10, scale=6), comment='经度')
    lng = Column('lng', DECIMAL(precision=10, scale=6), comment='纬度')
    birth_certificate_oss = Column('birth_certificate_oss', VARCHAR(length=255), comment='出生证明文件 OSS 路径')
    degree = Column('degree', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='学历 0 无 1 专科 2 本科 3 硕士 4 博士')
    care_exp = Column('care_exp', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')), comment='带娃经验(年)')
    child_count_max = Column('child_count_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='最多接待多少孩子')
    child_age_min = Column('child_age_min', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最小年龄')
    child_age_max = Column('child_age_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='接待孩子最大年龄')
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='0 正常 -1 删除')
    update_ts = Column('update_ts', INTEGER(display_width=10))


class UserChildModel(Base):
    __tablename__ = 'user_child'
    user_id = Column('user_id', INTEGER(display_width=11), primary_key=True, nullable=False)
    child_id = Column('child_id', INTEGER(display_width=11), primary_key=True, nullable=False)
    create_ts = Column('create_ts', INTEGER(display_width=10))
    status = Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('user_child_user_id_child_id_status_uindex', Column('user_id', INTEGER(display_width=11), primary_key=True, nullable=False), Column('child_id', INTEGER(display_width=11), primary_key=True, nullable=False), Column('status', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0'))), unique=True),
    )


class UserFollowModel(Base):
    __tablename__ = 'user_follow'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    from_user_id = Column('from_user_id', INTEGER(display_width=11), nullable=False)
    to_user_id = Column('to_user_id', INTEGER(display_width=11), nullable=False)
    status = Column('status', TINYINT(display_width=1), comment='0 已关注 1 未关注 2 被 to_user_id 拉黑')
    city_id = Column('city_id', INTEGER(display_width=11), comment='被follow用户的城市id')
    update_ts = Column('update_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('to_user_id', Column('to_user_id', INTEGER(display_width=11), nullable=False), Column('status', TINYINT(display_width=1), comment='0 已关注 1 未关注 2 被 to_user_id 拉黑')),
        Index('from_user_id', Column('from_user_id', INTEGER(display_width=11), nullable=False), Column('to_user_id', INTEGER(display_width=11), nullable=False), unique=True),
        Index('city_id', Column('city_id', INTEGER(display_width=11), comment='被follow用户的城市id')),
    )


class UserGuardianModel(Base):
    __tablename__ = 'user_guardian'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), nullable=False)
    id_card_no = Column('id_card_no', VARCHAR(length=18), nullable=False)
    realname = Column('realname', VARCHAR(length=16), nullable=False)
    mobile = Column('mobile', VARCHAR(length=11))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('user_guardian_id_card_no_UNIQUE', Column('id_card_no', VARCHAR(length=18), nullable=False)),
    )


class UserIdentityModel(Base):
    __tablename__ = 'user_identity'
    user_id = Column('user_id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    id_card_no = Column('id_card_no', VARCHAR(length=18), nullable=False)
    name = Column('name', VARCHAR(length=16), nullable=False)
    liveness_id = Column('liveness_id', VARCHAR(length=36))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    id_card_image_oss = Column('id_card_image_oss', VARCHAR(length=255))
    liveness_image_oss = Column('liveness_image_oss', VARCHAR(length=255))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))


class UserInfoModel(Base):
    __tablename__ = 'user_info'
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    realname = Column('realname', VARCHAR(length=32))
    nickname = Column('nickname', VARCHAR(length=32))
    mobile = Column('mobile', VARCHAR(length=11))
    child_relation = Column('child_relation', TINYINT(display_width=4))
    degree = Column('degree', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))
    id_card_no = Column('id_card_no', VARCHAR(length=18))
    country = Column('country', SMALLINT(display_width=6), server_default=DefaultClause(TextClause('1')))
    status = Column('status', TINYINT(display_width=4), server_default=DefaultClause(TextClause('0')))
    update_ts = Column('update_ts', INTEGER(display_width=10))
    avatar_oss = Column('avatar_oss', VARCHAR(length=255))
    born = Column('born', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')))


class UserKolModel(Base):
    __tablename__ = 'user_kol'
    user_id = Column('user_id', INTEGER(display_width=11), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), nullable=False)


class UserLikeModel(Base):
    __tablename__ = 'user_like'
    id = Column('id', INTEGER(display_width=10, unsigned=True), primary_key=True, nullable=False)
    from_user_id = Column('from_user_id', INTEGER(display_width=11), nullable=False)
    to_user_id = Column('to_user_id', INTEGER(display_width=11), nullable=False)
    status = Column('status', TINYINT(display_width=1))
    city_id = Column('city_id', INTEGER(display_width=11), comment='被like用户的城市id')
    update_ts = Column('update_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('city_id', Column('city_id', INTEGER(display_width=11), comment='被like用户的城市id')),
        Index('from_user_id', Column('from_user_id', INTEGER(display_width=11), nullable=False), Column('to_user_id', INTEGER(display_width=11), nullable=False), unique=True),
    )


class UserTrustModel(Base):
    __tablename__ = 'user_trust'
    user_id = Column('user_id', INTEGER(display_width=11), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False)
    score = Column('score', INTEGER(display_width=11), nullable=False, comment='100 百分 无小数点 复杂算法，其中之一数据源来自 【摩尔时光】')
    update_ts = Column('update_ts', INTEGER(display_width=10), nullable=False)


class VerifyHistoryModel(Base):
    __tablename__ = 'verify_history'
    verify_id = Column('verify_id', INTEGER(display_width=11), primary_key=True, nullable=False)
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='状态 (预留字段)')
    verify_ts = Column('verify_ts', INTEGER(display_width=10))
    result = Column('result', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')), comment='不通过原因 | 0 审核通过 | 1 视频涉黄 | 2 视频涉政 | 3 视频涉暴恐 | 4 经验认证未通过 | 5 介绍视频没有看护人 | 6 介绍内容不符合要求 | 7 场地不符合要求 ')
    remark = Column('remark', VARCHAR(length=200), comment='备注 | 最多两百字以内')
    assessor = Column('assessor', INTEGER(display_width=11), comment='审核员ID')
    user_id = Column('user_id', INTEGER(display_width=11, unsigned=True), nullable=False, comment='| 来自carer_application')
    intro_video_id = Column('intro_video_id', INTEGER(display_width=11, unsigned=True), nullable=False, comment='| 来自carer_application')
    playground_video_id = Column('playground_video_id', INTEGER(display_width=11, unsigned=True), nullable=False, comment='| 来自carer_application')
    extra_video_ids = Column('extra_video_ids', VARCHAR(length=64), server_default=DefaultClause(TextClause("''")), comment='| 来自carer_application')
    address_id = Column('address_id', INTEGER(display_width=11, unsigned=True), comment='| 来自carer_application')
    birth_certificate_oss = Column('birth_certificate_oss', VARCHAR(length=255), comment='| 来自carer_application')
    care_exp = Column('care_exp', INTEGER(display_width=11), server_default=DefaultClause(TextClause('0')), comment='| 来自carer_application')
    degree = Column('degree', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='| 来自carer_application')
    child_count_max = Column('child_count_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='| 来自carer_application')
    child_age_min = Column('child_age_min', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='| 来自carer_application')
    child_age_max = Column('child_age_max', TINYINT(display_width=1), server_default=DefaultClause(TextClause('0')), comment='| 来自carer_application')
    create_ts = Column('create_ts', INTEGER(display_width=10), comment='| 来自carer_application')
    update_ts = Column('update_ts', INTEGER(display_width=10), comment='| 来自carer_application')


class VideoModel(Base):
    __tablename__ = 'video'
    id = Column('id', INTEGER(display_width=11, unsigned=True), primary_key=True, nullable=False)
    cloud = Column('cloud', VARCHAR(length=16), nullable=False)
    bucket = Column('bucket', VARCHAR(length=64), nullable=False)
    key = Column('key', VARCHAR(length=128), nullable=False)
    etag = Column('etag', VARCHAR(length=32))
    mime_type = Column('mime_type', VARCHAR(length=16))
    size = Column('size', INTEGER(display_width=10, unsigned=True))
    duration = Column('duration', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    width = Column('width', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    height = Column('height', INTEGER(display_width=10, unsigned=True), server_default=DefaultClause(TextClause('0')))
    persistent_id = Column('persistent_id', VARCHAR(length=32))
    pfop_vframe_status = Column('pfop_vframe_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    pfop_transcode_status = Column('pfop_transcode_status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    status = Column('status', TINYINT(display_width=1), nullable=False, server_default=DefaultClause(TextClause('0')))
    create_ts = Column('create_ts', INTEGER(display_width=10), server_default=DefaultClause(TextClause('0')))
    __table_args__ = (
        Index('video_cloud_bucket_key_index_unique', Column('cloud', VARCHAR(length=16), nullable=False), Column('bucket', VARCHAR(length=64), nullable=False), Column('key', VARCHAR(length=128), nullable=False), unique=True),
    )


class WalletModel(Base):
    __tablename__ = 'wallet'
    id = Column('id', INTEGER(display_width=11), primary_key=True, nullable=False)
    customer_id = Column('customer_id', INTEGER(display_width=11))
    balance = Column('balance', INTEGER(display_width=11))
    freezed = Column('freezed', INTEGER(display_width=11))
    cashable = Column('cashable', INTEGER(display_width=11))
    uncashable = Column('uncashable', INTEGER(display_width=11))
    update_ts = Column('update_ts', INTEGER(display_width=10))
    __table_args__ = (
        Index('customer_id_UNIQUE', Column('customer_id', INTEGER(display_width=11)), unique=True),
    )
