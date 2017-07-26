# 登录地址
import ssl

import requests

login_url = 'https://kyfw.12306.cn/otn/login/init'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

# 使用session保持会话状态
session = requests.session()

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


# 打开登录页面获取页面上的参数
def open_login_page():
    print('打开登录页面，尝试解析登录所需的流水号')

    get_res = session.get(login_url, headers=headers)
    print(get_res.text)
    # pattern = re.compile(
    #     '<input type="hidden" name="lt" value="(.*?)" />.*<input type="hidden" name="execution" value="(.*?)" />', re.S)
    # match = re.search(pattern, get_res.text)
    # if not match:
    #     print("登录页面打开失败！")
    #     exit()
    #
    # print('获取登录所需的流水号成功！')
    # return match


if __name__ == '__main__':
    open_login_page()
