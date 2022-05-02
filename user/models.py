from django.db import models


# Create your models here.


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    user_name = models.CharField(max_length=20, verbose_name="应用名称", null=True)
    wx_nickName = models.CharField(max_length=20, verbose_name="微信名称")
    wx_openId = models.CharField(max_length=100,unique=True,verbose_name="微信id")
    wx_portrait = models.TextField(verbose_name="微信头像")
    token = models.CharField(max_length=200, verbose_name="用户token",null=True)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class Market(BaseModel):
    room_id = models.CharField(max_length=200, verbose_name="房间id")
    user = models.CharField(max_length=200, verbose_name="下单账号id")

    class Meta:
        verbose_name = '市场表'
        verbose_name_plural = verbose_name
