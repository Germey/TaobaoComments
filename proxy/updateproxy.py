# -*- coding:utf-8 -*-
from requests.exceptions import ConnectTimeout, ConnectionError, ChunkedEncodingError, ReadTimeout
from selenium import webdriver
import requests
import re
import threading
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.writetofile import write_to_txt
from copy import copy
from multiprocessing import Pool
from pyquery import PyQuery as pq

service_args = [
    '--load-images=false',
    '--disk-cache=true',
]

base_url = 'http://www.66ip.cn/areaindex_1/'

page_max = 15

test_url = 'http://www.baidu.com'

validate_proxies = []

file = 'proxy/proxy.txt'

driver = webdriver.PhantomJS(service_args=service_args)


def get_html(url):
    try:
        driver = webdriver.PhantomJS(service_args=service_args)
        driver.get(url)
        html = driver.page_source
        return html
    except (TimeoutException, OSError):
        print u'出现请求错误,跳过此链接'


def get_proxy_list(html):
    proxies = []
    pattern = re.compile('<tr><td>(\d.*?)</td><td>(.*?)</td>.*?</tr>', re.S)
    results = re.findall(pattern, html)
    for result in results:
        proxies.append(result[0] + ':' + result[1])
    print proxies
    return proxies


def test_proxy(proxy):
    try:
        service_args = [
            '--load-images=false',
            '--disk-cache=true',
            # '--proxy=120.76.142.46:16816',
            # '--proxy-auth=1016903103:9p69q4g8',
        ]
        service_args.append('--proxy=' + proxy)
        print service_args
        driver = webdriver.PhantomJS(service_args=service_args)
        driver.get(test_url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "title"))
        )
        html = driver.page_source
        driver.quit()
        doc = pq(html)
        title = doc('title').text()
        print title
        return True
    except (TimeoutException, ConnectTimeout):
        return False
    except (ConnectionError, ChunkedEncodingError, ReadTimeout, Exception):
        return False


def check_proxy(proxy):
    print u'正在检查代理', proxy
    if test_proxy(proxy):
        print u'代理有效', proxy
        validate_proxies.append(proxy)
        write_to_txt(proxy, file, proxy)
    else:
        print u'代理无效', proxy


def validate_proxy(proxies):
    threads = []
    # for proxy in proxies:
    #     check_proxy(proxy)
    pool = Pool(4)
    pool.map(check_proxy, proxies)

    '''
    for proxy in proxies:
        threads.append(threading.Thread(target=check_proxy, args=(proxy,)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    '''


def clear_file():
    with open(file, 'w') as f:
        f.write('')
        f.close()
        print u'已成功清理代理文本'


def update_proxy():
    clear_file()
    for page in range(1, page_max + 1):
        url = base_url + str(page) + '.html'
        print u'当前正在抓取第', page, '页代理', url
        html = get_html(url)
        proxies = get_proxy_list(html)
        validate_proxy(proxies)
        print u'当前已完成比例', page * 100 / page_max, u'%, 请稍后'
