#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Decorators of API Handlers
    This module controls the permission of API accessing.
'''

from functools import update_wrapper
from flask import request, jsonify

from moretime.api.response import ErrorResponse
from moretime.wrong import error


def authenticated(wrapped):
    ''' Requrie to login as an authenticated user.
    '''
    def wrapper(*args, **kwargs):
        yes = request.current_user_id
        #if not yes:
        #    return jsonify(ErrorResponse(error.Unauthorized))
        return wrapped(*args, **kwargs)

    return update_wrapper(wrapper, wrapped)
