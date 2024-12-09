
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/<str:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path('toggle_follow', views.toggle_follow, name='toggle_follow'),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("unlike_post/<int:post_id>", views.unlike_post, name="unlike_post"),
]
