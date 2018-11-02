# -*- coding: utf-8 -*-
"""
批量拷贝文件

https://developer.qiniu.com/kodo/api/1250/batch
"""
import random
from typing import List
from qiniu import build_batch_copy, build_batch_delete, Auth, BucketManager
from moretime.util.hash import double_sha256
from moretime.entity import Facade
from moretime.api.wapp import logworker
#from momidware.celerytask import app, MyTask


def rename(key: str):
    """ 由私有文件key生成公开文件key 目前粗略实现"""
    new_key = double_sha256('{}{}'.format(random.randint(0, 10000000), key))
    return new_key


#@app.task(base=MyTask)
def multi_copy(private_key_list: List[str]) -> List:
    access_key = Facade.config["qiniu"]["access_key"]
    secret_key = Facade.config["qiniu"]["secret_key"]
    # original code
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)

    # 1. what i do
    target_copy_dict = {}
    copy_key_list = []

    # 2. prepare copy name
    for private_key in private_key_list:
        target_copy_dict[private_key] = rename(private_key)
        copy_key_list.append(rename(private_key))

    public_bucket_name = Facade.config["qiniu"]["category"]["public"]["bucket"]
    private_bucket_name = Facade.config[
        "qiniu"]["category"]["private"]["bucket"]

    logworker.warning('------multi_copy---------start')
    logworker.warning(public_bucket_name)
    logworker.warning(private_bucket_name)
    logworker.warning(copy_key_list)
    logworker.warning('end------multi_copy---------')

    # force为true时强制同名覆盖, 字典的键为原文件，值为目标文件
    ops = build_batch_copy(private_bucket_name, target_copy_dict,
                           public_bucket_name, force='false')
    ret, info = bucket.batch(ops)

    return ret, info, copy_key_list


#@app.task(base=MyTask)
def multi_delete(where: str, delete_key_list: List[str])-> None:
    access_key = Facade.config["qiniu"]["access_key"]
    secret_key = Facade.config["qiniu"]["secret_key"]
    # original code
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)

    # 1. what i do
    bucket_name = Facade.config["qiniu"]["category"][where]

    logworker.warning('------multi_copy---------start')
    logworker.warning(delete_key_list)
    logworker.warning(bucket_name)
    logworker.warning('end------multi_copy---------')

    # original code
    ops = build_batch_delete(bucket_name, delete_key_list)
    ret, info = bucket.batch(ops)


def query_file(bucket_name: str, key: str):
    """ 查询文件状态，用于检测文件是否复制成功/删除成功 """
    access_key = Facade.config["qiniu"]["access_key"]
    secret_key = Facade.config["qiniu"]["secret_key"]
    # 初始化Auth状态
    q = Auth(access_key, secret_key)
    # 初始化BucketManager
    bucket = BucketManager(q)
    ret, info = bucket.stat(bucket_name, key)
