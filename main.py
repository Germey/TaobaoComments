# -*- coding: utf-8 -*-

import time
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getrecommends import get_recommends

times = []
timeout = 20
url = "https://detail.tmall.com/item.htm?spm=a222t.7785392.113.19.rhnRn1&id=526449276263&acm=lb-zebra-20612-413860.1003.4.511128&scm=1003.4.lb-zebra-20612-413860.ITEM_526449276263_511128&sku_properties=5919063:6536025;12304035:116177"
service_args = [
    '--load-images=false',
    '--disk-cache=true',
]

driver = webdriver.Chrome()
response = driver.get(url)

try:
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "J_TabRecommends"))
    )

    result = get_recommends(driver, 10)
    print result

    html = driver.page_source
    print html


    doc = pq(html)
    lis = doc('#J_TjWaterfall > li')
    for li in lis.items():
        url = li.find('a').attr('href')
        ps = li.find('p').items()
        for p in ps:
            print p.text()
finally:
    driver.quit()
