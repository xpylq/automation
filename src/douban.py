#!/usr/bin/python3

import os
import re
from time import sleep

from PIL import ImageGrab
from selenium import webdriver
from selenium.webdriver.common.by import By

import src.util.dbComponent as dbComponent


# 初始化cookies
def init_cookies(driver, user):
    for cookie in user.cookies:
        driver.add_cookie(cookie)


# 检查登录状态
def is_login(driver, user):
    driver.implicitly_wait(1)
    test = driver.find_elements_by_class_name("nav-user-account")
    driver.implicitly_wait(1)
    if test.__len__() == 0:
        dbComponent.delete_cookies(user.id)
        return False
    return True


# 检查是否还没有做
def is_not_down(driver):
    try:
        driver.implicitly_wait(1)
        driver.find_element_by_class_name("collection_date")
        driver.implicitly_wait(1)
    except Exception as e:
        return True
    return False


# 读取评论，一行一条
def init_file(file_path):
    comment_list = []
    if os.path.exists(file_path):
        file = open(file_path, "r")
        for line in file.readlines():
            line = re.sub("\n", "", line)
            comment_list.append(line)
    return comment_list


def auto(url, do_type, is_star, total, file_path):
    user_list = dbComponent.get_login_user(1, total)
    # 短评
    comment_list = init_file(file_path)
    driver = webdriver.Chrome()
    i = 0
    for user in user_list:
        try:
            driver.get(url)
            driver.implicitly_wait(30)
            init_cookies(driver, user)
            driver.get(url)
            driver.implicitly_wait(30)
            if is_login(driver, user):
                if is_not_down(driver):
                    button_list = driver.find_elements_by_class_name("colbutt")
                    if button_list.__len__() != 0:
                        button_list[do_type].click()
                        driver.implicitly_wait(30)
                        # 五星好评
                        if is_star:
                            driver.find_element(By.ID, "comment").send_keys(comment_list[i])
                            driver.find_element(By.ID, "rating").find_element(By.ID, "star5").click()
                            sleep(5)
                    driver.find_element(By.CLASS_NAME, "bn-flat").click()
                    sleep(5)
                driver.get_screenshot_as_file("/Users/youzhihao/Downloads/snapshot/" + str(i) + "-snapshot.png")
                driver.get("https://www.douban.com/mine/")
                driver.implicitly_wait(10)
                driver.get_screenshot_as_file("/Users/youzhihao/Downloads/snapshot/" + str(i) + "-mine.png")
                driver.find_element(By.ID, "usr-profile-nav-statuses").click()
                driver.implicitly_wait(10)
                driver.get_screenshot_as_file("/Users/youzhihao/Downloads/snapshot/" + str(i) + "-broadcast.png")
                i += 1
                sleep(5)
        except Exception as e:
            print(e)
        finally:
            driver.delete_all_cookies()


def dianzan(url, total):
    # 初始化点赞人
    key_word_list = init_file(file_path)
    user_list = dbComponent.get_login_user(1, total)
    driver = webdriver.Chrome()
    driver.fullscreen_window()
    i = 0
    for user in user_list:
        try:
            driver.implicitly_wait(30)
            driver.get(url)
            init_cookies(driver, user)
            driver.get(url)
            driver.implicitly_wait(1)
            comment_list = driver.find_elements(By.CLASS_NAME, "comment-item")
            for comment in comment_list:
                user_name = comment.find_element(By.CLASS_NAME, "comment-info").find_element(By.TAG_NAME, "a").text
                if user_name in key_word_list:
                    try:
                        comment.find_element(By.CLASS_NAME, "comment-vote").find_element(By.TAG_NAME, "a").click()
                        sleep(1)
                        comment.find_element(By.CLASS_NAME, "comment-vote").find_element(By.TAG_NAME, "a").click()
                    except Exception as e:
                        im = ImageGrab.grab()
                        im.save("/Users/youzhihao/Downloads/snapshot/" + str(i) + "-snapshot.png")
                        alert = driver.switch_to.alert
                        sleep(2)
                        alert.accept()
                        alert.accept()
                    driver.implicitly_wait(30)
                    driver.get("https://www.douban.com/mine/")
                    driver.get_screenshot_as_file("/Users/youzhihao/Downloads/snapshot/" + str(i) + "-mine.png")
        except Exception as e:
            print(e)
        finally:
            driver.delete_all_cookies()
        i += 1
        sleep(5)


if __name__ == "__main__":
    url = "https://movie.douban.com/subject/26905469/comments?status=F"
    do_type = 1
    is_start = True
    file_path = "/Users/youzhihao/Downloads/code/comment"
    dianzan(url, 10)
    # auto(url, do_type, is_start, 7, file_path)
