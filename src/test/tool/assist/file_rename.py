# 重命名

import os

pdf_dir = "E:\学习资料\电子书/gitbook/pdf/"
mobi_dir = "E:\学习资料\电子书/gitbook/mobi/"

for x in os.listdir(pdf_dir):
    src = os.path.join(pdf_dir, x)
    if os.path.isfile(src):
        title = x.title()
        if title.startswith('pdf'):
            try:
                os.rename(src, os.path.join(pdf_dir, title[3:]))
            except Exception:
                print(title + '重命名失败')

print('pdf重命名完成')


for x in os.listdir(mobi_dir):
    src = os.path.join(mobi_dir, x)
    if os.path.isfile(src):
        title = x.title()
        # print(title)
        if title.startswith('Mobi'):
            try:
                os.rename(src, os.path.join(mobi_dir, title[4:]))
            except Exception:
                print(title + '重命名失败')

print('mobi重命名完成')
