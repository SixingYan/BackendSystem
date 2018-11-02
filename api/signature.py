#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Verify request signature
    验证客户端请求的签名

签名算法
    SHA-256

参与签名的字段 !必须严格按照如下顺序拼接
    salt: 盐 在最前
    header: 以下几个字段的 value 按如下顺序拼接, key 不参与哈希
        token
        uuid
        sid
        ts
        did
        dplatform
        dbrand
        osv
        app
        appv
        resolution
        channel
        ac
    query:
        对所有 key=value 键值对按照 key 的 "字典顺序" 升序排序后拼接
    body:
        直接作为字符串拼接
    timestamp：
        时间戳 header['ts'] 放在最后

签名前字符串
    plain_data = salt + header + query + body + timestamp
    样例: 这是一把使用汉字的盐TokenABCUuid123Sid567-p1=value1&p2=value2{"name":"\u5218\u5927\u529b","money":321.12,,"email":"zhaohao@moremom.com","mobile":"13311234567"}1521710099068

签名过程:
    执行两次 SHA-256
    hash = SHA-256(SHA-256(plain_data).upper()).upper()

'''

import collections
from hashlib import sha256


def build_signature(d_header, d_param, s_body, s_salt) -> str:
    header_key = [
        "token",
        "uuid",
        "sid",
        "ts",
        "did",
        "dplatform",
        "dbrand",
        "osv",
        "app",
        "appv",
        "resolution",
        "channel",
        "ac",
    ]

    if len(d_header["ts"]) != 10:
        return False

    header_data = "".join([d_header.get(k, "") for k in header_key])

    ordered_query = collections.OrderedDict()

    for k in sorted(d_param.keys()):
        ordered_query[k] = d_param[k]
    query_data = '&'.join(['{}={}'.format(k, v)
                           for k, v in ordered_query.items()])

    plain = s_salt + header_data + query_data + s_body
    s1 = sha256(bytes(plain, encoding='utf8')).hexdigest()
    s2 = sha256(bytes(s1, encoding='utf8')).hexdigest()
    return s2


SALT = '棘心夭夭，母氏劬劳。母氏圣善，我无令人。'


def verify_signature(d_header, d_param, b_body) ->bool:
    try:
        body_str = b_body.decode('utf-8')
        server_signature = build_signature(d_header, d_param, body_str, SALT)
        request_signature = d_header['sig']
        return server_signature == request_signature
    except Exception as e:
        print("请求摘要出错========", e, "===========")
        return False
