import time
from src.util import dbComponent
from src.util import driverUtil
import json


def login(is_proxy):
    user_list = dbComponent.get_new_user(2)
    # user_list = dbComponent.get_un_login_user(2)
    driver = driverUtil.create_driver(is_proxy, False)
    fail_id_list = []
    for user in user_list:
        driver.get("https://www.zhihu.com/")
        driver.find_element_by_css_selector('.SignContainer-switch span').click()
        driver.find_element_by_css_selector('[name=username]').send_keys(user.name)
        driver.find_element_by_css_selector('[name=password]').send_keys(user.password)
        key = input("输入成功或失败:")
        if key == 'n' or key == 'N':
            driver.delete_all_cookies()
            fail_id_list.append(user.id)
            print(user.id)
        else:
            # 增加过期时间
            cookies = driver.get_cookies()
            dbComponent.save_cookies(user.id, cookies)
            driver.delete_all_cookies()
    print(fail_id_list)


def init_new():
    user_list = dbComponent.get_new_user(2)
    driver = driverUtil.create_driver(False, False)
    for user in user_list:
        try:
            driver.get("https://www.zhihu.com/")
            driverUtil.init_cookies(driver, user.cookies)
            driver.get("https://www.zhihu.com/")
            input("等待:")
            cookies = driver.get_cookies()
            dbComponent.save_cookies(user.id, cookies)
            dbComponent.update_isNew(user.id)
        except Exception as e:
            print(e, user.id)
        finally:
            driver.delete_all_cookies()


def dianzan(url, is_proxy):
    user_list = dbComponent.get_login_user(2, 10)
    for user in user_list:
        try:
            driver = driverUtil.create_driver(is_proxy, False)
            driver.get(url)
            driverUtil.init_cookies(driver, user.cookies)
            driver.get("https://www.zhihu.com/")
            url_token_json = driver.find_element_by_css_selector("[data-zop-usertoken]").get_attribute(
                "data-zop-usertoken")
            url_token = json.loads(url_token_json)["urlToken"]
            homepage = "https://www.zhihu.com/people/" + url_token
            driver.get(url)
            question_content = driver.find_element_by_css_selector(".QuestionAnswer-content")
            button = question_content.find_element_by_css_selector(".VoteButton--up")
            if "is-active" not in button.get_attribute("class"):
                driver.implicitly_wait(1)
                if driverUtil.contains(driver, "ContentItem-more"):
                    driver.find_element_by_css_selector(".ContentItem-more").click()
                button.click()
                time.sleep(10)
                driver.get_screenshot_as_file("/Users/youzhihao/Downloads/snapshot/" + str(user.id) + "-snap.png")
                driver.get(homepage)
                driver.get_screenshot_as_file("/Users/youzhihao/Downloads/snapshot/" + str(user.id) + "-home.png")
        except Exception as e:
            print(user.id, e)
        finally:
            driver.quit()
            print(homepage)
            time.sleep(10)


def yanghao():
    user_list = dbComponent.get_login_user(2, 2000)
    driver = driverUtil.create_driver(False, True)
    num = 0
    for user in user_list:
        try:
            driver.get("https://www.zhihu.com/")
            driverUtil.init_cookies(driver, user.cookies)
            driver.get("https://www.zhihu.com/")
            url_token_json = driver.find_element_by_css_selector("[data-zop-usertoken]").get_attribute(
                "data-zop-usertoken")
            url_token = json.loads(url_token_json)["urlToken"]
            if url_token == 'urlToken':
                dbComponent.delete_cookies(user.id)
            else:
                num += 1
                print(num)
        except Exception as e:
            dbComponent.delete_cookies(user.id)
        finally:
            driver.delete_all_cookies()
            time.sleep(5)
    print("totalNum:", num)


if __name__ == "__main__":
    # login(False)
    #init_new()
    # yanghao()
    dianzan("https://www.zhihu.com/question/27188550/answer/99120693", False)
