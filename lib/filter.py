# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import time
from pyquery import PyQuery as pq
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def filter_comment(url):
    timeout = config.TIMEOUT

    driver = config.C_DRIVER
    driver.get(url)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "J_TabBarBox"))
    )
    result = get_comments(driver, config.MAX_TRY)


    if result:
        print u'查找成功'
        comment_btn = driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a')
        print comment_btn
        comment_btn.click()
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "col-author"))
        )
        print u'已经找到评论'
        html = driver.page_source
        print html
        parse_comments(html)
    else:
        print u'请求超时, 获取失败, 此页面不存在相应内容'



def get_comments(driver, max_time = 10):
    count = 1
    result = try_get(driver)
    while not result:
        result = try_get(driver)
        count = count + 1
        if count == max_time:
            return False
    return True



def try_get(driver):
    js = "window.scrollTo(0,document.body.scrollHeight)"
    driver.execute_script(js)
    time.sleep(2)
    try:
        driver.find_element_by_id('J_TabBar')
    except NoSuchElementException:
        return False
    return True


def parse_comments(html):
    doc = pq(html)
    lis = doc('.rate-grid tr')
    for li in lis.items():
        print li
        date = li.find('.tm-rate-date').text()
        print date
        user = li.find('.rate-user-info').text()
        print user
