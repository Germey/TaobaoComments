#coding:utf-8

import PhoneTransferConfig,re


def phoneTransfer():
    r_file = open(PhoneTransferConfig.READ_FILE,'r')
    w_file = open(PhoneTransferConfig.WRITE_FILE,'w')
    
    line = ' '
    
    while line:
        line = r_file.readline()
        if (line == ''):
            continue
        pattern = re.compile(r'\d{11}')
        phone_number_list = re.findall(pattern, line)
        if phone_number_list:
            for phone_number in phone_number_list:
                w_file.write(phone_number)
                w_file.write('\n')
            
        else:
            continue
    r_file.close()
    w_file.close()