from django.db import models
import datetime
import os

# Create your models here.

class Login_info (models.Model):
    username= models.CharField(max_length =50)
    email=models.EmailField()
    password=models.CharField(max_length =10)

class User_profile (models.Model):
    username=models.ForeignKey(Login_info,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    surname=models.CharField(max_length=50)
    mobile_no=models.IntegerField()
    address=models.CharField(max_length=500)
    pincode=models.IntegerField()
    state=models.CharField(max_length=50)
    email=models.EmailField()
    def __str__(self):
        return self.name

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H_%M_%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('user_pro/', filename) 
  
class User_profile_img(models.Model):
    username=models.ForeignKey(Login_info,on_delete=models.CASCADE)
    dp=models.ImageField(upload_to=filepath, null=True, blank=True)


class User_count(models.Model):
    username=models.ForeignKey(Login_info,on_delete=models.CASCADE)
    post_cnt=models.IntegerField(default=0)
    follower_cnt=models.IntegerField(default=0)
    following_cnt=models.IntegerField(default=0)

class Friend_requests(models.Model):
    receiver=models.ForeignKey(Login_info,on_delete=models.CASCADE)
    sender=models.ForeignKey(User_profile,on_delete=models.CASCADE)
    sender_img=models.ForeignKey(User_profile_img,on_delete=models.CASCADE)


class Followers(models.Model):
    username=models.ForeignKey(Login_info,on_delete=models.CASCADE)
    followed_user_pro=models.ForeignKey(User_profile,on_delete=models.CASCADE)
    followed_user_pro_img=models.ForeignKey(User_profile_img,on_delete=models.CASCADE)
    
class Following(models.Model):
    username=models.ForeignKey(Login_info,on_delete=models.CASCADE)
    following_user_pro=models.ForeignKey(User_profile,on_delete=models.CASCADE)
    following_user_pro_img=models.ForeignKey(User_profile_img,on_delete=models.CASCADE)
  
def filepath1(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H_%M_%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('post/', filename) 

class Post(models.Model):
    user_pro=models.ForeignKey(User_profile,on_delete=models.CASCADE)
    # user_pro_img=models.ForeignKey(User_profile_img,on_delete=models.CASCADE)
    post_img=models.ImageField(upload_to=filepath1, null=True, blank=True)
    like_cnt=models.IntegerField()
    captions=models.CharField(max_length=200)

class Post1(models.Model):
    user_pro=models.ForeignKey(User_profile,on_delete=models.CASCADE)
    user_pro_img=models.ForeignKey(User_profile_img,on_delete=models.CASCADE)
    post_img=models.ImageField(upload_to=filepath1, null=True, blank=True)
    like_cnt=models.IntegerField()
    captions=models.CharField(max_length=200)


class Like(models.Model):
    username=models.ForeignKey(Login_info,on_delete=models.CASCADE)
    post=models.ForeignKey(Post1, on_delete=models.CASCADE)
    like=models.BooleanField(default=False)

