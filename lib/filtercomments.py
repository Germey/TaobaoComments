# -*- coding:utf-8 -*-
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import xlrd
import xlwt
# import c_config
import c_config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from xlutils.copy import copy
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def read_from_excel():
    workbook = xlrd.open_workbook(c_config.TO_EXCEL_FILE)
    sheet = workbook.sheet_by_index(0)
    row_num = sheet.nrows

    for i in range(0, row_num):
        info = sheet.row_values(i)
        if len(info) > 4:
            if info[0]:
                url = info[2]
                filter_comment_info(url, info)
                break




def filter_comment_info(url, info):
    driver = c_config.C_DRIVER
    timeout = c_config.TIMEOUT
    success_users = set([])
    print u'正在匹配评论', url
    c_config.NEXT_PAGE_COMMENTS = 1
    driver.get(url)
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "J_TabBar"))
        )
    except TimeoutException:
        print u'请求匹配评论页面超时'
    if is_comments_appear(driver):
        print u'已成功加载出评论页面'
        c_config.WRONG_DATE_COUNT = 0
        js = '''
        comment_btn = document.querySelectorAll('#J_TabBar li a')[1]
        comment_btn.click()
        '''
        try:
            driver.execute_script(js)
        except WebDriverException:
            print u'点击获取评论按钮失败'
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "col-author"))
            )
        except TimeoutException:
            print u'请求匹配评论页面超时'
        html = driver.page_source

        print html
        return
        comments = parse_comments(html)

        comment = filter_comments(comments, info[0], info[1])

    page_count = 1
    while c_config.NEXT_PAGE_COMMENTS:
        print u'正在分析后续评论'
        try:
            js = '''
            page = document.querySelectorAll('.rate-paginator a');
            length = page.length;
            a = page[length-1];
            a.click();
            '''
            # next = driver.find_element_by_css_selector('.rate-paginator a:contains("下一页>>")')
            # next.click()
            try:
                driver.execute_script(js)
            except WebDriverException:
                print u'评论数目少，无需翻页'
                break
            try:
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "col-author"))
                )
            except TimeoutException:
                print u'请求匹配评论页面超时'
            driver.implicitly_wait(c_config.NEXT_PAGE_WAIT)
            html = driver.page_source
            comments = parse_comments(html)
            for target in targets:
                target_user = target[0]
                target_content = target[1]
                comment = filter_comments(comments, target_user, target_content)
                if comment:
                    success_users.add((target_user, title, url, comment))
            page_count += 1
            print u'已经匹配评论页数', page_count, u'次'
            time.sleep(1)
        except UnicodeDecodeError:
            print  u'匹配结果错误，跳过此匹配'
        except TimeoutException:
            print u'翻页失败'
    if len(success_users) > 0:
        print u'该宝贝匹配到了用户'
        try:
            for success_user in success_users:
                print success_user[0]
        except Exception:
            print u'展示匹配到的用户失败'
    else:
        print u'该宝贝没有匹配到有效的旺旺'
    return success_users


def is_comments_appear(driver, max_time=10):
    count = 1
    result = scroll_bottom_comments(driver)
    while not result:
        result = scroll_bottom_comments(driver)
        count = count + 1
        if count == max_time:
            return False
    return True


def scroll_bottom_comments(driver):
    js = "window.scrollTo(0,document.body.scrollHeight)"
    driver.execute_script(js)
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('#J_TabBar li a')
    except NoSuchElementException:
        return False
    return True


def parse_comments(html):
    doc = pq(html)
    lis = doc('.rate-grid tr')
    dates = get_days(c_config.MAX_DAY)
    comments = []
    for li in lis.items():
        date = li.find('.tm-rate-date').text()
        comment_text = li.find('.tm-rate-fulltxt').text()
        meta = li.find('.col-meta').text()
        user = li.find('.rate-user-info').text().replace(' ', '')[0:5]
        filter_date = c_config.FILTER_DATE
        if filter_date:
            if date in dates or date == u'今天':
                comments.append((user, date, comment_text, meta))
            elif date.startswith(str(c_config.EXCEPT_YEAR)):
                print u'时间已经到', c_config.EXCEPT_YEAR, u'年，停止匹配'
                c_config.NEXT_PAGE_COMMENTS = 0
            else:
                print u'出现日期不符合的评论，当前评论日期为', date
                c_config.WRONG_DATE_COUNT += 1
                if c_config.DATE_COUNT_FILTER:
                    if c_config.WRONG_DATE_COUNT > c_config.WRONG_DATE_MAX_COUNT:
                        print u'当前不符合日期过多，不符合日期数是', c_config.WRONG_DATE_COUNT, u'，目前评论日期已到', date, u'旺旺号过于久远，直接跳过查询'
                        c_config.NEXT_PAGE_COMMENTS = 0
        else:
            comments.append((user, date, comment_text, meta))
    return comments


def equal_text(a, b):
    if a.decode('utf-8', 'ignore') == b.decode('utf-8', 'ignore'):
        return True
    return False


def filter_comments(comments, target_user=None, target_content=None):
    for comment in comments:
        user = comment[0]
        comment_text = comment[2].strip()
        target_content = target_content.strip()
        print 'comment_text',comment_text
        print 'target_content', target_content
        print 'user', user, 'target_user', target_user
        if target_user and len(target_user) >= 5:
            if equal_text(user[0], target_user[0]) and equal_text(user[4], target_user[-1]) and target_content in comment_text:
                print u'匹配到旺旺名', target_user
                return comment


def filter_user():
    driver = c_config.C_DRIVER
    driver.get(c_config.LOGIN_URL)
    print u'完成登录之后，请输入任意键，开始执行爬取'
    raw_input()

read_from_excel()

