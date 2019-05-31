# -*- coding:utf-8 -*-
"""
Exceptions' definition
"""


class ExitException(Exception):
    """
    这个异常指的是某种情况下要求client退出, 而非退出本身发生了异常
    """
    def __init__(self, message='Client exit!'):
        self.message = message

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.__repr__()


class IllegalInputException(Exception):
    """
    这个异常指的是用户输入有非法情况
    """
    def __init__(self, message='Illegal input!'):
        self.message = message

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.__repr__()