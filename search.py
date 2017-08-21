#!/usr/bin/env python
# encoding: utf-8

from api import NetEase
import time
import MySQLdb

def insert_song(song_info):
    song_name = song_info[0]['name']
    artist_id = song_info[0]['artists'][0]['id']
    album_id = song_info[0]['album']['id']
    mp3_url = str(song_info[0]['mp3Url'])
    comment_thread_id = song_info[0]['commentThreadId']
    popularity = song_info[0]['popularity']
    play_time = song_info[0]['bMusic']['playTime']
    bitrate = song_info[0]['bMusic']['bitrate']
    song_id = song_info[0]['id']
    
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="root",  # your password
                         db="netease_music")        # name of the data base
    cur = db.cursor()
    sql = 'INSERT INTO songs (song_name, artist_id, album_id, mp3_url, comment_thread_id, popularity, play_time, bitrate, song_id) VALUES \
    ("%s", %s, %s, "%s", "%s", %s, %s, %s, %s)' % (song_name, artist_id, album_id, mp3_url, comment_thread_id, popularity, play_time, bitrate, song_id)
    print sql
    cur.execute(sql)
    db.commit()
    db.close()
    return 0

joker = NetEase()
user_info = {}
local_account = 'lightstrawberry@163.com'
local_password = '3ca73b783f9735a749bb0192face29f3'
login_info = joker.login(local_account, local_password)
print login_info


# for i in range(478731242, 488731242):
#     song_info = joker.song_info(i)
#     print song_info
#     if song_info:
#         # insert_song(song_info)
#         try:
#             play_time = song_info[0]['bMusic']['playTime']/1000
#         except IndexError:
#             play_time = 60
#         print 'finish', i, joker.track_log(i, play_time)
#         time.sleep(1)