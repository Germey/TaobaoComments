# -*- coding: utf-8 -*-
import socket
import urllib2
import config
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twisted.python.win32 import WindowsError
from getrecommends import get_recommends
from lib.filter import filter_comment
from lib.newdriver import new_driver, new_proxy_driver
from lib.writetofile import write_count, get_count
from parse import parse_content
from lib.geturls import get_urls
from proxy.getproxy import update_proxy_pool


def scrap(url, fail_time=0):
    timeout = config.TIMEOUT

    print u'正在请求', url, u', 请稍后...'

    try:
        driver = config.DRIVER
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
            print u'请求超时, 获取失败, 此页面不存在相应内容'
    except TimeoutException:
        if fail_time >=2 :
            print u'请求超时, 正在切换代理, 继续重试'
            update_proxy_pool()
            new_proxy_driver()
        else:
            print u'请求超时,正在切换会话重试'
            new_driver()
        fail_time = fail_time + 1
        if config.CONSOLE_OUTPUT:
            print u'当前页面请求失败数', fail_time
        if fail_time == config.MAX_FAIL:
            update_proxy_pool()
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此请求'
            return False
        scrap(url, fail_time)
    except (socket.error, urllib2.URLError):
        print u'请求页面过于频繁, 请求被中断, 正在切换会话重试'
        new_driver()
        fail_time = fail_time + 1
        if config.CONSOLE_OUTPUT:
            print u'当前页面请求失败数', fail_time
        if fail_time == config.MAX_FAIL:
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此请求'
            return False
        scrap(url, fail_time)
    except (WindowsError, OSError, Exception):
        print u'未知错误, 跳过继续运行'



def from_file():
    urls = get_urls()
    print u'获取到如下链接列表'
    print urls
    config.TOTAL_COUNT = len(urls)
    print u'共有', config.TOTAL_COUNT, u'个链接'
    count = int(get_count())
    print u'上次爬取到第', int(count) + 1, u'个链接, 继续爬取'
    print u'输入 1 继续爬取,输入 2 重新爬取:'
    num = raw_input()
    if num == '2':
        count = 0
        print u'开始重新爬取'
    if count < config.TOTAL_COUNT:
        for count in range(count, config.TOTAL_COUNT):
            write_count(count, config.COUNT_TXT)
            url = urls[count]
            print u'正在爬取第', count+1, u'个网页, 共', config.TOTAL_COUNT, u'个'
            config.NOW_COUNT = count
            scrap(url)
            count = count + 1
            print u'当前已完成采集', config.NOW_COUNT + 1, u'个, 共', config.TOTAL_COUNT, u'个'
        print u'采集结束,完成了', len(urls), u'个链接的采集'
    else:
        print u'链接上次已经全部爬取完毕'




def from_input():
    url = raw_input('请输入宝贝链接:')
    scrap(url)
    print u'采集结束'


def filter_result():
    print u'正在开始过滤，请确保已经将过滤的文本放置到', config.FILTER_FILE
    print u'过滤后的结果会保存在', config.FILTER_OUT_PUT
    url = raw_input(u'输入淘宝链接:\n')
    #url = 'https://detail.tmall.com/item.htm?id=43953033637'
    filter_comment(url)
    print u'过滤结束, 请查看', config.FILTER_OUT_PUT, u'文件，得到相应内容'