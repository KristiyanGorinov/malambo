from django.contrib.auth import logout
from django.urls import path
from users.views import register_user, login_user, logout_user, HomeView, AboutView, \
    club_manage, user_home, user_profile, clubs, PostsView, PostDetailView

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('', HomeView.as_view(), name='home'),


    path('about/', AboutView.as_view(), name='about'),

    path('home/', user_home, name='user-home'),

    path('manage/' ,club_manage, name='club-manage'),

    path('profile/', user_profile, name='profile'),
    path('clubs/', clubs, name='clubs'),
    path('posts/', PostsView.as_view(), name='posts'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]