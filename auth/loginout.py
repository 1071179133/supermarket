#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from auth.login import LoginApi

#@LoginApi()
def loginout(*args,**kwargs):
    print("\033[35;1m感谢使用，再见！\033[0m")
    exit()