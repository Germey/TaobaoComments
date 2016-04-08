# -*- coding: utf-8 -*-

# 请求超时时间,单位秒
TIMEOUT = 30
# 加载重试次数
MAX_TRY = 10
# 读取的URL文件
FROM_FILE = 'file/urls.txt'
# 写入的文件
TO_TXT_FILE = 'file/result.txt'
# 写入的EXCEL文件
TO_EXCEL_FILE = 'file/result.xls'
# 写入的旺旺名
TO_WANG_FILE = 'file/wangwang.txt'
# 加载配置
SERVICE_ARGS = [
    '--load-images=false',
    '--disk-cache=true',
]

# 输出额外信息
CONSOLE_OUTPUT = True
