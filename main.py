# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getrecommends import get_recommends
from parse import parse_content
from geturls import get_urls

def scrap(url):
    timeout = 20

    print u'正在请求', url, u',请稍后...'
    service_args = [
        '--load-images=false',
        '--disk-cache=true',
    ]

    driver = webdriver.PhantomJS(service_args=service_args)
    driver.get(url)

    try:
        WebDriverWait(driver, timeout).until(
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

def main():
    urls = get_urls()
    print u'获取到如下链接列表'
    print urls
    for url in urls:
        scrap(url)


if __name__ == "__main__":
    main()


