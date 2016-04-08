# -*- coding:utf-8 -*-
from requests.exceptions import ConnectTimeout, ConnectionError

from selenium import webdriver
import requests
import re

service_args = [
    '--load-images=false',
    '--disk-cache=true',
]

url = 'http://www.66ip.cn/areaindex_1/1.html'

test_url = 'http://www.baidu.com'

validate_proxies = []

file = 'proxy.txt'


def get_html():
    driver = webdriver.PhantomJS(service_args=service_args)
    driver.get(url)
    html = driver.page_source
    return html


def get_proxy_list(html):
    proxies = []
    pattern = re.compile('<tr><td>(\d.*?)</td><td>(.*?)</td>.*?</tr>', re.S)
    results = re.findall(pattern, html)
    for result in results:
        proxies.append(result[0] + ':' + result[1])
    print proxies
    return proxies


def check_proxy(proxy):
    try:
        proxy = {
            'http': 'http://' + proxy
        }
        response = requests.get(test_url, proxies=proxy, timeout=10)
        if response:
            return True
        else:
            return False
    except ConnectTimeout:
        print u'超时,代理无效', proxy
        return False
    except ConnectionError:
        print u'超时,代理无效', proxy
        return False


def validate_proxy(proxies):
    clear_file()
    for proxy in proxies:
        print u'正在测试', proxy
        if check_proxy(proxy):
            print u'代理有效'
            validate_proxies.append(proxy)
            write_to_file(proxy)
        else:
            print u'代理无效'


def write_to_file(proxy):
    with open(file, 'a') as f:
        f.write(proxy + '\n')
        f.close()


def clear_file():
    with open(file, 'w') as f:
        f.write('')
        f.close()


if __name__ == '__main__':
    html = get_html()
    proxies = get_proxy_list(html)
    validate_proxy(proxies)
