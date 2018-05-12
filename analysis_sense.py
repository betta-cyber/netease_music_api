#!/usr/bin/env python
# encoding: utf-8

from aip import AipNlp
import MySQLdb
import json

APP_ID = '11229238'
API_KEY = 'W32Vla3bkxY9XQYPVMpnQhNQ'
SECRET_KEY = 'U2PyC6k0e5WGer5Wt6e7vzFRigNYgrG6'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


conn = MySQLdb.Connect(host = '127.0.0.1',
                       user = 'root',
                       passwd = 'root',
                       db = 'netease',
                       charset = 'utf8')

cur = conn.cursor()
sql = "SELECT content from netease_music_comments order by update_time limit 10"
cur.execute(sql)
result=cur.fetchall()

for r in result:
    sense = client.sentimentClassify(r[0].encode('utf-8'))
    print json.dumps(sense)

