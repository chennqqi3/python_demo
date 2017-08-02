# 帮外甥投票
import requests

vote_url = 'http://www.bbxsy.cn/app/index.php?i=3&c=entry&rid=170&id=8951&do=vote&m=tyzm_diamondvote'

cookie_str = '__cfduid=df19c80bba45042c02f85168e3e3cb9461501411459;' \
             ' 641d_cuserinfo=eyJvcGVuaWQiOiJvTnlIa3doa0lPLXV0bzNKcUhoOWd1dHFkZmRkZCIsIm5pY2tuYW1lIjoiXHU1MWFjXHU2NzY1XHU1MWFjXHU1ZjgwIiwic2V4IjoxLCJsYW5ndWFnZSI6InpoX0NOIiwiY2l0eSI6IiIsInByb3ZpbmNlIjoiIiwiY291bnRyeSI6Ilx1NGUyZFx1NTZmZFx1NTNmMFx1NmU3ZSIsImhlYWRpbWd1cmwiOiJodHRwOlwvXC93eC5xbG9nby5jblwvbW1vcGVuXC9QaWFqeFNxQlJhRUlHYlpWWEY3eVRWOVQ3NUNYcFRJVGwySHlEdTVET0xOeTk0UWhpYkZOMGxrOEw1azg2RVpYMEdxc1BZMmljNEg4WWJiVUtPMFl1T1BjQVwvMTMyIiwicHJpdmlsZWdlIjpbXSwiYXZhdGFyIjoiaHR0cDpcL1wvd3gucWxvZ28uY25cL21tb3BlblwvUGlhanhTcUJSYUVJR2JaVlhGN3lUVjlUNzVDWHBUSVRsMkh5RHU1RE9MTnk5NFFoaWJGTjBsazhMNWs4NkVaWDBHcXNQWTJpYzRIOFliYlVLTzBZdU9QY0FcLzEzMiJ9;' \
             ' PHPSESSID=adf0f3cfe88e9a9984e4f5df183d7f82'
headers = {
    'Host': 'www.bbxsy.cn',
    'Content-Length': '22',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://www.bbxsy.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://www.bbxsy.cn/app/index.php?i=3&c=entry&rid=170&id=8951&do=view&m=tyzm_diamondvote&u=1030937&wxref=mp.weixin.qq.com&from=groupmessage&isappinstalled=0&wxref=mp.weixin.qq.com&wxref=mp.weixin.qq.com',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
    'Cookie': cookie_str,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.556.400 QQBrowser/9.0.2524.400'
}

# cookie_dict = {'__cfduid': 'df19c80bba45042c02f85168e3e3cb9461501411459',
#                'PHPSESSID': 'adf0f3cfe88e9a9984e4f5df183d7f82',
#                '641d_cuserinfo': 'eyJvcGVuaWQiOiJvTnlIa3doa0lPLXV0bzNKcUhoOWd1dHFtTnlvIiwibmlja25hbWUiOiJcdTUxYWNcdTY3NjVcdTUxYWNcdTVmODAiLCJzZXgiOjEsImxhbmd1YWdlIjoiemhfQ04iLCJjaXR5IjoiIiwicHJvdmluY2UiOiIiLCJjb3VudHJ5IjoiXHU0ZTJkXHU1NmZkXHU1M2YwXHU2ZTdlIiwiaGVhZGltZ3VybCI6Imh0dHA6XC9cL3d4LnFsb2dvLmNuXC9tbW9wZW5cL1BpYWp4U3FCUmFFSUdiWlZYRjd5VFY5VDc1Q1hwVElUbDJIeUR1NURPTE55OTRRaGliRk4wbGs4TDVrODZFWlgwR3FzUFkyaWM0SDhZYmJVS08wWXVPUGNBXC8xMzIiLCJwcml2aWxlZ2UiOltdLCJhdmF0YXIiOiJodHRwOlwvXC93eC5xbG9nby5jblwvbW1vcGVuXC9QaWFqeFNxQlJhRUlHYlpWWEY3eVRWOVQ3NUNYcFRJVGwySHlEdTVET0xOeTk0UWhpYkZOMGxrOEw1azg2RVpYMEdxc1BZMmljNEg4WWJiVUtPMFl1T1BjQVwvMTMyIn0%3D'}

vote_data = {'latitude': 0, 'longitude': 0}

res = requests.post(vote_url, data=vote_data, headers=headers)

print(res)
print(res.text)
