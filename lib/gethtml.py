# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq

def parse(html):

    doc = pq(html)
    lis = doc('#J_TjWaterfall > li')
    for li in lis.items():
        url = li.find('a').attr('href')
        ps = li.find('p').items()
        for p in ps:
            print p.text()