import os
import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def start_to_work():
    with open('travel_with_English.csv', 'w', encoding="utf-8") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        with open("track_id.csv", "r", encoding="utf-8") as csvfile:
            # 读取csv文件，返回的是迭代类型
            read = csv.reader(csvfile)
            driver = "C:\Program Files\internet explorer\IEDriverServer.exe"
            os.environ["webdriver.ie.driver"] = driver
            driver = webdriver.Ie()
            for i in read:
                url = 'https://www.ximalaya.com/waiyu/2990376/' + i[0]

                # ele = driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
                driver.get(url)
                try:
                    title = driver.find_element_by_css_selector(".title-wrapper")
                    article = driver.find_element_by_css_selector("article")
                    more = driver.find_element_by_class_name('blur')
                    # print(more)
                    # 文字过多被折叠，需要调用js点击展开更多
                    if more:
                        driver.execute_script('document.getElementsByClassName("blur")[0].click();')
                    sub_title = title.text
                    sub_text = article.text
                    csvwriter.writerow([url, sub_title, sub_text])
                    # print(sub_text)
                except NoSuchElementException:
                    csvwriter.writerow([url, 'error'])
                    continue


if __name__ == '__main__':
    start_to_work()