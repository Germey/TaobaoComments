# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getrecommends import get_recommends
from parse import parse_content

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
    if result:
        print u'查找成功'
        html = driver.page_source
        parse_content(html)
    else:
        print u'请求超时,获取失败'
        driver.quit()



finally:
    driver.quit()
