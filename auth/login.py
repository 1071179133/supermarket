#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import json
import time

userinfo = {}
##定义读取文件函数
def read_info(username):
    global userinfo
    f = open('%s/db/%s.json' % (p_dir, username), 'r', encoding='utf-8')
    for line in f:
        userinfo = json.loads(line)
    f.close()
    return userinfo
##定义写入文件函数
def write_into(username,userinfo):
    f = open('%s/db/%s.json'%(p_dir,username), 'w', encoding='utf-8')
    json.dump(userinfo, f)
    f.close()
    '''如果字典是汉字，存到文本就是二进制字符，这种字符计算机认识就可以了
       如果字典是英文，存到文件就是英文了
    '''
user_status = False  ##用户登录了就把这个改成True
def LoginApi():
    def outer(func):
        def inner(*args,**kwargs):
            while True:
                global user_status
                global username
                if user_status == False:
                    select_info = input("你是否有注册过账号了? Please select Y/N:")
                    ##用户注册信息
                    if select_info == 'N' or select_info == 'n':
                        print("开始注册用户信息：")
                        username = input("Please enter your username:")
                        password = input("Please enter your password:")
                        phone_number = input("Please enter your phon_number:")
                        if not os.path.exists('%s/db/%s.json'%(p_dir,username)):
                            userinfo[username] = {
                                    "info":[
                                        {
                                            "username":"%s" %username,
                                            "password":"%s" %password,
                                            "phon_number":"%s" %phone_number,
                                            "login_count":0
                                        }
                                    ],
                                    "money":[
                                        {}
                                    ],
                                    "already_get_commodity":[],
                            }
                            write_into(username,userinfo)
                            print("恭喜注册成功！")
                        else:
                            print("用户已存在...")
                            continue

                    ##用户登陆验证信息
                    elif select_info == 'Y' or select_info == 'y':
                        #count = 0
                        while True:
                            #print(userinfo)
                            print("开始登录验证信息：")
                            username = input("Please enter your username:")
                            password = input("Please enter your password:")
                            ##第一次判断输入用户是否存在
                            if os.path.exists('%s/db/%s.json' % (p_dir, username)):
                                read_info(username)
                                if not username in userinfo:
                                    print("没有该用户，请确认你的用户名！")
                                    continue
                                #判断用户登陆失败的次数是否小于3
                                if userinfo[username]['info'][0]['login_count'] < 3:
                                    ##判断用户账号密码是否吻合
                                    if username in userinfo and password == userinfo[username]['info'][0]['password']:       ##【优化2次】用户及密码已经一一对应
                                        print("\033[35;1mwelcom login {_username}\033[0m".format(_username=username).center(150,'#'))
                                        ##登陆成功后将失败次数清零，便于下一次统计
                                        userinfo[username]['info'][0]['login_count'] = 0
                                        write_into(username, userinfo)
                                        ##返回username给后面函数调用
                                        user_status = True
                                        func(username,userinfo)
                                        return True
                                        #return username,userinfo
                                        #break
                                    else:
                                        #count += 1
                                        ##修改用户登陆失败的次数
                                        userinfo[username]['info'][0]['login_count'] = userinfo[username]['info'][0]['login_count'] + 1
                                        print('Check fail...Check again...')
                                        print("您还有%s次登录机会" % (3 - userinfo[username]['info'][0]['login_count']))
                                        write_into(username, userinfo)
                                        continue
                                else:
                                    print("重复登陆多次失败，请15分钟后再尝试登陆...")
                                    userinfo[username]['info'][0]['login_count'] = 0
                                    write_into(username, userinfo)
                                    time.sleep(15)
                                    exit()
                            else:
                                print("用户不存在，请注册...")
                                break
                    else:
                        print("您输入的内容错误! Please enter again...")
                        continue
                if user_status == True:
                    print("##装饰器备注使用：用户已登录")
                    func(username,userinfo)
                    return True
        return inner
    return outer