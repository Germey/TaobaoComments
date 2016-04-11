# -*- coding: utf-8 -*-
import xlrd
from xlutils.copy import copy

import config

def merge_file():
    excel = config.TO_EXCEL_FILE
    phone = config.PHONE_TXT
    rb = xlrd.open_workbook(excel)
    sheet = rb.sheets()[0]
    names = sheet.col_values(0)
    phone_txt = open(phone, 'r').read()
    phones = phone_txt.split('\n')
    #print phones
    wb = copy(rb)
    write_sheet = wb.get_sheet(0)
    count = 0
    for name in names:
        count = count + 1
        for phone in phones:
            info = phone.split(' ')
            if len(info) == 2:
                first = info[0]
                second = info[1]
                if name == first:
                    print u'匹配到用户', name
                    print u'电话号码', phone
                    if len(second) == 11:
                        write_sheet.write(count, 4, second)
                        wb.save(excel)
                    else:
                        print u'电话号码信息不完整, 没有导入'





