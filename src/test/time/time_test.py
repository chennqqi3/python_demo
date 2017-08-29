import time

# Tue Jun 27 15:40:35 2017
import datetime

print(time.asctime())


# 以秒为单位
# 1498549402.3872733
print(time.time())

# 十位时间戳
print(int(time.time()))

# 13位时间戳
print(int(round(time.time()*1000)))

# 1498549402.0
print(time.mktime(datetime.datetime.now().timetuple()))

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
