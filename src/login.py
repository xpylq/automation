#!/usr/bin/python3
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.util import dbComponent
from src.util import driverUtil


# 登录



def login_douban(is_proxy):
    user_list = dbComponent.get_un_login_user(1)
    for user in user_list:
        driver = driverUtil.create_driver(is_proxy, False)
        driver.get("https://accounts.douban.com/login")
        account = driver.find_element(By.ID, "email")
        account.send_keys(user.name)
        remember = driver.find_element(By.ID, "remember")
        remember.click()
        while True:
            submit_buttom = None
            try:
                driver.implicitly_wait(1)
                submit_buttom = driver.find_element(By.NAME, "login")
                password = driver.find_element(By.ID, "password")
                password.send_keys(user.password)
                captcha_field = driver.find_element(By.ID, "captcha_field")
                captcha_field.send_keys(input("输入验证码:"))
                submit_buttom.submit()
                if driver.current_url.find("https://accounts.douban.com/login") == -1:
                    break
            except Exception as e:
                submit_buttom.submit()
                if driver.current_url.find("https://accounts.douban.com/login") == -1:
                    break
                print(e)
        cookies = driver.get_cookies()
        # 增加过期时间
        for cookie in cookies:
            cookie['expiry'] = time.time() + 60 * 60 * 24 * 365 * 10
        dbComponent.save_cookies(user.id, cookies)
        driver.delete_all_cookies()
        driver.close()


# 检查登录状态
def check_login_status():
    user_list = dbComponent.get_login_user(1, 2000)
    driver = webdriver.Chrome()
    for user in user_list:
        time.sleep(5)
        driver.implicitly_wait(30)
        driver.get("https://www.douban.com/")
        for cookie in user.cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.douban.com/")
        driver.implicitly_wait(1)
        test = driver.find_elements_by_class_name("nav-user-account")
        driver.implicitly_wait(1)
        if test.__len__() == 0:
            dbComponent.delete_cookies(user.id)
            print(user.name, "无效")
        else:
            print(user.name, "有效")


#if __name__ == "__main__":
# login_douban(False)
# check_login_status()
