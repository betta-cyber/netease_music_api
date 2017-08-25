#!/usr/bin/env python
# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
from PIL import ImageChops,ImageDraw
import urllib2
import random
import os

local_account = 'at7400@163.com'
local_password = '5kz231'

def get_token():
    driver = webdriver.Chrome("./chromedriver")
    #driver = webdriver.Chrome(executable_path='/usr/bin/chromium-browser')
    driver.get('http://music.163.com/')

    time.sleep(1)

    driver.execute_script("top.login()")

    login_button = driver.find_element_by_xpath('//*[starts-with(@id, "auto-id-")]/div/div[2]/ul/li[4]/a')
    login_button.click()

    time.sleep(1)

    username = driver.find_elements_by_css_selector("input[type='text']")[1]
    password = driver.find_elements_by_css_selector("input[type='password']")[0]
    username.send_keys(local_account)
    password.send_keys(local_password)

    login = driver.find_element_by_xpath('//div[@class="f-mgt20"]/a')
    login.click()

    time.sleep(3)
    name = driver.find_elements_by_css_selector("input[type='text']")[1]
    name.send_keys("asdasfasglkafsnas")

    time.sleep(2)

    picurl = driver.find_element_by_xpath('//div[@class="puzzleBg"]/img').get_attribute('src')
    slider = driver.find_element_by_xpath('//div[@class="slideFg"]')
    req = urllib2.Request(picurl)
    data = urllib2.urlopen(req, timeout=30).read()
    path = '1.JPG'
    f = open(path, 'wb')
    f.write(data)
    f.close()

    check_loc = ''
    for each in os.walk('Pathed'):
        for afile in each[2]:
            similarrate = calc_similar_by_path('Pathed/'+afile, path)
            print similarrate
            if similarrate > 0.6:
                print(afile)
                check_loc = 'Pathed/'+afile
                break
    if check_loc == '':
        time.sleep(100)
        #driver.close()
        exit()
    img = ImageChops.difference(Image.open(path), Image.open(check_loc))
    pix = img.load()
    bk = 0
    print img.size[0], img.size[1]
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = pix[x, y]
            if r>50 and g>50 and b>50:
                print(pix[x,y])
                draw = ImageDraw.Draw(img)
                draw.line(((x,0), (x,img.size[1]-1)), fill=255)
                print(x,y)
                img.save("final.jpg")
                bk = 1
                locatex = x
                print locatex
                break
        if bk == 1:
            break

    ActionChains(driver).click_and_hold(on_element=slider).perform()

    #totalmove = int((334.0 / 389.0) * locatex) + 18
    totalmove = localex + 5
    print(totalmove)
    now = 0
    while now < totalmove - 40:
        nmove = int(random.random()*20)
        if now+nmove>totalmove - 40:
            nmove = totalmove - now - 40
        ActionChains(driver).move_by_offset(nmove,0).perform()
        time.sleep(int(random.random()*10)/100)
        now+=nmove
    while now < totalmove:
        nmove = int(random.random()*3)
        if now+nmove>totalmove:
            nmove = totalmove - now
        ActionChains(driver).move_by_offset(nmove,0).perform()
        time.sleep(int(random.random()*10)/100)
        now+=nmove
    ActionChains(driver).release(on_element=slider).perform()

    time.sleep(100)

    driver.implicitly_wait(2)

    driver.quit()

    return driver.find_element_by_xpath('/html/body/p').text

def make_regalur_image(img, size = (256, 256)):
    return img.resize(size).convert('RGB')

def split_image(img, part_size = (64, 64)):
    w, h = img.size
    pw, ph = part_size
    assert w % pw == h % ph == 0
    return [img.crop((i, j, i+pw, j+ph)).copy() \
                for i in xrange(0, w, pw) \
                for j in xrange(0, h, ph)]

def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def calc_similar(li, ri):
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0

def calc_similar_by_path(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    print li, ri
    return calc_similar(li, ri)


if __name__ == "__main__":
    get_token()
