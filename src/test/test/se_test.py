from selenium import webdriver


def auto():
    driver = webdriver.Firefox()
    driver.get('https://www.baidu.com/')
    driver.find_element_by_id('kw').send_keys('java')
    driver.find_element_by_id('su').submit()


if __name__ == '__main__':
    auto()
