#列出目录下的文件
import os


path='C:/Users/weidd/Desktop/war'

# L=[]
pa=''
def listfile(path,pa):
    for x in os.listdir(path):
        newpath=os.path.join(path,x)
        if os.path.isfile(newpath):
            print(pa+x+'\n')
        elif os.path.isdir(newpath):
            print(pa+x+'\n')
            listfile(newpath,pa+'--')

listfile(path,pa)
# print(L)