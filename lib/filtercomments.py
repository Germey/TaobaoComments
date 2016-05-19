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
from lib.get_days import get_days
from lib.to_new_file import write_to_excel

reload(sys)
sys.setdefaultencoding("utf-8")


def read_from_excel(start):
    workbook = xlrd.open_workbook(c_config.TO_EXCEL_FILE)
    sheet = workbook.sheet_by_index(0)
    row_num = sheet.nrows
    if not start < row_num:
        print u'已经过滤完毕'
        return
    for i in range(start, row_num):
        try:
            info = sheet.row_values(i)
            write_count(i, c_config.COUNT_TXT)

            if len(info) > 3:
                print u'开始过滤第', str(int(i)+1), u'行的信息'
                if info[0]:
                    url = info[2]
                    print u'旺旺号',info[0]
                    filter_comment_info(url, info)
            else:
                print u'该行无有效旺旺信息，跳过过滤'
        except Exception:
            print u'旺旺信息不完整，跳过该过滤'





def filter_comment_info(url, info):
    driver = c_config.C_DRIVER
    timeout = c_config.TIMEOUT
    success_users = set([])
    print u'正在匹配评论', url,u'请稍后'
    c_config.NEXT_PAGE_COMMENTS = 1
    driver.get(url)
    max_page = 100
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "J_TabBarBox"))
        )
    except TimeoutException:
        print u'请求匹配评论页面超时'
    if is_comments_appear(driver):
        print u'已成功加载出评论页面'
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

        js='''
        a=document.querySelector('.tm-r-time')
        a.click()
        '''
        try:
            driver.execute_script(js)
        except WebDriverException:
            print u'点击时间排序失败'
        time.sleep(2)
        print u'已经将评论按照时间排序'
        html = driver.page_source

        max_page = int(get_comments_count(html)) / 20 + 1
        comments = parse_comments(html)
        print 'user', info[0], 'comment', info[1]
        comment = filter_comments(comments, info[0], info[1])
        if comment:
            contents = (info[0], info[1], comment[1], comment[3], info[2], info[3])
            write_to_excel(contents, c_config.FILTER_RESULT)
            return

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

            comment = filter_comments(comments, info[0], info[1])
            if comment:
                contents = (info[0], info[1], comment[1], comment[3], info[2], info[3])
                write_to_excel(contents, c_config.FILTER_RESULT)
                return
            page_count += 1
            if page_count > max_page:
                print u'评论全部循环完毕'
                c_config.NEXT_PAGE_COMMENTS = 0
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
        print '匿名旺旺名', user, '待查找旺旺名', target_user
        if target_user and len(target_user) >= 5:
            if equal_text(user[0], target_user[0]) and equal_text(user[4], target_user[-1]) and target_content in comment_text:
                print u'匹配到旺旺名和相关评论', target_user
                return comment
    print u'没有匹配到指定日期内的旺旺'
    return None


def get_count():
    try:
        with open(c_config.COUNT_TXT, 'r') as f:
            page = f.read()
            if not page:
                return 0
            else:
                return page
    except Exception:
        print u'不存在计数文件'
        return 0

def write_count(count, file):
    try:
        with open(file, 'w') as f:
            f.write(str(count))
            f.close()
    except TypeError:
        print u'页码写入失败'

def filter_user():
    driver = c_config.C_DRIVER
    driver.get(c_config.LOGIN_URL)
    print u'完成登录之后，请输入任意键，开始执行爬取'
    raw_input()

    workbook = xlrd.open_workbook(c_config.TO_EXCEL_FILE)
    sheet = workbook.sheet_by_index(0)
    row_num = sheet.nrows
    c_config.TOTAL_COUNT = row_num
    
    print u'共有', c_config.TOTAL_COUNT, u'个待过滤旺旺号'
    count = int(get_count())
    print u'上次过滤到第', count, u'个'
    print u'输入 1 继续过滤,输入 2 重新过滤:'
    num = raw_input()
    if num == '2':
        count = 0
        print u'开始重新过滤'
    if count < c_config.TOTAL_COUNT:
        read_from_excel(count)
    else:
        print u'上次已经全部过滤完毕'
    


def get_comments_count(html):
    doc = pq(html)
    comments_count = doc('.J_ReviewsCount').eq(0).text()
    return comments_count