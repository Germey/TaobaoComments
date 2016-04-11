# -*- coding: utf-8 -*-

import requests
import config

def update_proxy_pool():

    print u'正在更新代理池'
    url = 'http://dev.kuaidaili.com/api/getproxy?orderid=926035281998084&num=30&quality=1&carrier=6&protocol=1&method=1&sort=1'

    response = requests.get(url)
    print u'获取代理如下'
    print response.content
    with open(config.PROXY_POOL, 'w') as f:
        f.write(response.content)
    print u'成功更新了代理'