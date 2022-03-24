from django.contrib import admin

# Register your models here.
from app.models import Hotel, Room, Hotel_img, Room_img, Crawler

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Hotel_img)
admin.site.register(Room_img)
admin.site.register(Crawler)


admin.site.site_title = "酒店管理｜系统后台"
admin.site.site_header = "不二家旅行｜后台管理系统"
admin.site.index_title = "不二家旅行"
