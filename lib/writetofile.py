# -*- coding: utf-8 -*-

import config
import xlwt
import xlrd
from xlutils.copy import copy


def write_to_txt(content, file, key=''):
    try:
        content = content.encode('utf-8', 'ignore')
        if not repeat_txt(key, file):
            with open(file, 'a') as f:
                f.write(content)
                f.write('\n')
                f.close()
                if config.CONSOLE_OUTPUT:
                    print u'成功写入到文本', file
        else:
            if config.CONSOLE_OUTPUT:
                print u'内容已存在, 跳过写入文本', file
    except UnicodeDecodeError, e:
        if config.CONSOLE_OUTPUT:
            print u'写入文件失败, 编码问题', file, e.message
    except IOError, e:
        if config.CONSOLE_OUTPUT:
            print u'文件不存在, 正在创建新文件', file, e.message
        with open(file, 'w') as f:
            f.write(content)
            f.write('\n')
            f.close()
            if config.CONSOLE_OUTPUT:
                print u'已创建并写入到文件', file


def write_to_excel(contents, file):
    try:
        rb = xlrd.open_workbook(file)
        sheet = rb.sheets()[0]
        row = sheet.nrows
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        count = 0
        name = contents[0]
        if not repeat_excel(name, file):
            for content in contents:
                sheet.write(row, count, content)
                count = count + 1
                wb.save(file)
            if config.CONSOLE_OUTPUT:
                print u'已成功写入到文件', file, u'第', row + 1, u'行'
        else:
            if config.CONSOLE_OUTPUT:
                print u'内容已存在, 跳过写入文件', file

    except IOError:
        if config.CONSOLE_OUTPUT:
            print u'未找到该文件', file
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        book.add_sheet('sheet1', cell_overwrite_ok=True)
        book.save(file)
        if config.CONSOLE_OUTPUT:
            print u'已成功创建该文件', file
        write_to_excel(contents, file)


def repeat_txt(word, file):
    word = word.encode('utf-8', 'ignore')
    f = open(file, 'r')
    content = f.read()
    f.close()
    if word in content:
        return True
    else:
        return False


def repeat_excel(word, file):
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)
    words = sheet.col_values(0)
    if word in words:
        return True
    else:
        return False

def write_count(count, file):
    try:
        with open(file, 'w') as f:
            f.write(str(count))
            f.close()
    except TypeError:
        print u'页码写入失败'


def get_count():
    try:
        with open(config.COUNT_TXT, 'r') as f:
            page = f.read()
            if not page:
                return 0
            else:
                return page
    except Exception:
        print '读页码失败'
