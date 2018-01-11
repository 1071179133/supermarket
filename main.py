#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
import os
from shopping.shopping import Get_commodity
from atm.atm import check_balance
from atm.atm import transfer_accounts
from atm.atm import Checkout_money
from atm.atm import take_money
from auth.loginout import loginout
from atm.logger import logger
from atm.manager import adminer


if __name__ == '__main__':
    ##菜单
    menu = u'''
################## SuperMarket ##################\033[32;1m
        1. 购物(Get_commodity)
        2. 余额及消费流水(check_balance)
        3. 转账(transfer_accounts)
        4. 结账(Checkout_money,在购物下自动完成)
        5. 提现(take_money)
        6. 操作日志记录(logger)
        7. 后台管理(adminer)
        8. 退出(loginout)
        \033[0m'''
    menu_dic = {
        '1': Get_commodity,
        '2': check_balance,
        '3': transfer_accounts,
        '4': Checkout_money,
        '5': take_money,
        '6': logger,
        '7': adminer,
        '8': loginout,
    }

if __name__ == '__main__':
    while True:
        print(menu)
        choice = input("请输入操作序号：").strip()
        if choice in menu_dic:
            menu_dic[choice]()
            input('输入任意键继续：')
            print("\n")
            continue
        else:
            print("输入有误，请重新输入")
            continue