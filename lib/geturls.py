# -*- coding:utf-8 -*-

import re

import config


def get_urls():

    try:
        # read file
        file = open(config.FROM_FILE, 'r')
        content = file.read()

        # extract urls from txt
        pattern = re.compile(r'(http.*?)\s', re.S)
        urls = re.findall(pattern, content)
        return urls

    except Exception, e:
        print u'获取链接失败', e.message