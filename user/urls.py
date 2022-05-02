# -------------------------------------------------------------------------------
# Description:  
# Reference:
# Author: 
# Date:   2022/4/10
# -------------------------------------------------------------------------------


from django.urls import path

from user import views
from user.views import WsService, WsSendAll

app_name = 'user'

urlpatterns = [
    # 注册用户
    path('add',views.AddUser.as_view()),
    # 下单
    path('order',views.Order.as_view()),
    # ws 用户 server
    path('ws_service',WsService),
    # ws 客服 server
    path('ws_send_service',WsSendAll)
]