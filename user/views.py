import json
import time
import base64
import hmac
import uuid
import requests as rq
import django
from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from dwebsocket import accept_websocket
from django.views.decorators.csrf import csrf_exempt

from app.models import Room
from tool import ret_code
from user.models import User, Market, advertising

token_key = "BEJjjs2022"
clients = {}
artificial_clients = []
artificial_customer_service_dict = {}


def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    print(token_list)
    if len(token_list) < 2:
        return False
    time_str = token_list[0]
    if float(time_str) < time.time():
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), time_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        return False
    return True


def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_ts_hex_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_ts_hex_str
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


class AddUser(View):
    @csrf_exempt
    def post(self, request):
        json_body = json.loads(request.body)
        try:
            user_obj = User()
            nickName = json_body.get('nickName')
            code = json_body.get("code")
            wx_portrait = json_body.get("wx_portrait")
            token = generate_token(token_key)

            APPID = "wx3c85cc30cf14f728"
            SECRET = "1e77684d1e3ef3e94c74a25601827505"
            url = f"https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={code}&grant_type=authorization_code"
            data = rq.get(url)
            wx_openId = data.json().get("openid")
            if wx_openId is not None:
                is_user = User.objects.filter(wx_openId=wx_openId).first()
                if is_user is None:
                    user_obj.wx_nickName = nickName
                    user_obj.wx_openId = wx_openId
                    user_obj.wx_portrait = wx_portrait
                    user_obj.token = token
                    user_obj.save()
                else:
                    is_user.token = token
                    is_user.save()
                return JsonResponse(ret_code(200, data=token))
            else:
                return JsonResponse(ret_code(207))
        except django.db.utils.IntegrityError:
            openId = User.objects.filter(wx_openId=json_body.get("openId")).first()
            token = generate_token(token_key)
            User.objects.filter(id=openId.id).update(token=token)
            return JsonResponse(ret_code(203, data=token))


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
                artificial_customer_service_dict[userid].send(
                    json.dumps({"msg": message, "id": userid}).encode("'utf-8'"))
            else:
                pass


@accept_websocket
def WsSendAll(request):
    if request.is_websocket():
        while 1:
            message = request.websocket.wait()
            message = str(message, encoding="utf-8")
            if message == "小杨":
                artificial_clients.append({"id": str(uuid.uuid1()), "num": 0, "name": "小杨",
                                           "client": request.websocket, "people": []})
            elif message.startswith("h"):
                send_data = message.split("|")
                send_user, send_data = send_data[1], send_data[2]
                clients[send_user].send(send_data.encode("'utf-8'"))


class Order(View):
    def post(self, request):
        try:
            json_body = json.loads(request.body)
            room_id = json_body.get("room_id")
            token = json_body.get("token")
            name = json_body.get("name")
            phone = json_body.get("phone")
            if name is None or phone is None:
                return JsonResponse(ret_code(201))
            if certify_token(token_key, token):
                user_obj = User.objects.filter(token=token).first()
                market_obj = Market()
                market_obj.room_id = room_id
                market_obj.user = user_obj.id
                market_obj.save()
                return JsonResponse(ret_code(205))
            else:
                return JsonResponse(ret_code(204))
        except Exception as e:
            return JsonResponse(ret_code(206, data=str(e)))


class Banner(View):
    def get(self, request):
        url = advertising.objects.order_by("-created_time")[:3]
        img = []
        for i in url:
            img.append("https://hotel.buerclub.com/get_hotel_img?image_path={}".format(i.img))
        ret = {
            "hotel_img": img
        }
        return JsonResponse(ret_code(200, data=ret))


class Reservation(View):
    def get(self, request):

        token = request.GET.get("token")
        if certify_token(token_key, token):
            user_obj = User.objects.filter(token=token).first()
            reservation = Market.objects.filter(user=user_obj.id).all()
            room_dict = {}
            room_list = []
            for n in reservation:
                room_dict[n.room_id] = n.created_time.strftime("%Y-%m-%d, %H:%M:%S")
                room_list.append(n.room_id)
            room_obj = Room.objects.filter(id__in=room_list).all()
            ret_list = []
            for i in room_obj:
                ret = {"name": i.hotel.hotel_name,
                       "create_time":room_dict[str(i.id)],
                       "status":0
                       }
                ret_list.append(ret)
            return JsonResponse(ret_code(200, data=ret_list))
        else:
            return JsonResponse(ret_code(204))
