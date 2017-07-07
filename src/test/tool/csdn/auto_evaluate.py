# 自动填写csdn评价
import re

import requests


# 打开登录页面获取页面上的lt和execution两个参数
def open_login_page():
    global login_url, headers, session
    # 登录地址
    login_url = 'https://passport.csdn.net/account/login?from=http%3A%2F%2Fmy.csdn.net%2Fmy%2Fmycsdn'
    #
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    # 使用session保持会话状态
    session = requests.session()
    # 先使用get请求获取lt和execution两个参数
    # get_res = requests.get(login_url, headers=headers)
    get_res = session.get(login_url, headers=headers)
    pattern = re.compile(
        '<input type="hidden" name="lt" value="(.*?)" />.*<input type="hidden" name="execution" value="(.*?)" />', re.S)
    match = re.search(pattern, get_res.text)
    if not match:
        print("登录页面打开失败！")
        exit()

    return match


# 读取本地文件获取CSDN的账号和密码
def get_account():
    # 账号密码
    with open('account.txt', 'r') as f:
        pattern = re.compile('name:(.*?)\npwd:(.*?)$', re.S)

        match = re.search(pattern, f.read())

        if not match:
            print("账号文件格式不匹配")
            exit()

    return match


# 登录
def login():
    login_data = {'username': account_match.group(1), 'password': account_match.group(2),
                  'lt': login_match.group(1),
                  'execution': login_match.group(2),
                  '_eventId': 'submit'}
    # login_res = requests.post(login_url, login_data, headers=headers)
    login_res = session.post(login_url, headers=headers, data=login_data)
    # print(login_res.status)
    if not 200 == login_res.status_code:
        print('登录失败！')
        exit()
        # print(login_res.headers['Set-Cookie'])


# 打开下载列表页面
def open_download_page():
    # 获取下载列表
    download_list_url = 'http://download.csdn.net/my/downloads'
    download_list_res = session.get(download_list_url, headers=headers)
    print(download_list_res.text)


if __name__ == '__main__':
    login_match = open_login_page()

    account_match = get_account()

    login()

    open_download_page()
