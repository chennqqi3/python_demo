dest_file = 'C:\\Users\weidongdong\Desktop\\temp\python\out\\result.txt'

input_list = []
# 在指定行后面追加内容
with open(dest_file, 'r+') as write_f:
    write_f.writable()