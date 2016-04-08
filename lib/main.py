# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

import config
from getrecommends import get_recommends
from parse import parse_content
from lib.geturls import get_urls


def scrap(url):
    timeout = config.TIMEOUT

    print u'正在请求', url, u',请稍后...'
    service_args = config.SERVICE_ARGS
    driver = webdriver.PhantomJS(service_args=service_args)
    try:
        driver.get(url)

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "J_TabRecommends"))
        )
        result = get_recommends(driver, config.MAX_TRY)
        if result:
            print u'查找成功'
            html = driver.page_source
            parse_content(html)
        else:
            print u'请求超时,获取失败'
            driver.quit()

    except TimeoutException:
        print u'请求超时, 继续重试'
        scrap(url)
    except Exception:
        print u'未知错误, 继续重试'
        scrap(url)

    finally:
        driver.quit()


def from_file():
    urls = get_urls()
    print u'获取到如下链接列表'
    print urls
    for url in urls:
        scrap(url)


def from_input():
    url = raw_input('请输入宝贝链接:')
    scrap(url)
