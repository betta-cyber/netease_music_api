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
    try:
        sql = (
            "INSERT INTO netease_music_albums (name, artist_id, album_id, comment_thread_id, description, pic_url, type, size, publish_time) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        sql_data = (data['name'], data['artist']['id'], data['id'], data['commentThreadId'], data['description'], data['picUrl'], data['type'], data['size'], data['publishTime'])
        cur.execute(sql, sql_data)
        conn.commit()
    except:
        print 'error'

conn = MySQLdb.Connect(host = '127.0.0.1',
                       user = 'root',
                       passwd = 'root',
                       db = 'netease',
                       charset = 'utf8')

cur = conn.cursor()
sql = "SELECT artist_id from netease_music_artists where artist_id > 18437"
cur.execute(sql)
result=cur.fetchall()

for i in result:
    print "artist_id %s" % (i)
    artist_id = i[0]
    album_detail = joker.artist_album(artist_id)
    if album_detail['code'] == 200:
        albums = album_detail['hotAlbums']
        for a in albums:
            save2sql(conn, a)
    else:
        print album_detail['msg']
    sleep(1)

conn.close()
