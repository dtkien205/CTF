from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from urllib.parse import parse_qs
from .sandbox import unpickle

@login_required(login_url='login')
def HomePage(request):
    if request.method == 'POST':
        user_data = parse_qs(request.body.decode('utf-8'))
        user_data.pop('csrfmiddlewaretoken', None)
        user_data = {k: v[0] for k, v in user_data.items()}
        try:
            users = []
            user = User.objects.filter(**user_data).first()
            if user is not None:
                users.append(user)
                return render(request, 'home.html', {'users': users})
            else:
                context = {'error_message': 'Username is not found'}
                return render(request, 'home.html', context)
        except Exception:
            context = {'error_message': 'An error occurred'}
            return render(request, 'home.html', context)
    return render(request, 'home.html')
 
def SignupPage(request):
    if request.user.is_authenticated:
            return redirect('home')

    if request.method == 'POST':
        user_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }
        confirm_password = request.POST.get('confirm_password')
        
        if user_data['password'] != confirm_password:
            context = {'error_message': 'Your password and confirm password are not the same!'}
            return render(request, 'signup.html', context)
        else:
            try:
                if not user_data['username'] or not user_data['email']:
                    context = {'error_message': 'Username or Email cannot be empty!'}
                    return render(request, 'signup.html', context)
                elif not user_data['password'] or not confirm_password:
                    context = {'error_message': 'Password cannot be empty!'}
                    return render(request, 'signup.html', context)
                
                user = User.objects.create(**user_data)
                user.save()
                return redirect('login')
            except Exception:
                context = {'error_message': 'An error occurred'}
                return render(request, 'signup.html', context)

    return render(request, 'signup.html')

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        user_data = {
            'username': request.POST.get('username'),
            'password': request.POST.get('password')
        }
        try:
            user = User.objects.filter(**user_data).first()
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context = {'error_message': 'Username or Password is incorrect!!!'}
                return render(request, 'login.html', context)
        except Exception:
            context = {'error_message': 'An error occurred'}
            return render(request, 'login.html', context)

    return render(request, 'login.html')

def LogoutPage(request):
    try:
        logout(request)
    except Exception:
        context = {'error_message': 'An error occurred'}
        return render(request, 'home.html', context)
    return redirect('login')

def AdminPage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff:
        if request.method == 'POST':
            pickle_data = request.POST.get('pickle_data')
            try:
                result = unpickle(pickle_data)
                context = {'error_message': f'{result}'}
                return render(request, 'admin.html', context)
            except Exception:
                context = {'error_message': 'An error occurred'}
                return render(request, 'admin.html', context)
        return render(request, 'admin.html')

    return redirect('home')