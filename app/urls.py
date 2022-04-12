# -------------------------------------------------------------------------------
# Description:  
# Reference:
# Author: 
# Date:   2022/4/10
# -------------------------------------------------------------------------------
from django.urls import path

from app import views

app_name = 'hotel'

urlpatterns = [
    # 热门酒店推荐
    path('hot/list',views.HotList.as_view()),
    # 酒店详情
    path('detail',views.HotelDetail.as_view()),
    # 热门城市
    path('hot/city',views.HotHotel.as_view())
]