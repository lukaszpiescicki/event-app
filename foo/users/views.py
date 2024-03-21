from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import CustomUser, FriendRequest


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Dear {username}, you have successfully signed up!"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", context={"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your user's been updated!")
            return redirect(profile)

    return render(request, "users/profile.html", {"user_form": UserUpdateForm()})

@login_required
def send_friend_request(request, user_id):
    from_user = request.user
    to_user = CustomUser.objects.filter(id=user_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('friend request sent')
    return HttpResponse('friend request was already sent')

@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')
