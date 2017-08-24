#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: betta

'''
netease music api
'''

from api import NetEase
import time
import gevent
from gevent.threadpool import ThreadPool

pool = ThreadPool(10)

# 考虑到歌单最多10000首歌，故采用多个歌单
wait_song_list = [644264533, 644752348, 644765343, 644738922, 644776005, 644749639, 644756477, 644818427, 644835023, 644810557,
                  644806753, 644811524, 644800922, 644793786]
# wait_song_list = [644810557, 644806753, 644811524, 644800922, 644793786]
back_song_list = [583517654, 431743699]

joker = NetEase()
user_info = {}
local_account = 'lightstrawberry@163.com'
local_password = '3ca73b783f9735a749bb0192face29f3'
#local_account = 'oxp202@163.com'
#local_password = '36ed58c5c14dc2f58eef099585d2a939'

login_info = joker.login(local_account, local_password)
print login_info

def track_log(i):
    song_info = joker.song_info(i)
    if song_info:
        #print song_info
        try:
            play_time = song_info[0]['bMusic']['playTime']/1000
        except IndexError:
            play_time = 60

        print 'finish %s %s' % (i, joker.track_log(i, play_time))
        #time.sleep(0.5)
    else:
        print 'no song'



# Start 10 threads
print joker.sendmail([277526727], '你爱我吗？')
print joker.send_song_list_mail(622835784, 'sssss' ,[277526727])

#for k in range(462942247, 500000000):
#    pool.spawn(track_log, k)
#
#gevent.wait()
#print "finish all"
#
#for i in reversed(back_song_list):
#    print "current %s" % i
#    need_add_track_logs = []
#    song_list_detail = joker.playlist_detail(i)
#    for song_detail in song_list_detail:
#        need_add_track_logs.append(song_detail['id'])
#    print need_add_track_logs
#
#    for song_id in need_add_track_logs:
#        song_info = joker.song_info(song_id)
#        # print song_info
#        try:
#            play_time = song_info[0]['bMusic']['playTime']/1000
#        except IndexError:
#            play_time = 60
#        # print play_time/1000
#        # print current_song_list
#
#        print 'finish', song_id, joker.track_log(song_id, play_time, i)
#        time.sleep(3)

# print joker.track_log(410519492)

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
# flag = 0
# w = 0
# for i in range(229251, 9999999):
#     print "current %s" % i
#     need_add_tracks = []
#     song_list_detail = joker.album(i)
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
#     time.sleep(0.5)
#     flag += 1
#     if flag > 300:
#         time.sleep(5)
#         flag = 0
