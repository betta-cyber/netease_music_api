#!/usr/bin/env python
# encoding: utf-8

from selenium import webdriver

def get_token():
    driver = webdriver.PhantomJS('/Users/shokill/phantomjs') # or add to your PATH
    driver.set_window_size(1024, 768) # optional
    driver.get('http://127.0.0.1:8080/gettoken.html')


    submit_button = driver.find_element_by_xpath('//*[@id="submitForm"]/input[3]')
    submit_button.click()

    driver.implicitly_wait(2)

    return driver.find_element_by_xpath('/html/body/p').text
