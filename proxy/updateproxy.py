# -*- coding:utf-8 -*-
from requests.exceptions import ConnectTimeout, ConnectionError, ChunkedEncodingError, ReadTimeout
from selenium import webdriver
import requests
import re
import threading
from selenium.common.exceptions import TimeoutException
from lib.writetofile import write_to_txt

service_args = [
    '--load-images=false',
    '--disk-cache=true',
]

base_url = 'http://www.66ip.cn/areaindex_1/'

page_max = 15

test_url = 'http://www.baidu.com'

validate_proxies = []

file = 'proxy/proxy.txt'


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
        proxies = {
            'http': 'http://' + proxy
        }
        response = requests.get(test_url, proxies=proxies, timeout=10)
        if response:
            return True
        else:
            return False
    except ConnectTimeout:
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
    for proxy in proxies:
        threads.append(threading.Thread(target=check_proxy, args=(proxy,)))
    for t in threads:
        t.setDaemon(True)
        t.start()


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
