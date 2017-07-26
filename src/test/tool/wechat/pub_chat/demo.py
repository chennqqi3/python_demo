import json

import requests


def get_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid': '',
              'corpsecret': ''}
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    print(data)
    return data["access_token"]


def send_msg():
    agent_url = 'https://qyapi.weixin.qq.com/cgi-bin/agent/get?access_token=' + get_token() + "&agentid=1000002"
    rep = requests.get(agent_url)
    print(rep.text)
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + get_token()
    send_values = {
        "touser": 'WeiDongDong',  # 企业号中的用户帐号
        "toparty": "1",  # 企业号中的部门id
        "totag": "",
        "msgtype": "text",  # 企业号中的应用id，消息类型。
        "agentid": "1000002",
        "text": {
            "content": 'hello,from pub_wx'
        },
        "safe": "0"
    }
    send_data = json.dumps(send_values, ensure_ascii=False)
    req = requests.post(url, send_data)
    print(req.text)


if __name__ == '__main__':
    send_msg()
