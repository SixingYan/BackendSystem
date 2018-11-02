#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from moretime.api.blueprint import create_blueprint

blueprint = create_blueprint(
    'moretime_blueprint', __name__, url_prefix='/v1/moretime')

from . import order_poster  # noqa
from . import reply
from . import poster
from . import info
#from . import user
