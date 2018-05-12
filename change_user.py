#!/usr/bin/env python
# encoding: utf-8

import random
import hashlib
from api import NetEase

cookie_path = "~/.netease-music_api/cookie"

def md5(passwd):
    md = hashlib.md5()
    md.update(passwd)
    return md.hexdigest()


def change_user():
    #file = open('163.md')
    file = open('account.txt')
    try:
        alist = file.read()
    finally:
        file.close()
    account_list = alist.splitlines()
    account = random.choice(account_list)

    user = account.split(",")[0]
    passwd = md5(account.split(",")[1])

    joker = NetEase()
    login_info = joker.login(user, passwd)

    print login_info
    return login_info

