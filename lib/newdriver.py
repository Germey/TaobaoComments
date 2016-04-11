# -*- coding: utf-8 -*-
from selenium import webdriver
import config
from lib.getproxy import get_random_proxy
import copy
import random

def new_driver():
    service_args = copy.copy(config.SERVICE_ARGS)
    config.DRIVER = webdriver.PhantomJS(service_args=service_args)


def new_proxy_driver():
    service_args = copy.copy(config.SERVICE_ARGS)
    proxy = get_random_proxy()
    num = random.randint(1,10)
    if num > 4:
        service_args.append('--proxy=' + proxy)
    print service_args
    config.DRIVER = webdriver.PhantomJS(service_args=service_args)