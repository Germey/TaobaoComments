# -*- coding: utf-8 -*-
from selenium import webdriver
from pyquery import PyQuery as pq
from twisted.python.win32 import WindowsError
import config
import time
import socket
import urllib2

def get_product(url):

    try:
        time.sleep(1)
        driver = config.DRIVER
        driver.get(url)
        html = driver.page_source
        doc = pq(html)
        title = doc('title').text()
        return title
    except socket.error:
        print u'获取宝贝名称失败, 请求过于频繁, 正在重试'
        time.sleep(5)
        get_product(url)
    except urllib2.URLError:
        print u'请求过于频繁，正在切换会话重试'
        config.DRIVER = webdriver.PhantomJS(service_args=config.SERVICE_ARGS)
        get_product(url)
    except WindowsError:
        print u'未知错误, 跳过继续运行'
    except OSError:
        print u'未知错误, 跳过继续运行'