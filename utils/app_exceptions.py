# -*- coding: utf-8 -*-
class AppException(Exception):
    pass

class QueueFullException(AppException):
    pass

class MessageException(AppException):
    pass