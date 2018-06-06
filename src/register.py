#!/usr/bin/python3
import random
import re
import string
import time
import threading

from selenium.webdriver.common.by import By

import src.util.driverUtil as driverUtil
import src.util.proxyUtil as proxyUtil
import src.util.dbComponent as dbComponent


# 生成一个n位的随机账号
def create_account(n):
    l1 = string.digits  # 数字
    l2 = string.ascii_uppercase  # 大写字母
    l3 = string.ascii_lowercase  # 小写字母
    l4 = l1 + l2 + l3
    n = int(n)
    s1 = random.sample(l2 + l3, 1)
    s2 = random.sample(l4, n)
    return ''.join((s1 + s2))


def create_password(n):
    l1 = string.digits  # 数字
    l3 = string.ascii_lowercase  # 小写字母
    l4 = l1 + l3
    n = int(n)
    s1 = random.sample(l3, 1)
    s2 = random.sample(l4, n)
    return ''.join((s1 + s2))


# 邮箱注册
def zhihu_register(nickname_list):
    while True:
        try:
            driver = driverUtil.create_driver(True, False)
            code = 'not_receive'
            for i in range(3):
                driver.get("https://www.zhihu.com/signup")
                mobile = proxyUtil.get_mobile()
                driver.find_element(By.NAME, "phoneNo").clear()
                driver.find_element(By.NAME, "phoneNo").send_keys(mobile)
                driver.find_element(By.CLASS_NAME, 'CountingDownButton').click()
                time.sleep(2)
                if not driverUtil.contains(driver, '.SignFlowInput-errorMask span'):
                    for i in range(3):
                        time.sleep(20)
                        code = proxyUtil.get_code(mobile)
                        if code != 'not_receive':
                            break
                if code != 'not_receive':
                    break
            code = re.findall("\d{6}", code)[0]
            driver.find_element(By.CSS_SELECTOR, '.SignFlow-smsInput input').send_keys(code)
            driver.find_element(By.CLASS_NAME, 'Register-submitButton').click()
            driverUtil.wait(driver, '[name=fullname]', 30)
            driverUtil.wait(driver, '[type=password]', 30)
            driverUtil.wait(driver, '[type=submit]', 30)
            time.sleep(10)
            password = create_password(8)
            nickname = nickname_list.pop()
            driver.find_element(By.CSS_SELECTOR, '[name=fullname]').send_keys(nickname)
            driver.find_element(By.CSS_SELECTOR, '[name=password]').send_keys(password)
            driver.find_element(By.CSS_SELECTOR, '[type=submit]').click()
            time.sleep(10)
            print('mobile', mobile)
            print('password', password)
            dbComponent.add_user_and_cookies(mobile, password, 2, driver.get_cookies())
        except Exception as e:
            print(e)
        finally:
            driver.quit()


def get_nickname():
    try:
        nickname_list = []
        file = open('/Users/youzhihao/Downloads/douban/nickname.txt', 'r')
        for line in file.readlines():
            nickname_list.append(line.replace("\n", ""))
        nickname_list.remove('')
    except Exception as e:
        print(e)
    return nickname_list


class MyThread(threading.Thread):
    def __init__(self, nickname_list):
        threading.Thread.__init__(self)
        self.nickname_list = nickname_list

    def run(self):
        zhihu_register(self.nickname_list)


if __name__ == "__main__":
    nickname_list = get_nickname()
    zhihu_register(nickname_list)
    # MyThread(nickname_list).start()

