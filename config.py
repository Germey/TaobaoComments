# -*- coding: utf-8 -*-

# 请求超时时间,单位秒
TIMEOUT = 20
# 加载重试次数
MAX_TRY = 10
# 读取的URL文件
FROM_FILE = 'file/urls.txt'
# 写入的文件
TO_FILE = 'file/result.txt'

# 加载配置
SERVICE_ARGS = [
    '--load-images=false',
    '--disk-cache=true',
]

