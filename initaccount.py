#!/usr/bin/env python
# encoding: utf-8

from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
from PIL import ImageChops,ImageDraw
import urllib2
import random
import os
from coolname import generate_slug
from mmap import mmap

def get_token(local_account, local_password):

    PROXY = "60.161.244.28:53281" # IP:PORT or HOST:PORT
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/lib/chromium-browser/chromedriver')

    #driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
    #firefox_capabilities = DesiredCapabilities.FIREFOX
    #firefox_capabilities['marionette'] = True
    #firefox_capabilities['binary'] = 'geckodriver'
    #driver = webdriver.Firefox(capabilities=firefox_capabilities)
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
    time.sleep(5)

    # 登录时候会出现滑动验证
    try:
        driver.find_element_by_xpath('//div[@class="slideFg"]')
        repassword = driver.find_elements_by_css_selector("input[type='password']")[0]
        if repassword:
            track_captcha(driver)
            login.click()
    except:
        print "no captcha"

    time.sleep(1)
    try:
        name = driver.find_elements_by_css_selector("input[type='text']")[1]
        random_name = generate_slug(2)
        name.send_keys(random_name)
    except IndexError:
        driver.quit()
        return 0

    time.sleep(2)

    track_captcha(driver)

    file = open('163.md', 'a')
    file.write('%s,%s' % (local_account, local_password))
    file.close()

    time.sleep(2)
    driver.implicitly_wait(2)
    driver.quit()


def track_captcha(driver):
    path = '1.JPG'
    check_loc = ''
    slider = driver.find_element_by_xpath('//div[@class="slideFg"]')

    while check_loc == '':
        check_loc = get_img(driver, path, slider)

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

    # 滑动
    track_slide(driver, locatex, slider)


def get_img(driver, path, slider):
    picurl = driver.find_element_by_xpath('//div[@class="puzzleBg"]/img').get_attribute('src')
    req = urllib2.Request(picurl)
    data = urllib2.urlopen(req, timeout=30).read()
    f = open(path, 'wb')
    f.write(data)
    f.close()

    check_loc = ''
    for each in os.walk('Pathed'):
        for afile in each[2]:
            similarrate = calc_similar_by_path('Pathed/'+afile, path)
            if similarrate > 0.65:
                print(afile)
                check_loc = 'Pathed/'+afile
                return check_loc
                break
    if check_loc == '':
        track_slide(driver, 100, slider)
        return ''


def track_slide(driver, locatex, slider):
    ActionChains(driver).click_and_hold(on_element=slider).perform()

    totalmove = (int((220.0 / 320.0) * locatex) - 7.5)

    now = 0
    while now < totalmove - 40:
        nmove = int(random.random()*20)
        if now+nmove>totalmove - 40:
            nmove = totalmove - now - 40
        hmove = int(random.uniform(-1, 1)*10)
        ActionChains(driver).move_by_offset(nmove,hmove).perform()
        time.sleep(int(random.random()*10)/1000)
        now+=nmove
    while now < totalmove:
        nmove = int(random.random()*3)
        if now+nmove>totalmove:
            nmove = totalmove - now
        hmove = int(random.uniform(-1, 1)*10)
        ActionChains(driver).move_by_offset(nmove,hmove).perform()
        time.sleep(int(random.random()*10)/50)
        now+=nmove

    time.sleep(0.5)
    ActionChains(driver).release(on_element=slider).perform()


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

def removeLine(filename, lineno):
    f=os.open(filename, os.O_RDWR)
    m=mmap(f,0)
    p=0
    for i in range(lineno-1):
        p=m.find('\n',p)+1
    q=m.find('\n',p)
    m[p:q] = ' '*(q-p)
    os.close(f)


if __name__ == "__main__":
    lineno = 0
    for line in open('account.txt'):
        lineno += 1
        if line:
            a = line.split(',')
            print a[0], a[1]
            get_token(a[0], a[1])
            removeLine('account.txt', lineno)
            time.sleep(10)
