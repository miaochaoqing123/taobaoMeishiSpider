from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# driver = webdriver.Chrome()
# 把config.py里设置的放入到PhantomJS
driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)  # 用PhantomJS让程序后台运行
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
wait = WebDriverWait(driver, 10)

driver.set_window_size(1366, 768)

# 模拟输入美食和点击搜索
def search():
    print("正在搜索.....")
    try:
        driver.get('https://www.taobao.com/')
        # 输入框
        input_tb = wait.until(
            EC.presence_of_element_located((By.ID, 'q'))
        )
        # 搜索按钮
        submit_tb = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        # driver.find_element_by_css_selector('#J_TSearchForm > div.search-button > button').click()
        input_tb.send_keys('美食')
        submit_tb.click()
        # sleep(3)
        # 取出总页数
        sleep(2)
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()  # 调用下面的解析方法
        total = total.text
        total = int(re.compile('(\d+)').search(total).group(1))
        return total
    except TimeoutError:
        return search()

# 下一页
def next_page(page_number):
    print('正在翻第 '+ str(page_number) + ' 页')
    try:
        # 找到页码的输入框
        input_tb = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        # 页码确定按钮
        submit_tb = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        # driver.find_element_by_css_selector('#J_TSearchForm > div.search-button > button').click()
        input_tb.clear()  # 先清除里面的数字
        input_tb.send_keys(page_number)  # 再输入页码
        submit_tb.click()  # 点击确认,转入到下一页
        sleep(2)
        # 判断高亮是否为本页
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutError:
        # 如果出现TimeoutError的错误,则继续
        next_page(page_number)

# 解析内容
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = driver.page_source  # 获得网页源码
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()  # 得到所有的items
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print("存储到MONGODB成功",result)
    except Exception:
        print("存储到MONGODB失败",result)




def main():
    # 异常处理:无论程序有无出现异常,最后都要关闭浏览器
    try:
        total = search()
        print(total)
        # 用for循环遍历页码
        for i in range(2,total + 1):
            next_page(i)
    except Exception:
        print("出错了...")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()




