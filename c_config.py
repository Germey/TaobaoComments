# -*- coding: utf-8 -*-

from selenium import webdriver

# 加载配置
SERVICE_ARGS = [
    '--load-images=false',
]

# 星级查询网站
STAR_INFO_URL = 'http://www.taoyitu.com/'
# 请求会话
#DRIVER = webdriver.PhantomJS(service_args=SERVICE_ARGS)

C_DRIVER = webdriver.Chrome(executable_path='./chromedriver')
# 请求超时时间,单位秒
TIMEOUT = 30
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

# 电话号文本
PHONE_TXT = 'file/phone.txt'

# 计数文本
COUNT_TXT = 'file/count_filter.txt'

# 最大星级
MAX_STAR = 5

# 最大失败次数
MAX_FAIL = 7

# 输出额外信息
CONSOLE_OUTPUT = True

# 是否过滤星级
STAR_FILTER = True

# 总共的连接数
TOTAL_COUNT = 1

# 当前的链接第几个
NOW_COUNT = 0

# 间隔最大天数
MAX_DAY = 10

# 过滤的文本
FILTER_FILE = 'file/filter.txt'

# 过滤评论后的文本
FILTER_RESULT = 'file/final.xls'

# 翻页
NEXT_END = 0

# 最大不匹配数
END_MAX = 20

# 不匹配数
END_COUNT = 0

# 匹配文件
FILTER_OUT_PUT = 'file/filter_res.txt'


URLS_FILE = 'file/urls.txt'

OUT_FILE = 'file/result.xls'



MAX_SCROLL_TIME = 10

ANONYMOUS_STR = '***'


FILTER_STAR = True


WRONG_DATE_COUNT = 0

WRONG_DATE_MAX_COUNT = 50

NEXT_PAGE_COMMENTS = 1

FILTER_DATE = True

MAX_COMMENTS_COUNT = 5000

MAX_COMMENTS_LIMIT = True

NEXT_PAGE_WAIT = 2

TOTAL_URLS_COUNT = 0


NOW_URL_COUNT = 0

LOGIN_URL = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.50862.754894437.1.MVF6jc&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F'


EXCEPT_YEAR = 2015

DATE_COUNT_FILTER = True