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
import time


joker = NetEase()
user_info = {}
local_account = 'betta551@163.com'
local_password = 'c7236970bfc8e9f7aa83ad3d6d14d59a'

#login_info = joker.login(local_account, local_password)
#print login_info

def save2sql(conn, data, song_id):
    try:
        sql = (
            "INSERT INTO netease_music_comments (content, song_id, liked_count, user_id, comment_id, send_time) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        time_tmp = time.localtime(data['time']/1000)
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tmp)
        sql_data = (data['content'], song_id, data['likedCount'], data['user']['userId'], data['commentId'], cur_time)
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
#sql = "SELECT song_id from netease_music_songs where id > (select song_id from netease_music_comments order by id desc limit 1)"
sql = "SELECT song_id from netease_music_songs where id > 186664 order by id "
cur.execute(sql)
result=cur.fetchall()

for s in result:
    print "song_id %s" % (s)
    id = s[0]
    flag = True
    page = 0
    while flag:
        detail = joker.comment(id, page)
        print detail
        if detail:
            flag = detail['more']
            comments = detail['comments']
            for s in comments:
                save2sql(conn, s, id)
        else:
            flag = False
        sleep(0.5)
        page += 1
    sleep(0.5)


conn.close()
