from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, View

from .forms import UserRegisterForm, UserUpdateForm
from .models import CustomUser, FriendRequest


class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        messages.success(
            self.request, f"Dear {username}, you have successfully signed up!"
        )
        return super().form_valid(form)


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your user's been updated!")
        return super().form_valid(form)


class SendFriendRequestView(View):
    def get(self, request, user_id):
        from_user = request.user
        to_user = get_object_or_404(CustomUser, id=user_id)
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )
        if created:
            return HttpResponse("friend request sent")
        return HttpResponse("friend request was already sent")


class AcceptFriendRequestView(View):
    def get(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, pk=request_id)
        if friend_request.to_user == request.user:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return HttpResponse("friend request accepted")

        return HttpResponse("friend request not accepted")
