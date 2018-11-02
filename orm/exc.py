#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ERROR_DUPLICATE_ENTRY = 1062


def is_duplicate_entry_exception(exc) ->bool:
    return exc.orig.args[0] == ERROR_DUPLICATE_ENTRY
