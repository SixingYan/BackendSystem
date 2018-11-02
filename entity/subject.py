#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal


class CarerApplication(object):
    def __init__(self, user_id, intro_video_id, playground_video_id, extra_video_ids, address_id, birth_certificate_oss, care_exp, degree, child_count_max, child_age_min, child_age_max):
        self.user_id = user_id
        self.intro_video_id = intro_video_id
        self.playground_video_id = playground_video_id
        self.extra_video_ids = extra_video_ids
        self.address_id = address_id
        self.birth_certificate_oss = birth_certificate_oss
        self.care_exp = care_exp
        self.degree = degree
        self.child_count_max = child_count_max
        self.child_age_min = child_age_min
        self.child_age_max = child_age_max

    @classmethod
    def default(cls):
        instance = CarerApplication(
            user_id=int(),
            intro_video_id=int(),
            playground_video_id=int(),
            extra_video_ids=str(),
            address_id=int(),
            birth_certificate_oss=str(),
            care_exp=int(),
            degree=int(),
            child_count_max=int(),
            child_age_min=int(),
            child_age_max=int(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = CarerApplication(
            user_id=d['user_id'],
            intro_video_id=d['intro_video_id'],
            playground_video_id=d['playground_video_id'],
            extra_video_ids=d['extra_video_ids'],
            address_id=d['address_id'],
            birth_certificate_oss=d['birth_certificate_oss'],
            care_exp=d['care_exp'],
            degree=d['degree'],
            child_count_max=d['child_count_max'],
            child_age_min=d['child_age_min'],
            child_age_max=d['child_age_max'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = CarerApplication(
            user_id=getattr(o, 'user_id'),
            intro_video_id=getattr(o, 'intro_video_id'),
            playground_video_id=getattr(o, 'playground_video_id'),
            extra_video_ids=getattr(o, 'extra_video_ids'),
            address_id=getattr(o, 'address_id'),
            birth_certificate_oss=getattr(o, 'birth_certificate_oss'),
            care_exp=getattr(o, 'care_exp'),
            degree=getattr(o, 'degree'),
            child_count_max=getattr(o, 'child_count_max'),
            child_age_min=getattr(o, 'child_age_min'),
            child_age_max=getattr(o, 'child_age_max'),
        )
        return instance


class Child(object):
    def __init__(self, id, id_card_no, realname, nickname, birth_ts, gender):
        self.id = id
        self.id_card_no = id_card_no
        self.realname = realname
        self.nickname = nickname
        self.birth_ts = birth_ts
        self.gender = gender

    @classmethod
    def default(cls):
        instance = Child(
            id=int(),
            id_card_no=str(),
            realname=str(),
            nickname=str(),
            birth_ts=int(),
            gender=int(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = Child(
            id=d['id'],
            id_card_no=d['id_card_no'],
            realname=d['realname'],
            nickname=d['nickname'],
            birth_ts=d['birth_ts'],
            gender=d['gender'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = Child(
            id=getattr(o, 'id'),
            id_card_no=getattr(o, 'id_card_no'),
            realname=getattr(o, 'realname'),
            nickname=getattr(o, 'nickname'),
            birth_ts=getattr(o, 'birth_ts'),
            gender=getattr(o, 'gender'),
        )
        return instance


class Oid(object):
    def __init__(self, id, uuid):
        self.id = id
        self.uuid = uuid

    @classmethod
    def default(cls):
        instance = Oid(
            id=int(),
            uuid=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = Oid(
            id=d['id'],
            uuid=d['uuid'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = Oid(
            id=getattr(o, 'id'),
            uuid=getattr(o, 'uuid'),
        )
        return instance


class Oss(object):
    def __init__(self, id, cloud, bucket, key, etag, mime_type, size, created_time):
        self.id = id
        self.cloud = cloud
        self.bucket = bucket
        self.key = key
        self.etag = etag
        self.mime_type = mime_type
        self.size = size
        self.created_time = created_time

    @classmethod
    def default(cls):
        instance = Oss(
            id=int(),
            cloud=str(),
            bucket=str(),
            key=str(),
            etag=str(),
            mime_type=str(),
            size=int(),
            created_time=datetime(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = Oss(
            id=d['id'],
            cloud=d['cloud'],
            bucket=d['bucket'],
            key=d['key'],
            etag=d['etag'],
            mime_type=d['mime_type'],
            size=d['size'],
            created_time=d['created_time'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = Oss(
            id=getattr(o, 'id'),
            cloud=getattr(o, 'cloud'),
            bucket=getattr(o, 'bucket'),
            key=getattr(o, 'key'),
            etag=getattr(o, 'etag'),
            mime_type=getattr(o, 'mime_type'),
            size=getattr(o, 'size'),
            created_time=getattr(o, 'created_time'),
        )
        return instance


class OssRef(object):
    def __init__(self, id, user_id, object_id, tag, created_time):
        self.id = id
        self.user_id = user_id
        self.object_id = object_id
        self.tag = tag
        self.created_time = created_time

    @classmethod
    def default(cls):
        instance = OssRef(
            id=int(),
            user_id=int(),
            object_id=int(),
            tag=str(),
            created_time=datetime(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = OssRef(
            id=d['id'],
            user_id=d['user_id'],
            object_id=d['object_id'],
            tag=d['tag'],
            created_time=d['created_time'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = OssRef(
            id=getattr(o, 'id'),
            user_id=getattr(o, 'user_id'),
            object_id=getattr(o, 'object_id'),
            tag=getattr(o, 'tag'),
            created_time=getattr(o, 'created_time'),
        )
        return instance


class Playground(object):
    def __init__(self, id, user_id, address_id, type, capacity, space, equip):
        self.id = id
        self.user_id = user_id
        self.address_id = address_id
        self.type = type
        self.capacity = capacity
        self.space = space
        self.equip = equip

    @classmethod
    def default(cls):
        instance = Playground(
            id=int(),
            user_id=int(),
            address_id=int(),
            type=int(),
            capacity=int(),
            space=int(),
            equip=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = Playground(
            id=d['id'],
            user_id=d['user_id'],
            address_id=d['address_id'],
            type=d['type'],
            capacity=d['capacity'],
            space=d['space'],
            equip=d['equip'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = Playground(
            id=getattr(o, 'id'),
            user_id=getattr(o, 'user_id'),
            address_id=getattr(o, 'address_id'),
            type=getattr(o, 'type'),
            capacity=getattr(o, 'capacity'),
            space=getattr(o, 'space'),
            equip=getattr(o, 'equip'),
        )
        return instance


class TimeSharing(object):
    def __init__(self, id, user_id, child_age_min, child_age_max, child_count_max, address_id, start_ts, end_ts, price, activity, description, accompany_required, child_count):
        self.id = id
        self.user_id = user_id
        self.child_age_min = child_age_min
        self.child_age_max = child_age_max
        self.child_count_max = child_count_max
        self.address_id = address_id
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.price = price
        self.activity = activity
        self.description = description
        self.accompany_required = accompany_required
        self.child_count = child_count

    @classmethod
    def default(cls):
        instance = TimeSharing(
            id=int(),
            user_id=int(),
            child_age_min=int(),
            child_age_max=int(),
            child_count_max=int(),
            address_id=int(),
            start_ts=int(),
            end_ts=int(),
            price=int(),
            activity=str(),
            description=str(),
            accompany_required=int(),
            child_count=int(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = TimeSharing(
            id=d['id'],
            user_id=d['user_id'],
            child_age_min=d['child_age_min'],
            child_age_max=d['child_age_max'],
            child_count_max=d['child_count_max'],
            address_id=d['address_id'],
            start_ts=d['start_ts'],
            end_ts=d['end_ts'],
            price=d['price'],
            activity=d['activity'],
            description=d['description'],
            accompany_required=d['accompany_required'],
            child_count=d['child_count'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = TimeSharing(
            id=getattr(o, 'id'),
            user_id=getattr(o, 'user_id'),
            child_age_min=getattr(o, 'child_age_min'),
            child_age_max=getattr(o, 'child_age_max'),
            child_count_max=getattr(o, 'child_count_max'),
            address_id=getattr(o, 'address_id'),
            start_ts=getattr(o, 'start_ts'),
            end_ts=getattr(o, 'end_ts'),
            price=getattr(o, 'price'),
            activity=getattr(o, 'activity'),
            description=getattr(o, 'description'),
            accompany_required=getattr(o, 'accompany_required'),
            child_count=getattr(o, 'child_count'),
        )
        return instance


class Uid(object):
    def __init__(self, id, uuid):
        self.id = id
        self.uuid = uuid

    @classmethod
    def default(cls):
        instance = Uid(
            id=int(),
            uuid=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = Uid(
            id=d['id'],
            uuid=d['uuid'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = Uid(
            id=getattr(o, 'id'),
            uuid=getattr(o, 'uuid'),
        )
        return instance


class User(object):
    def __init__(self, id, uid, uuid, code, mobile, password):
        self.id = id
        self.uid = uid
        self.uuid = uuid
        self.code = code
        self.mobile = mobile
        self.password = password

    @classmethod
    def default(cls):
        instance = User(
            id=int(),
            uid=str(),
            uuid=str(),
            code=str(),
            mobile=str(),
            password=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = User(
            id=d['id'],
            uid=d['uid'],
            uuid=d['uuid'],
            code=d['code'],
            mobile=d['mobile'],
            password=d['password'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = User(
            id=getattr(o, 'id'),
            uid=getattr(o, 'uid'),
            uuid=getattr(o, 'uuid'),
            code=getattr(o, 'code'),
            mobile=getattr(o, 'mobile'),
            password=getattr(o, 'password'),
        )
        return instance


class UserAddress(object):
    def __init__(self, id, user_id, lat, lng, province, city, district, address, name, room, poi_id):
        self.id = id
        self.user_id = user_id
        self.lat = lat
        self.lng = lng
        self.province = province
        self.city = city
        self.district = district
        self.address = address
        self.name = name
        self.room = room
        self.poi_id = poi_id

    @classmethod
    def default(cls):
        instance = UserAddress(
            id=int(),
            user_id=int(),
            lat=Decimal(),
            lng=Decimal(),
            province=str(),
            city=str(),
            district=str(),
            address=str(),
            name=str(),
            room=str(),
            poi_id=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = UserAddress(
            id=d['id'],
            user_id=d['user_id'],
            lat=d['lat'],
            lng=d['lng'],
            province=d['province'],
            city=d['city'],
            district=d['district'],
            address=d['address'],
            name=d['name'],
            room=d['room'],
            poi_id=d['poi_id'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = UserAddress(
            id=getattr(o, 'id'),
            user_id=getattr(o, 'user_id'),
            lat=getattr(o, 'lat'),
            lng=getattr(o, 'lng'),
            province=getattr(o, 'province'),
            city=getattr(o, 'city'),
            district=getattr(o, 'district'),
            address=getattr(o, 'address'),
            name=getattr(o, 'name'),
            room=getattr(o, 'room'),
            poi_id=getattr(o, 'poi_id'),
        )
        return instance


class UserCarerInfo(object):
    def __init__(self, user_id, intro_video_id, playground_video_id, extra_video_ids, address_id, birth_certificate_oss, degree, care_exp, child_count_max, child_age_min, child_age_max):
        self.user_id = user_id
        self.intro_video_id = intro_video_id
        self.playground_video_id = playground_video_id
        self.extra_video_ids = extra_video_ids
        self.address_id = address_id
        self.birth_certificate_oss = birth_certificate_oss
        self.degree = degree
        self.care_exp = care_exp
        self.child_count_max = child_count_max
        self.child_age_min = child_age_min
        self.child_age_max = child_age_max

    @classmethod
    def default(cls):
        instance = UserCarerInfo(
            user_id=int(),
            intro_video_id=int(),
            playground_video_id=int(),
            extra_video_ids=str(),
            address_id=int(),
            birth_certificate_oss=str(),
            degree=int(),
            care_exp=int(),
            child_count_max=int(),
            child_age_min=int(),
            child_age_max=int(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = UserCarerInfo(
            user_id=d['user_id'],
            intro_video_id=d['intro_video_id'],
            playground_video_id=d['playground_video_id'],
            extra_video_ids=d['extra_video_ids'],
            address_id=d['address_id'],
            birth_certificate_oss=d['birth_certificate_oss'],
            degree=d['degree'],
            care_exp=d['care_exp'],
            child_count_max=d['child_count_max'],
            child_age_min=d['child_age_min'],
            child_age_max=d['child_age_max'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = UserCarerInfo(
            user_id=getattr(o, 'user_id'),
            intro_video_id=getattr(o, 'intro_video_id'),
            playground_video_id=getattr(o, 'playground_video_id'),
            extra_video_ids=getattr(o, 'extra_video_ids'),
            address_id=getattr(o, 'address_id'),
            birth_certificate_oss=getattr(o, 'birth_certificate_oss'),
            degree=getattr(o, 'degree'),
            care_exp=getattr(o, 'care_exp'),
            child_count_max=getattr(o, 'child_count_max'),
            child_age_min=getattr(o, 'child_age_min'),
            child_age_max=getattr(o, 'child_age_max'),
        )
        return instance


class UserChild(object):
    def __init__(self, user_id, child_id):
        self.user_id = user_id
        self.child_id = child_id

    @classmethod
    def default(cls):
        instance = UserChild(
            user_id=int(),
            child_id=int(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = UserChild(
            user_id=d['user_id'],
            child_id=d['child_id'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = UserChild(
            user_id=getattr(o, 'user_id'),
            child_id=getattr(o, 'child_id'),
        )
        return instance


class UserFollow(object):
    def __init__(self, id, from_user_id, to_user_id):
        self.id = id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id

    @classmethod
    def default(cls):
        instance = UserFollow(
            id=int(),
            from_user_id=int(),
            to_user_id=int(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = UserFollow(
            id=d['id'],
            from_user_id=d['from_user_id'],
            to_user_id=d['to_user_id'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = UserFollow(
            id=getattr(o, 'id'),
            from_user_id=getattr(o, 'from_user_id'),
            to_user_id=getattr(o, 'to_user_id'),
        )
        return instance


class UserGuardian(object):
    def __init__(self, id, user_id, id_card_no, realname, mobile):
        self.id = id
        self.user_id = user_id
        self.id_card_no = id_card_no
        self.realname = realname
        self.mobile = mobile

    @classmethod
    def default(cls):
        instance = UserGuardian(
            id=int(),
            user_id=int(),
            id_card_no=str(),
            realname=str(),
            mobile=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = UserGuardian(
            id=d['id'],
            user_id=d['user_id'],
            id_card_no=d['id_card_no'],
            realname=d['realname'],
            mobile=d['mobile'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = UserGuardian(
            id=getattr(o, 'id'),
            user_id=getattr(o, 'user_id'),
            id_card_no=getattr(o, 'id_card_no'),
            realname=getattr(o, 'realname'),
            mobile=getattr(o, 'mobile'),
        )
        return instance


class UserIdentity(object):
    def __init__(self, user_id, id_card_no, name, liveness_id, id_card_image_oss, liveness_image_oss):
        self.user_id = user_id
        self.id_card_no = id_card_no
        self.name = name
        self.liveness_id = liveness_id
        self.id_card_image_oss = id_card_image_oss
        self.liveness_image_oss = liveness_image_oss

    @classmethod
    def default(cls):
        instance = UserIdentity(
            user_id=int(),
            id_card_no=str(),
            name=str(),
            liveness_id=str(),
            id_card_image_oss=str(),
            liveness_image_oss=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = UserIdentity(
            user_id=d['user_id'],
            id_card_no=d['id_card_no'],
            name=d['name'],
            liveness_id=d['liveness_id'],
            id_card_image_oss=d['id_card_image_oss'],
            liveness_image_oss=d['liveness_image_oss'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = UserIdentity(
            user_id=getattr(o, 'user_id'),
            id_card_no=getattr(o, 'id_card_no'),
            name=getattr(o, 'name'),
            liveness_id=getattr(o, 'liveness_id'),
            id_card_image_oss=getattr(o, 'id_card_image_oss'),
            liveness_image_oss=getattr(o, 'liveness_image_oss'),
        )
        return instance


class UserInfo(object):
    def __init__(self, user_id, realname, nickname, mobile, child_relation, degree, id_card_no, country, avatar_oss):
        self.user_id = user_id
        self.realname = realname
        self.nickname = nickname
        self.mobile = mobile
        self.child_relation = child_relation
        self.degree = degree
        self.id_card_no = id_card_no
        self.country = country
        self.avatar_oss = avatar_oss
        self.is_carer = False
        self.carer_apply_status = -1

    @classmethod
    def default(cls):
        instance = UserInfo(
            user_id=int(),
            realname=str(),
            nickname=str(),
            mobile=str(),
            child_relation=int(),
            degree=int(),
            id_card_no=str(),
            country=int(),
            avatar_oss=str(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = UserInfo(
            user_id=d['user_id'],
            realname=d['realname'],
            nickname=d['nickname'],
            mobile=d['mobile'],
            child_relation=d['child_relation'],
            degree=d['degree'],
            id_card_no=d['id_card_no'],
            country=d['country'],
            avatar_oss=d['avatar_oss'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = UserInfo(
            user_id=getattr(o, 'user_id'),
            realname=getattr(o, 'realname'),
            nickname=getattr(o, 'nickname'),
            mobile=getattr(o, 'mobile'),
            child_relation=getattr(o, 'child_relation'),
            degree=getattr(o, 'degree'),
            id_card_no=getattr(o, 'id_card_no'),
            country=getattr(o, 'country'),
            avatar_oss=getattr(o, 'avatar_oss'),
        )
        return instance


class Video(object):
    def __init__(self, id, cloud, bucket, key, etag, mime_type, size, duration, width, height, persistent_id, pfop_vframe_status, pfop_transcode_status):
        self.id = id
        self.cloud = cloud
        self.bucket = bucket
        self.key = key
        self.etag = etag
        self.mime_type = mime_type
        self.size = size
        self.duration = duration
        self.width = width
        self.height = height
        self.persistent_id = persistent_id
        self.pfop_vframe_status = pfop_vframe_status
        self.pfop_transcode_status = pfop_transcode_status

    @classmethod
    def default(cls):
        instance = Video(
            id=int(),
            cloud=str(),
            bucket=str(),
            key=str(),
            etag=str(),
            mime_type=str(),
            size=int(),
            duration=int(),
            width=int(),
            height=int(),
            persistent_id=str(),
            pfop_vframe_status=int(),
            pfop_transcode_status=int(),
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = Video(
            id=d['id'],
            cloud=d['cloud'],
            bucket=d['bucket'],
            key=d['key'],
            etag=d['etag'],
            mime_type=d['mime_type'],
            size=d['size'],
            duration=d['duration'],
            width=d['width'],
            height=d['height'],
            persistent_id=d['persistent_id'],
            pfop_vframe_status=d['pfop_vframe_status'],
            pfop_transcode_status=d['pfop_transcode_status'],
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = Video(
            id=getattr(o, 'id'),
            cloud=getattr(o, 'cloud'),
            bucket=getattr(o, 'bucket'),
            key=getattr(o, 'key'),
            etag=getattr(o, 'etag'),
            mime_type=getattr(o, 'mime_type'),
            size=getattr(o, 'size'),
            duration=getattr(o, 'duration'),
            width=getattr(o, 'width'),
            height=getattr(o, 'height'),
            persistent_id=getattr(o, 'persistent_id'),
            pfop_vframe_status=getattr(o, 'pfop_vframe_status'),
            pfop_transcode_status=getattr(o, 'pfop_transcode_status'),
        )
        return instance
