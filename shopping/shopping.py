#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
def print_red(messages):
    print('\033[1;35m %s \033[0m' %messages)
##绿色
def print_green(messages):
    print('\033[1;32m %s \033[0m' %messages)
##黄色
def print_yellow(messages):
    print('\033[1;33m %s \033[0m' %messages)

import os,sys,time
import logging

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.login import write_into
from auth.login import LoginApi
from auth.login import read_info
now_time = time.strftime("%Y-%m-%d")

commodity_list = [
    ['华为meta 10',6999],
    ['iphone X',9999],
    ['游戏主机',19999],
    ['曲面显示屏',2999],
    ['游戏本',7999],
    ['机械键盘',599]
]

##商城购物函数
@LoginApi()
def Get_commodity(username,userinfo):
    logging.basicConfig(filename='logs/%s_%s.log' %(username,now_time), format='%(asctime)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    already_get_commodity = []
    userinfo = read_info(username)
    if userinfo[username]['money'][0]:
        print("你的余额为：\033[1;32m %s元 \033[0m，你的购买历史如下：" % userinfo[username]['money'][0]['money'])
        print("#   序号 商品    价格    购买时间")
        for i in userinfo[username]['already_get_commodity']:
            if i:
                print('#   ',i['ID'], i['商品'], i['价格'],i['购买时间'])
        print_yellow('购物历史清单End'.center(25,'#'))
    while True:
        if not userinfo[username]['money'][0]:
            money = input("请输入你拥有的金额：")
            if money.isdigit():
                money = int(money)
                userinfo[username]['money'][0]['money'] = '%s' % money
                logging.info('充值金额： %s元'%money)
                break
            else:
                print("请输入数字金额！")
                logging.warning('充值金额时输入错误...')
                continue
        else:
            break

    while True:
        while True:
            print(' ')
            print_red('商品列表'.center(25,'#'))
            print("#   序号 商品  价格")
            ##获取商品列表
            for key,commodity in enumerate(commodity_list):
                print('#   ',key,commodity[0],commodity[1])
            print(' ')
            get_commodity = input("\033[1;35m请选择你购买商品的序号：\033[0m")
            buy_time = time.strftime("%Y-%m-%d %H:%M:%S")
            ##得到商品序号
            if get_commodity.isdigit() and int(get_commodity) < len(commodity_list):
                get_commodity = int(get_commodity)
                ##判断商品价格是否大于用户金钱数
                if commodity_list[get_commodity][1] <= int(userinfo[username]['money'][0]['money']):
                    ##计算用户金钱数
                    real_money = int(userinfo[username]['money'][0]['money']) - int(commodity_list[get_commodity][1])
                    money = real_money
                    ##把当前购买的商品信息写到已购买商品的信息字典
                    already_get_commodity.append(['%s' %get_commodity,'%s' %commodity_list[get_commodity][0],'%s' %commodity_list[get_commodity][1],'%s'%buy_time])
                    #print(already_get_commodity)
                    print("购买商品\033[1;32m %s \033[0m成功，你余额为\033[1;32m %s元 \033[0m" %(commodity_list[get_commodity][0],money))
                    logging.info('在商场购买商品 %s 成功，话费 %s元'%(commodity_list[get_commodity][0],money))
                    ##追加总商品信息到字典
                    userinfo[username]['already_get_commodity'].append({"ID": "%s" %get_commodity, "商品": "%s" %commodity_list[get_commodity][0], "价格": "%s" %commodity_list[get_commodity][1],"购买时间":"%s"%buy_time})
                    ##修改用户信息剩余金钱
                    userinfo[username]['money'][0]['money'] = '%s' %money
                    #print(UF.UserInfo)
                else:
                    print("你没有足够的金钱去购买\033[1;35m %s \033[0m，它的价格为\033[1;35m %s元 \033[0m,而你的余额为\033[1;35m %s元 \033[0m" %(commodity_list[get_commodity][0],commodity_list[get_commodity][1],userinfo[username]['money'][0]['money']))
                    logging.warning('%s 没有足够的金钱去购买 %s ,该商品价格为 %s元'%(username,commodity_list[get_commodity][0],commodity_list[get_commodity][1]))
                print(' ')
                per_select = input("请问是否继续购买商品\033[1;35my/n\033[0m:")
                if per_select.startswith('y'):
                    continue
                elif per_select.startswith('n'):
                    print(' ')
                    print("\033[1;32m你本次购买的商品如下：\033[0m")
                    print_red('商品列表'.center(25, '#'))
                    print("#   序号 商品  价格")
                    for already_getp in already_get_commodity:
                        print('#   ',already_getp[0],already_getp[1],already_getp[2])
                    print("你的余额为：\033[1;32m %s元 \033[0m" %userinfo[username]['money'][0]['money'])
                    print_red('结算结束'.center(25, '#'))
                    ##退出程序前，把所有信息写进json信息记录文件，以便下一次登陆提取
                    write_into(username,userinfo)
                    return
            else:
                print("输入有错，请重新输入！")
                logging.warning('购买时输入商品序号错误....')
                continue