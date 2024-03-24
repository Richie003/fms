import secrets

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.
from django.views.decorators.csrf import csrf_protect

from accounts.models import UserBio

def sign_up(request):
    context = {}
    return render(request, "accounts/signup.html", context)

@csrf_protect
def login_page(request):
    nums = secrets.token_hex()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user1 = request.user
            login(request, user)
            check = UserBio.objects.filter(user=user1)
            if not check:
                bio = UserBio.objects.create(user=user1, code=nums[0:9])
                bio.save()
            else:
                check.update()
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('home')
        else:
            messages.info(request, 'registration number OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def log_out(request):
    # context={'num':num}
    logout(request)
    return redirect('login')
