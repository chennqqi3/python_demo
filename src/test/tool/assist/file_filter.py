# 过滤out_log.txt日志内容，将"下载完成"的文件保留，其余的删除
import datetime
import re
import threading

import os
import threadpool

file_dir = "E:\学习资料\电子书/gitbook/pdf/"

del_n = 0


def file_filter():
    global filename_list, del_n
    comp = re.compile('.*,(.*)下载完成', re.S)
    filename_list = []
    with open('out_log.txt', 'rb') as f:
        for line in f.readlines():
            decode = line.decode('utf-8')
            search = re.search(comp, decode)
            if search:
                filename_list.append(search.group(1).upper())
                # print(search.group(1))
    print(len(filename_list))
    # print(filename_list)
    pool = threadpool.ThreadPool(1000)
    files = os.listdir(file_dir)
    requests_pool = threadpool.makeRequests(del_file, files)
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()

    print('共删除' + str(del_n) + '个文件')


def del_file(x):
    # for x in os.listdir(file_dir):
    title = x.title()
    if title.upper() in filename_list:
        print_th(title + '下载完成，不删除')
        # continue
    else:
        try:
            os.remove(os.path.join(file_dir, x))
            print(title + '删除成功')
            # del_n += 1
        except Exception:
            print_th(title + '删除失败')
            # continue


def print_th(ori_str):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('当前时间:' + time + ',当前线程：' + threading.current_thread().name + ',' + ori_str)


if __name__ == '__main__':
    file_filter()
