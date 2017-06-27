src_file = 'C:\\Users\weidongdong\Desktop\\temp\python\\args.txt'
dest_file = 'C:\\Users\weidongdong\Desktop\\temp\python\out\\result.txt'

# 复制文件内容
with open(src_file, 'r') as read_f:
    with open(dest_file, 'w') as write_f:
        for line in read_f.readlines():
            write_f.write(line)
