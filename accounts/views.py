from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def signup(request):
    if request.method == 'POST':
        # Sign up
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'username': 'Username or password is incorrect.'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'password2': 'Passwords must match'})
    else:
        # Send sign up form
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'accounts/login.html', {'next': request.GET.get('next')})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
