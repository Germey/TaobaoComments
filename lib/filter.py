# -*- coding: utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import time
from pyquery import PyQuery as pq
import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lib.getdays import get_days
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

filter_res = set([])

config.NEXT_END = 0
config.END_COUNT = 0


def filter_comment(url):
    timeout = config.TIMEOUT
    driver = config.DRIVER
    driver.get(url)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "J_TabBarBox"))
    )
    result = get_comments(driver, config.MAX_TRY)

    if result:
        driver.get_screenshot_as_file('a.png')
        print u'网页加载成功，正在切换至评论页面'
        js ='''
        comment_btn = document.querySelectorAll('#J_TabBar li a')[1]
        comment_btn.click()
        '''
        driver.execute_script(js)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "col-author"))
        )
        print u'已经找到评论，开始分析第一页评论'
        html = driver.page_source

        parse_comments(html)

        # next_btn = driver.find_element_by_xpath('//*[@id="J_Reviews"]//div[@class="rate-paginator"]/')
        # next_btn.click()
        # next_btn= driver.find_element_by_css_selector('#J_Reviews .rate-paginator a:last-child')
        # print next_btn
        # next_btn.click()
        count = 0
        while not config.NEXT_END:
            print u'正在分析后续评论'
            try:
                js = '''
                page = document.querySelectorAll('.rate-paginator a');
                length = page.length;
                a = page[length-1];
                a.click();
                '''
                driver.execute_script(js)
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "col-author"))
                )
                html = driver.page_source
                parse_comments(html)
                count += 1
                print u'已经翻页', count, u'次'
                time.sleep(1)
            except UnicodeDecodeError:
                print  u'匹配结果错误，跳过此匹配'
        print u'匹配结果，最后获取到如下匿名用户', filter_res
        print u'正在写入文件....'
        write_to_file(filter_res)
        print u'写入文件结束，请查看', config.FILTER_OUT_PUT, u'文件的内容，即为匹配完成的内容'
        driver.close()
    else:
        print u'请求超时, 获取失败, 此页面不存在相应内容'


def get_comments(driver, max_time=15):
    print u'正在等待网页加载....'
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
    dates = get_days(config.MAX_DAY)
    for li in lis.items():
        date = li.find('.tm-rate-date').text()
        if date in dates or date == u'今天':
            user = li.find('.rate-user-info').text()
            user = user.replace(' ', '')
            if len(user) > 5:
                user = user[0:5]
            find_file(user)
        else:
            print u'出现不匹配，当前评论日期为', date
            config.END_COUNT += 1
            print u'当前日期不匹配次数为', config.END_COUNT
            if config.END_COUNT > config.END_MAX:
                config.NEXT_END = 1


def find_file(user):
    with open(config.FILTER_FILE, 'r') as f:
        content = f.read()
        contents = content.split('\n')

        for info in contents:
            infos = info.split(' ')
            if len(infos) == 2:
                user_info = infos[0]
                if user.decode('utf-8', 'ignore') == user_info.decode('utf-8', 'ignore'):
                    if not user in filter_res:
                        print u'已经匹配到', user, '的评论'
                    filter_res.add(user)

def find_id(user):
    with open(config.FILTER_FILE, 'r') as f:
        content = f.read()
        contents = content.split('\n')

        for info in contents:
            infos = info.split(' ')
            if len(infos) == 2:
                user_info = infos[0]
                user_id = infos[1]
                if user.decode('utf-8', 'ignore') == user_info.decode('utf-8', 'ignore'):
                    return user_id


def write_to_file(users):
    with open(config.FILTER_OUT_PUT, 'a') as f:
        for user in users:
            id = find_id(user)
            f.write(user + ' ' + id)
            f.write('\n')
    f.close()

