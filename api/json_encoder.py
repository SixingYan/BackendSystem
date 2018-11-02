#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import decimal
import flask


class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)
