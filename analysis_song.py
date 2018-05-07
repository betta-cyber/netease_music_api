#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import MySQLdb
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


mysql_cn= MySQLdb.connect(host='localhost', port=3306,user='root', passwd='root', db='netease')
df = pd.read_sql('select * from netease_music_users where birthday <> "0000-00-00 00:00:00" and birthday <> "1970-01-02 00:00:00";', con=mysql_cn, index_col="birthday")
#df = pd.read_sql('select * from netease_music_users;', con=mysql_cn, index_col="birthday")
mysql_cn.close()


x = df.index
y = df['listen_songs']


plt.figure(1, figsize=(8,6), dpi=80)

plt.scatter(x, y, s=1, label='$like')

plt.show()
