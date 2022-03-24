from django.db import models

# Create your models here.
import os


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}{1}.{2}'.format(instance.name, instance.identity_card, ext)
    return os.path.join(instance.major.name, filename)


class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=20, verbose_name="酒店名称")
    hotel_mian_img = models.ImageField(upload_to=user_directory_path, verbose_name="酒店主图")
    decs = models.TextField(verbose_name="酒店简介")
    phone = models.CharField(max_length=20,verbose_name="联系电话")
    address = models.CharField(max_length=200,verbose_name="酒店地址")

    class Meta:
        verbose_name = '添加新的酒店'
        verbose_name_plural = verbose_name


class Room(BaseModel):
    room_name = models.CharField(max_length=20, verbose_name="房型名称")
    room_price = models.CharField(max_length=10, verbose_name="房型价格")
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, verbose_name="对应酒店")
    room_mian_img = models.ImageField(upload_to=user_directory_path, verbose_name="房型主图")
    room_num = models.IntegerField(verbose_name="房间总数")
    room_reservation = models.IntegerField(verbose_name="已预定数")
    note = models.CharField(max_length=200, verbose_name="备注")

    class Meta:
        verbose_name = '根据酒店添加新的房型'
        verbose_name_plural = verbose_name


class Hotel_img(BaseModel):
    hotel = models.ForeignKey(Hotel, verbose_name="对应酒店", on_delete=models.CASCADE)
    img = models.ImageField(upload_to=user_directory_path, verbose_name="酒店环境图")

    class Meta:
        verbose_name = '酒店图'
        verbose_name_plural = verbose_name
    

class Room_img(BaseModel):
    room = models.ForeignKey(Hotel, verbose_name="对应房间", on_delete=models.CASCADE)
    img = models.ImageField(upload_to=Room, verbose_name="房间环境图")

    class Meta:
        verbose_name = '房型图'
        verbose_name_plural = verbose_name


class Crawler(BaseModel):
    url = models.CharField(max_length=200,verbose_name="爬取网址")
    data = models.CharField(max_length=20,verbose_name="爬取关键信息")
    callback = models.CharField(max_length=20, verbose_name="回调｜备注")

    class Meta:
        verbose_name = '爬虫'
        verbose_name_plural = verbose_name
