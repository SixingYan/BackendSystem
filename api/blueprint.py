#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Common blueprint creation function
'''

from flask import Blueprint


def create_blueprint(name, import_name, **kwargs):
    ''' Provides basic blueprint creation for all API handlers.
    '''
    url_prefix = kwargs.pop('url_prefix', '')
    bp = Blueprint(name, import_name, url_prefix=url_prefix)

    # Set App level before-request middleware.
    bp.before_app_first_request(lambda: None)

    # Set global before-request
    bp.before_app_request(lambda: None)

    return bp
