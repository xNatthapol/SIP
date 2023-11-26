from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from SIP.models import Player


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save the new user
            user = form.save()
            Player.objects.create(user=user)
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username,
                                password=raw_password)
            login(request, user)

            messages.success(request, 'Registration successful!')

            # redirect to home page
            return redirect('SIP:index')
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
