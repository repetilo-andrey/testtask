from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from coworkers.forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                previous_page = request.META.get('HTTP_REFERER')
                previous_page = 'hierarchy' if '/login/' in previous_page else previous_page
                return redirect(previous_page)
            else:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page, 'hierarchy')
