# 自动填写csdn评价
import http
import re
import urllib

import requests


def get_download_list(headers, opener):
    # 获取下载列表
    download_list_url = 'http://download.csdn.net/my/downloads'

    # cookies = {
    #     # 'UserInfo': 'LHQJ2qvxiRaOx5Zr7bBZZpFt3fMfFIS5MR2C8vwvYg2cxxrqsRDKKIS2i%2F%2B9tkWRnQdqOSTKAB0OE20Lesbmi1dQp%2B9hBFNHiPc4pwiqQE08oIJrFcltyLT4DCCNew3i5MWvkUtsyUfzyNKDGHnsuQ%3D%3D',
    #     # 'uuid_tt_dd': '1888378061935299429_20170630',
    #     '__message_sys_msg_id': '0',
    #     '__message_gu_msg_id': '0',
    #     '__message_cnel_msg_id': '0',
    #     '__message_district_code': '110000',
    #     '__message_in_school': '0',
    #     # 'Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac': '1498812796,1499054579',
    #     # 'Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac': '1499062059',
    #     'dc_tos': 'osi3oq',
    #     'dc_session_id': '1499061930614',
    #     'UserName': 'donglaidongwang524',
    #     'UserInfo': 'LHQJ2qvxiRaOx5Zr7bBZZpFt3fMfFIS5MR2C8vwvYg2cxxrqsRDKK6S2i%2F%2B9tkWRnQdqOSTKAB0OE20Lesbmi1dQp%2B9hBFNHiPc4pwiqQE08oIJrFcltyLT4DCCNew3i5MWvkUtsyUfzyNKDGHnsuQ%3D%3D',
    #     'UserNick': '%E5%86%AC%E6%9D%A5%E5%86%AC%E5%BE%80',
    #     'AU': 'E67',
    #     'UN': 'donglaidongwang524',
    #     'UE': '843833533@qq.com',
    #     'BT': '1499062066621',
    #     'access-token': '12f6d355-7659-4ede-9f36-5f6f41b75a7b'}

    # requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
    # download_list_res = requests.get(download_list_url, headers=headers, cookies=cookies)
    opener.addheaders = [("User-Agent",
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36")]
    download_list_res = opener.open(download_list_url)
    print(download_list_res.read().decode())
    # print(download_list_res.text)


def login(login_url, lt, execution, cookie, opener):
    # 账号密码
    login_data = {'username': '843833533@qq.com', 'password': '5880290',
                  'lt': lt,
                  'execution': execution,
                  '_eventId': 'submit'}

    post_data = urllib.parse.urlencode(login_data).encode()

    # headers['Content-Length'] = '116'
    # headers['Content-Type'] = 'application/x-www-form-urlencoded'
    # headers['Origin'] = 'https://passport.csdn.net'

    opener.addheaders = [("User-Agent",
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36")]
    login_res = opener.open(login_url, post_data)
    cookie.save(ignore_discard=True, ignore_expires=True)
    # login_res = opener.open(urllib.request.Request(login_url, post_data, headers))

    # login_res = requests.post(login_url, login_data, headers=headers)
    # print(login_res.status)
    if 200 == login_res.status:
        print('登录成功！')
        #
        # print(login_res.headers['Set-Cookie'])


if __name__ == '__main__':

    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)

    # 登录地址
    login_url = 'https://passport.csdn.net/account/login?from=http%3A%2F%2Fmy.csdn.net%2Fmy%2Fmycsdn'
    #
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate,sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Content-Length': '116',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'JSESSIONID=D7689FFDDDDE4DF1AD9645F63608A0BE.tomcat2; '
        #           'uuid_tt_dd=1888378061935299429_20170630; '
        #           'JSESSIONID=D7689FFDDDDE4DF1AD9645F63608A0BE.tomcat2; __message_sys_msg_id=0; '
        #           '__message_gu_msg_id=0; __message_cnel_msg_id=0; __message_district_code=110000; '
        #           '__message_in_school=0; UN=donglaidongwang524; UE="843833533@qq.com"; BT=1498817497363; '
        #           'LSSC=LSSC-2622997-yGKz4v5i00QsApSNcdrR4ea7vQMrx4-passport.csdn.net; '
        #           'Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1498812796; '
        #           'Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1498817538; dc_tos=oscv0i; '
        #           'dc_session_id=1498817499772',
        'Host': 'passport.csdn.net',
        # 'Origin': 'https://passport.csdn.net',
        'Referer': 'http://my.csdn.net/my/mycsdn',
        'Upgrade-Insecure-Requests': '1'}

    # session = requests.session()

    # 先使用get请求获取lt和execution两个参数
    get_res = requests.get(login_url, headers=headers)
    # print(get_res.cookies)
    #
    pattern = re.compile(
        '<input type="hidden" name="lt" value="(.*?)" />.*<input type="hidden" name="execution" value="(.*?)" />', re.S)

    match = re.search(pattern, get_res.text)
    # #
    if not match:
        print("登录页面打开失败！")
        exit()

    lt = match.group(1)
    execution = match.group(2)
    # print(lt + ',' + execution)

    login(login_url, match.group(1), match.group(2), cookie, opener)

    get_download_list(headers, opener)
