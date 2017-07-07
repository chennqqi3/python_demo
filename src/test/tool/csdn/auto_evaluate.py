# 自动填写csdn评价
import re
# 登录地址
import time

import requests

login_url = 'https://passport.csdn.net/account/login?from=http%3A%2F%2Fmy.csdn.net%2Fmy%2Fmycsdn'

# 下载列表页面地址
domain = 'http://download.csdn.net'
download_list_url = domain + '/my/downloads'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

# 使用session保持会话状态
session = requests.session()


# 打开登录页面获取页面上的lt和execution两个参数
def open_login_page():
    print('打开登录页面，尝试解析登录所需的流水号')
    # global login_url, headers, session
    # 先使用get请求获取lt和execution两个参数
    # get_res = requests.get(login_url, headers=headers)
    get_res = session.get(login_url, headers=headers)
    pattern = re.compile(
        '<input type="hidden" name="lt" value="(.*?)" />.*<input type="hidden" name="execution" value="(.*?)" />', re.S)
    match = re.search(pattern, get_res.text)
    if not match:
        print("登录页面打开失败！")
        exit()

    print('获取登录所需的流水号成功！')
    return match


# 读取本地文件获取CSDN的账号和密码
def get_account():
    print('从本地账号文件读取账号密码')
    # 账号密码
    with open('account.txt', 'r') as f:
        pattern = re.compile('name:(.*?)\npwd:(.*?)$', re.S)

        match = re.search(pattern, f.read())

        if not match:
            print("账号文件格式不匹配")
            exit()

    print('本地账号密码读取成功！')
    return match


# 登录
def login():
    print('开始尝试登录')
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

    print('登录成功')


# 打开下载列表页面
def open_download_page():
    print('打开下载列表页面')
    download_list_res = session.get(download_list_url, headers=headers)

    if 200 == download_list_res.status_code:
        print('下载页面打开成功')
    # print(download_list_res.text)

    download_url_list = []

    match_page = re.search(re.compile('<div class="page_nav">共.*?个.*&nbsp; 共(.*?)页', re.S), download_list_res.text)
    page_cnt = match_page.group(1)
    print('共有' + page_cnt + '页')

    # 循环每一个，获取待评价的项的访问链接到数组
    page_loop(page_cnt, download_url_list)
    # print(download_url_list)

    # 循环数组，访问待评价页面
    for download_uri in download_url_list:
        download_page_res = session.get(domain + download_uri, headers=headers)


def submit_evaluate(id):
    # 提交参数
    jsonpcallback = ''
    sourceid = id
    # 评论内容
    content = '很好的学习资料，谢谢分享'
    txt_validcode = 'undefined'
    # 打分
    rating = 5
    # 应该是提交的时间戳
    t = str(int(round(time.time() * 1000)))
    # 应该是打开页面的时间戳
    _ = str(int(round(time.time() * 1000)))

    # 提交URL
    evaluate_url = 'http://download.csdn.net/index.php/comment/post_comment?jsonpcallback=jQuery111104839852002988987_1499424460935&sourceid=9748056&content=%E8%B0%A2%E8%B0%A2%E5%88%86%E4%BA%AB%EF%BC%8C%E5%BE%88%E5%A5%BD%E7%9A%84%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99&txt_validcode=undefined&rating=5&t=1499424636324&_=1499424460940'


# 打开每页列表
def page_loop(page_cnt, download_url_list):
    for page in range(0, int(page_cnt)):
        page_s = str(page + 1)
        print('打开第' + page_s + '页')
        download_list_res = session.get(download_list_url + '/' + page_s, headers=headers)

        if 200 == download_list_res.status_code:
            print('第' + page_s + '页面打开成功')
            # 匹配所有的li
            lis = re.findall(re.compile('<li>.*?<div class="card clearfix">(.*?)</li>', re.S | re.M),
                             download_list_res.text)

            # 一共有几个下载文件项
            # lis_len = len(lis)
            # print(lis_len)
            # print(lis)

            # 获取个待评价项的链接
            get_item_url_by_li(download_url_list, lis)


# 循环每个下载项，并将子项的打开链接保存在数组中
def get_item_url_by_li(download_url_list, lis):
    print('解析下载项的打开链接')
    for li in lis:
        # 匹配每一项里的"立即评价"的链接
        match_li = re.search(
            re.compile('<div class="flag">.*<a target="_blank" href="(/detail/.*?#comment)">立即评价</a>', re.S), li)
        if match_li:
            # print(match_li.group(1))
            # 保存评价地址到数组
            download_url_list.append(match_li.group(1))


if __name__ == '__main__':
    login_match = open_login_page()

    account_match = get_account()

    login()

    open_download_page()
