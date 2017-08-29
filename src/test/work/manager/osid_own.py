import time

from selenium import webdriver

# 使用谷歌浏览器打开
driver = webdriver.Chrome()
# 最大化
driver.maximize_window()


# def get_account():
#     print('从本地账号文件读取账号密码')
#     # 账号密码
#     with open('../account.txt', 'r') as f:
#         pattern = re.compile('name:(.*?)\npwd:(.*?)$', re.S)
#
#         match = re.search(pattern, f.read())
#
#         if not match:
#             print("账号文件格式不匹配")
#             exit()
#
#     print('本地账号密码读取成功！')
#     # return match


def login():
    # account_match = get_account()
    # 登录页
    taobao_login_url = 'https://passport.qiku.com/index.jsp?appid=1010060&callback=http://dev.manager.ota.360os.com/ota-manager-api/v1/login'

    # 打开登录页
    driver.get(taobao_login_url)

    # 点击蒙层
    driver.find_element_by_class_name('prompt').click()

    # 用户名
    driver.find_element_by_name('account').send_keys('1173456493@qq.com')

    # 密码
    driver.find_element_by_name('password').send_keys('5880290*')

    # 10秒时间手动输验证码
    time.sleep(10)

    # 登录
    driver.find_element_by_class_name('quc-submit').click()

    # sleep等页面完全跳转
    time.sleep(3)


def version():
    # 版本发布
    driver.find_element_by_xpath("//p[text()='版本发布']").click()
    time.sleep(1)
    # --创建版本
    driver.find_element_by_xpath("//p[text()='创建版本']").click()
    time.sleep(1)
    # --测试中的版本
    driver.find_element_by_xpath("//p[text()='测试中的版本']").click()
    time.sleep(1)
    # --测试通过的版本
    driver.find_element_by_xpath("//p[text()='测试通过的版本']").click()
    time.sleep(1)
    # --灰度审批
    driver.find_element_by_xpath("//p[text()='灰度审批']").click()
    time.sleep(1)
    # --灰度发布的版本
    driver.find_element_by_xpath("//p[text()='灰度发布的版本']").click()
    time.sleep(1)
    # --全量审批
    driver.find_element_by_xpath("//p[text()='全量审批']").click()
    time.sleep(1)
    # --全量发布的版本
    driver.find_element_by_xpath("//p[text()='全量发布的版本']").click()
    time.sleep(1)


def manage():
    # 系统管理
    driver.find_element_by_xpath("//p[text()='系统管理']").click()
    time.sleep(1)
    # --账号管理
    driver.find_element_by_xpath("//p[text()='帐号管理（超级管理员）']").click()
    time.sleep(1)
    # --角色管理
    driver.find_element_by_xpath("//p[text()='角色管理']").click()
    time.sleep(1)
    # --菜单管理
    driver.find_element_by_xpath("//p[text()='菜单管理']").click()
    time.sleep(1)
    # --设置OS项目管理员
    driver.find_element_by_xpath("//p[text()='设置OS项目管理员']").click()
    time.sleep(1)
    # --项目角色管理
    driver.find_element_by_xpath("//p[text()='项目角色管理']").click()
    time.sleep(1)


if __name__ == '__main__':
    login()

    version()

    manage()
