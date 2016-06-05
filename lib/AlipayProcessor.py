#coding:utf-8

import AlipayConfig
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from time import sleep


def Init():
    driver = webdriver.Chrome()
    return driver

def LoginAndDispatch(driver):
    #打开登录页面
    driver.get("https://auth.alipay.com/login/index.htm?needTransfer=true&goto=http://fu.alipay.com/transfer/index.htm")
    login_id_element = driver.find_element_by_css_selector('#J-input-user')
    login_psw_element = driver.find_element_by_css_selector('#password_rsainput')
    login_id_element.send_keys(AlipayConfig.USERNAME)
    login_psw_element.send_keys(AlipayConfig.PASSWORD)
    sleep(2)
    login_psw_element.send_keys(Keys.RETURN)
    
    #等待
    driver.implicitly_wait(5)
    
    #跳转到支付页面
    dispatcher_element = driver.find_element_by_link_text(AlipayConfig.DISPATCHER_TEXT)
    sleep(2)
    dispatcher_element.click()
    driver.implicitly_wait(3)
    return driver

init_js = '''
var e= document.createElement('div');
e.setAttribute('id','__msg');
e.style.display = 'none';
document.body.appendChild(e);
'''

change_js = 'document.getElementById(\'__msg\').innerHTML = document.getElementById(\'ipt-search-key\').value'

def ExcuteAlipayProcessor():
    driver = Init()
    driver = LoginAndDispatch(driver)
    
    read_file = open(AlipayConfig.NEED_READ_FILE,'r')
    
    line = read_file.readline()
    
    sleep(2)
    
    driver.execute_script(init_js)
    sleep(1)
    
    while line:
        pattern = re.compile(r'\d{11}')
        phone_number_list = re.findall(pattern, line)
        
        if phone_number_list:
            for phone_number in phone_number_list:
                sleep(1)
                phone_input_element = driver.find_element_by_css_selector('#ipt-search-key')
                phone_input_element.clear()
                print phone_number
                sleep(1)
                phone_input_element.send_keys(phone_number)
                print '-----------'
                blank = driver.find_element_by_css_selector('#faq')
                blank.click()
                driver.implicitly_wait(3)
                #phone_input_element = driver.find_element_by_css_selector('#ipt-search-key')
                sleep(1)
                driver.execute_script(change_js)
                page = driver.page_source
                soup = BeautifulSoup(page,'html.parser')
                sleep(1)
                msg_list = soup.select('#__msg')
                 
                result = msg_list[0].get_text()
                #print result
                if(result.isdigit()):
                    driver.refresh()
                    driver.execute_script(init_js)
                    continue
                else:
                    print result
                    result += '\n'
                    write_file = open(AlipayConfig.RESULT_FILR,'a')
                    result = result.encode('utf-8')
                    write_file.write(result)
                    write_file.close()
                
                sleep(1)
                driver.implicitly_wait(2)
                driver.refresh()
                driver.execute_script(init_js)
                
        else:
            line += '\n'
            write_file = open(AlipayConfig.RESULT_FILR,'a')
            line = line.decode('utf-8').encode('utf-8')
            write_file.write(line)
            write_file.close()
        
        line = read_file.readline()
    
    read_file.close()
    
    
    
    