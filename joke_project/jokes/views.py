from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import httpx
from .models import UserProfile, Joke

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
def display_jokes(request):
    jokes = Joke.objects.all()
    return render(request, 'list.html', {'jokes': jokes})
def user_logout(request):
    logout(request)
    return redirect('login')

def fetch_joke():
    response = httpx.get('https://official-joke-api.appspot.com/random_joke')
    if response.status_code == 200:
        joke_data = response.json()
        joke = Joke.objects.create(
            setup=joke_data['setup'],
            punchline=joke_data['punchline']
        )
        return joke
    return None

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.last_joke:
        joke = fetch_joke()
        if joke:
            user_profile.last_joke = joke
            user_profile.save()
    
    if request.method == 'POST':
        joke = fetch_joke()
        if joke:
            user_profile.last_joke = joke
            user_profile.save()

    return render(request, 'home.html', {'joke': user_profile.last_joke})
