from django.shortcuts import render,redirect
from my_app.models import Login_info
from django.contrib.auth import authenticate, alogin
from django.contrib import messages
from .models import User_profile, Login_info , User_profile_img,Post1,Friend_requests,Followers,Following,User_count,Like
from django.contrib.auth import logout
import os
import random
def login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]        
        alluser = Login_info.objects.all()
        for user in alluser:
            if user.username==username:
                if user.password==password:
                    alogin(request, user)
                    request.session['user_id'] = user.id
                    request.session['username']=username
                    login_info = Login_info.objects.get(username=username)
                    if User_profile.objects.filter(username=login_info).exists():
                        return redirect("/home")
                    return redirect("/create_profile")
                else:
                    messages.info(request, "Incorrect Password")
                    return redirect("/main/login")
        messages.info(request, "Username Does not exist")
        
    return render(request, "login.html")

def register(request):
    if request.method=="POST":
        # print("in post")
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        if Login_info.objects.filter(username=username).exists():
            messages.error(request,"Username already taken")
            return redirect("/main/register")
        ins = Login_info(username=username , email=email , password=password)
        ins.save()
        # print("data stored")
        messages.info(request, "Registerd Successfully.")
        return redirect("/main/login")
    return render(request, "register.html")

def change_pass(request):
      if request.method=="POST":
            username=request.POST.get('username')
            new_pass=request.POST.get('new_password')
            con_pass=request.POST.get('con_password')
            if Login_info.objects.filter(username=username).exists():
                if new_pass==con_pass:
                      Login_info.objects.filter(username=username).update(password=new_pass)
                      messages.info(request, "Password Changed Successfully.")
                      return redirect("/main/login")
                else:
                    messages.info(request, "Password does not match")
                    return render(request, "forget_pass.html")
            else:
                messages.info(request, "Username Does not exist")
                return render(request, "forget_pass.html")
            

      return render(request, "forget_pass.html")

def home(request):
    if request.method == "POST" :
        username = request.POST.get('username')
        request.session['receiver']=username
        # print(username)
        if Login_info.objects.filter(username=username).exists():
            if User_profile.objects.filter(username=Login_info.objects.get(username=username)).exists():
            # print('hello')
                user1=request.session['username']
                # current logged in user
                user1_login=Login_info.objects.get(username=user1) 
                user1_pro=User_profile.objects.get(username=user1_login)
                #searched user
                login_info = Login_info.objects.get(username=username)  
                user_pro=User_profile.objects.get(username=login_info)
                user_pro_img=User_profile_img.objects.get(username=login_info)
                # all following of current user
                following = Following.objects.all().filter(username = user1_login)

                for f in following:
                    # check for searched user is in following or not
                    if f.following_user_pro == User_profile.objects.get(username = login_info):
                        post= Post1.objects.all().filter(user_pro = User_profile.objects.get(username = login_info))
                        cnt=User_count.objects.get(username=login_info)
                        # show posts and unfollow button
                        context={
                        'info' : User_profile.objects.get(username=login_info),
                        'img' : User_profile_img.objects.get(username=login_info),
                        #'req' : ins,
                        'f' : f,
                        'posts' : post,
                        'cnt' : cnt,
                        }
                        return render(request,"searched_user.html" , context)
                    
                # check for friend request is already sent or not
                if Friend_requests.objects.filter(sender= user1_pro).exists():
                    fr = Friend_requests.objects.all().filter(sender=user1_pro)
                    for f in fr:
                        if f.receiver==login_info:
                            cnt=User_count.objects.get(username=login_info)
                            # show requested btn
                            context={
                                'info': user_pro,
                                'img': user_pro_img,
                                'req' : fr,
                                'cnt' : cnt,
                            }
                        else:
                            # show follow btn
                            cnt=User_count.objects.get(username=login_info)
                            context={
                                'info': user_pro,
                                'img': user_pro_img,
                                'cnt' : cnt,
                            }
                else:
                    # Show follow btn Frd req not sent
                    cnt=User_count.objects.get(username=login_info)
                    context={
                        'info': user_pro,
                        'img': user_pro_img,
                        'cnt' : cnt,
                    }
                return render(request,"searched_user.html" , context)
            else:
                messages.info(request, "Username not Found")
        else:
            messages.info(request, "Username not Found")
        
    # home page logic
    post_list=[]
    session_username = request.session['username']
    login_info = Login_info.objects.get(username=session_username)  
    #find all following of current user
    fol = Following.objects.all().filter(username=login_info)

    # for all following user add post and like status of current user in list
    for f in fol:
        posts = Post1.objects.all().filter(user_pro=f.following_user_pro)
        for p in posts:
            if Like.objects.filter(post=p).filter(username=login_info).exists():
                like=Like.objects.filter(post=p).get(username=login_info)
                post_list.append((p,like))
            else:
                like=Like()
                post_list.append((p,like))
    random.shuffle(post_list)
    # print(post_list)

    # suggetion account if not any following account
    profiles = User_profile.objects.exclude(username=login_info)
    profile_img_list = []
    for profile in profiles:
        profile_img = User_profile_img.objects.filter(username=profile.username).first()
        profile_img_list.append((profile, profile_img))

    context={
        'posts' : post_list,
        'profile_img_list': profile_img_list,
    }
    return render(request,"home.html" , context)

def create_profile(request):
    username=request.session['username']
    login_info = Login_info.objects.get(username=username)
    if request.method=="POST":
            ins = User_profile()
            ins.username = login_info
            ins.name = request.POST.get('name')
            ins.surname = request.POST.get('surname')
            ins.mobile_no = request.POST.get('mobile')
            ins.address = request.POST.get('address')
            ins.pincode = request.POST.get('pincode')
            ins.state = request.POST.get('state')
            ins.email = request.POST.get('email')
            ins.save()
            cnt = User_count()
            cnt.username=login_info
            cnt.save()
            return redirect("/home")
    
    return render(request, "profile.html")


def upload_photo(request):
    if request.method == "POST":
        session_username = request.session['username']
        login_info = Login_info.objects.get(username=session_username)  
        if User_profile_img.objects.filter(username=login_info).exists():
            #if user_profile_img is already exist then delete that obj and create new obj
            ins=User_profile_img.objects.filter(username=login_info)
            ins.delete()
            obj = User_profile_img(username=login_info, dp=request.FILES['imp'])
            obj.save()
            context={'obj':obj}
            return render(request, "profile.html", context)
        else:
            #if user_profile_img is not exist thencreate new obj
            ins = User_profile_img(username=login_info, dp=request.FILES['imp'])
            # imp -> field name in html form
            ins.save()
            context = {'obj': ins}
            return render(request, "profile.html", context)
    return render(request, "profile.html", context)

def edit_upload_photo(request):
    session_username = request.session['username']
    login_info = Login_info.objects.get(username=session_username)  
    user_pro=User_profile.objects.get(username=login_info)
    user_pro_img=User_profile_img.objects.get(username=login_info)
    context={
        'info': user_pro,
        'img': user_pro_img,
    }
    if request.method == "POST":
        if User_profile_img.objects.filter(username=login_info).exists():
            ins=User_profile_img.objects.filter(username=login_info)
            ins.delete()
            obj = User_profile_img(username=login_info, dp=request.FILES['imp'])
            obj.save()
            context={'img':obj , 'info' : user_pro}
            return render(request, "edit_profile.html", context)
        else:
            ins = User_profile_img(username=login_info, dp=request.FILES['imp'])
            ins.save()
            context={'img':ins , 'info' : user_pro}
            return render(request, "edit_profile.html", context)
    return render(request, "edit_profile.html", context)

def edit_profile(request):
    username=request.session['username']
    login_info = Login_info.objects.get(username=username)
    user_pro=User_profile.objects.get(username=login_info)
    user_pro_img=User_profile_img.objects.get(username=login_info)
    context={
        'info': user_pro,
        'img': user_pro_img,
    }
    if request.method == "POST":
        if User_profile.objects.filter(username=login_info).exists():
            User_profile.objects.filter(username=login_info).update(name = request.POST.get('name'))
            User_profile.objects.filter(username=login_info).update(surname = request.POST.get('surname'))
            User_profile.objects.filter(username=login_info).update(mobile_no = request.POST.get('mobile'))
            User_profile.objects.filter(username=login_info).update(address = request.POST.get('address'))
            User_profile.objects.filter(username=login_info).update(pincode = request.POST.get('pincode'))
            User_profile.objects.filter(username=login_info).update(state = request.POST.get('state'))
            User_profile.objects.filter(username=login_info).update(email = request.POST.get('email'))
            return redirect("/show_profile")
    return render(request , "edit_profile.html" , context)

def show_profile(request):
    session_username = request.session['username']
    login_info = Login_info.objects.get(username=session_username)  
    user_pro=User_profile.objects.get(username=login_info)
    user_pro_img=User_profile_img.objects.get(username=login_info)
    posts=Post1.objects.all().filter(user_pro=user_pro)
    cnt=User_count.objects.get(username=login_info)
    # print(posts)
    context={
        'info': user_pro,
        'img': user_pro_img,
        'posts':posts,
        'cnt' : cnt,
    }
    # print(context)
    return render(request,"show_profile.html" , context )

def post_create(request):
    session_username = request.session['username']
    login_info = Login_info.objects.get(username=session_username)
    user_pro=User_profile.objects.get(username=login_info)
    user_pro_img=User_profile_img.objects.get(username=login_info)
    # print(user_pro.username.email)
    if request.method == "POST":
        ins=Post1()
        ins.user_pro=user_pro
        ins.user_pro_img=user_pro_img
        ins.post_img=request.FILES['fileUpload']
        ins.like_cnt=0
        ins.captions=request.POST.get('caption')
        ins.save()
        cnt = User_count.objects.get(username=login_info)
        User_count.objects.filter(username=login_info).update(post_cnt=cnt.post_cnt+1)
        return redirect("/show_profile")
    return render(request , "post_create.html")

# for showing searched user profile
def searched_user(request):
    # calling Searched user from get method
    if request.method=="GET":
        # print("in get")
        username=request.GET.get('login_info')
        request.session['receiver']=username
        login_info=Login_info.objects.get(username=username)
        session_username = request.session['username']
        ses_login=Login_info.objects.get(username=session_username)
        # if user is logged in user 
        if username==session_username:
            return redirect("show_profile")
        #get all foll of cur user
        fol=Following.objects.all().filter(username=ses_login)
        if fol :
            for f in fol:
                # check for searched user is in following or not
                if f.following_user_pro==User_profile.objects.get(username=login_info):
                    #show all posts of user and unfollow btn
                    context={
                        'info' : User_profile.objects.get(username=login_info),
                        'img' : User_profile_img.objects.get(username=login_info),
                        'cnt' : User_count.objects.get(username=login_info) ,
                        'posts' : Post1.objects.all().filter(user_pro=User_profile.objects.get(username=login_info)),
                        'f' : f,
                    }
                else:
                    #just show name user profile img and follow btn
                    context={
                        'info' : User_profile.objects.get(username=login_info),
                        'img' : User_profile_img.objects.get(username=login_info),
                        'cnt' : User_count.objects.get(username=login_info) , 
                    }
        else:
            context={
                        'info' : User_profile.objects.get(username=login_info),
                        'img' : User_profile_img.objects.get(username=login_info),
                        'cnt' : User_count.objects.get(username=login_info) , 
                    }

    # logic of sending  frd request
    if request.method=="POST":
        #searched user
        receiver = request.session['receiver']
        # curr user
        session_username = request.session['username']
        login_info = Login_info.objects.get(username=session_username)  
        user_pro=User_profile.objects.get(username=login_info)
        user_pro_img=User_profile_img.objects.get(username=login_info)
        rec=Login_info.objects.get(username=receiver)
        ins = Friend_requests()
        ins.receiver=rec # searched user login_info
        # current user data
        ins.sender=user_pro
        ins.sender_img=user_pro_img
        ins.save()
        cnt=User_count.objects.get(username=rec)
        context={
            'info' : User_profile.objects.get(username=rec),
            'img' : User_profile_img.objects.get(username=rec),
            'req' : ins,
            'cnt' : cnt , 
        }
    return render(request , "searched_user.html" ,context)

def delete_post(request):
    if request.method == "GET":
        # print("hello")
        id = request.GET.get('id')
        post = Post1.objects.get(id=id)
        post.delete()
        session_username = request.session['username']
        login_info = Login_info.objects.get(username=session_username)
        cnt = User_count.objects.get(username = login_info)
        # reduce the post_cnt by 1
        User_count.objects.filter(username=login_info).update(post_cnt=cnt.post_cnt-1)
    return redirect("show_profile")

# for showing the frd_req page
def friend_request(request):
    session_username = request.session['username']
    login_info = Login_info.objects.get(username=session_username)
    user_pro=User_profile.objects.get(username=login_info)
    fr = Friend_requests.objects.all().filter(receiver = login_info)
    context = {
        'fr' : fr,
    }

    # for follow
    if request.method == "POST":
        # info of sender
        send=request.POST.get('send')
        sender_pro = User_profile.objects.get(name=send)
        sender_pro_img=User_profile_img.objects.get(username=sender_pro.username)
        #all frd_req of curr logged in user
        fr1 = Friend_requests.objects.all().filter(receiver = login_info)
        #info of current user
        receiver_pro = User_profile.objects.get(username = login_info)
        receiver_pro_img = User_profile_img.objects.get(username=receiver_pro.username)
        
        for i in fr1:
            # print(i)
            # find the request with our sender
            if i.sender == sender_pro:
                #delete frd_req object
                i.delete()
                # create follower object of current user and increment the follower cnt 
                ins= Followers()
                ins.username=login_info
                ins.followed_user_pro=sender_pro
                ins.followed_user_pro_img=sender_pro_img
                ins.save()
                cnt = User_count.objects.get(username=login_info)
                User_count.objects.filter(username=login_info).update(follower_cnt=cnt.follower_cnt+1)

                # create following object of sender user and inc following cnt
                ins1 = Following()
                ins1.username = sender_pro.username
                ins1.following_user_pro = receiver_pro
                ins1.following_user_pro_img = receiver_pro_img
                ins1.save()
                cnt = User_count.objects.get(username=sender_pro.username)
                User_count.objects.filter(username=sender_pro.username).update(following_cnt=cnt.following_cnt+1)
                return render(request , "friend_request.html", context)

    return render(request , "friend_request.html", context)

def request_decline(request):
        session_username = request.session['username']
        login_info = Login_info.objects.get(username=session_username)
        user_pro=User_profile.objects.get(username=login_info)
        fr = Friend_requests.objects.all().filter(receiver = login_info)
        context = {
            'fr' : fr,
        }
        if request.method == "POST":
            send=request.POST.get('send')
            sender_pro = User_profile.objects.get(name=send)
            # print(sender_pro)
            sender_pro_img=User_profile_img.objects.get(username=sender_pro.username)
            fr1 = Friend_requests.objects.all().filter(receiver = login_info)
            for i in fr1:
                #find the req with correct  sender and delete it
                if i.sender == sender_pro:
                    i.delete()
                    return render(request , "friend_request.html",context)
        return render(request , "friend_request.html",context)


def unfollow(request):
    if request.method == "POST":
        # info of curr user
        session_username = request.session['username']
        login_info = Login_info.objects.get(username=session_username)
        # info of searched user
        rec_user = request.session['receiver']
        rec_login = Login_info.objects.get(username=rec_user)
        following = Following.objects.all().filter(username = login_info)
        # delete the following object of current use and dec the following cnt
        for f in following:
            if f.following_user_pro==User_profile.objects.get(username = rec_login):
                f.delete()
                cnt = User_count.objects.get(username=login_info)
                User_count.objects.filter(username=login_info).update(following_cnt=cnt.following_cnt-1)
        follower =Followers.objects.all().filter(username = rec_login)
        # delete the follower object of searched user and dec follower cnt
        for f in follower:
            if f.followed_user_pro==User_profile.objects.get(username=login_info):
                f.delete()
                cnt = User_count.objects.get(username=rec_login)
                User_count.objects.filter(username=rec_login).update(follower_cnt=cnt.follower_cnt-1)
        cnt=User_count.objects.get(username=rec_login)
        context={
            'info' : User_profile.objects.get(username=rec_login),
            'img' : User_profile_img.objects.get(username=rec_login),
            'cnt' : cnt,
        }
    return render(request , "searched_user.html" ,context)


def show_post(request):
    if request.method=="GET":
        session_username = request.session['username']
        p_id=request.GET.get('post')
        p=Post1.objects.get(id=p_id)
        login_info = Login_info.objects.get(username=p.user_pro.username.username)
        user_pro_img=User_profile_img.objects.get(username=login_info)
        # check the like status of cur user with this post
        if Like.objects.filter(username=Login_info.objects.get(username=session_username)).filter(post=p).exists():
            like=Like.objects.filter(username=Login_info.objects.get(username=session_username)).get(post=p)
        else:
            like=Like()
        # if post is of curr user show delete post btn
        if session_username==p.user_pro.username.username:
            context = {
                'post' : p,
                'login' : login_info,
                'img' : user_pro_img,
                'like' : like,
                'd' : True,
            }
        else:
            context = {
                'post' : p,
                'login' : login_info,
                'img' : user_pro_img,
                'like' : like,
            }
    return render(request , "show_post.html" , context)
    

def like_unlike(request):
    if request.method=="GET":
        post_id=request.GET.get('post_id')
        post=Post1.objects.get(id=post_id)
        session_username = request.session['username']
        login_info = Login_info.objects.get(username=session_username)
        # check for like obj is exists or not
        if Like.objects.filter(username=login_info).filter(post=post).exists():
            like=Like.objects.filter(username=login_info).get(post=post)
            # if like status is false then make it true and inc post like cnt
            if like.like==False:
                Post1.objects.filter(id=post_id).update(like_cnt=post.like_cnt+1)
                Like.objects.filter(username=login_info).filter(post=post).update(like=True)
            #Else make like status false and dec post like cnt
            else:
                Post1.objects.filter(id=post_id).update(like_cnt=post.like_cnt-1)
                Like.objects.filter(username=login_info).filter(post=post).update(like=False)
        # first time like by user on this post
        else:
            ins=Like()
            ins.username=login_info
            ins.post=post
            ins.like=True
            ins.save()
            Post1.objects.filter(id=post_id).update(like_cnt=post.like_cnt+1)
        # if function is called from show post page after like redirect to show post page
        if request.GET.get('page')=="post":
            return redirect(f'/show_post?post={post_id}')
    return redirect("home")


def followers_list(request):
    session_username = request.session['username']
    login_info = Login_info.objects.get(username=session_username)
    followers=Followers.objects.all().filter(username=login_info)
    context={
        'followers' : followers,
    }
    return render(request , "followers_list.html", context)

def following_list(request):
    session_username = request.session['username']
    login_info = Login_info.objects.get(username=session_username)
    followings=Following.objects.all().filter(username=login_info)
    context={
        'followings' : followings,
    }
    return render(request , "following_list.html", context)


def log_out(request):
    logout(request)
    return redirect('login')
