from django.contrib.auth import logout
from django.urls import path
from users.views import register_user, login_user, logout_user, HomeView, AboutView, \
    user_profile, PostsView, PostDetailView, PostCreateView, PostEditView, \
    PostDeleteView, ClubsView, ClubDetailView, join_club, leave_club, CompetitionsView, CompetitionDetailView, \
    ClubCreateView, ClubEditView, ClubDeleteView, add_competition, UserHomeView, CompetitionCreateView, \
    CompetitionEditView, CompetitionDeleteView, BecomeStaffView, PanelView, delete_user, make_superuser, \
    CompetitionRegisterView, RegistrationDeleteView, ClubAdminPanelView, RemoveUserFromClubView, RevokeStaffView

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
    path('create-competition/', CompetitionCreateView.as_view(), name='create_competition'),
    path('edit-competition/<slug:slug>/', CompetitionEditView.as_view(), name='edit_competition'),
    path('delete-competition/<slug:slug>/', CompetitionDeleteView.as_view(), name='delete_competition'),
    path('competition/<slug:slug>/', CompetitionDetailView.as_view(), name='competition_detail'),
    path('<int:competitions_id>/add/', add_competition, name='add_competition'),
    path('become-staff/', BecomeStaffView.as_view(), name="become_staff"),
    path('admin-panel', PanelView.as_view(), name='admin-panel'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('make_superuser/<int:user_id>/', make_superuser, name='make_superuser'),
    path('register-competition/<slug:slug>/', CompetitionRegisterView.as_view(), name='register-competition'),
    path('delete-registration/<int:pk>/', RegistrationDeleteView.as_view(), name='delete_registration'),
    path('admin-club-panel/', ClubAdminPanelView.as_view(), name='admin_club_panel'),
    path('remove-user/<int:club_id>/<int:user_id>/', RemoveUserFromClubView.as_view(), name='remove_user_from_club'),
    path('revoke-staff/<int:user_id>/', RevokeStaffView.as_view(), name='revoke_staff'),

]
