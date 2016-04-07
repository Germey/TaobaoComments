# -*- coding: utf-8 -*-

from selenium import webdriver
from pyquery import PyQuery as pq


def get_product(url):

    service_args = [
        '--load-images=false',
        '--disk-cache=true',
    ]

    driver = webdriver.PhantomJS(service_args=service_args)
    driver.get(url)
    html = driver.page_source
    doc = pq(html)
    title = doc('title').text()
    return title