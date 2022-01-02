import hashlib
import json
import platform
import web
import requests
import receive
import replay

if platform.system().lower() == 'windows':
    botIp = "127.0.0.1"
elif platform.system().lower() == 'linux':
    botIp = "rasa_ep"  # docker-compose use network

botPort = '5005'


def get_chat_content(userid, content):
    params = {"sender": userid, "message": content}

    rasaUrl = "http://{0}:{1}/webhooks/rest/webhook".format(botIp, botPort)
    response = requests.post(
        rasaUrl,
        data=json.dumps(params),
        headers={'Content-Type': 'application/json'}
    )
    return response.text.encode('utf-8').decode("unicode-escape")


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            print(data)
            if len(data) == 0:
                return "hello, this is handle view, no data input"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "dy654321"  # 请按照公众平台官网\基本配置中信息填写

            li = [token, timestamp, nonce]
            li.sort()
            # 需要将加密的数据编码成utf-8的，不然会出错，Token验证失败
            tmp_str = "".join(li).encode('utf-8')
            # 进行sha1加密
            hashcode = hashlib.sha1(tmp_str).hexdigest()

            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            print("post")
            webData = web.data()
            print("Handle Post webdata is ", webData.decode('utf-8'))
            # 后台打日志
            recMsg = receive.parse_xml(webData)
            # 该模块是处理文本数据信息
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                # 获取到并解析出来用户发送过来的数据信息
                recContent = recMsg.Content.decode('utf-8')
                print("user message:", recContent, type(recContent))
                # 获取到MsgID 作为信息唯一标识送入RASA中
                msgID = recMsg.MsgId
                print("user message ID :", msgID, type(recContent))
                # 获取RASA服务端得到的返回结果
                result = get_chat_content(msgID, recContent)
                result_json = json.loads(result, strict=False)
                replayContent = ""
                for i in range(len(result_json)):
                    bot_utterence = result_json[i]["text"]
                    print("Bot:", bot_utterence)
                    replayContent += bot_utterence

                print("bot recContent: ", replayContent)
                # 接受信息与发送信息的主体对象转换一下
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # 定义好需要返回给用户的数据文本内容
                replyMsg = replay.TextMsg(
                    toUser, fromUser, replayContent, msgID)
                return replyMsg.send()
            else:
                print("暂且不处理")
                return "success"
        except Exception as Argment:
            return Argment
