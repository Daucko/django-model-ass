from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class Signup(View):
    def get(self, request):
        return render(request, 'home/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password1')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'home/signup.html', {'username': username, 'email': email})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'home/signup.html', {'username': username, 'email': email})

        try:
            user = User.objects.create_user(
                username=username, 
                last_name=last_name,
                first_name=first_name, 
                email=email, 
                password=password
            )
            messages.success(request, 'Account created successfully')
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'home/signup.html', {'username': username, 'email': email})


class Login(View):
    def get(self, request):
        return render(request, 'home/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both fields are required")
            return render(request, 'home/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Login successful! Welcome back, {username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'home/login.html')


class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')
