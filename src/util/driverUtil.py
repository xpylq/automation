from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import src.util.proxyUtil as proxyUtil


def contains(driver, css_selector):
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
    if elements.__len__() == 0:
        return False
    return True


def wait(driver, css_selector, second):
    WebDriverWait(driver, second).until(lambda x: x.find_element_by_css_selector(css_selector))


def create_driver(is_proxy, is_headless):
    option = webdriver.ChromeOptions()
    if is_proxy:
        proxy = proxyUtil.get_proxy()
        # 设置代理(一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152)
        option.add_argument("--proxy-server=http://" + proxy['ip'] + ":" + proxy['port'])
    if is_headless:
        option.add_argument('--headless')
        option.add_argument(
            '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    return webdriver.Chrome(chrome_options=option)


# 初始化cookies
def init_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)
