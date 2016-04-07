# -*- coding: utf-8 -*-
from selenium import webdriver
from pyquery import PyQuery as pq
import config


def get_product(url):

    try:
        service_args = config.SERVICE_ARGS

        driver = webdriver.PhantomJS(service_args=service_args)
        driver.get(url)
        html = driver.page_source
        doc = pq(html)
        title = doc('title').text()
        return title
    except Exception, e:
        print u'获取宝贝名称失败', e.message