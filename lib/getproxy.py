# -*- coding: utf-8 -*-
from random import randint
import config


def get_random_proxy():
    with open(config.PROXY_POOL, 'r') as f:
        proxy_pool = f.read()
        proxies = proxy_pool.split('\n')
        length = len(proxies)
        rand = randint(0, length - 1)
        random_proxy = proxies[rand]
        print u'当前代理,', random_proxy
        return random_proxy
