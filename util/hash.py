#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hashlib import md5 as hashlib_md5, sha256


def md5(s) -> str:
    m = hashlib_md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def double_sha256(s) -> str:
    h1 = sha256(bytes(s, encoding="utf8")).hexdigest()
    h2 = sha256(bytes(h1, encoding="utf8")).hexdigest()
    return h2
