from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gamemodel.models import GameSession


@login_required
def profile(request):
    # Отримати всі ігрові сесії користувача
    games = GameSession.objects.filter(user=request.user).order_by('-created_at')

    # Обчислити статистику
    stats = {
        "total_games": games.count(),
        "wins": games.filter(result="Win").count(),
        "losses": games.filter(result="Lose").count(),
    }
    if stats["total_games"] > 0:
        stats["win_percentage"] = round(stats["wins"] * 100 / stats["total_games"], 2)
        stats["loss_percentage"] = round(stats["losses"] * 100 / stats["total_games"], 2)
    else:
        stats["win_percentage"] = stats["loss_percentage"] = 0

    return render(request, "profile.html", {"games": games, "stats": stats})


from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Перенаправлення на головну сторінку після виходу
    else:
        return HttpResponseForbidden("Метод не дозволений")
