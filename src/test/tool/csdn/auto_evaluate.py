# 自动填写csdn评价
import re
# 登录地址
import threading
import time

import requests

from src.test.tool.csdn.download_item import DownloadItem

login_url = 'https://passport.csdn.net/account/login?from=http%3A%2F%2Fmy.csdn.net%2Fmy%2Fmycsdn'

# 下载列表页面地址
domain = 'http://download.csdn.net'
download_list_url = domain + '/my/downloads'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

# 使用session保持会话状态
session = requests.session()

success_cnt = 0
lock = threading.Lock()


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

    download_item_list = []

    match_page = re.search(re.compile('<div class="page_nav">共.*?个.*&nbsp; 共(.*?)页', re.S), download_list_res.text)
    page_cnt = match_page.group(1)
    print('共有' + page_cnt + '页')

    # 循环每一个，获取待评价的项的访问链接到数组
    page_loop(page_cnt, download_item_list)
    # print(download_item_list)

    print('共有' + str(len(download_item_list)) + '项待评论资源')

    ls_thread = []
    # 循环数组，访问待评价页面
    for download_item in download_item_list:
        # open_item_url(download_item)
        # submit_evaluate(download_item.id)
        # 每次评论需要间隔60s
        # time.sleep(60)

        thr = threading.Thread(target=submit_evaluate, args=(download_item.id,))
        thr.start()
        ls_thread.append(thr)

    # 等待执行完毕
    for th in ls_thread:
        th.join()

    print('脚本执行完成！成功评论'+str(success_cnt)+'条资源')


# 打开下载项页面
# def open_item_url(download_item):
#     print('打开下载项页面')
#     download_page_res = session.get(domain + download_item.uri, headers=headers)
#
#     if 200 == download_page_res.status_code:
#         print(str(download_item.id) + '详情页打开成功')

# 提交评价
# 对于跨域请求，Python不需要模拟jsonp，直接同普通方式请求即可
def submit_evaluate(id):
    # 提交参数
    # jsonpcallback = ''
    sourceid = id
    # 评论内容
    content = '很好的学习资料，谢谢分享'
    txt_validcode = 'undefined'
    # 打分
    rating = str(5)
    # 应该是提交的时间戳
    t = str(int(round(time.time() * 1000)))
    # 应该是打开页面的时间戳
    _ = str(int(round(time.time() * 1000)))

    # 提交URL
    evaluate_url = 'http://download.csdn.net/index.php/comment/post_comment' \
                   '?sourceid=' + sourceid + \
                   '&content=' + content + \
                   '&txt_validcode=' + txt_validcode + \
                   '&rating=' + rating + \
                   '&t=' + t + \
                   '&_=' + _
    evaluate_res = session.get(evaluate_url, headers=headers)

    global success_cnt
    if 200 == evaluate_res.status_code:
        match_evlu = re.search(re.compile('{"succ":1}'), evaluate_res.text)
        if match_evlu:
            print(id + '评价成功！')
            lock.acquire()
            try:
                success_cnt += 1
            finally:
                lock.release()


# 打开每页列表
def page_loop(page_cnt, download_item_list):
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
            get_item_url_by_li(download_item_list, lis)


# 循环每个下载项，并将子项的打开链接保存在数组中
def get_item_url_by_li(download_item_list, lis):
    print('解析下载项的打开链接')
    for li in lis:
        # 匹配每一项里的"立即评价"的链接
        match_li = re.search(
            re.compile(
                '<h3>.*href="/detail/.*/(.*?)".*</h3>.*<div class="flag">.*<a target="_blank" href="(/detail/.*?#comment)">立即评价</a>',
                re.S), li)
        if match_li:
            # print(match_li.group(1))
            # 保存评价地址到数组
            download_item_list.append(DownloadItem(match_li.group(1), match_li.group(2)))


if __name__ == '__main__':
    login_match = open_login_page()

    account_match = get_account()

    login()

    open_download_page()
