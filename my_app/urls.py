from django.urls import path

from . import views 


urlpatterns = [
    path('',views.login,name='login'),
    path('login',views.login,name='login'),
    path('register', views.register ,name='register'),
    path('change_pass',views.change_pass,name='change_pass'),
    path('create_profile',views.create_profile,name='create_profile'),
    path('upload_photo' , views.upload_photo , name='upload_photo' ),
    path('home',views.home, name='home'),
    path('show_profile',views.show_profile,name='show_profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('edit_upload_photo',views.edit_upload_photo,name='edit_upload_photo'),
    path('post_create' , views.post_create,name='post_create'),
    path('searched_user' , views.searched_user,name='searched_user'),
    path('friend_request' , views.friend_request,name='friend_request'),
    path('request_decline' , views.request_decline,name='request_decline'),
    path('unfollow' , views.unfollow,name='unfollow'),
    path('show_post' , views.show_post,name='show_post'),
    path('delete_post' , views.delete_post,name='delete_post'),
    path('like_unlike' , views.like_unlike , name='like_unlike'),
    path('followers_list' , views.followers_list , name='followers_list'),
    path('following_list' , views.following_list , name='following_list'),
    path('logout' , views.log_out , name='logout'),
]

