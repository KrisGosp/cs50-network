from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from .models import User, Post, Following, Like


def index(request):
    posts = Post.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # take ids of all posts that currUser has liked
    liked_posts = Like.objects.filter(user=request.user).values_list('post', flat=True)
    


    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })

@login_required
def following(request):
    # get users that currUser follows
    following_users = request.user.following.values_list('followed', flat=True)

    # get posts from users that currUser follows + Paginator
    posts = Post.objects.filter(user__in=following_users).order_by("-created_at")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        body = data["body"]
        user = request.user
        new_post = Post.objects.create(body=body, user=user)
        new_post.save()

        return JsonResponse({'message': 'Post created successfully'}, status=201)

    return JsonResponse({'message': 'Route can only be accessed via POST'}, status=400)

@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        body = data["body"]
        post = Post.objects.get(id=post_id)
        post.body = body
        post.save()

        return JsonResponse({'message': 'Post edited successfully'}, status=201)

    return JsonResponse({'message': 'Route can only be accessed via PUT'}, status=400)

@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)

# Paginator
    posts = Post.objects.filter(user=user).order_by("-created_at")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

# following
    user_following = Following.objects.filter(user=user).count()
    user_followed = Following.objects.filter(followed=user).count()

# check whether user is followed
    followed = Following.objects.filter(user=request.user, followed=user).exists()

# check if this user is visiting their account
    is_own_profile = int(user_id) == int(request.user.id)

    return render(request, "network/profile.html", {
        "user": user,
        "page_obj": page_obj,
        "following": user_following,
        "followers": user_followed,
        "followed": followed,
        "is_own_profile": is_own_profile
    })


@login_required
def toggle_follow(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]

        user = User.objects.get(id=user_id)

        # toggle the follow value in Following table
        followed = Following.objects.filter(user=request.user, followed=user).exists()
        if followed:
            Following.objects.filter(user=request.user, followed=user).delete()
        else:
            new_follow = Following.objects.create(user=request.user, followed=user)
            new_follow.save()

        return redirect('profile', user_id=user_id)

    return JsonResponse({'message': 'Route can only be accessed via POST'}, status=400)

@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method == "PUT":
        # update post likes count
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()

        # create a new Like object
        Like.objects.create(user=request.user, post=post)

        return JsonResponse({'message': 'Post liked successfully'}, status=201)
    return JsonResponse({'message': 'Route can only be accessed via PUT'}, status=400)

@login_required
def unlike_post(request, post_id):
    if request.method == "PUT":
        # update post likes count
        post = Post.objects.get(id=post_id)
        post.likes -= 1
        post.save()

        # delete the Like object
        Like.objects.filter(user=request.user, post=post).delete()

        return JsonResponse({'message': 'Post liked successfully'}, status=201)
    return JsonResponse({'message': 'Route can only be accessed via PUT'}, status=400)
    
