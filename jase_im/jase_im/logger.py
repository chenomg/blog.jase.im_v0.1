#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")

find_connectionpool = re.compile(r'connectionpool')


def set_connectionpool_debug(record):
    # 设置日志过滤器
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        record.exc_info[0] = 'WARN'
        # print(record.exc_info)
        # if find_connectionpool.findall(exc_value):
            # record.exc_info[0] = ''
            # record.exc_info[1] = ''
    return True


LOGGING = {
    'version': 1,  # 保留的参数，默认是1
    'disable_existing_loggers': False,  # 是否禁用已经存在的logger实例
    # 日志输出格式的定义
    'formatters': {
        'standard': {  # 标准的日志格式化
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'error': {  # 错误日志输出格式
            'format':
            '%(levelname)s %(asctime)s %(pathname)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },
    # 日志过滤器, 待完成
    'filters': {
        # 特殊过滤器，替换foo成bar，可以自己配置
        'set_connectionpool_debug': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': set_connectionpool_debug,
        },
        # 是否支持DEBUG级别日志过滤
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    # 处理器：需要处理什么级别的日志及如何处理
    'handlers': {
        # 将日志打印到终端
        'console': {
            'level': 'DEBUG',  # 日志级别
            'class': 'logging.StreamHandler',  # 使用什么类去处理日志流
            'formatter': 'simple'  # 指定上面定义过的一种日志输出格式
        },
        # 默认日志处理器
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "debug.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,  # 日志文件备份的数量
            'formatter': 'standard',  # 日志输出格式
            'encoding': 'utf-8',
            'filters': ['set_connectionpool_debug'],
        },
        # 默认日志处理器
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "default.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,  # 日志文件备份的数量
            'formatter': 'standard',  # 日志输出格式
            'encoding': 'utf-8',
            'filters': ['set_connectionpool_debug'],
        },
        # 日志处理级别warn
        'warn': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "warn.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,  # 日志文件备份的数量
            'formatter': 'standard',  # 日志格式
            'encoding': 'utf-8',
        },
        # 日志级别error
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "error.log"),  # 日志文件路径
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 5,
            'formatter': 'error',  # 日志格式
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        # 默认的logger应用如下配置
        '': {
            'handlers': ['debug', 'default', 'warn', 'error'],
            'level': 'DEBUG',
            'propagate': True,  # 如果有父级的logger示例，表示不要向上传递日志流
        },
        'collect': {
            'handlers': ['console', 'debug', 'default', 'warn', 'error'],
            'level': 'INFO',
        }
    },
}
