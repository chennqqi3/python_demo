#web内容实现
#Request内容可以通过environ获得，response内容可以通过start_response设置
from nt import environ
def application(environ,start_response):
    start_response('200 OK',[('Content-Type','text/html')])
    body='<h1>Hello,%s!</h1>'%(environ['PATH_INFO'][1:])
    return [body.encode('utf_8')]