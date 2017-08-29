str = ''
with open('str.txt', 'rb') as f:
    for line in f.readlines():
        # rstrip()去掉右侧的空格、回车\r，换行\n，制表符\t， 换页符\f
        dec = line.decode('utf-8').rstrip()
        str += '\'' + dec + '\','

print(str)