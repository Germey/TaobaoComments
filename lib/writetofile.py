# -*- coding: utf-8 -*-

import config
import xlwt
import xlrd
from xlutils.copy import copy
def write_to_txt(content, file):
    try:
        content = content.encode('utf-8', 'ignore')
        with open(file, 'a') as f:
            f.write(content)
            f.write('\n')
            f.close()
            if config.CONSOLE_OUTPUT:
                print u'写入文件成功'
    except Exception, e:
        print u'写入文件失败', e.message


def write_to_excel(contents, file):
    try:
        rb = xlrd.open_workbook(file)
        sheet = rb.sheets()[0]
        row = sheet.nrows
        wb = copy(rb)
        sheet = wb.get_sheet(0)
        count = 0
        for content in contents:
            sheet.write(row, count, content)
            count = count + 1
            wb.save(file)

    except IOError:
        print u'未找到该文件'
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        book.add_sheet('sheet1', cell_overwrite_ok=True)
        book.save(file)
        print u'已成功创建该文件'
        write_to_excel(contents, file)
