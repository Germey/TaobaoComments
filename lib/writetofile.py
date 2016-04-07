# -*- coding: utf-8 -*-

import config


def write_to_file(content):
    content = content.encode('utf-8', 'ignore')
    with open(config.TO_FILE, 'a') as f:
        f.write(content)
        f.write('\n')
        f.close()
        print u'写入文件成功'