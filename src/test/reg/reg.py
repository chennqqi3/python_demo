# -*- coding:utf-8 -*-
import re

a = 'a1bc2vc3-=-=-e4[5'

pa = re.compile('.*?\d(.*?)\d.*?\d(.*?)\d')

items = re.findall(pa, a)

a = []

for i in items:
    print("%s,%s" % (i[0], i[1]))
