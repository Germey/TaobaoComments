#coding:utf-8

import AlipayConfig
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re,signal
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import TimeLimited
from threading import Thread
import time,httplib



class TimeoutException(Exception):
    pass

ThreadStop = Thread._Thread__stop

def timelimited(timeout):
    def decorator(function):
        def decorator2(*args,**kwargs):
            class TimeLimited(Thread):
                def __init__(self,_error= None,):
                    Thread.__init__(self)
                    self._error =  _error
                    
                def run(self):
                    try:
                        self.result = function(*args,**kwargs)
                    except Exception,e:
                        self._error =e

                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)

            t = TimeLimited()
            t.start()
            t.join(timeout)
     
            if isinstance(t._error,TimeoutException):
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t.isAlive():
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t._error is None:
                return t.result

        return decorator2
    return decorator



def Init():
    AlipayConfig.driver = webdriver.Chrome()

def LoginAndDispatch():
    #打开登录页面
    AlipayConfig.driver.get("https://auth.alipay.com/login/index.htm?needTransfer=true&goto=http://fu.alipay.com/transfer/index.htm")
    login_id_element = AlipayConfig.driver.find_element_by_css_selector('#J-input-user')
    login_psw_element = AlipayConfig.driver.find_element_by_css_selector('#password_rsainput')
    login_id_element.send_keys(AlipayConfig.USERNAME)
    login_psw_element.send_keys(AlipayConfig.PASSWORD)
    sleep(2)
    login_psw_element.send_keys(Keys.RETURN)
    
    #等待
    AlipayConfig.driver.implicitly_wait(5)
    
    #跳转到支付页面
    dispatcher_element = AlipayConfig.driver.find_element_by_link_text(AlipayConfig.DISPATCHER_TEXT)
    sleep(2)
    dispatcher_element.click()
    AlipayConfig.driver.implicitly_wait(3)

@timelimited(1)
def input(phone_input_element,phone_number):
    phone_input_element.send_keys(phone_number)

def refresh_input(phone_number):
    sleep(0.5)
    try:
        AlipayConfig.driver.refresh()
    except httplib.CannotSendRequest:
        print 'refresh error'
        return 2
    #phone_input_element = driver.find_element_by_css_selector('#ipt-search-key')
    phone_input_element = WebDriverWait(AlipayConfig.driver,5).until(EC.presence_of_element_located((By.ID,'ipt-search-key')))
    AlipayConfig.driver.execute_script(init_js)
    #phone_input_element.clear()
    print phone_number
    #sleep(1)
    try:
        input(phone_input_element,phone_number)
    except TimeoutException:
        return 2
    return 1
    

init_js = '''
var e= document.createElement('div');
e.setAttribute('id','__msg');
e.style.display = 'none';
document.body.appendChild(e);
'''

change_js = 'document.getElementById(\'__msg\').innerHTML = document.getElementById(\'ipt-search-key\').value'

def ExcuteAlipayProcessor():
    
    Init()
    LoginAndDispatch()
    
    read_file = open(AlipayConfig.NEED_READ_FILE,'r')
    
    line = read_file.readline()
    
    sleep(2)
    
    AlipayConfig.driver.execute_script(init_js)
    sleep(1)
    
    while line:
        pattern = re.compile(r'\d{11}')
        phone_number_list = re.findall(pattern, line)
        
        if phone_number_list:
            for phone_number in phone_number_list:
                
                status = refresh_input(phone_number)
                if(status == 2 ):
                    print u'输入失败'
                    continue
                
                print '-----------'
                 
                error_count = 5
                blank = AlipayConfig.driver.find_element_by_css_selector('#faq')
                blank.click()
                AlipayConfig.driver.implicitly_wait(3)
                #phone_input_element = driver.find_element_by_css_selector('#ipt-search-key')
                sleep(0.5)
                AlipayConfig.driver.execute_script(change_js)
                page = AlipayConfig.driver.page_source
                soup = BeautifulSoup(page,'html.parser')
                #sleep(0.5)
                msg_list = soup.select('#__msg')
                 
                result = msg_list[0].get_text()
                #print result
                if(result.isdigit()):
                    continue
                else:
                    print result
                    result += '\n'
                    write_file = open(AlipayConfig.RESULT_FILR,'a')
                    result = result.encode('utf-8')
                    write_file.write(result)
                    write_file.close()
                
                #sleep(1)
                AlipayConfig.driver.implicitly_wait(2)
                
                
        else:
            line += '\n'
            write_file = open(AlipayConfig.RESULT_FILR,'a')
            line = line.decode('utf-8').encode('utf-8')
            write_file.write(line)
            write_file.close()
        
        line = read_file.readline()
    
    read_file.close()
    
    
    
    