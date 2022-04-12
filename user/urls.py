# -------------------------------------------------------------------------------
# Description:  
# Reference:
# Author: 
# Date:   2022/4/10
# -------------------------------------------------------------------------------


from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    # 热门酒店推荐
    path('add',views.AddUser.as_view()),
]