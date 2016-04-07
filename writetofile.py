# -*- coding: utf-8 -*-

def write_to_file(file_name, content):
    content = content.encode('utf-8', 'ignore')
    with open(file_name, 'a') as f:
        f.write(content)
        f.write('\n')
        f.close()
        print u'写入文件成功'