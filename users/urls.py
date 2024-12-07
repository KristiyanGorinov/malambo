from django.contrib.auth import logout
from django.urls import path
from users.views import register_user, login_user, logout_user, HomeView, AboutView, \
    user_profile, PostsView, PostDetailView, PostCreateView, PostEditView, \
    PostDeleteView, ClubsView, ClubDetailView, join_club, leave_club, CompetitionsView, CompetitionDetailView, \
    ClubCreateView, ClubEditView, ClubDeleteView, add_competition, UserHomeView

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('', HomeView.as_view(), name='home'),

    path('about/', AboutView.as_view(), name='about'),

    path('home/', UserHomeView.as_view(), name='user-home'),
    path('profile/', user_profile, name='profile'),
    path('clubs/', ClubsView.as_view(), name='clubs'),
    path('posts/', PostsView.as_view(), name='posts'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('create-post/', PostCreateView.as_view(), name='create_post'),
    path('edit-post/<slug:slug>/', PostEditView.as_view(), name='edit_post'),
    path('delete-post/<slug:slug>/', PostDeleteView.as_view(), name='delete_post'),
    path('club/<slug:slug>/', ClubDetailView.as_view(), name='club_detail'),
    path('create-club/', ClubCreateView.as_view(), name='create_club'),
    path('edit-club/<slug:slug>/', ClubEditView.as_view(), name='edit_club'),
    path('delete-club/<slug:slug>/', ClubDeleteView.as_view(), name='delete_club'),
    path('<int:club_id>/join/', join_club, name='join_club'),
    path('leave_club/', leave_club, name='leave_club'),
    path('competitions/', CompetitionsView.as_view(), name='competitions'),
    path('competition/<slug:slug>/', CompetitionDetailView.as_view(), name='competition_detail'),
    path('<int:competitions_id>/add/', add_competition, name='add_competition'),

]
