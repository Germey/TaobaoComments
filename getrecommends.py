# -*- coding:utf-8 -*-

import time

def get_recommends(driver, max_time = 10):
    count = 1
    result = try_get(driver)
    while not result:
        result = try_get(driver)
        count = count + 1
        if result:
            return True
        if count == max_time:
            return False




def try_get(driver):
    js = "window.scrollTo(0,document.body.scrollHeight)"
    driver.execute_script(js)
    time.sleep(2)
    element = driver.find_element_by_id('J_TjWaterfall')
    print u'element-----', element
    return element
