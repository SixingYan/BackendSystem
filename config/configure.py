#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import toml


class RunEnvTypes(object):
    LOCAL = "LOCAL"
    DEV = "DEVELOPMENT"
    PROD = "PRODUCTION"


def is_locale_env():
    print(os.environ.get("SERVER_MODE"))
    return os.environ.get("SERVER_MODE") == RunEnvTypes.LOCAL


def is_dev_env():
    print(os.environ.get("SERVER_MODE"))
    return os.environ.get("SERVER_MODE") == RunEnvTypes.DEV

def is_prod_env():
    print(os.environ.get("SERVER_MODE"))
    return os.environ.get("SERVER_MODE") == RunEnvTypes.PROD


def get_common_config():
    cur_dir_path = os.path.abspath(os.path.dirname(__file__))
    if is_locale_env():
        file_path = os.path.join(cur_dir_path, 'local.toml')
        return toml.load(file_path)
    elif is_dev_env():
        file_path = os.path.join(cur_dir_path, 'dev.toml')
        return toml.load(file_path)
    elif is_prod_env():
        file_path = os.path.join(cur_dir_path, 'prod.toml')
        return toml.load(file_path)
    else:
        raise Exception("unknown env type")
