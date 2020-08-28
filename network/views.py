from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("allposts"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        profile = Profile.objects.create(user=user)
        profile.save()
        return HttpResponseRedirect(reverse("allposts"))
    else:
        return render(request, "network/register.html")


@login_required
def allPost(request):
    posts = Post.objects.all().order_by('timestamp').reverse()
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        posts = paginator.page(request.GET.get("page"))
    else:
        posts = paginator.page(1)
    return render(request, 'network/allpost.html', {'posts': posts})


@login_required
def profile(request, username):    
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=User.objects.get(username=username))
    posts = Post.objects.filter(user=user).order_by('timestamp').reverse()
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        posts = paginator.page(request.GET.get("page"))
    else:
        posts = paginator.page(1)
    return render(request, 'network/profile.html', {'posts': posts, "user": user, "profile": profile,'users_profile': Profile.objects.get(user=request.user)})


@login_required
def following(request):
    if request.method == 'GET':
        following = Profile.objects.get(user=request.user).following.all()
        posts = Post.objects.filter(user__in=following).order_by('timestamp').reverse()
        paginator = Paginator(posts, 10)
        if request.GET.get("page") != None:
            posts = paginator.page(request.GET.get("page"))
        else:
            posts = paginator.page(1)
        return render(request, 'network/following.html', {'posts': posts})


@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        like = request.POST.get('is_liked')
        post = Post.objects.get(id=post_id)
        if request.user in post.like.all():
            post.like.remove(request.user)
            like = 'no'
        else:
            post.like.add(request.user)
            like = 'yes'
        post.save()
        return JsonResponse({'like_count': post.like.count(), 'is_liked': like, "status": 201})


@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        user = request.POST.get('user')
        action = request.POST.get('action')
        user = User.objects.get(username=user)
        profile1 = Profile.objects.get(user=request.user)
        profile2 = Profile.objects.get(user=user)
        if action == 'Follow':
            profile1.following.add(user)
            profile1.save()
            profile2.follower.add(request.user)
            profile2.save()
            return JsonResponse({'status': 201, 'action': "Unfollow", "follower_count": profile2.follower.count()}, status=201)
        else:
            profile1.following.remove(user)
            profile1.save()
            profile2.follower.remove(request.user)
            profile2.save()
            return JsonResponse({'status': 201, 'action': "Follow", "follower_count": profile1.follower.count()}, status=201)


@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        pid = request.POST.get('id')
        post = Post.objects.get(id=pid)
        content = request.POST.get('post')
        if post.user == request.user:
            post.post = content
            post.save()
            return JsonResponse({}, status=201)

@login_required
@csrf_exempt
def addpost(request):
    if request.method == "POST":
        content = request.POST.get('post')
        if len(content) != 0:
            newp = Post.objects.create(post=content, user=request.user)
            newp.save()
            return JsonResponse({'status': 201,'post_id': newp.id,'username': request.user.username,'timestamp': newp.timestamp.strftime("%B %d, %Y, %I:%M %p")}, status=201)
