from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"}
wait = WebDriverWait(browser,10)

def search():
    browser.get('https://www.taobao.com/')
    # 输入框
    element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
    )
    # 搜索按钮
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_SearchForm > button')))






