from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views import View
from app.models import Hotel, Room
from tool import ret_code
import os


def get_img(request):
    image_path = request.GET.get('image_path')
    image_data = open(os.path.join(os.path.abspath('.'), "upload", image_path), "rb").read()
    return HttpResponse(image_data, content_type="image/png")


class HotList(View):
    def get(self, request):
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 5)
        city = request.GET.get('city')

        reservation_time = request.GET.get('reservation_time')  # 预定时间
        room_num = request.GET.get('room_num')
        adult = request.GET.get('adult')
        children = request.GET.get('children')
        special_room = request.GET.get('special_room')

        q = Q()
        if city is not None:
            q &= Q(city=city)

        start = (page - 1) * page_size  # 页码数据开头的索引
        end = page * page_size  # 页码数据结尾的索引
        hotel_obj = Hotel.objects.filter(q).all().order_by("-created_time")
        if len(hotel_obj) < end:
            end = len(hotel_obj)
        data = hotel_obj[start:end]  # 截取数据

        ret_dict = dict()
        ret_list = []
        for i in data:
            ret = {
                "hotel_name": i.hotel_name,
                "desc": i.decs,
                "hotel_img": str(i.hotel_mian_img),
                "hotel_id": i.id
            }
            ret_list.append(ret)
        ret_dict["data"] = ret_list
        ret_dict['total'] = len(hotel_obj)

        return JsonResponse(ret_code(200, data=ret_dict))


class HotelDetail(View):
    def get(self, request):
        hotel_id = request.GET.get('id')
        if hotel_id is None:
            return JsonResponse(ret_code(201))
        hotel_obj = Hotel.objects.filter(id=hotel_id).first()
        if hotel_obj is None:
            return JsonResponse(ret_code(202))

        ret = dict()
        hotel_ret_obj = {
            "hotel_name": hotel_obj.hotel_name,
            "hotel_img": str(hotel_obj.hotel_mian_img),
            "phone": hotel_obj.phone,
            "address": hotel_obj.address
        }
        ret["hotel_ret_obj"] = hotel_ret_obj

        room_obj = Room.objects.filter(hotel=hotel_id).all()

        room_ret_list = list()
        for i in room_obj:
            room_ret_obj = {
                "room_name": i.room_name,
                "room_num": i.room_num,
                "room_img": str(i.room_mian_img),
                "room_price": i.room_price,
                "note": i.note
            }
            room_ret_list.append(room_ret_obj)

        ret["room_ret_list"] = room_ret_list

        return JsonResponse(ret_code(200, data=ret))


class HotHotel(View):
    def get(self, request):
        hotel_obj = Hotel.objects.all()
        hot_city = list()
        for i in hotel_obj:
            hot_city.append(i.city)

        return JsonResponse(ret_code(200, data=hot_city[:10]))
