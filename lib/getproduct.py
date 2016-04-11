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
from lib.newdriver import new_proxy_driver, new_driver
from proxy.getproxy import update_proxy_pool


def get_product(url, fail_time=0):
    try:
        time.sleep(1)
        driver = config.DRIVER
        driver.get(url)
        WebDriverWait(driver, config.TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "title"))
        )
        html = driver.page_source
        doc = pq(html)
        title = doc('title').text()
        return title
    except TimeoutException:
        if fail_time >=2 :
            print u'请求超时, 正在切换代理, 继续重试'
            update_proxy_pool()
            new_proxy_driver()
        else:
            print u'请求超时,正在切换会话重试'
            new_driver()
        fail_time = fail_time + 1
        if config.CONSOLE_OUTPUT:
            print u'当前失败次数', fail_time
        if fail_time == config.MAX_FAIL:
            update_proxy_pool()
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此请求'
            return False
        get_product(url, fail_time)
    except (socket.error, urllib2.URLError):
        print u'请求宝贝过于频繁, 请求被中断, 正在切换会话重试'
        new_driver()
        fail_time = fail_time + 1
        if config.CONSOLE_OUTPUT:
            print u'当前失败次数', fail_time
        if fail_time == config.MAX_FAIL:
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此请求'
            return False
        get_product(url, fail_time)
    except (WindowsError, OSError, Exception):
        print u'未知错误, 跳过继续运行'
