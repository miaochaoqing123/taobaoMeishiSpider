from time import sleep
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
wait = WebDriverWait(driver, 10)

# 模拟输入美食和点击搜索
def search():
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
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        # print(total)
        total = total.text
        # 正则匹配
        total = int(re.compile('(\d+)').search(total).group(1))
        # print(total)
        # sleep(3)
        # driver.quit()
        return total
    except TimeoutError:
        return search()

# 下一页
def next_page(page_number):
    try:
        input_tb = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        # 搜索按钮
        submit_tb = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        # driver.find_element_by_css_selector('#J_TSearchForm > div.search-button > button').click()
        input_tb.clear()
        input_tb.send_keys(page_number)
        submit_tb.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
    except TimeoutError:
        next_page(page_number)

def main():
    total = search()
    print(total)
    for i in range(2,total + 1):
        next_page(i)

if __name__ == '__main__':
    main()




