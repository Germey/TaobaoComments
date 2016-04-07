# -*- coding:utf-8 -*-

import re

def get_urls():

    # read file
    file = open('urls.txt', 'r')
    content = file.read()

    # extract urls from txt
    pattern = re.compile(r'(http.*?)\s', re.S)
    urls = re.findall(pattern, content)
    print urls
    return urls

get_urls()