import re
import threading
import urllib

import requests

from src.test.tool.gitbook.ebook_item import EBookItem

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

out_dir = "E:\学习资料\电子书\gitbook"


def open_page():
    ebooks = []
    i = 0
    # page_url = 'https://www.gitbook.com/explore?page=0&lang=zh'
    # for i in range(0, 100):
    while i >= 0:
        page_url = 'https://www.gitbook.com/explore?page=' + str(i) + '&lang=zh'
        print('打开第' + str(i) + '页')
        get_res = requests.get(page_url, headers=headers)

        # print(get_res.text)
        pattern = re.compile(
            '{"id":".*?","status":".*?","name":".*?","title":".*?","description":".*?","public":.*?,"template":".*?","topics":.*?].*?"download":.*?"github":.*?}}}',
            re.S)
        items_match = re.findall(pattern, get_res.text)
        # print(len(items_match))
        if len(items_match) == 0:
            print("第" + str(i) + "页面打开失败！")
            break

        for item_str in items_match:
            item_pattern = re.compile(
                '"title":"(.*?)".*"mobi":"(.*?)".*"pdf":"(.*?)"', re.S)
            item_match = re.search(item_pattern, item_str)

            ebooks.append(EBookItem(item_match.group(1), item_match.group(2), item_match.group(3)))
            # return match

        i = i + 1
        # while结束

    print("循环结束，一共抓取到" + str(len(ebooks)) + "本电子书")
    print("开始下载。。。。")

    # 循环下载项
    ls_thread = []
    # 循环数组，访问待评价页面
    for ebook in ebooks:
        # 忽略的文件
        tit_com = re.compile(
            '前端|前段|ios|Android|安卓|h5|css|js|javascript|html|swift|jquery|mac|asp|.net|go|php|scala|c\+\+|ruby|c语言',
            re.IGNORECASE)
        title = ebook.title
        if re.search(tit_com, title):
            print("跳过下载：" + title)
            continue

        thr = threading.Thread(target=download_ebook, args=(ebook,))
        thr.start()
        ls_thread.append(thr)

    # 等待执行完毕
    for th in ls_thread:
        th.join()

    print('全部下载完成。。')


def download_ebook(ebook):
    print("开始下载:" + ebook.title)
    urllib.request.urlretrieve(ebook.pdf_url, out_dir + ebook.title + ".pdf")
    # urllib.request.urlretrieve(ebook.mobi_url,
    #                            "C:/Users\weidongdong\Desktop/temp\python\demo\gitbook/mobi/" + ebook.title + ".mobi")
    print(ebook.title + "下载完成。")


if __name__ == '__main__':
    open_page()
