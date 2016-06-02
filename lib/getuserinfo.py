# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from twisted.python.win32 import WindowsError
import config
import time
import socket
import re
import urllib2
from urllib import quote
from lib.newdriver import new_driver, new_proxy_driver
from proxy.getproxy import update_proxy_pool


def get_user_info(user, fail_time=0):
    print u'找到用户',user ,u'的评论, 正在查询', user, u'的星级'
    base_url = config.STAR_INFO_URL
    url = base_url #+ quote(user.encode('utf-8', 'ignore'))
    allow_star = range(1, config.MAX_STAR + 1)
    try:
        time.sleep(1)
        driver = config.DRIVER
        driver.get(url)
        element = driver.find_element_by_id('txt_name')
        element.send_keys(user, Keys.ENTER)
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "buyer_ratecount"))
        )

        html = driver.page_source
        #time.sleep(1)
        pattern = re.compile('<span id="buyer_ratecount.*?src="(.*?)gif', re.S)
        result = re.search(pattern, html)
        print result.group(0)
        src = result.group(0)
        #driver.get('http://www.baidu.com')
        for allow in allow_star:
            if 'b_red_'+ str(allow) in src:
                print u'该用户', user, u'星级符合要求'
                return True
        print u'该用户', user, u'星级不符合要求'
        return False
    except TimeoutException:
        print u'查询失败, 正在重试'
        fail_time = fail_time + 1
        if fail_time == 3:
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此用户'
            return False
        return get_user_info(user, fail_time)
    except (socket.error, urllib2.URLError):
        print u'查询失败, 跳过该用户'
        return False
    except NoSuchElementException:
        print u'查询星级失败, 正在重试'
        if fail_time >=2 :
            print u'请求超时, 正在切换代理, 继续重试'
            print u'请打开 http://www.taonienie.com/ 输入验证码,即可迅速解决问题'
        else:
            print u'请求超时,正在切换会话重试'
            new_driver()
        time.sleep(1)
        fail_time = fail_time + 1
        if fail_time == 5:
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此用户'
                print u'请打开 http://www.taonienie.com/ 输入验证码,即可迅速解决问题'

            return False
        return get_user_info(user, fail_time)