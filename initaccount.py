#!/usr/bin/env python
# encoding: utf-8

from api import NetEase
import time

joker = NetEase()
user_info = {}
local_account = 'gnrphl@163.com'
local_password = 'b9cd4a29fc0fe94c2be28834a4fe66cc'
login_info = joker.login(local_account, local_password)
print login_info

print joker.add_playlist(21225462)
