'''
注意：visible_usecase都是 第三者本位的，所有的查询逻辑都是 公众可见？是公众吗？
where_to_delete 和 which_to_delete 尚未定义
设计逻辑：visible针对的是第三者意外访问的情况，
        所有显示的敏感内容首选都是使用公开文件地址，
        当公开文件地址被清除后，可以较好地避免还能取到数据的情况
userID从session中取
'''
from flask import request
from typing import List

from moretime.api.wapp import logworker
from moretime.task import qiniu_multi
from moretime.util import DictObject
from moretime.wrong import exception
from moretime.config.const import VisibleBucket, VisibleLevel, PublicVisible
from moretime.usecase import common as common_usecase


def check_visible(
        info: DictObject,
        role: bool=False,
        content: bool=False,
        picvid: bool=False)->bool:
    result = False

    if role and content:  # 检查当前用户是否可见当前内容
        if obtain_role_visible(info) == obtain_content_visible(info):
            # (公众True=公开True) (非公众False=非公开False)
            result = True

    if role:
        if obtain_role_visible(info):
            result = True

    return result


def obtain_visible_choose(info: DictObject)->int:
    """ 1==给私有  2==给公开  3==不给 """
    result = VisibleLevel.Others.value  # 不给你看视频/图片哦
    role = obtain_role_visible(info)

    if role is True:  # 他是第三者 True (是公众)
        content = obtain_content_visible(info)

        if content is False:  # 文字内容竟然都不可见，你这是一个错误的访问！
            raise exception.MoretimeAuthorityException

        else:  # 文字是可见的
            picvid = obtain_picvid_visible(info)

            if picvid is False:  # 不给你看视频/图片哦
                result = VisibleLevel.Others.value

            else:  # 只给你看公开的视频/图片呢
                result = VisibleLevel.Public.value

    else:  # 他是家长/卖家
        result = VisibleLevel.Private.value

    return result


def obtain_role_visible(info)->bool:
    # 是公众吗？True 是 | False 不是
    user_id = request.current_user_id
    result = True

    if user_id == info.from_user_id or user_id == info.to_user_id:
        result = False

    return result


def obtain_content_visible(info)->bool:
    # 内容可公开见吗？
    result = True

    if info.content_visible == PublicVisible.No.value:
        result = False

    return result


def obtain_picvid_visible(info)->bool:
    # 视频/图片公开可见吗？
    result = True

    if info.picvid_visible == PublicVisible.No.value:
        result = False

    return result


def delete_public(keys: List):
    """"""
    ret, info = qiniu_multi.multi_delete(
        VisibleBucket.Public.value, keys)

    if info.status_code != 200:
        logworker.error('delete_public: ' +
                        str(keys) + ' : ' + info.text_body)


def delete_private(keys: List):
    """"""
    ret, info = qiniu_multi.multi_delete(
        VisibleBucket.Private.value, keys)

    if info.status_code != 200:
        logworker.error('delete_private: ' +
                        str(keys) + ' : ' + info.text_body)


def copy_to_public(keys: List):
    """"""
    ret, info, public_key_list = qiniu_multi.multi_copy(keys)
    if info.status_code != 200:
        logworker.error('copy_to_public: ' +
                        str(keys) + ' : ' + info.text_body)

    return public_key_list
