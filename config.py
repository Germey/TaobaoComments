# -*- coding: utf-8 -*-

from selenium import webdriver

# 加载配置
SERVICE_ARGS = [
    '--load-images=false',
    '--ignore-ssl-errors=true',
]

# 星级查询网站
STAR_INFO_URL = 'http://www.kehuda.com/g/x/#username='
# 请求会话
DRIVER = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# 请求超时时间,单位秒
TIMEOUT = 10
# 加载重试次数
MAX_TRY = 6
# 读取的URL文件
FROM_FILE = 'file/urls.txt'
# 写入的文件
TO_TXT_FILE = 'file/result.txt'
# 写入的EXCEL文件
TO_EXCEL_FILE = 'file/result.xls'
# 写入的旺旺名
TO_WANG_FILE = 'file/wangwang.txt'
# 代理池路径
PROXY_POOL = 'proxy/proxy.txt'
# 最大星级
MAX_STAR = 3
# 最大失败次数
MAX_FAIL = 7

# 输出额外信息
CONSOLE_OUTPUT = True

# 是否过滤星级
STAR_FILTER = False

