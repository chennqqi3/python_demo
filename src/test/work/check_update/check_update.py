#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import hashlib
import re
import sys
import threading
import time
import urllib
import urllib.request

import datetime
import os
import requests

# 全局变量
success_cnt = 0
fail_cnt = 0
lock = threading.Lock()
input_list = []


# 入参数据结构
class OtaModel:
    def __init__(self, index, hw, hwv, swv):
        self.index = index
        self.hw = hw
        self.hwv = hwv
        self.swv = swv

    def __str__(self):
        return 'hw:%s,hwv:%s,swv:%s' % (self.hw, self.hwv, self.swv)


class OtaTestScript:
    # 初始化方法，定义一些变量
    def __init__(self, ota_model, output_dir):
        self.success = False
        self.dir = output_dir + '/'
        self.ota_model = ota_model

    def get_url(self):
        return 'http://t.ota1.os.qiku.com/ota/checkupdate' + \
               '?m2=4a5a82237b2675d098352934a0522ec6' + \
               '&cpuid=unknow' + \
               '&userstart=1' + \
               '&hw=' + self.ota_model.hw + \
               '&imei=8948a03ce379af65a3bba93e1dd9cb2d' + \
               '&hwv=' + self.ota_model.hwv + \
               '&swv=' + self.ota_model.swv + \
               '&src_type=stable' \
               '&serialno=47f569cd' \
               '&curnetwork=0' \
               '&emmc=90014a484247346132a447f569cdc300'

    # 根据入参模拟请求
    def open_url(self):
        print_th('开始请求：' + self.get_url())

        try:
            response = requests.get(self.get_url())
            res_status = str(response.status_code)
            print_th('请求返回：' + res_status)

            if '200' != res_status:
                self.add_fail_reason('生成地址请求返回' + res_status)
                return ''

            # print('请求返回：' + response.text)
            return response.text
        except BaseException as e:
            self.add_fail_reason('生成地址请求失败')
            print_th('请求地址发生错误')
            return ''

    # 下载文件
    def download(self, url):
        print_th('解析下载地址为：' + url)
        print_th('开始下载文件。。。')

        splits = url.split('/')
        split_len = splits.__len__()

        # 下载的文件名
        file_name = ''
        for i in range(split_len - 4, split_len):
            if i < (split_len - 1):
                file_name += splits[i] + "#"
            else:
                file_name += splits[i]

        # local_file = self.dir + str(time.time()) + '_' + threading.current_thread().name + '_' + file_name
        local_file = self.dir + file_name

        # 有可能一个线程创建了文件但是没有写完，另一个文件读取来读取，此时返回的md5就不正确
        # 所以文件名最近后缀'当前线程名+时间戳'，防止重复

        # if os.path.exists(local_file):
        #     print_th('文件已经存在：' + file_name)
        # else:
        try:
            urllib.request.urlretrieve(url, local_file)
            print_th('文件下载完成。。。')
        except BaseException as e:
            self.add_fail_reason('文件下载失败')
            print_th('文件下载失败')
            return ''

        return local_file

    def start(self):
        content = self.open_url()

        if '' == content:
            return

        # 如果返回CHECK_UPDATE_RESULT等于1，说明失败
        if -1 != content.find('CHECK_UPDATE_RESULT:1'):
            self.add_fail_reason('CHECK_UPDATE_RESULT返回值为1')
            print_th('CHECK_UPDATE_RESULT返回值为1')
            return

        pattern = re.compile('<downloadURL>(.*)</downloadURL>.*<md5>(.*)</md5>', re.S)

        match = re.search(pattern, content)

        if match:
            downloadurl = match.group(1)
            response_md5 = match.group(2)

            # 验证下载链接
            local_file = self.download(downloadurl)

            # 验证md5
            self.check_md5(response_md5, local_file)
        else:
            self.add_fail_reason('返回报文没有downloadURL或md5')
            print_th('返回报文没有downloadURL或md5')

    # 校验md5
    def check_md5(self, response_md5, local_file):
        if '' == local_file:
            return

        print_th('开始验证md5。。。')
        print_th('解析返回的md5为:' + response_md5)

        md5 = hashlib.md5()

        with open(local_file, 'rb') as f:
            md5.update(f.read())

        digest_md5 = md5.hexdigest()
        print_th('计算得到的md5为:' + digest_md5)

        if response_md5.upper() == digest_md5.upper():
            print_th("md5值相同，验证通过")
            self.success = True
        else:
            self.add_fail_reason("md5不一致")
            print_th("md5不一致，验证不通过")

    # 统计错误信息
    def add_fail_reason(self, reason):
        global input_list, lock

        lock.acquire()
        try:
            input_list[self.ota_model.index - 1] += '\t' + reason
        finally:
            lock.release()


# 将入参文件解析为入参列表
def analyze_input(input_file):
    if not os.path.exists(input_file):
        print_th("参数文件不存在，请确认文件路径！！")
        exit()

    global input_list

    params_list = []
    index = 1
    with open(input_file) as input_f:
        for line in input_f.readlines():
            # 一定要注意使用strip()函数去掉换行符'\n'
            line = line.strip()

            # 保存行的内容到list
            input_list.append(line)

            # 解析按tab分隔的每一项
            r = re.compile('\t+')
            split = r.split(line)
            params_list.append(OtaModel(index, split[0], split[1], split[2]))

            index += 1

    return params_list


# 线程执行验证
def test_thread(index, ota_model):
    print_th('第' + str(index + 1) + '条')
    spider = OtaTestScript(ota_model, out_dir)
    spider.start()

    global success_cnt, fail_cnt, lock, input_list
    lock.acquire()
    try:
        if spider.success:
            success_cnt += 1
            input_list[index] += '\t\t验证通过\n'
        else:
            fail_cnt += 1
            input_list[index] += '\t验证不通过\n'
    finally:
        lock.release()


# 线程写入结果文件
def write_result_thread(result_file):
    global input_list
    res = ''.join(input_list)

    with open(result_file, 'w') as result_w:
        result_w.write(res)


# 重写print方法，加入当前线程的前缀
def print_th(ori_str):
    print('当前线程：' + threading.current_thread().name + ',' + ori_str)


# main函数，程序入口
if __name__ == '__main__':
    start_time = time.time()

    params = analyze_input(sys.argv[1])

    out_dir = sys.argv[2]
    if not os.path.exists(out_dir):
        print_th("输出目录不存在，请确认！！")
        exit()

    input_len = params.__len__()

    # 保存启动的线程，主线程控制
    ls_thread = []
    for i in range(0, input_len):
        thr = threading.Thread(target=test_thread, args=(i, params[i]), name=str(i + 1))
        thr.start()
        ls_thread.append(thr)
        # thread_m(i, params[i])

    # 等待执行完毕
    for th in ls_thread:
        th.join()

    # 输出结果文件
    txt_ = out_dir + '/result_' + datetime.datetime.now().strftime('%y%m%d%H%M%S') + '.txt'
    w_r_t = threading.Thread(target=write_result_thread, args=(txt_,))
    w_r_t.start()

    end_time = time.time()
    print('\n脚本执行完成，共耗时：' + str(end_time - start_time) + '秒，共有:%d条，成功：%d条，失败：%d条' % (input_len, success_cnt, fail_cnt))
