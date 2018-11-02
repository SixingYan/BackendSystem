#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Facade(object):

    """ 全局变量集中营
    """
    config = None			# 配置信息
    redis_cli = None		# Redis 连接
