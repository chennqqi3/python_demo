from urllib import request


def main():
    file = 'C:/Users/weidongdong/Desktop/临时/t.html'
    with request.urlopen('http://www.baidu.com') as u:
        data = u.read()
        #         print(f.status,f.reason)
        #         for k,v in f.getheaders():
        #             print('%s,%s' %(k,v))
        #         print('Data',data.decode('utf-8'))
        write(file, data)


def write(file, con):
    with open(file, 'wb') as f:
        f.write(con)


if __name__ == '__main__':
    main()
