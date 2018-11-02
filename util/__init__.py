#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from hashlib import md5 as hashlib_md5, sha256


def current_timestamp() -> int:
    return int(time.mktime(time.localtime()))


def md5(s) -> str:
    m = hashlib_md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def double_sha256(s) -> str:
    h1 = sha256(bytes(s, encoding="utf8")).hexdigest()
    h2 = sha256(bytes(h1, encoding="utf8")).hexdigest()
    return h2


class DictObject(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)
