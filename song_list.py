#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: betta

'''
netease music api
'''

from api import NetEase
from download import main_download
import re
import requests
import json
import urllib2
import os
import sys
import time


joker = NetEase()
user_info = {}
local_account = 'lightstrawberry@163.com'
local_password = '3ca73b783f9735a749bb0192face29f3'
# login_info = joker.login(local_account, local_password)
# print login_info
flag = 0
for i in range(1000259, 9999999):
    print "current %s" % i
    need_add_tracks = []
    song_list_detail = joker.playlist_detail(i)
    for song_detail in song_list_detail:
        need_add_tracks.append(song_detail['id'])
    print need_add_tracks

    print joker.track_playlist_add(need_add_tracks)
    
    time.sleep(1)
    flag += 1
    if flag > 100:
        time.sleep(600)
        flag = 0
