#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
import os,sys,time
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from auth.login import LoginApi
import logging

@LoginApi()
def logger(username,userinfo):
    pass