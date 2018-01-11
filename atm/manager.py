#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
import os,sys,time
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from auth.login import read_info
from auth.login import write_into

def set_username(username,userinfo):
    return
    print("现在的用户名是 %s"%userinfo[username]['info'][0]['username'])
    new_name = input("请输入新的名字：").strip()
    userinfo[username]['info'][0]['username'] = new_name
    write_into(username,userinfo)
    print("修改用户名成功")
    print("现在的用户名是 %s" % userinfo[username]['info'][0]['username'])

def set_password(username,userinfo):
    print("现在的用户密码是 %s" % userinfo[username]['info'][0]['password'])
    new_password = input("请输入新的密码：").strip()
    userinfo[username]['info'][0]['password'] = new_password
    write_into(username, userinfo)
    print("修改用户密码成功")
    print("现在的用户密码是 %s" % userinfo[username]['info'][0]['password'])

def set_money(username,userinfo):
    print("现在的用户余额是 %s元" % userinfo[username]['money'][0]['money'])
    new_money = int(input("请输入新的余额：").strip())
    userinfo[username]['money'][0]['money'] = new_money
    write_into(username, userinfo)
    print("修改用户余额成功")
    print("现在的用户余额是 %s元" % userinfo[username]['money'][0]['money'])

def set_login(username,userinfo):
    userinfo[username]['info'][0]['login_count'] = 10
    write_into(username, userinfo)
    print("冻结用户成功")


def mamager_info():
    menu = u'''
    ################## 后台管理 ##################\033[32;1m
            1. 修改用户名(不支持，因为字典设计问题，修改很麻烦)
            2. 修改用户密码
            3. 充值或余额更改
            4. 冻结账户(此处只冻结一次)
            5. 退出后台管理
            \033[0m'''
    menu_dic = {
        '1': set_username,
        '2': set_password,
        '3': set_money,
        '4': set_login
    }
    username = input("请输入普通用户的名字：").strip()
    if os.path.exists('%s/db/%s.json' % (p_dir, username)):
        userinfo = read_info(username)
        while True:
            print(menu)
            choice = input("请输入操作序号：").strip()
            if choice in menu_dic:
                menu_dic[choice](username,userinfo)
                input('输入任意键继续：')
                print("\n")
                continue
            elif choice == '5':
                print("退出后台管理")
                break
            else:
                print("输入有误，请重新输入")
                continue
    else:
        print('没有这个用户！')


def adminer():
    while True:
        userinfo = read_info('adm')
        #print(userinfo)
        select_info = input("你是否有注册过管理员账号了? Please select Y/N:")
        if select_info == 'N' or select_info == 'n':
            print("开始注册用户信息【只允许注册3个管理员账号】：")
            rgcode = input("请输入注册邀请码(默认定为'root123456.')：").strip()
            if rgcode == userinfo['rgcode']:
                if userinfo['now_number'] < userinfo['max_number']:
                    username = input("Please enter your username:")
                    password = input("Please enter your password:")
                    phone_number = input("Please enter your phon_number:")

                    if not os.path.exists('%s/db/%s.json' % (p_dir, username)):
                        userinfo['now_number'] = userinfo['now_number'] + 1
                        write_into('adm',userinfo)
                        userinfo = {}
                        userinfo = {
                            "%s"%username: [
                                {
                                    "username": "%s" % username,
                                    "password": "%s" % password,
                                    "phon_number": "%s" % phone_number,
                                    "login_count": 0
                                }
                            ],
                        }
                        write_into(username, userinfo)
                        print("恭喜注册成功！")
                    else:
                        print("用户已存在...")
                        #continue
                else:
                    print("管理员名额已满，不可注册")
            else:
                print("你的邀请码无效，不可以注册管理员账号。")
        elif select_info == 'Y' or select_info == 'y':
            print("开始登录验证信息：")
            username = input("Please enter your username:")
            password = input("Please enter your password:")
            ##第一次判断输入用户是否存在
            if os.path.exists('%s/db/%s.json' % (p_dir, username)):
                userinfo = read_info(username)
                if not username in userinfo:
                    print("没有该用户，请确认你的用户名！")
                    #continue
                # 判断用户登陆失败的次数是否小于3
                #print(userinfo)
                if userinfo[username][0]['login_count'] < 3:
                    ##判断用户账号密码是否吻合
                    if username in userinfo and password == userinfo[username][0]['password']:  ##【优化2次】用户及密码已经一一对应
                        print("\033[35;1mwelcom login {_username}\033[0m".format(_username=username).center(150, '#'))
                        ##登陆成功后将失败次数清零，便于下一次统计
                        userinfo[username][0]['login_count'] = 0
                        write_into(username,userinfo)
                        ##开始执行后台管理菜单
                        mamager_info()
                        break
                        ##返回username给后面函数调用
                        # return username,userinfo
                        # break
                    else:
                        # count += 1
                        ##修改用户登陆失败的次数
                        userinfo[username][0]['login_count'] = userinfo[username][0]['login_count'] + 1
                        print('Check fail...Check again...')
                        print("您还有%s次登录机会" % (3 - userinfo[username][0]['login_count']))
                        write_into(username, userinfo)
                        continue
                else:
                    print("重复登陆多次失败，请15分钟后再尝试登陆...")
                    userinfo[username][0]['login_count'] = 0
                    write_into(username, userinfo)
                    time.sleep(15)
                    continue
            else:
                print("用户不存在，请注册...")
        else:
            print("您输入的内容错误! Please enter again...")
            continue

