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
        time.sleep(0.5)
        driver = config.DRIVER
        driver.get(url)
        html = driver.page_source
        doc = pq(html)
        title = doc('title').text()
        return title
    except socket.error:
        print u'请求宝贝过于频繁, 请求被中断, 正在切换会话重试'
        config.DRIVER = webdriver.PhantomJS(service_args=config.SERVICE_ARGS)
        get_product(url)
    except urllib2.URLError:
        print u'请求宝贝过于频繁, 发生网络错误, 正在切换会话重试'
        config.DRIVER = webdriver.PhantomJS(service_args=config.SERVICE_ARGS)
        get_product(url)
    except WindowsError:
        print u'未知错误, 跳过继续运行'
    except OSError:
        print u'未知错误, 跳过继续运行'