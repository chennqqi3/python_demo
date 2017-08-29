import datetime
import re
import threading
import time
import urllib

import os
import requests
import threadpool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

pdf_dir = "E:\学习资料\电子书/gitbook/pdf/"
# mobi_dir = "E:\学习资料\电子书/gitbook/mobi/"

pool = threadpool.ThreadPool(10000)


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

    ebooks = []
    try_cnt = 0
    while True:
        try:
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
            for item_str in items_match:
                item_pattern = re.compile(
                    '"title":"(.*?)".*"mobi":"(.*?)".*"pdf":"(.*?)"', re.S)
                item_match = re.search(item_pattern, item_str)

                title = item_match.group(1)
                # 忽略的文件
                tit_com = re.compile(
                    '前端|前段|ios|Android|安卓|h5|css|js|script|html|swift|jquery|mac|asp|.net|php|scala|c\+\+|ruby'
                    '|c语言|c 语言|go 语言|go-|golang|c#|object-c|matlab|vue',
                    re.IGNORECASE)
                if re.search(tit_com, title):
                    print_th("跳过下载：" + title)
                    continue

                ebooks.append(EBookItem(i, title, item_match.group(2), item_match.group(3)))

            break
        except Exception:
            try_cnt += 1
            if try_cnt == 10:
                print_th('第' + i + '页，失败重试10次，放弃该页')
                break

            print_th('第' + i + '页，打开失败(' + str(try_cnt) + ')，重试')
            time.sleep(1)

    books_requests = threadpool.makeRequests(download_ebook, ebooks)
    [pool.putRequest(req) for req in books_requests]
    # books_pool.wait()


def download_ebook(ebook):
    print_th("开始下载第" + ebook.page + "页的:" + ebook.title + '.Pdf')
    retry_cnt = 0
    pdf_full_path = pdf_dir + ebook.title + '.pdf'

    while True:
        try:
            urllib.request.urlretrieve(ebook.pdf_url, pdf_full_path)
            # urllib.request.urlretrieve(ebook.mobi_url,
            #                            "C:/Users\weidongdong\Desktop/temp\python\demo\gitbook/mobi/" + ebook.title + ".mobi")
            print_th(ebook.title + ".Pdf下载完成。")
            break
        except Exception:
            retry_cnt += 1
            if retry_cnt == 10:
                print_th(ebook.title + '已重试10次，取消下载')
                os.remove(pdf_full_path)
                print_th(ebook.title + '.pdf已删除')
                break

            print_th(ebook.title + '异常重试(' + str(retry_cnt) + ')')
            time.sleep(1)

            # print_th("开始下载第" + ebook.page + "页的:" + ebook.title+'.mobi')
            # urllib.request.urlretrieve(ebook.pdf_url, mobi_dir + ebook.title+'.mobi')
            # # urllib.request.urlretrieve(ebook.mobi_url,
            # #                            "C:/Users\weidongdong\Desktop/temp\python\demo\gitbook/mobi/" + ebook.title + ".mobi")
            # print_th(ebook.title + ".mobi下载完成。")


def print_th(ori_str):
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('当前时间:' + cur_time + ',当前线程：' + threading.current_thread().name + ',' + ori_str)


if __name__ == '__main__':
    while True:
        if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') == '2017-08-10 23:00:00':
            print_th('开始执行。。')
            open_page()
            break
