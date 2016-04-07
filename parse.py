# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from writetofile import write_to_file
from getproduct import get_product

def parse_content(html):

    doc = pq(html)
    lis = doc('#J_TjWaterfall > li')
    print lis.items()
    for li in lis.items():
        url = li.find('a').attr('href')
        url = parse_url(url)
        title = get_product(url)
        ps = li.find('p').items()
        for p in ps:
            text = p.text()
            if not '***' in text:
                result = text + str(' ') + url + str(' ') + title
                print result
                write_to_file('result.txt', result)


def parse_url(url):
    if not url.startswith('http'):
        url = 'https:' + url
    return url

