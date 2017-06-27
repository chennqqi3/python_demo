#判断文件编码格式
import os
import chardet

path='C:\workspace\DtgPlatform_trunk'

fileDict={}
def getFileEncodingDict(x,path):
    with open(path,'rb') as f:
        fileDict[x]=chardet.detect(f.read())

def listforder(path):
    for x in os.listdir(path):
        newpath=os.path.join(path,x)
        if os.path.isfile(newpath):
            if x.endswith('.java'):
                getFileEncodingDict(x,newpath)
        elif os.path.isdir(newpath):
            listforder(newpath)

def filterUtf8():
    listforder(path)
    print('UTF-8编码的文件:')
    for (k,v) in fileDict.items():
        fileEncode=fileDict[k]['encoding']
        if fileEncode.upper() == 'UTF-8':
            print('%s' %k)
    
if __name__ == '__main__':
    filterUtf8()