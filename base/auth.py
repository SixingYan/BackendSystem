#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from hashlib import sha256


private_key = "Before God we are all equally wise - and equally foolish.人人生而平等。"


def create_token(device_id, uuid) -> str:
    if len(device_id) != 32:
        raise Exception("Wrong device_id length")
    if len(uuid) != 6:
        raise Exception("Wrong uuid length")
    ts = int(time.time())
    tmp = "{0}{1}{2}{3}".format(device_id, uuid, ts, private_key)
    sig = sha256(sha256(tmp.encode("utf8")).digest()).hexdigest()
    return "{0}{1}{2}".format(sig, uuid, ts)


# token dict
# {t , h , i } / { date , hash token string, db_id }
def parse_token(token, device_id) -> str:
    if len(device_id) != 32:
        raise Exception("Wrong device_id length")
    if len(token) != 80:
        raise Exception("Wrong token length")
    ts = token[-10:]
    uuid = token[-16:-10]
    sig = token[:-16]
    tmp = "{0}{1}{2}{3}".format(device_id, uuid, ts, private_key)
    vsig = sha256(sha256(tmp.encode("utf8")).digest()).hexdigest()
    if sig == vsig:
        return uuid
    else:
        return None
