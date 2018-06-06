import time

import src.util.driverUtil as driverUtil
from src.util import dbComponent

user = dbComponent.get_login_user_by_id(39)
driver = driverUtil.create_driver(False, False)
driver.get("https://www.zhihu.com/")
for cookie in user.cookies:
    cookie['expiry'] = time.time() + 60 * 60 * 24 * 365 * 10
    driver.add_cookie(cookie)
dbComponent.save_cookies(39, user.cookies)
driver.get("https://www.zhihu.com/")
input("wait")
