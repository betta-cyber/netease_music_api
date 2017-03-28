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

# 考虑到歌单最多10000首歌，故采用多个歌单
wait_song_list = [644264533, 644752348, 644765343, 644738922, 644776005, 644749639, 644756477, 644818427, 644835023, 644810557, 
            644806753, 644811524, 644800922, 644793786]

# 基于用户的歌单取收藏 这样不好，有重复
# flag = 0
# w = 0
# for i in range(1000797, 9999999):
#     print "current %s" % i
#     need_add_tracks = []
#     song_list_detail = joker.playlist_detail(i)
#     for song_detail in song_list_detail:
#         need_add_tracks.append(song_detail['id'])
#     print need_add_tracks
#     
#     pid = wait_song_list[w]
# 
#     result = joker.track_playlist_add(pid, need_add_tracks)
#     print result
#     if result['code'] == 505:
#         print "this song list is full."
#         w += 1
#         joker.track_playlist_add(pid, need_add_tracks)
#     
#     time.sleep(1)
#     flag += 1
#     if flag > 300:
#         time.sleep(60)
#         flag = 0

# 扫album，然后添加到songlist中
flag = 0
w = 0
for i in range(229251, 9999999):
    print "current %s" % i
    need_add_tracks = []
    song_list_detail = joker.album(i)
    for song_detail in song_list_detail:
        need_add_tracks.append(song_detail['id'])
    print need_add_tracks
    
    pid = wait_song_list[w]

    result = joker.track_playlist_add(pid, need_add_tracks)
    print result
    if result['code'] == 505:
        print "this song list is full."
        w += 1
        joker.track_playlist_add(pid, need_add_tracks)
    
    time.sleep(0.5)
    flag += 1
    if flag > 300:
        time.sleep(5)
        flag = 0
