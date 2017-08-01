# 过滤out_log.txt日志内容，将"下载完成"的文件保留，其余的删除
import re

import os

file_dir = "E:\学习资料\电子书/gitbook/"

comp = re.compile('^(.*)下载完成', re.S)

filename_list = []
with open('out_log.txt', 'rb') as f:
    for line in f.readlines():
        decode = line.decode('utf-8')
        search = re.search(comp, decode)
        if search:
            filename_list.append(search.group(1) + '.Pdf')
            # print(search.group(1))

print(len(filename_list))
# print(filename_list)
del_n = 0
for x in os.listdir(file_dir):
    title = x.title()
    if title in filename_list:
        print(title+'下载完成，不删除')
        continue
    else:
        try:
            os.remove(os.path.join(file_dir, x))
            print(title + '删除成功')
            del_n += 1
        except Exception:
            print(title + '删除失败')
            continue

print('共删除' + str(del_n) + '个文件')
