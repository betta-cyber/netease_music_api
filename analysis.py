#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import MySQLdb
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


mysql_cn= MySQLdb.connect(host='localhost', port=3306,user='root', passwd='root', db='netease')
df = pd.read_sql('select * from netease_music_users;', con=mysql_cn)
mysql_cn.close()

nosex = df[df.gender == 0]
male = df[df.gender == 1]
famale = df[df.gender == 2]

labels = [u'男',u'女',u'不详']
fracs = [male.shape[0]*100/df.shape[0], famale.shape[0]*100/df.shape[0], nosex.shape[0]*100/df.shape[0]]
#fracs = [15, 30.55, 54.44]
explode = [0, 0, 0.1]

plt.figure(1, figsize=(6,6))
plt.pie(x=fracs, labels=labels, autopct = '%3.1f %%', shadow = False, labeldistance=1.1, startangle = 90,pctdistance = 0.6)
plt.title(u'网易云音乐用户男女比例', bbox={'facecolor':'0.8', 'pad':5})
plt.show()
