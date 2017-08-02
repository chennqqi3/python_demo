# 自动申请淘宝试用
import re
import time
from selenium import webdriver

# 试用谷歌浏览器打开
driver = webdriver.Chrome()
# 最大化
driver.maximize_window()


def get_account():
    print('从本地账号文件读取账号密码')
    # 账号密码
    with open('../account.txt', 'r') as f:
        pattern = re.compile('name:(.*?)\npwd:(.*?)$', re.S)

        match = re.search(pattern, f.read())

        if not match:
            print("账号文件格式不匹配")
            exit()

    print('本地账号密码读取成功！')
    return match


def login():
    account_match = get_account()
    # 登录页并指向试用页面
    taobao_login_url = 'https://login.taobao.com/member/login.jhtml?spm=a1z0i.1000799.754894437.1.5dcec31cy2KU7M&f=top&redirectURL=https%3A%2F%2Ftry.taobao.com%2F'

    # 打开登录页
    driver.get(taobao_login_url)

    # 点击由二维码显示为输入用户名密码
    driver.find_element_by_id('J_Quick2Static').click()

    # 用户名
    driver.find_element_by_name('TPL_username').send_keys(account_match.group(1))

    # 密码
    driver.find_element_by_name('TPL_password').send_keys(account_match.group(2))

    # 登录
    driver.find_element_by_id('J_SubmitStatic').click()


def try_use():
    # sleep一秒钟，等页面完全跳转
    time.sleep(1)
    print(driver.title)

    # 点击”手机数码“
    elec = driver.find_element_by_partial_link_text('手机数码')
    elec.click()

    time.sleep(1)
    # 找所有"申请试用"按钮
    # for try_btn in driver.find_elements_by_class_name('tb-try-button'):
        # try_btn.click()
        #
        # time.sleep(2)
        # driver.find_element_by_class_name('J_TbTry_Apply').click()


if __name__ == '__main__':
    login()
    try_use()
