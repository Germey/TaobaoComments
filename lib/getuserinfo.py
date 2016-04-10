# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from twisted.python.win32 import WindowsError
import config
import time
import socket
import urllib2
from urllib import quote

def get_user_info(user, fail_time=0):
    print u'找到用户',user ,u'的评论, 正在查询', user, '的星级'
    base_url = config.STAR_INFO_URL
    url = base_url + quote(user.encode('utf-8', 'ignore'))
    allow_star = range(1, config.MAX_STAR + 1)
    try:
        time.sleep(0.5)
        driver = config.DRIVER
        driver.get(url)
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "address"))
        )
        html = driver.page_source
        doc = pq(html)
        star = doc('div.tb_result.fl .infomation > ol > li:nth-child(4) a img')
        src =  star.attr('src')
        print src
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
    except (WindowsError, OSError, Exception):
        print u'用户星级不符合要求'
