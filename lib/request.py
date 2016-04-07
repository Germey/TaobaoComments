# -*- coding: utf-8 -*-
from selenium import webdriver
from pyquery import PyQuery as pq

import config

url = 'https://detail.tmall.com/item.htm?id=524579313746&pvid=6b384b7e-69b7-4aec-aa3a-2188470fe575&abbucket=_AB-M67_B13&acm=03067.1003.1.668656&aldid=vxfqpU0p&abtest=_AB-LR67-PR67&scm=1007.12776.28398.100200300000000&pos=1'

service_args = config.SERVICE_ARGS

driver = webdriver.PhantomJS(service_args=service_args)
driver.get(url)
html = driver.page_source
doc = pq(html)
title = doc('title').text()
