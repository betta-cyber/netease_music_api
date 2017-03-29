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


joker = NetEase()
user_info = {}
local_account = 'lightstrawberry@163.com'
local_password = '3ca73b783f9735a749bb0192face29f3'
# login_info = joker.login(local_account, local_password)
# print login_info

songdir = "songs_dir"
if not os.path.exists(songdir):
    os.makedirs(songdir)

print "fetching msg from " + sys.argv[1] + "\n"

song_list_detail = joker.playlist_detail(sys.argv[1])


need_download_songs = {}
for i in song_list_detail:
    song_name = i['name'] + "-" + i['artists'][0]['name']
    need_download_songs[i['id']] = song_name


song_details = joker.song_detail(list(need_download_songs.keys()))['data']

for song in song_details:
    songlink = song['url']
    song_br = song['br']
    songname = need_download_songs[song['id']]


    filename = "./" + songdir + "/" + songname + ".flac"

    f = urllib2.urlopen(songlink)
    headers = f.headers
    if not os.path.isfile(filename) and int(song_br) > 320000:
        print "%s is downloading now ......\n" % filename
        main_download(url=songlink, thread=10, save_file=filename, buffer=4096)
    #     with open(filename, "wb") as code:
    #         code.write(f.read())
    # if int(song_br) <= 320000:
    #     print "%s not have SQ music. Finding next song...\n" % songname
    else:
        print "%s is already downloaded. Finding next song...\n" % songname

print "\n================================================================\n"
print "Download finish!\nSongs' directory is " + os.getcwd() + "/songs_dir"

#
# kk = a.sendmail('[30395352]', "http://music.163.com/#/playlist?id=93303640")
# print(kk)
# for i in range(1003204, 2000000):
#     user_info = a.user_playlist(i);
#     if(user_info != []):
#         if(user_info[0]['creator'] != None):
#             user_id = user_info[0]['creator']['userId']
#             nickname = user_info[0]['creator']['nickname']
#             insert_user(nickname, user_id)
#         else:
#             print "账号已注销"
#     else:
#         print "false", i

    # url = 'https://pcs.baidu.com/rest/2.0/pcs/file?method=download&access_token=23.c696cb3121881b3e7029f074c63c9302.2592000.1491408013.3038143909-1551844&path=/apps/pcs_test_12/[八木教广] Claymore Vol_27.mobi'
    # main(url=url, thread=10, save_file='Claymore Vol_27.mobi', buffer=4096)
