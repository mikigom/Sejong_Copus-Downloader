from selenium import webdriver
import re
import sys
import time

def download(login_id, login_pw, w_time):
    def url_open_wt_driver(url):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(url)
        time.sleep(1)
        return driver

    def login_wt_driver(driver, login_id, login_pw):
        id_form = driver.find_element_by_name('loginId')
        id_form.send_keys(login_id)
        time.sleep(0.5)
        pw_form = driver.find_element_by_id("password")
        pw_form.send_keys(login_pw)
        time.sleep(0.5)
        driver.execute_script('javascript:doLogin()')
        return driver

    def get_last_page(driver):
        driver.get('https://ithub.korean.go.kr/user/corpus/corpusManager.do')
        driver.execute_script('javascript:getList(1)')
        time.sleep(1)
        go_list = driver.find_element_by_xpath('.//span[@class = "last"]')
        get_last_text = go_list.get_attribute('innerHTML')
        return int(re.findall(r'onclick="goPage\((.*?)\);', get_last_text)[0]), driver

    driver = url_open_wt_driver('https://ithub.korean.go.kr/user/login.do')
    driver = login_wt_driver(driver, login_id, login_pw)

    current_page = 1
    page_last, driver = get_last_page(driver)
    w = float(w_time)

    for i in range(current_page, page_last + 1):
        current_page = i
        time.sleep(w)
        driver.get('https://ithub.korean.go.kr/user/corpus/corpusManager.do')
        time.sleep(3*w)
        driver.execute_script('javascript:getList(' + str(i) +')')
        time.sleep(10*w)
        content_table = driver.find_element_by_xpath('.//table[@class = "tbl_list"]')
        content_table_text = content_table.get_attribute('innerHTML')
        content_list = re.findall(r'a href="javascript:doView\((.*?)\);"', content_table_text)
        for _, j in enumerate(content_list):
            time.sleep(w)
            driver.get('https://ithub.korean.go.kr/user/corpus/corpusManager.do')
            time.sleep(w)
            driver.execute_script('javascript:doView(' + j +')')
            time.sleep(w)
            driver.find_element_by_name("orgFileSeq").click()
            time.sleep(w)
            driver.execute_script('javascript:showAgreementDownloadLayer()')
            time.sleep(w)
            driver.find_element_by_name("agreementYn").click()
            time.sleep(w)
            driver.execute_script('doDownloadFile()')

if __name__ == '__main__':
    download(sys.argv[1], sys.argv[2], sys.argv[3])
