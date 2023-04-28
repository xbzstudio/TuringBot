import requests, turingAPI, time, math, json
chatgptUserID = '' #字符串内填写你的ChatGPT账号。可以在chat2.wuguokai.cn获取。
icodeCookie = input('使用什么cookie？内置cookie或新cookie？')
if icodeCookie == '内置':
    chatgptBot = turingAPI.icodeUser('') #字符串内填你自己的账号的cookie
else:
    chatgptBot = turingAPI.icodeUser(icodeCookie)
print('icode登录信息：', chatgptBot.info)
print('chatgpt账户：',chatgptUserID)
banList = ['urs-phoneyd.49c78c0400b5403b8@163.com'] #黑名单（你可以在这行代码中填入所有黑名单人员的userId，chatgpt会自动忽视他们的留言。记得将网址上的转义符改成@。）
while True:
    message = chatgptBot.getMessage(1,200,True)
    aList = []
    for i in message:
        if i['haveRead'] == 0:
            if '@ChatGPT' in i['content']:
                aList.append(i)
            if '@New Bing' in i['content']:
                if not i in aList:
                    aList.append(i)
        else:
            break
    aList = aList[::-1]
    if aList != []:
        print('待回复消息列表：',[i['content'] for i in aList])
    for i in aList:
        print('收到来自',i['actionUserName'],i['actionUserId'],'的消息：', i['content'])
        chatgptBot.readMessage(i['id'])
        if i['actionUserId'] in banList:
            print('检测到黑名单人员',i['actionUserId'],'的留言，已忽视。')
        else:
            print('开始应答...')
            commentTo = chatgptBot.getPersonWorks(i['actionUserId'],1,1,True)
            if not (commentTo == []):
                if '@ChatGPT' in i['content']:
                    chatgptReply = repr(requests.post('https://chat2.wuguokai.cn/api/chat-process',data=('{"prompt":"'+str(i['content'])+'","options":{},"userId":"'+str(chatgptUserID)+'","usingContext":true}').encode('utf-8'),headers={'content-type': 'application/json','referer': 'https://chat.wuguokai.cn/','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39'}).text).replace('\\n',' ')[1:-1:1]
                else:
                    chatgptReply = json.loads(repr(requests.get(('http://127.0.0.1:5000/api?style=balanced&question={}'.format(i['content'])).replace('@New Bing','').replace('@ChatGPT','')).text).replace('\\n',' ')[1:-1:1].replace('\\','\\\\'))['data']['answer']
                if len(chatgptReply)>200:
                    print('开始分条发送信息')
                    for i in range(0,math.ceil(len(chatgptReply)/200)):
                        data = repr(chatgptReply[i*200:-1:1] if i==math.ceil(len(chatgptReply)/200)-1 else chatgptReply[i*200:i*200+200:1])
                        chatgptBot.comment(commentTo[0]['id'], data[1:-1:1]).data.decode('utf-8')
                        time.sleep(5.3)
                else:
                    print('开始直接发送信息：回复')
                    chatgptBot.comment(commentTo[0]['id'], chatgptReply)
                    time.sleep(5.3)
                print('成功应答：',chatgptReply)
                print('\n\n')
