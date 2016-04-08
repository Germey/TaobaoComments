# -*- coding: utf-8 -*-
from selenium import webdriver
import config
from lib.getproxy import get_random_proxy


def new_driver():
    service_args = config.SERVICE_ARGS
    config.DRIVER = webdriver.PhantomJS(service_args=service_args)


def new_proxy_driver():
    service_args = config.SERVICE_ARGS
    proxy = get_random_proxy()
    service_args.append('--proxy=' + proxy)
    config.DRIVER = webdriver.PhantomJS(service_args=service_args)