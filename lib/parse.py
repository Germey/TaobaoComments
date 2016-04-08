# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import config
from lib.writetofile import write_to_excel
from lib.writetofile import write_to_txt
from getproduct import get_product


def parse_content(html):
    doc = pq(html)
    lis = doc('#J_TjWaterfall > li')
    print u'在此宝贝推荐链接中找到如下用户评论:'
    for li in lis.items():
        url = li.find('a').attr('href')
        url = parse_url(url)
        title = get_product(url)
        ps = li.find('p').items()
        for p in ps:
            text = p.text()
            if not '***' in text:
                name = p.find('b').text()
                comment = text.replace(name, '')
                print name, comment, url, title
                write_content = [name, comment, url, title]
                write_to_excel(write_content, config.TO_EXCEL_FILE)
                write_to_txt(" ".join(write_content),config.TO_TXT_FILE, name)
                write_to_txt(name, config.TO_WANG_FILE, name)




def parse_url(url):
    if not url.startswith('http'):
        url = 'https:' + url
    return url

