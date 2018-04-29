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
            "INSERT INTO netease_music_songs (name, artist_id, album_id, song_id, comment_thread_id, description, pic_url, mv_id, pop) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        sql_data = (data['name'], data['ar'][0]['id'], data['al']['id'], data['id'], "", "", "", data['mv'], data['pop'])
        print sql_data
        cur.execute(sql, sql_data)
        conn.commit()
    except Exception, e:
        print Exception, ":", e


conn = MySQLdb.Connect(host = '127.0.0.1',
                       user = 'root',
                       passwd = 'root',
                       db = 'netease',
                       charset = 'utf8')

cur = conn.cursor()
sql = "SELECT album_id from netease_music_albums where id > (select max(id) from netease_music_albums where album_id = (select album_id from netease_music_songs order by id desc limit 1))"
cur.execute(sql)
result=cur.fetchall()

#print json.dumps(joker.album(34898697))

for i in result:
    print "album_id %s" % (i)
    a_id = i[0]
    detail = joker.album(a_id)
    print detail
    if detail:
        songs = detail['songs']
        for s in songs:
            save2sql(conn, s)
    sleep(0.5)


conn.close()
