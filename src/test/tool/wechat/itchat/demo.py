import itchat

if __name__ == '__main__':
    # 登录，弹出登录二维码，设置hotReload，不需要重复扫码
    itchat.auto_login(hotReload=True)

    # 向文件助手发送消息,发送成功
    itchat.send('hi，demo', toUserName='filehelper')
    # 给自己发消息，可以收到
    itchat.send('吃饭了吗')
    # 向好友发送消息不成功
    itchat.send('干嘛呢', toUserName='@1b15c43c8af30267ae5e179351096ef62cf17e7105eb1210a2328d9c234c6a48')

    # 获取好友列表
    friends = itchat.get_friends()
    print('您有：' + str(len(friends)) + '个好友')
    for friend in friends:
        print(friend)

    # print(itchat.get_chatrooms)
    # print(itchat.get_contact)
