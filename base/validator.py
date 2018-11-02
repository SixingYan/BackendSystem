#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

from stdnum import luhn
from stdnum import exceptions as stdnum_exceptions


def v_mobile(value) ->bool:
    if not value:
        return False
    p = re.compile(r'^1[3|4|5|6|7|8|9]\d{9}$')
    m = p.match(value)
    return True if m else False


def v_id_number_bits(value) ->bool:
    s = sum(
        map(lambda x: x[0] * x[1],
            zip([7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2],
                map(int, value[:-1]))))
    r = s % 11
    last_bit = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']
    if str(value[-1]) != last_bit[r]:
        return False
    return True


def v_id_number(value) ->bool:
    if not value:
        return False
    value = value.lower()
    RE_ID_NUMBER = r'(^\d{15}$)|(^\d{17}([0-9]|x)$)'
    if not re.match(RE_ID_NUMBER, value):
        return False
    return v_id_number_bits(value)


def v_bank_card_number(value) ->bool:
    if not value or not 16 <= len(value) <= 19:
        return False
    try:
        luhn.validate(value)
    except (stdnum_exceptions.InvalidFormat,
            stdnum_exceptions.InvalidChecksum):
        return False
    return True


def v_include_chinese(value) ->bool:
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    for o in value:
        if u'\u4e00' <= o <= u'\u9fff':
            return True
    return False


def v_enc_id(value) ->bool:
    return True


def v_enc_user_id(value) ->bool:
    return True


def v_enc_message_id(value) ->bool:
    return True


if __name__ == '__main__':
    print(v_mobile('18612250030'))
    print(v_mobile('11812250030'))
    print(v_id_number('220382198608195319'))
    print(v_id_number('220382197908195319'))
    print(v_bank_card_number('6214860145860819'))
    print(v_bank_card_number('6214860145810819'))
    print(v_include_chinese('hello你好world'))
    print(v_include_chinese('hello world'))
