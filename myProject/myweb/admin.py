from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User_db)
admin.site.register(Order_detail)
admin.site.register(Goods_info)
admin.site.register(Receiver)
admin.site.register(Goods_list)
admin.site.register(Ord)

# class User_db_admin(admin.modelAdmin):
#     list_display = ['']