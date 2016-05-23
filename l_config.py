#-*- coding: utf-8 -*-

from selenium import webdriver

__author__ = 'CQC'
LINK = 'https://www.tmall.com/?spm=a220m.1000858.a2226n0.1.kM59nz'

# 加载配置
SERVICE_ARGS = [
    '--load-images=false',
]

TIMEOUT = 30

DRIVER = webdriver.PhantomJS(service_args=SERVICE_ARGS)

#DRIVER = webdriver.Chrome()

FILE = 'file/url.txt'
