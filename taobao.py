import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

# 提高效率
SERVICE_ARGS = ['--load-images=false','--disk-cache=true']

browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400, 900)
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.taobao.com')
        _input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="q"]'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search'))
        )
        _input.send_keys('美食')
        submit.click()
        # print("click")
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    try:
        _input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input.input:nth-child(2)'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.btn:nth-child(4)'))
        )
        _input.clear()
        _input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'li.active > span:nth-child(1)'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('.m-itemlist .items .item').items()
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


def main():
    try:
        total = search()
        # print(total)
        total = int(re.compile('(\d+)').search(total).group(1))
        print(total)
        # search()
        for i in range(2,total+1):
            next_page(i)
    finally:
        browser.close()

if __name__ == '__main__':
    main()
