import asyncio
import os
import threading

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
data = {"vacant_classroom": {'sh': {}, 'xyl': {}}, "valid_boya": {}}

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests

options = webdriver.ChromeOptions()  # 创建一个配置对象
options.add_argument("--headless")  # 开启无界面模式
options.add_argument("--disable-gpu")  # 禁用gpu

service = Service(
    executable_path=os.getenv("BANHANG_CHROMEDRIVER_PATH")
    if os.getenv("BANHANG_CHROMEDRIVER_PATH")
    else '.venv/Scripts/chromedriver.exe'
)
browser = webdriver.Chrome(service=service, options=options)


def check_and_login(browser):
    time.sleep(2)
    try:
        browser.switch_to.frame("loginIframe")
        (browser.find_element(By.ID, 'unPassword')
         .send_keys(os.getenv("BUAA_USERNAME")))
        (browser.find_element(By.ID, 'pwPassword')
         .send_keys(os.getenv("BUAA_PASSWORD")))
        browser.find_element(By.XPATH, '//*[@id="content-con"]/div[1]/div[7]/input').click()
    except:
        print('no need login')
    browser.switch_to.default_content()
    time.sleep(2)


def get_void_class():
    browser.get('https://app.buaa.edu.cn/site/classRoomQuery/index')
    check_and_login(browser)
    sess = requests.Session()
    cookies = browser.get_cookies()
    # 填充cookies
    for cookie in cookies:
        sess.cookies.set(cookie['name'], cookie['value'])
    date = time.strftime('%Y-%m-%d', time.localtime())
    res_sh = sess.get(f'https://app.buaa.edu.cn/buaafreeclass/wap/default/search1?xqid=2&floorid=&date={date}')
    data1 = (json.loads(res_sh.text))
    res_xyl = sess.get(f'https://app.buaa.edu.cn/buaafreeclass/wap/default/search1?xqid=1&floorid=&date={date}')
    data2 = (json.loads(res_xyl.text))
    return {'sh': data1['d']['list'], 'xyl': data2['d']['list']}


@scheduler.scheduled_job('interval', minutes=5)
async def update_vacant_classroom():
    global data
    print('updatting vacant classroom')
    data['vacant_classroom'] = get_void_class()


thread = threading.Thread(target=lambda: asyncio.run(update_vacant_classroom()))
thread.start()
