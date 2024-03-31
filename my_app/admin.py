from django.contrib import admin
from my_app.models import Login_info,User_profile,User_profile_img,Post,Followers,Following,Friend_requests,User_count,Post1,Like
# Register your models here.

admin.site.register(Login_info)
admin.site.register(User_profile)
admin.site.register(User_profile_img)
admin.site.register(Post)
admin.site.register(Post1)
admin.site.register(Friend_requests)
admin.site.register(Followers)
admin.site.register(Following)
admin.site.register(User_count)
admin.site.register(Like)

