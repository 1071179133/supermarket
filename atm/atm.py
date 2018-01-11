#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
##黄色
def print_yellow(messages):
    print('\033[1;33m %s \033[0m' %messages)

import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from auth.login import write_into
from auth.login import read_info
from  auth.login import LoginApi

##查询余额及账单
@LoginApi()
def check_balance(username,userinfo):
    if userinfo[username]['money'][0]:
        print_yellow('账单查询Start'.center(25, '#'))
        print("你的余额为：\033[1;32m %s元 \033[0m，你的购买历史如下：" % userinfo[username]['money'][0]['money'])
        if userinfo[username]['already_get_commodity']:
            print("#      购买时间        序号   商品    价格")
            for i in userinfo[username]['already_get_commodity']:
                if i:
                    print('#   ',i['购买时间'],i['ID'], i['商品'], i['价格'])
            print_yellow('账单查询End'.center(25,'#'))
        else:
            print("没有购买历史，去尽情购买吧！")
    else:
        print("没有充值历史和购物历史，请进入商城充值及购物！")
##提现
@LoginApi()
def take_money(username,userinfo):
    print("您现在的余额为 %s元"%userinfo[username]['money'][0]['money'])
    ta_money = int(input("提现需要5%的手续费，请输入提现金额："))
    ot_money = ta_money * 0.05
    tb_money = ot_money + ta_money
    if ta_money <= int(userinfo[username]['money'][0]['money']):
        new_money = int(userinfo[username]['money'][0]['money']) - tb_money
        userinfo[username]['money'][0]['money'] = new_money
        write_into(username, userinfo)
        print("本次提现%s元，手续费%s元，账户余额%s元,请保管好你的钱包！"%(ta_money,ot_money,new_money))

##转账
@LoginApi()
def transfer_accounts(username,userinfo):
    if userinfo[username]['money'][0]:
        print("您现在的余额为 %s元"%userinfo[username]['money'][0]['money'])
        to_username = input("请输入目的账户用户名：")
        if os.path.exists('%s/db/%s.json' % (p_dir,to_username)):
            to_money = int(input("请输入转账金额/元："))
            if to_money <= int(userinfo[username]['money'][0]['money']):
                ##更新转账用户的信息
                money = int(userinfo[username]['money'][0]['money']) - to_money
                userinfo[username]['money'][0]['money'] = money
                write_into(username, userinfo)
                print("更新数据成功")
                ##更新转账目的用户的信息
                userinfo = read_info(to_username)
                #print(userinfo)
                if not userinfo[to_username]['money'][0]:
                    userinfo[to_username]['money'][0]['money'] = 0
                new_money = int(userinfo[to_username]['money'][0]['money']) + to_money
                userinfo[to_username]['money'][0]['money'] = new_money
                write_into(to_username,userinfo)
                print("转账成功")
                userinfo = read_info(username)
            else:
                print("你的账户余额小于转账金额，转账取消....")
        else:
            print("用户不存在...")
            exit()
    else:
        print("您的账户中还没有余额，请前去商城充值...")
        exit()

##结账
@LoginApi()
def Checkout_money(username,userinfo):
    return
    balance = int(userinfo[username]['money'][0]['money']) - spend_money
    userinfo[username]['money'][0]['money'] = balance
    write_into(username, userinfo)