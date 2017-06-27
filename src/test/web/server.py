from wsgiref.simple_server import make_server

#导入web的实现类，即hello.py
from test.web.hello import application

httpd=make_server('',8089,application)
print('server started 8089')

httpd.serve_forever()