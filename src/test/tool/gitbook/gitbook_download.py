import re
import threading
import urllib

import requests
import threadpool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

out_dir = "E:\学习资料\电子书/gitbook/"

pool = threadpool.ThreadPool(2000)


class EBookItem:
    def __init__(self, page, title, mobi_url, pdf_url):
        self.page = page
        self.title = title
        self.mobi_url = mobi_url
        self.pdf_url = pdf_url


def open_page():
    requests_pool = threadpool.makeRequests(loop_page, range(0, 1400))
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()

    print('全部下载完成。。')


def loop_page(i):
    i = str(i)
    page_url = 'https://www.gitbook.com/explore?page=' + i + '&lang=zh'
    print_th('打开第' + i + '页')
    get_res = requests.get(page_url, headers=headers)

    # print(get_res.text)
    pattern = re.compile(
        '{"id":".*?","status":".*?","name":".*?","title":".*?","description":".*?","public":.*?,"template":".*?","topics":.*?].*?"download":.*?"github":.*?}}}',
        re.S)
    items_match = re.findall(pattern, get_res.text)
    # print(len(items_match))
    if len(items_match) == 0:
        print_th("第" + i + "页面打开失败！")
        # loop_page_go = False

    ebooks = []
    for item_str in items_match:
        item_pattern = re.compile(
            '"title":"(.*?)".*"mobi":"(.*?)".*"pdf":"(.*?)"', re.S)
        item_match = re.search(item_pattern, item_str)

        title = item_match.group(1)
        # 忽略的文件
        tit_com = re.compile(
            '前端|前段|ios|Android|安卓|h5|css|js|script|html|swift|jquery|mac|asp|.net|php|scala|c\+\+|ruby'
            '|c语言|c 语言|go 语言|c#|object-c|matlab',
            re.IGNORECASE)
        if re.search(tit_com, title):
            print_th("跳过下载：" + title)
            continue

        ebooks.append(EBookItem(i, title + '.pdf', item_match.group(2), item_match.group(3)))

    # books_pool = threadpool.ThreadPool(10)
    books_requests = threadpool.makeRequests(download_ebook, ebooks)
    [pool.putRequest(req) for req in books_requests]
    # books_pool.wait()


def download_ebook(ebook):
    print_th("开始下载第" + ebook.page + "页的:" + ebook.title)
    urllib.request.urlretrieve(ebook.pdf_url, out_dir + ebook.title)
    # urllib.request.urlretrieve(ebook.mobi_url,
    #                            "C:/Users\weidongdong\Desktop/temp\python\demo\gitbook/mobi/" + ebook.title + ".mobi")
    print_th(ebook.title + "下载完成。")


def print_th(ori_str):
    print('当前线程：' + threading.current_thread().name + ',' + ori_str)


if __name__ == '__main__':
    open_page()
