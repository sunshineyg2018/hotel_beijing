import json
import time
import base64
import hmac
import uuid

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from dwebsocket import accept_websocket

from tool import ret_code
from user.models import User

clients = {}
artificial_clients = []
artificial_customer_service_dict = {}


def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_ts_hex_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_ts_hex_str
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


class AddUser(View):
    def post(self, request):
        user_obj = User()
        nickName = request.POST.get('nickName')
        wx_openId = request.POST.get("openId")
        wx_portrait = request.POST.get("wx_portrait")
        user_obj.wx_nickName = nickName
        user_obj.wx_openId = wx_openId
        user_obj.wx_portrait = wx_portrait
        token = generate_token(str(user_obj.id))
        User.objects.filter(id=user_obj.id).update(token=token)
        return JsonResponse(ret_code(200, data=token))


class Login(View):
    pass


@accept_websocket
def WsService(request):
    if request.is_websocket():
        artificial_customer_service = False
        userid = str(uuid.uuid1())
        clients[userid] = request.websocket
        clients[userid].send("*****************************".encode("'utf-8'"))
        clients[userid].send("你好,不二家客服机器人为您服务".encode("'utf-8'"))
        clients[userid].send("如需退出,请输入:(退出)".encode("'utf-8'"))
        clients[userid].send("人工客服请,输入:(人工客服)".encode("'utf-8'"))
        clients[userid].send("*****************************".encode("'utf-8'"))
        while 1:
            message = request.websocket.wait()
            message = str(message, encoding="utf-8")
            if message == "退出":
                break
            elif message == "人工客服":
                clients[userid].send("正在接入人工客服.请耐心等待".encode("'utf-8'"))
                if len(artificial_clients) == 0:
                    time.sleep(5)
                    clients[userid].send("暂无人工客服在线,客服在线时间9:00 - 17:30".encode("'utf-8'"))
                else:
                    service_code = True
                    for artificial in artificial_clients:
                        if artificial["num"] < 5:
                            clients[userid].send("人工客服:{},为您服务".format(artificial["name"]).encode("'utf-8'"))
                            service_code = False
                            artificial["people"].append(userid)
                            artificial_customer_service = True
                            artificial_customer_service_dict[userid] = artificial['client']
                            break
                    if service_code:
                        clients[userid].send("当前客户数已达到最大服务数量。请稍后再试～".encode("'utf-8'"))
            elif artificial_customer_service:
                artificial_customer_service_dict[userid].send(json.dumps({"msg":message,"id":userid}).encode("'utf-8'"))
            else:
                pass


@accept_websocket
def WsSendAll(request):
    if request.is_websocket():
        while 1:
            message = request.websocket.wait()
            message = str(message, encoding="utf-8")
            if message == "小杨":
                artificial_clients.append({"id":str(uuid.uuid1()),"num":0,"name":"小杨",
                                           "client":request.websocket,"people":[]})
            elif message.startswith("h"):
                send_data = message.split("|")
                send_user,send_data = send_data[1],send_data[2]
                clients[send_user].send(send_data.encode("'utf-8'"))






