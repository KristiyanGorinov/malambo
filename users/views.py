from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction, connection
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView

from SoftUniFinalExam.utils import get_user_obj
from clubs.forms import ClubCreateForm, ClubEditForm, ClubDeleteForm
from competitions.models import Competitions
from posts.forms import PostCreateForm, PostsEditForm, PostDeleteForm
from posts.models import Post
from clubs.models import Club
from .decorators import unauthenticated_user, allowed_users, AllowedUsersMixin
from .forms import CreateUserForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.models import *


class HomeView(ListView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'public/public-page.html'


class AboutView(ListView):
    model = User
    template_name = 'public/about-me.html'


class PostsView(LoginRequiredMixin, AllowedUsersMixin, ListView):
    model = Post
    template_name = 'user/posts.html'
    context_object_name = 'posts'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']


class PostDetailView(LoginRequiredMixin, AllowedUsersMixin, DetailView):
    model = Post
    template_name = 'Posts/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        related_posts = Post.objects.exclude(id=self.object.id)[:4]
        context['related_posts'] = related_posts

        return context


class PostCreateView(LoginRequiredMixin, AllowedUsersMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'Posts/post_create.html'
    success_url = reverse_lazy('posts')
    context_object_name = 'posts'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def form_valid(self, form):
        logged_in_user = self.request.user
        try:
            custom_user = Users.objects.get(user=logged_in_user)
        except Users.DoesNotExist:
            raise ValueError("No corresponding Users instance found for the logged-in user.")

        form.instance.user = custom_user
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, AllowedUsersMixin, UpdateView):
    model = Post
    form_class = PostsEditForm
    template_name = 'Posts/post_edit.html'
    success_url = reverse_lazy('posts')
    context_object_name = 'posts'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def form_valid(self, form):
        logged_in_user = self.request.user
        try:
            custom_user = Users.objects.get(user=logged_in_user)
        except Users.DoesNotExist:
            raise ValueError("No corresponding Users instance found for the logged-in user.")

        form.instance.user = custom_user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, AllowedUsersMixin, DeleteView):
    model = Post
    form_class = PostDeleteForm
    template_name = 'Posts/post_delete.html'
    success_url = reverse_lazy('posts')
    context_object_name = 'posts'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)


class ClubsView(LoginRequiredMixin, AllowedUsersMixin, ListView):
    model = Club
    template_name = 'user/clubs.html'
    context_object_name = 'clubs'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']


class ClubDetailView(LoginRequiredMixin, AllowedUsersMixin, DetailView):
    model = Club
    template_name = 'Clubs/club_details.html'
    context_object_name = 'club'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        related_clubs = Club.objects.exclude(id=self.object.id)[:4]
        context['related_clubs'] = related_clubs

        return context


class ClubCreateView(LoginRequiredMixin, AllowedUsersMixin, CreateView):
    model = Club
    form_class = ClubCreateForm
    template_name = 'Clubs/club_create.html'
    success_url = reverse_lazy('clubs')
    context_object_name = 'clubs'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def form_valid(self, form):
        logged_in_user = self.request.user
        try:
            custom_user = Users.objects.get(user=logged_in_user)
        except Users.DoesNotExist:
            raise ValueError("No corresponding Users instance found for the logged-in user.")

        form.instance.user = custom_user
        return super().form_valid(form)


class ClubEditView(LoginRequiredMixin, AllowedUsersMixin, UpdateView):
    model = Club
    form_class = ClubEditForm
    template_name = 'Clubs/club_edit.html'
    success_url = reverse_lazy('clubs')
    context_object_name = 'clubs'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def form_valid(self, form):
        logged_in_user = self.request.user
        try:
            custom_user = Users.objects.get(user=logged_in_user)
        except Users.DoesNotExist:
            raise ValueError("No corresponding Users instance found for the logged-in user.")

        form.instance.user = custom_user
        return super().form_valid(form)


class ClubDeleteView(LoginRequiredMixin, AllowedUsersMixin, DeleteView):
    model = Club
    form_class = ClubDeleteForm
    template_name = 'Clubs/club_delete.html'
    success_url = reverse_lazy('clubs')
    context_object_name = 'clubs'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)


@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'user'])
def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM clubs_club_members WHERE club_id = %s AND user_id = %s",
            [club_id, user_id]
        )
        is_member_of_current_club = cursor.fetchone()

    if is_member_of_current_club:
        messages.info(request, "You are already a member of this club!")
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT club_id FROM clubs_club_members WHERE user_id = %s",
                [user_id]
            )
            other_club = cursor.fetchone()

        if other_club:
            messages.error(
                request,
                f"You are already a member of another club. Leave it before joining a new one."
            )
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO clubs_club_members (club_id, user_id) VALUES (%s, %s)",
                    [club_id, user_id]
                )
            messages.success(request, "You have successfully joined the club!")

    return redirect('club_detail', club.slug)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'user', 'staff'])
def leave_club(request):
    user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE FROM clubs_club_members WHERE user_id = %s",
            [user_id]
        )

    messages.success(request, "You have successfully left the club!")

    return redirect('profile')


class CompetitionsView(LoginRequiredMixin, AllowedUsersMixin, ListView):
    model = Competitions
    template_name = 'user/competitions.html'
    context_object_name = 'competitions'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']


class CompetitionDetailView(LoginRequiredMixin, AllowedUsersMixin, DetailView):
    model = Competitions
    template_name = 'Competitions/competition_details.html'
    context_object_name = 'competitions'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        related_competitions = Competitions.objects.exclude(id=self.object.id)[:4]
        context['related_competitions'] = related_competitions

        return context


def add_competition(request, competitions_id):
    competition = get_object_or_404(Competitions, id=competitions_id)
    user_id = request.user.id

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM competitions_competitions_participants WHERE competitions_id = %s AND user_id = %s",
            [competitions_id, user_id]
        )
        is_member_of_current_competition = cursor.fetchone()

    if is_member_of_current_competition :
        messages.info(request, "You have already added this competition in your profile")
    else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO competitions_competitions_participants (competitions_id, user_id) VALUES (%s, %s)",
                    [competitions_id, user_id]
                )
            messages.success(request, "You have already added this competition to your profile")

    return redirect('competition_detail', competition.slug)


class UserHomeView(LoginRequiredMixin,AllowedUsersMixin, ListView):
    model = Post
    template_name = 'user/user-page.html'
    context_object_name = 'posts'
    login_url = 'login'
    allowed_roles = ['admin', 'staff', 'user']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = Post.objects.all().order_by('uploaded_at')[:4]
        context['posts'] = posts

        return context


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'user', 'staff'])
def user_profile(request):
    user = request.user
    try:
        profile = user.users
    except Users.DoesNotExist:
        profile = Users.objects.create(
            user=user,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            email=user.email or f"default_email_{user.pk}@example.com",
            phone="",
            info="",
        )

    user_id = request.user.id
    user_clubs = Club.objects.filter(members=user_id)
    user_competitions= Competitions.objects.filter(participants=user_id)

    if request.method == 'POST':
        if 'leave_club' in request.POST:
            user_id = request.user.id
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM clubs_club_members WHERE user_id = %s",
                    [user_id]
                )
        else:
            form = ProfileUpdateForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save()
                profile.phone = request.POST.get('phone', profile.phone)
                profile.info = request.POST.get('info', profile.info)
                profile.first_name = user.first_name
                profile.last_name = user.last_name
                profile.email = user.email
                profile.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')


    else:
        form = ProfileUpdateForm(instance=user)

    context = {
        'form': form,
        'profile': profile,
        'user_clubs': user_clubs,
        'user_competitions': user_competitions,
    }
    return render(request, 'user/user-profile.html', context)


@unauthenticated_user
def register_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered in our system.")
                return render(request, 'user/register-user.html', {'form': form})

            if Users.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered in our system.")
                return render(request, 'user/register-user.html', {'form': form})

            try:
                with transaction.atomic():
                    user = form.save()

                    group = Group.objects.get(name='user')
                    user.groups.add(group)

                    existing_users_record = Users.objects.filter(user=user).first()
                    if not existing_users_record:
                        Users.objects.create(
                            user=user,
                            username=user.username,
                            email=email
                        )
                    else:
                        existing_users_record.username = user.username
                        existing_users_record.email = email
                        existing_users_record.save()

                messages.success(request, f'Account created for {form.cleaned_data["username"]}')
                return redirect('login')

            except IntegrityError:
                messages.error(request, "There was an error creating your account. Please try again.")
                return render(request, 'user/register-user.html', {'form': form})

        else:
            messages.error(request, "There were errors in the form.")

    context = {'form': form}
    return render(request, 'user/register-user.html', context)


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('user-home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'user/login-user.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'user', 'staff'])
def logout_user(request):
    logout(request)
    return redirect('home')
