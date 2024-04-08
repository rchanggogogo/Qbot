#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@file        :models.py
@time        :2024/04/08 22:44:11
@author      :changlei
'''

class SecurityInfo(object):
    """
    用于获取股票信息
    """
    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.display_name = kwargs.get("display_name", None)
        self.name = kwargs.get("name", None)
        self.start_date = kwargs.get("start_date", None)
        self.end_date = kwargs.get("end_date", None)
        self.type = kwargs.get("type", None)
        self.parent = kwargs.get("parent", None)
        
    def __repr__(self):
        return self.code
    
    def __str__(self):
        return self.code
