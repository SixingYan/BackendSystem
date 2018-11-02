import logging
import logging.handlers
import os
from os import path

#返回当前文件所在的目录  
api_path = path.dirname(__file__)

# 获得d所在的目录,即d的父级目录
moretime_path = os.path.dirname(api_path)

# logs 文件所在目录
LOG_PATH_ = os.path.join(moretime_path, 'logs/')

LOG_TAG_ = ''  # 可输入自定义标签

LOG_FORMAT_SIMP = logging.Formatter(
    '%(asctime)s-%(levelname)s-%(message)s')

LOG_FORMAT_COMX = logging.Formatter(
    '%(asctime)s-%(levelname)s-%(funcName)s-%(message)s')


def setup_logging():
    logworker = logging.getLogger('MainLog')
    logworker.setLevel(logging.DEBUG)

    # 1M = 1kB = 1024 * 1024 Byte = 2^20 Byte, it will have info_log.log, info_log.log.1,
    # ..., info_log.log.4 最多会有4个这样的文件

    infolog = logging.handlers.RotatingFileHandler(LOG_PATH_ + 'InfoLog{0}.log'.format(
        LOG_TAG_), mode='a', maxBytes=2**20, backupCount=4, encoding='utf8')
    infolog.setLevel(logging.INFO)
    infolog.setFormatter(LOG_FORMAT_COMX)

    warnlog = logging.handlers.RotatingFileHandler(LOG_PATH_ + 'WarnLog{0}.log'.format(
        LOG_TAG_), mode='a', maxBytes=2**20, backupCount=4, encoding='utf8')
    warnlog.setLevel(logging.WARN)
    warnlog.setFormatter(LOG_FORMAT_COMX)

    errlog = logging.handlers.RotatingFileHandler(LOG_PATH_ + 'ErrorLog{0}.log'.format(
        LOG_TAG_), mode='a', maxBytes=2**20, backupCount=4, encoding='utf8')
    errlog.setLevel(logging.ERROR)
    errlog.setFormatter(LOG_FORMAT_COMX)

    logworker.addHandler(infolog)
    logworker.addHandler(warnlog)
    logworker.addHandler(errlog)

    return logworker


"""
common_usecase.inject_log()
"""
