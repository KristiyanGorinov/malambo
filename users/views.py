from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView

from SoftUniFinalExam.utils import get_user_obj
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'staff'])
def club_manage(request):
    return render(request, 'staff-user/manage-club.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'user', 'staff'])
def user_home(request):
    return render(request, 'user/user-page.html')


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

    if request.method == 'POST':
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
