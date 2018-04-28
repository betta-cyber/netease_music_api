#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: betta

'''
netease music api
'''

import re
import os
import json
import requests
from Crypto.Cipher import AES
from cookielib import LWPCookieJar
from bs4 import BeautifulSoup
import time
import hashlib
import base64
from gettoken import get_token
from storage import Storage


default_timeout = 10

# log = logger.getLogger(__name__)

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


# 歌曲加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic脚本实现
def encrypted_id(id):
    magic = bytearray('3go8&$8*3*3h0k(2)2')
    song_id = bytearray(id)
    magic_len = len(magic)
    for i in xrange(len(song_id)):
        song_id[i] = song_id[i] ^ magic[i % magic_len]
    m = hashlib.md5(song_id)
    result = m.digest().encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result


# 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
def encrypted_request(text):
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    return data

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(text.encode('hex'), 16),  int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)

def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


# list去重
def uniq(arr):
    arr2 = list(set(arr))
    arr2.sort(key=arr.index)
    return arr2


# 获取高音质mp3 url
# def geturl(song):
#     config = Config()
#     quality = Config().get_item("music_quality")
#     if song['hMusic'] and quality <= 0:
#         music = song['hMusic']
#         quality = 'HD'
#     elif song['mMusic'] and quality <= 1:
#         music = song['mMusic']
#         quality = 'MD'
#     elif song['lMusic'] and quality <= 2:
#         music = song['lMusic']
#         quality = 'LD'
#     else:
#         return song['mp3Url'], ''
#
#
#     quality = quality + ' {0}k'.format(music['bitrate'] / 1000)
#     song_id = str(music['dfsId'])
#     enc_id = encrypted_id(song_id)
#     url = "http://m%s.music.126.net/%s/%s.mp3" % (random.randrange(1, 3), enc_id, song_id)
#     return url, quality


class NetEase:
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        self.cookies = {
            'appver': '1.5.2'
        }
        self.playlist_class_dict = {}
        self.session = requests.Session()
        self.storage = Storage()
        self.session.cookies = LWPCookieJar(self.storage.cookie_path)
        try:
            self.session.cookies.load()
            self.file = file(self.storage.cookie_path, 'r')
            cookie = self.file.read()
            self.file.close()
            pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
            str = pattern.findall(cookie)
            if str:
                if str[0] < time.strftime('%Y-%m-%d', time.localtime(time.time())):
                    self.storage.database['user'] = {
                        "username": "",
                        "password": "",
                        "user_id": "",
                        "nickname": "",
                    }
                    self.storage.save()
                    os.remove(self.storage.cookie_path)
        except:
            self.session.cookies.save()

    def return_toplists(self):
        temp = []
        for i in range(len(top_list_all)):
            temp.append(top_list_all[i][0])
        return temp

    def httpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):
        connection = json.loads(self.rawHttpRequest(method, action, query, urlencoded, callback, timeout))
        return connection

    def rawHttpRequest(self, method, action, query=None, urlencoded=None, callback=None, timeout=None):
        if (method == 'GET'):
            url = action if (query == None) else (action + '?' + query)
            connection = self.session.get(url, headers=self.header, timeout=default_timeout)

        elif (method == 'POST'):
            connection = self.session.post(
                    action,
                    data=query,
                    headers=self.header,
                    timeout=default_timeout
            )

        elif (method == 'Login_POST'):
            connection = self.session.post(
                    action,
                    data=query,
                    headers=self.header,
                    timeout=default_timeout
            )
            self.session.cookies.save()

        connection.encoding = "UTF-8"
        return connection.text

    # 登录
    def login(self, username, password):
        pattern = re.compile(r'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$')
        if (pattern.match(username)):
            return self.phone_login(username, password)
        clientToken = get_token()
        print clientToken
        action = 'http://music.163.com/weapi/login'
        text = {
            'username': username,
            'password': password,
            'rememberLogin': 'true',
            'clientToken': clientToken
        }
        data = encrypted_request(text)
        print data
        try:
            return self.httpRequest('Login_POST', action, data)
        except:
            return {'code': 501}

    # 手机登录
    def phone_login(self, username, password):
        action = 'https://music.163.com/weapi/login/cellphone'
        text = {
            'phone': username,
            'password': password,
            'rememberLogin': 'true'
        }
        data = encrypted_request(text)
        try:
            return self.httpRequest('Login_POST', action, data)
        except:
            return {'code': 501}

    # 每日签到
    def daily_signin(self, type):
        action = 'http://music.163.com/weapi/point/dailyTask'
        text = {
            'type': type
        }
        data = encrypted_request(text)
        try:
            return self.httpRequest('POST', action, data)
        except:
            return -1

    # 用户歌单
    def user_playlist(self, uid, offset=0, limit=100):
        action = 'http://music.163.com/api/user/playlist/?offset=' + str(offset) + '&limit=' + str(
                limit) + '&uid=' + str(uid)
        try:
            data = self.httpRequest('GET', action)
            return data['playlist']
        except:
            return -1


    # 每日推荐歌单
    def recommend_playlist(self):
        try:
            action = 'http://music.163.com/weapi/v1/discovery/recommend/songs?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "offset": 0,
                "total": True,
                "limit": 20,
                "csrf_token": csrf
            }
            #print(encrypted_request(req))
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)["recommend"]
            song_ids = []
            for result in results:
                song_ids.append(result["id"])
            data = map(self.song_detail, song_ids)
            result = []
            for foo in range(len(data)):
                result.append(data[foo][0])
            return result
        except:
            return False

    def follow(self, userId):
        try:
            action = 'http://music.163.com/weapi/user/follow/30395352?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "userId": userId,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            print(page.text)
            results = json.loads(page.text)
            if results["code"] == 200:
                return True
            elif results["code"] == 201:
                return "已经关注"
        except:
            return False

    def record(self, uid):
        try:
            action = 'http://music.163.com/weapi/v1/play/record?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "offset": 0,
                "total": True,
                "limit": 100,
                "type": 1,
                "uid": uid,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            print(page.text)
            results = json.loads(page.text)
            if results["code"] == 200:
                return True
            elif results["code"] == 201:
                return "11"
        except:
            return False

    def sendmail(self, userIds, msg):
        try:
            action = 'http://music.163.com/weapi/msg/private/send?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "type": "text",
                "msg": msg,
                "userIds": userIds,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            print results
            # if results["code"] == 200:
            #     return "发送成功"
        except:
            return False

    def initProfile(self, nickname, captchaId, captcha):
        try:
            action = 'http://music.163.com/weapi/activate/initProfile?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "nickname": nickname,
                "captchaId": captchaId,
                "captcha": captcha,
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            print(page.text)
            results = json.loads(page.text)
            if results["code"] == 200:
                return True
            elif results["code"] == 201:
                return ""
        except:
            return False


    # /**
    # 收藏歌单
    # **/
    def add_playlist(self, playlist_id):
        try:
            action = 'http://music.163.com/weapi/playlist/subscribe/?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "id": playlist_id,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            print(page.text)
            results = json.loads(page.text)
            if results["code"] == 200:
                s = '已收藏 {id} 号歌单.'
                return s.format(id = playlist_id)
            elif results["code"] == 501:
                return "已经收藏过了"
        except:
            return False

    # 点赞
    #def like(self, eid, origin, threadId):
    #    try:
    #        action = 'http://music.163.com/api/v1/comment/like/?csrf_token='
    #        self.session.cookies.load()
    #        csrf = ""
    #        for cookie in self.session.cookies:
    #            if cookie.name == "__csrf":
    #                csrf = cookie.value
    #        if csrf == "":
    #            return False
    #        action += csrf
    #        req = {
    #            "eid": eid,
    #            "origin": origin,
    #            "threadId": threadId,
    #            "csrf_token": csrf
    #        }
    #        page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
    #        print(page.text)
    #        results = json.loads(page.text)
    #        if results["code"] == 200:
    #            return True
    #        elif results["code"] == 501:
    #            return "已经点过赞了"
    #    except:
    #        return False

    def like(self, commentId, threadId):
        try:
            action = 'http://music.163.com/weapi/v1/comment/like/?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "commentId": commentId,
                "threadId": threadId,
                "like": "true",
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            print(page.text)
            results = json.loads(page.text)
            if results["code"] == 200:
                return True
            elif results["code"] == 501:
                return "已经点过赞了"
        except:
            return False


    # 私人FM
    def personal_fm(self):
        action = 'http://music.163.com/api/radio/get'
        try:
            data = self.httpRequest('GET', action)
            return data['data']
        except:
            return -1

    # like
    def fm_like(self, songid, like=True, time=25, alg='itembased'):
        if like:
            action = 'http://music.163.com/api/radio/like?alg=' + alg + '&trackId=' + str(
                    songid) + '&like=true&time=' + str(time)
        else:
            action = 'http://music.163.com/api/radio/like?alg=' + alg + '&trackId=' + str(
                    songid) + '&like=false&time=' + str(time)
        try:
            data = self.httpRequest('GET', action)
            if data['code'] == 200:
                return data
            else:
                return -1
        except:
            return -1

    # FM trash
    def fm_trash(self, songid, time=25, alg='RT'):
        action = 'http://music.163.com/api/radio/trash/add?alg=' + alg + '&songId=' + str(songid) + '&time=' + str(time)
        try:
            data = self.httpRequest('GET', action)
            if data['code'] == 200:
                return data
            else:
                return -1
        except:
            return -1

    # 搜索单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002) *(type)*
    def search(self, s, stype=1, offset=0, total='true', limit=60):
        action = 'http://music.163.com/api/search/get'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        return self.httpRequest('POST', action, data)

    # 新碟上架 http://music.163.com/#/discover/album/
    def new_albums(self, offset=0, limit=50):
        action = 'http://music.163.com/api/album/new?area=ALL&offset=' + str(offset) + '&total=true&limit=' + str(limit)
        try:
            data = self.httpRequest('GET', action)
            return data['albums']
        except:
            return []

    # 歌单（网友精选碟） hot||new http://music.163.com/#/discover/playlist/
    def top_playlists(self, category='全部', order='hot', offset=0, limit=50):
        action = 'http://music.163.com/api/playlist/list?cat=' + category + '&order=' + order + '&offset=' + str(
                offset) + '&total=' + ('true' if offset else 'false') + '&limit=' + str(limit)
        try:
            data = self.httpRequest('GET', action)
            return data['playlists']
        except:
            return []

    # 分类歌单
    def playlist_classes(self):
        action = 'http://music.163.com/discover/playlist/'
        try:
            data = self.rawHttpRequest('GET', action)
            return data
        except:
            return []

    # 分类歌单中某一个分类的详情
    def playlist_class_detail(self):
        pass

    # 歌单详情
    def playlist_detail(self, playlist_id):
        action = 'http://music.163.com/api/playlist/detail?id=' + str(playlist_id)
        try:
            data = self.httpRequest('GET', action)
            return data['result']['tracks']
        except:
            return []

    # 热门歌手 http://music.163.com/#/discover/artist/
    def top_artists(self, offset=0, limit=100):
        action = 'http://music.163.com/api/artist/top?offset=' + str(offset) + '&total=false&limit=' + str(limit)
        try:
            data = self.httpRequest('GET', action)
            return data['artists']
        except:
            return []

    # 热门单曲 http://music.163.com/discover/toplist?id=
    def top_songlist(self, idx=0, offset=0, limit=100):
        action = 'http://music.163.com' + top_list_all[idx][1]
        try:
            connection = requests.get(action, headers=self.header, timeout=default_timeout)
            connection.encoding = 'UTF-8'
            songids = re.findall(r'/song\?id=(\d+)', connection.text)
            if songids == []:
                return []
            # 去重
            songids = uniq(songids)
            return self.songs_detail(songids)
        except:
            return []

    # 歌手信息
    def artist(self, artist_id):
        # action = 'http://music.163.com/weapi/artist/introduction?csrf_token='
        try:
            action = 'http://music.163.com/weapi/v1/artist/%s?csrf_token=' % (artist_id)
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "id": artist_id,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            if results["code"] == 200:
                return results
        except:
            return []

    def artist_album(self, artist_id):
        try:
            action = 'http://music.163.com/weapi/artist/albums/%s?csrf_token=' % (artist_id)
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "offset": 0,
                "total": True,
                "limit": 100,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            return results
        except:
            return []

    def album(self, album_id):
        try:
            action = 'http://music.163.com/weapi/v1/album/%s?csrf_token=' % (album_id)
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            if results["code"] == 200:
                return results
        except:
            return []


    # song ids --> song urls ( details )
    def songs_detail(self, ids, offset=0):
        tmpids = ids[offset:]
        tmpids = tmpids[0:100]
        tmpids = map(str, tmpids)
        action = 'http://music.163.com/api/song/detail?ids=[' + (',').join(tmpids) + ']'
        try:
            data = self.httpRequest('GET', action)

            # the order of data['songs'] is no longer the same as tmpids, so just make the order back
            data["songs"].sort(key=lambda song: tmpids.index(str(song["id"])))

            return data['songs']
        except:
            return []

    # song id --> song url ( details )
    def song_info(self, music_id):
        action = "http://music.163.com/api/song/detail/?id=" + str(music_id) + "&ids=[" + str(music_id) + "]"
        print action
        try:
            data = self.httpRequest('GET', action)
            print data
            return data['songs']
        except:
            return []

    def song_detail(self, music_id):
        try:
            action = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "ids": music_id,
                "br": 999999,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            print results
            if results["code"] == 200:
                return results
        except:
            return 0


    # lyric http://music.163.com/api/song/lyric?os=osx&id= &lv=-1&kv=-1&tv=-1
    def song_lyric(self, music_id):
        action = "http://music.163.com/api/song/lyric?os=osx&id=" + str(music_id) + "&lv=-1&kv=-1&tv=-1"
        try:
            data = self.httpRequest('GET', action)
            if data['lrc']['lyric'] != None:
                lyric_info = data['lrc']['lyric']
            else:
                lyric_info = '未找到歌词'
            return lyric_info
        except:
            return []

    def song_tlyric(self, music_id):
        action = "http://music.163.com/api/song/lyric?os=osx&id=" + str(music_id) + "&lv=-1&kv=-1&tv=-1"
        try:
            data = self.httpRequest('GET', action)
            if data['tlyric']['lyric'] != None:
                lyric_info = data['tlyric']['lyric'][1:]
            else:
                lyric_info = '未找到歌词翻译'
            return lyric_info
        except:
            return []

    # 今日最热（0）, 本周最热（10），历史最热（20），最新节目（30）
    def djchannels(self, stype=0, offset=0, limit=50):
        action = 'http://music.163.com/discover/djchannel?type=' + str(stype) + '&offset=' + str(
                offset) + '&limit=' + str(limit)
        try:
            connection = requests.get(action, headers=self.header, timeout=default_timeout)
            connection.encoding = 'UTF-8'
            channelids = re.findall(r'/dj\?id=(\d+)', connection.text)
            channelids = uniq(channelids)
            return self.channel_detail(channelids)
        except:
            return []

    # DJchannel ( id, channel_name ) ids --> song urls ( details )
    # 将 channels 整理为 songs 类型
    def channel_detail(self, channelids, offset=0):
        channels = []
        for i in range(0, len(channelids)):
            action = 'http://music.163.com/api/dj/program/detail?id=' + str(channelids[i])
            try:
                data = self.httpRequest('GET', action)
                channel = self.dig_info(data['program']['mainSong'], 'channels')
                channels.append(channel)
            except:
                continue

        return channels

    # 获取版本
    def get_version(self):
        action = 'https://pypi.python.org/pypi?:action=doap&name=NetEase-MusicBox'
        try:
            data = requests.get(action)
            return data.content
        except:
            return []

    def dig_info(self, data, dig_type):
        temp = []
        if dig_type == 'songs' or dig_type == 'fmsongs':
            for i in range(0, len(data)):
                url, quality = geturl(data[i])

                if data[i]['album'] != None:
                    album_name = data[i]['album']['name']
                else:
                    album_name = '未知专辑'

                song_info = {
                    'song_id': data[i]['id'],
                    'artist': [],
                    'song_name': data[i]['name'],
                    'album_name': album_name,
                    'mp3_url': url,
                    'quality': quality
                }
                if 'artist' in data[i]:
                    song_info['artist'] = data[i]['artist']
                elif 'artists' in data[i]:
                    for j in range(0, len(data[i]['artists'])):
                        song_info['artist'].append(data[i]['artists'][j]['name'])
                    song_info['artist'] = ', '.join(song_info['artist'])
                else:
                    song_info['artist'] = '未知艺术家'

                temp.append(song_info)

        elif dig_type == 'artists':
            temp = []
            for i in range(0, len(data)):
                artists_info = {
                    'artist_id': data[i]['id'],
                    'artists_name': data[i]['name'],
                    'alias': ''.join(data[i]['alias'])
                }
                temp.append(artists_info)

            return temp

        elif dig_type == 'albums':
            for i in range(0, len(data)):
                albums_info = {
                    'album_id': data[i]['id'],
                    'albums_name': data[i]['name'],
                    'artists_name': data[i]['artist']['name']
                }
                temp.append(albums_info)

        elif dig_type == 'top_playlists':
            for i in range(0, len(data)):
                playlists_info = {
                    'playlist_id': data[i]['id'],
                    'playlists_name': data[i]['name'],
                    'creator_name': data[i]['creator']['nickname']
                }
                temp.append(playlists_info)


        elif dig_type == 'channels':
            url, quality = geturl(data)
            channel_info = {
                'song_id': data['id'],
                'song_name': data['name'],
                'artist': data['artists'][0]['name'],
                'album_name': 'DJ节目',
                'mp3_url': url,
                'quality': quality
            }
            temp = channel_info

        elif dig_type == 'playlist_classes':
            soup = BeautifulSoup(data)
            dls = soup.select('dl.f-cb')
            for dl in dls:
                title = dl.dt.text
                sub = [item.text for item in dl.select('a')]
                temp.append(title)
                self.playlist_class_dict[title] = sub

        elif dig_type == 'playlist_class_detail':
            log.debug(data)
            temp = self.playlist_class_dict[data]

        return temp


    def track_playlist_add(self, pid, trackIds):
        try:
            action = 'http://music.163.com/weapi/playlist/manipulate/tracks?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "op": "add",
                "pid": pid,
                "trackIds": trackIds,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            return results
        except:
            results = {}
            results['code'] = 100
            return results


    # 播放音乐
    def track_log(self, song_id, play_time):
        try:
            action = 'http://music.163.com/weapi/feedback/weblog?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "logs": '[{"action": "play","json":{"type": "song","wifi": 0,"download": 0,"id": %s,"time": %s,"end": "ui"}}]' % (song_id, play_time),
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            return results
        except:
            return {}


    def create_new_songlist(self, name):
        try:
            action = 'http://music.163.com/weapi/playlist/create?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "name": name,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            return results
        except:
            return {}


    def send_song_list_mail(self, songlist_id, msg, userIds):
        try:
            action = 'http://music.163.com/weapi/msg/private/send?csrf_token='
            self.session.cookies.load()
            csrf = ""
            for cookie in self.session.cookies:
                if cookie.name == "__csrf":
                    csrf = cookie.value
            if csrf == "":
                return False
            action += csrf
            req = {
                "id": songlist_id,
                "type": "playlist",
                "msg": msg,
                "userIds": userIds,
                "csrf_token": csrf
            }
            page = self.session.post(action, data=encrypted_request(req), headers=self.header, timeout=default_timeout)
            results = json.loads(page.text)
            return results
        except:
            return {}
