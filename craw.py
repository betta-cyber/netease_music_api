#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: betta

'''
netease music api
'''

from api import NetEase
import json
import _mysql
import MySQLdb
from time import sleep


joker = NetEase()
user_info = {}
local_account = 'betta551@163.com'
local_password = 'c7236970bfc8e9f7aa83ad3d6d14d59a'

#login_info = joker.login(local_account, local_password)
#print login_info


def save2sql(conn, data):
    artist = data['artist']
    print artist['name']
    try:
        cur = conn.cursor()
        sql = (
            "INSERT INTO netease_music_artists (name, artist_id, brief_desc, pic_url, pic_id, mv_size, album_size, music_size) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        sql_data = (artist['name'], artist['id'], artist['briefDesc'], artist['picUrl'], artist['picId'], artist['mvSize'], artist['albumSize'], artist['musicSize'])
        cur.execute(sql, sql_data)
        conn.commit()
    except:
        print 'error'

conn = MySQLdb.Connect(host = '127.0.0.1',
                       user = 'root',
                       passwd = 'root',
                       db = 'netease',
                       charset = 'utf8')
for i in range(18437, 962804):
    print str(i)+'\n'
    artists_info = joker.artist(i)
    #print artists_info
    if artists_info:
        save2sql(conn, artists_info)
    sleep(1)
conn.close()
#print json.dumps(joker.artist(6452)).decode("unicode-escape")




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
