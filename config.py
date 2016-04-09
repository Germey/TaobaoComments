# -*- coding: utf-8 -*-

from selenium import webdriver

# 加载配置
SERVICE_ARGS = [
    '--load-images=false',
    '--disk-cache=true',
    #'--proxy=106.37.177.251:3128'
]

# 请求会话
DRIVER = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# 请求超时时间,单位秒
TIMEOUT = 20
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

# 最大失败次数
MAX_FAIL = 7

# 输出额外信息
CONSOLE_OUTPUT = True


