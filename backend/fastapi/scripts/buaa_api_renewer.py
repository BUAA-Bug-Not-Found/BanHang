import asyncio
import os
import threading

from apscheduler.schedulers.asyncio import AsyncIOScheduler

ENABLE = True

scheduler = AsyncIOScheduler()
data = {"vacant_classroom": {'sh': {}, 'xyl': {}}, "boya": []}

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import threading
lock = threading.Lock()

options = webdriver.ChromeOptions()  # 创建一个配置对象
options.add_argument("--headless")  # 开启无界面模式
options.add_argument("--disable-gpu")  # 禁用gpu
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1050")
if ENABLE and (os.getenv("BANHANG_DATABASE_PATH") is None):
    service = Service(
        executable_path=os.getenv("BANHANG_CHROMEDRIVER_PATH")
        if os.getenv("BANHANG_CHROMEDRIVER_PATH")
        else '.venv/Scripts/chromedriver.exe'
    )
    browser = webdriver.Chrome(service=service, options=options)
else:
    service = None
    browser = None


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


def get_boya():
    browser.get("https://bykc.buaa.edu.cn/")
    check_and_login(browser)
    time.sleep(5)
    browser.find_element(By.XPATH, '/html/body/main/div[1]/aside/div/ul/li[3]/div').click()
    time.sleep(1)
    browser.find_element(By.XPATH, '/html/body/main/div[1]/aside/div/ul/li[3]/div/ul/li[1]').click()
    time.sleep(1)
    xpath_map = {'state': '/td[1]/div/span',
                 'name': '/td[2]',
                 'type': '/td[3]/span',
                 'position': '/td[4]/div[1]',
                 'teacher': '/td[4]/div[2]',
                 'school': '/td[4]/div[3]',
                 'start_time': '/td[5]/div[1]',
                 'end_time': '/td[5]/div[2]',
                 'select_start_time': '/td[7]/div/div[2]',
                 'select_end_time': '/td[7]/div/div[3]',
                 'unselect_end_time': '/td[7]/div/div[4]',
                 'selected_number': '/td[9]/span[1]',
                 'capacity_number': '/td[9]/span[3]'
                 }
    root_path = "/html/body/main/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[2]/table/tbody/tr[{}]"
    resultList = []
    for i in range(1, 21):
        resultList.append({})
        result = resultList[-1]
        for key in xpath_map:
            try:
                result[key] = browser.find_element(By.XPATH, root_path.format(i)+xpath_map[key]).text
            except:
                result[key] = ''
    return resultList

@scheduler.scheduled_job('interval', minutes=5)
async def update_vacant_classroom():
    global data
    print('updatting vacant classroom')
    if ENABLE:
        lock.acquire()
        try:
            data['vacant_classroom'] = get_void_class()
        finally:
            lock.release()

@scheduler.scheduled_job('interval', minutes=5)
async def update_boya_info():
    global data
    print('updatting boya')
    if ENABLE:
        lock.acquire()
        try:
            data['boya'] = get_boya()
        finally:
            lock.release()

if os.getenv("BANHANG_DATABASE_PATH") is None:
    thread = threading.Thread(target=lambda: asyncio.run(update_vacant_classroom()))
    thread.start()
    thread = threading.Thread(target=lambda: asyncio.run(update_boya_info()))
    thread.start()