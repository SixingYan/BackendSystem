# -*- coding: utf-8 -*-

''' Generated codes

Marshmallow schema classes accord with model definitions in Swagger.
BE VERY CAREFUL to change this file manually.

'''

import marshmallow
from base import validator


''' SCHEMAS FROM MODEL DEFINITIONS.
'''


class AppDownloadRecord(object):
    __slots__ = ['poster_id', 'phone_type', '_original_data']

    def __init__(self, poster_id=None, phone_type=None, original_data=None):
        self.poster_id = poster_id
        self.phone_type = phone_type
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class AppDownloadRecordSchema(marshmallow.Schema):
    poster_id = marshmallow.fields.Integer()  # poster ID
    phone_type = marshmallow.fields.Integer()  # 系统

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = AppDownloadRecord(**data)
        return obj


class MoretimeMedia(object):
    __slots__ = ['key', 'mime_type', 'etag', 'size', 'width', 'height', 'duration', 'cover_url', 'video_url', '_original_data']

    def __init__(self, key=None, mime_type=None, etag=None, size=None, width=None, height=None, duration=None, cover_url=None, video_url=None, original_data=None):
        self.key = key
        self.mime_type = mime_type
        self.etag = etag
        self.size = size
        self.width = width
        self.height = height
        self.duration = duration
        self.cover_url = cover_url
        self.video_url = video_url
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class MoretimeMediaSchema(marshmallow.Schema):
    key = marshmallow.fields.String()  # qiniu oss key example: user_id_123/avatar/2018/03/138/etag.jpg
    mime_type = marshmallow.fields.String()  # 文件类型 mimeType example: video/mp4
    etag = marshmallow.fields.String()  # 使用 qiniu sdk 计算的 etag example: 7DsdkdFSKkdljfksQWET-TUI
    size = marshmallow.fields.Integer()  # 文件大小 example: 536123
    width = marshmallow.fields.Integer()  # 分辨率 宽 example: 1080
    height = marshmallow.fields.Integer()  # 分辨率 高 example: 1920
    duration = marshmallow.fields.Decimal()  # 播放时长 example: 10.0
    cover_url = marshmallow.fields.String()  # qiniu oss key example: moretime.cn/user_id_123/avatar/2018/03/138/etag.jpg
    video_url = marshmallow.fields.String()  # qiniu oss key example: moretime.cn/user_id_123/avatar/2018/03/138/etag.mp4

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = MoretimeMedia(**data)
        return obj


class ObjectInfo(object):
    __slots__ = ['key', 'mime_type', 'etag', 'size', 'persistent_id', 'width', 'height', 'duration', '_original_data']

    def __init__(self, key, mime_type=None, etag=None, size=None, persistent_id=None, width=None, height=None, duration=None, original_data=None):
        self.key = key
        self.mime_type = mime_type
        self.etag = etag
        self.size = size
        self.persistent_id = persistent_id
        self.width = width
        self.height = height
        self.duration = duration
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ObjectInfoSchema(marshmallow.Schema):
    key = marshmallow.fields.String(required=True)  # qiniu oss key example: user_id_123/avatar/2018/03/138/etag.jpg
    mime_type = marshmallow.fields.String()  # 文件类型 mimeType example: image/jpeg
    etag = marshmallow.fields.String()  # 使用 qiniu sdk 计算的 etag example: 7DsdkdFSKkdljfksQWET-TUI
    size = marshmallow.fields.Integer()  # 文件大小 example: 536123
    persistent_id = marshmallow.fields.String()  # 七牛持久化操作 ID 用于查询视频转码和截图等异步操作的结果 example: z1.5ade998d856db843bc8fe6f2
    width = marshmallow.fields.Integer()  # 分辨率 宽 example: 1080
    height = marshmallow.fields.Integer()  # 分辨率 高 example: 1920
    duration = marshmallow.fields.Decimal()  # 播放时长 example: 10.0

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ObjectInfo(**data)
        return obj


class OrderGet(object):
    __slots__ = ['order_no', '_original_data']

    def __init__(self, order_no=None, original_data=None):
        self.order_no = order_no
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class OrderGetSchema(marshmallow.Schema):
    order_no = marshmallow.fields.Integer()  # 订单号 example: 123456789

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = OrderGet(**data)
        return obj


class PageRequest(object):
    __slots__ = ['offset', 'limit', '_original_data']

    def __init__(self, offset=None, limit=None, original_data=None):
        self.offset = offset
        self.limit = limit
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PageRequestSchema(marshmallow.Schema):
    offset = marshmallow.fields.Integer(missing=-1)  # 从第几行起
    limit = marshmallow.fields.Integer(missing=-1)  # 行数量

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PageRequest(**data)
        return obj


class PosterCreate(object):
    __slots__ = ['poster_id', '_original_data']

    def __init__(self, poster_id=None, original_data=None):
        self.poster_id = poster_id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterCreateSchema(marshmallow.Schema):
    poster_id = marshmallow.fields.Integer()  # 创建的摩尔时光ID example: 123456789

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterCreate(**data)
        return obj


class PosterDelete(object):
    __slots__ = ['poster_id', '_original_data']

    def __init__(self, poster_id, original_data=None):
        self.poster_id = poster_id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterDeleteSchema(marshmallow.Schema):
    poster_id = marshmallow.fields.Integer(required=True)  # 摩尔时光的ID example: 123456789

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterDelete(**data)
        return obj


class PosterGet(object):
    __slots__ = ['poster_id', 'offset', 'limit', '_original_data']

    def __init__(self, poster_id, offset=None, limit=None, original_data=None):
        self.poster_id = poster_id
        self.offset = offset
        self.limit = limit
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterGetSchema(marshmallow.Schema):
    poster_id = marshmallow.fields.Integer(required=True)  # 摩尔时光的ID example: 123456789
    offset = marshmallow.fields.Integer()  # 从第几行起
    limit = marshmallow.fields.Integer()  # 行数量

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterGet(**data)
        return obj


class PosterShare(object):
    __slots__ = ['title', 'description', 'webpage_url', 'thumb_image_url', '_original_data']

    def __init__(self, title=None, description=None, webpage_url=None, thumb_image_url=None, original_data=None):
        self.title = title
        self.description = description
        self.webpage_url = webpage_url
        self.thumb_image_url = thumb_image_url
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterShareSchema(marshmallow.Schema):
    title = marshmallow.fields.String()  # 标题
    description = marshmallow.fields.String()  # 描述
    webpage_url = marshmallow.fields.String()  # 分享页链接
    thumb_image_url = marshmallow.fields.String()  # 缩略图url

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterShare(**data)
        return obj


class PosterVisible(object):
    __slots__ = ['poster_id', 'is_content', 'set_visible', '_original_data']

    def __init__(self, poster_id, is_content, set_visible, original_data=None):
        self.poster_id = poster_id
        self.is_content = is_content
        self.set_visible = set_visible
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterVisibleSchema(marshmallow.Schema):
    poster_id = marshmallow.fields.Integer(required=True)  # 摩尔时光的ID example: 123456789
    is_content = marshmallow.fields.Boolean(required=True)  # 是否是更新文字
    set_visible = marshmallow.fields.Boolean(required=True)  # 可见性

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterVisible(**data)
        return obj


class RatePost(object):
    __slots__ = ['order_no', 'rate', '_original_data']

    def __init__(self, order_no=None, rate=None, original_data=None):
        self.order_no = order_no
        self.rate = rate
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class RatePostSchema(marshmallow.Schema):
    order_no = marshmallow.fields.Integer()  # 订单号
    rate = marshmallow.fields.Integer()  # 打分

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = RatePost(**data)
        return obj


class ReplyCreate(object):
    __slots__ = ['reply_id', 'to_user_id', '_original_data']

    def __init__(self, reply_id=None, to_user_id=None, original_data=None):
        self.reply_id = reply_id
        self.to_user_id = to_user_id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyCreateSchema(marshmallow.Schema):
    reply_id = marshmallow.fields.Integer()  # 回复ID example: 1234567890
    to_user_id = marshmallow.fields.Integer()  # 回复目标的ID example: 1234567890

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyCreate(**data)
        return obj


class ReplyDelete(object):
    __slots__ = ['reply_id', '_original_data']

    def __init__(self, reply_id=None, original_data=None):
        self.reply_id = reply_id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyDeleteSchema(marshmallow.Schema):
    reply_id = marshmallow.fields.Integer()  # 评论ID example: 1234567890

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyDelete(**data)
        return obj


class ReplyGet(object):
    __slots__ = ['reply_id', '_original_data']

    def __init__(self, reply_id, original_data=None):
        self.reply_id = reply_id
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyGetSchema(marshmallow.Schema):
    reply_id = marshmallow.fields.Integer(required=True)  # 评论ID example: 1234567890

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyGet(**data)
        return obj


class ReplyToRead(object):
    __slots__ = ['reply_id', 'content', '_original_data']

    def __init__(self, reply_id=None, content=None, original_data=None):
        self.reply_id = reply_id
        self.content = content
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyToReadSchema(marshmallow.Schema):
    reply_id = marshmallow.fields.Integer()  # 评论ID example: 1234567890
    content = marshmallow.fields.String()  # 评论内容 example: 这是坠吼的

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyToRead(**data)
        return obj


class ReplyToUserCount(object):
    __slots__ = ['count', '_original_data']

    def __init__(self, count=None, original_data=None):
        self.count = count
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyToUserCountSchema(marshmallow.Schema):
    count = marshmallow.fields.Integer()  # 计数 example: 12

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyToUserCount(**data)
        return obj


class ReplyToUserGet(object):
    __slots__ = ['user_id', 'offset', 'limit', '_original_data']

    def __init__(self, user_id=None, offset=None, limit=None, original_data=None):
        self.user_id = user_id
        self.offset = offset
        self.limit = limit
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyToUserGetSchema(marshmallow.Schema):
    user_id = marshmallow.fields.Integer()  # 要求查看的个人主页 example: 1234567890
    offset = marshmallow.fields.Integer()  # 从第几行起
    limit = marshmallow.fields.Integer()  # 行数量

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyToUserGet(**data)
        return obj


class Status(object):
    __slots__ = ['code', 'msg', '_original_data']

    def __init__(self, code, msg, original_data=None):
        self.code = code
        self.msg = msg
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class StatusSchema(marshmallow.Schema):
    code = marshmallow.fields.Integer(required=True)  # 错误码，成功为 0
    msg = marshmallow.fields.String(required=True)  # 错误信息

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = Status(**data)
        return obj


class User(object):
    __slots__ = ['user_id', 'avatar_url', 'nickname', '_original_data']

    def __init__(self, user_id=None, avatar_url=None, nickname=None, original_data=None):
        self.user_id = user_id
        self.avatar_url = avatar_url
        self.nickname = nickname
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class UserSchema(marshmallow.Schema):
    user_id = marshmallow.fields.Integer()  # 用户 ID example: 123
    avatar_url = marshmallow.fields.URL(relative=True)  # 个人头像图片 URL example: qiniu.com/image/2018/03/11/avatar.jpg
    nickname = marshmallow.fields.String()  # 用户昵称 example: 煎饼侠的姥爷

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = User(**data)
        return obj


class Poster(object):
    __slots__ = ['start_ts', 'user', 'poster_id', 'media_obj_list', 'order_no', 'content', 'from_user_id', 'to_user_id', 'child_nickname', 'is_media_public', 'create_ts', 'rate', '_original_data']

    def __init__(self, start_ts=None, user=None, poster_id=None, media_obj_list=None, order_no=None, content=None, from_user_id=None, to_user_id=None, child_nickname=None, is_media_public=None, create_ts=None, rate=None, original_data=None):
        self.start_ts = start_ts
        self.user = user
        self.poster_id = poster_id
        self.media_obj_list = media_obj_list
        self.order_no = order_no
        self.content = content
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.child_nickname = child_nickname
        self.is_media_public = is_media_public
        self.create_ts = create_ts
        self.rate = rate
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterSchema(marshmallow.Schema):
    start_ts = marshmallow.fields.Integer()  # 共享时间-开始时间 example: 1234567890
    user = marshmallow.fields.Nested(UserSchema())
    poster_id = marshmallow.fields.Integer()  # 摩尔时光ID example: 1234567890
    media_obj_list = marshmallow.fields.List(marshmallow.fields.Nested(MoretimeMediaSchema()))
    order_no = marshmallow.fields.Integer()  # 订单编号
    content = marshmallow.fields.String()  # 文字内容 example: 我说你另请高明吧
    from_user_id = marshmallow.fields.Integer()  # 发布poster的人 example: 1234567890
    to_user_id = marshmallow.fields.Integer()  # 接受该poster的人 example: 1234567890
    child_nickname = marshmallow.fields.String()  # 孩子昵称，用于显示标题/评分 example: 香港记者
    is_media_public = marshmallow.fields.Integer()  # 是否公开可见
    create_ts = marshmallow.fields.Integer()  # poster 创建时间 example: 1234567890
    rate = marshmallow.fields.Integer(missing=-1)  # 评分，-1为未评分状态 example: -1

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = Poster(**data)
        return obj


class PosterPost_PicturesInfoPrivate(object):
    __slots__ = ['order_index', 'media', '_original_data']

    def __init__(self, order_index=None, media=None, original_data=None):
        self.order_index = order_index
        self.media = media
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterPost_PicturesInfoPrivateSchema(marshmallow.Schema):
    order_index = marshmallow.fields.Integer()  # 媒体排序序号
    media = marshmallow.fields.Nested(ObjectInfoSchema())

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterPost_PicturesInfoPrivate(**data)
        return obj


class PosterPost_VideosInfoPrivate(object):
    __slots__ = ['order_index', 'media', '_original_data']

    def __init__(self, order_index=None, media=None, original_data=None):
        self.order_index = order_index
        self.media = media
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterPost_VideosInfoPrivateSchema(marshmallow.Schema):
    order_index = marshmallow.fields.Integer()  # 媒体排序序号, 从0开始
    media = marshmallow.fields.Nested(ObjectInfoSchema())

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterPost_VideosInfoPrivate(**data)
        return obj


class Reply(object):
    __slots__ = ['reply_id', 'user', 'from_user_id', 'to_user_id', 'content', 'media_obj_list', 'create_ts', '_original_data']

    def __init__(self, reply_id=None, user=None, from_user_id=None, to_user_id=None, content=None, media_obj_list=None, create_ts=None, original_data=None):
        self.reply_id = reply_id
        self.user = user
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.content = content
        self.media_obj_list = media_obj_list
        self.create_ts = create_ts
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplySchema(marshmallow.Schema):
    reply_id = marshmallow.fields.Integer()  # 回复id example: 123456789
    user = marshmallow.fields.Nested(UserSchema())
    from_user_id = marshmallow.fields.Integer()  # 发送评论的人 example: 123456789
    to_user_id = marshmallow.fields.Integer()  # 接收评论的人 example: 123456789
    content = marshmallow.fields.String()  # 评论内容 example: 只是做了一点微小的工作，谢谢大家
    media_obj_list = marshmallow.fields.List(marshmallow.fields.Nested(MoretimeMediaSchema()))
    create_ts = marshmallow.fields.Integer()  # 创建时间 example: 1234567890

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = Reply(**data)
        return obj


class ReplyPost_PicturesInfoPrivate(object):
    __slots__ = ['order_index', 'media', '_original_data']

    def __init__(self, order_index=None, media=None, original_data=None):
        self.order_index = order_index
        self.media = media
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyPost_PicturesInfoPrivateSchema(marshmallow.Schema):
    order_index = marshmallow.fields.Integer()  # 媒体排序序号
    media = marshmallow.fields.Nested(ObjectInfoSchema())

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyPost_PicturesInfoPrivate(**data)
        return obj


class ReplyPost_VideosInfoPrivate(object):
    __slots__ = ['order_index', 'media', '_original_data']

    def __init__(self, order_index=None, media=None, original_data=None):
        self.order_index = order_index
        self.media = media
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyPost_VideosInfoPrivateSchema(marshmallow.Schema):
    order_index = marshmallow.fields.Integer()  # 媒体排序序号, 从0开始
    media = marshmallow.fields.Nested(ObjectInfoSchema())

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyPost_VideosInfoPrivate(**data)
        return obj


class PosterPost(object):
    __slots__ = ['order_no', 'content', 'videos_info_private', 'pictures_info_private', '_original_data']

    def __init__(self, order_no, content, videos_info_private=None, pictures_info_private=None, original_data=None):
        self.order_no = order_no
        self.content = content
        self.videos_info_private = videos_info_private
        self.pictures_info_private = pictures_info_private
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterPostSchema(marshmallow.Schema):
    order_no = marshmallow.fields.Integer(required=True)  # 订单号 example: 123456789
    content = marshmallow.fields.String(required=True)  # 文字内容 example: 你说我一个上海市委书记怎么就到了北京
    videos_info_private = marshmallow.fields.List(marshmallow.fields.Nested(PosterPost_VideosInfoPrivateSchema()))  # 视频私有存储信息列表
    pictures_info_private = marshmallow.fields.List(marshmallow.fields.Nested(PosterPost_PicturesInfoPrivateSchema()))  # 图片私有存储信息列表

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterPost(**data)
        return obj


class PosterReply(object):
    __slots__ = ['poster_id', 'reply', 'follow_reply_list', '_original_data']

    def __init__(self, poster_id=None, reply=None, follow_reply_list=None, original_data=None):
        self.poster_id = poster_id
        self.reply = reply
        self.follow_reply_list = follow_reply_list
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterReplySchema(marshmallow.Schema):
    poster_id = marshmallow.fields.Integer()  # 隶属的poster example: 123456789
    reply = marshmallow.fields.Nested(ReplySchema())
    follow_reply_list = marshmallow.fields.List(marshmallow.fields.Nested(ReplySchema()))  # 跟随的评论的评论

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterReply(**data)
        return obj


class PosterReplyRate(object):
    __slots__ = ['rate', 'poster_id', 'reply', 'follow_reply_list', '_original_data']

    def __init__(self, rate=None, poster_id=None, reply=None, follow_reply_list=None, original_data=None):
        self.rate = rate
        self.poster_id = poster_id
        self.reply = reply
        self.follow_reply_list = follow_reply_list
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterReplyRateSchema(marshmallow.Schema):
    rate = marshmallow.fields.Integer(missing=-1)  # 第一条家长的评论会附带评分，评分不为-1
    poster_id = marshmallow.fields.Integer()  # 隶属的poster example: 123456789
    reply = marshmallow.fields.Nested(ReplySchema())
    follow_reply_list = marshmallow.fields.List(marshmallow.fields.Nested(ReplySchema()))  # 跟随的评论的评论

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterReplyRate(**data)
        return obj


class ReplyPost(object):
    __slots__ = ['poster_id', 'prior_id', 'content', 'videos_info_private', 'pictures_info_private', 'set_visible', '_original_data']

    def __init__(self, poster_id, content, prior_id=None, videos_info_private=None, pictures_info_private=None, set_visible=None, original_data=None):
        self.poster_id = poster_id
        self.prior_id = prior_id
        self.content = content
        self.videos_info_private = videos_info_private
        self.pictures_info_private = pictures_info_private
        self.set_visible = set_visible
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class ReplyPostSchema(marshmallow.Schema):
    poster_id = marshmallow.fields.Integer(required=True)  # 摩尔时光ID example: 1234567890
    prior_id = marshmallow.fields.Integer(missing=-1)  # 前置评论的ID
    content = marshmallow.fields.String(required=True)  # 评论内容 example: 这是坠吼的
    videos_info_private = marshmallow.fields.List(marshmallow.fields.Nested(ReplyPost_VideosInfoPrivateSchema()))  # 视频私有存储信息列表
    pictures_info_private = marshmallow.fields.List(marshmallow.fields.Nested(ReplyPost_PicturesInfoPrivateSchema()))  # 图片私有存储信息列表
    set_visible = marshmallow.fields.Boolean()  # 买家同时设置可见状态

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = ReplyPost(**data)
        return obj


class PosterAndReply(object):
    __slots__ = ['poster', 'reply_list', '_original_data']

    def __init__(self, poster=None, reply_list=None, original_data=None):
        self.poster = poster
        self.reply_list = reply_list
        self._original_data = original_data

    @property
    def dict(self):
        return self._original_data


class PosterAndReplySchema(marshmallow.Schema):
    poster = marshmallow.fields.Nested(PosterSchema())
    reply_list = marshmallow.fields.List(marshmallow.fields.Nested(PosterReplySchema()))

    @marshmallow.post_load(pass_original=True)
    def make_object(self, data, original_data):
        data['original_data'] = original_data
        obj = PosterAndReply(**data)
        return obj
