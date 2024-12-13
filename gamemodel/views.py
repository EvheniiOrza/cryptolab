from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import GameSession
import random
from django.contrib.auth.decorators import login_required


@login_required
def start_game(request):
    # Генеруємо випадкове число для гри
    target_number = random.randint(1, 100)

    # Створюємо нову ігрову сесію
    session = GameSession.objects.create(
        user=request.user,
        result="In Progress",
        attempts_left=5,
        target_number=target_number,  # Додаємо значення для target_number
    )
    return redirect('play_game', session_id=session.id)

def play_game(request, session_id):
    session = GameSession.objects.get(id=session_id)

    # Якщо гра завершена, повертаємо повідомлення
    if not session.is_active:
        return redirect('play_game', session_id=session.id)  # Перенаправлення на правильну сторінку

    # Обробка POST запиту (коли користувач вводить число)
    if request.method == "POST":
        guess = int(request.POST['guess'])
        if guess == session.target_number:
            session.is_active = False
            session.result = "Win"  # Оновлюємо результат на "Win"
            session.save()
            return render(request, 'play.html', {'session': session, 'message': ""})
        elif guess < session.target_number:
            hint = "Більше"
        else:
            hint = "Менше"

        # Зменшуємо кількість спроб і перевіряємо, чи залишилися спроби
        session.attempts_left -= 1
        if session.attempts_left == 0:
            session.is_active = False
            session.result = "Lose"  # Оновлюємо результат на "Lose"
            session.save()
            return render(request, 'play.html', {'session': session,
                                                 'message': "Ви програли! Правильне число: {}".format(
                                                     session.target_number)})

        session.save()

        return render(request, "game.html", {"hint": hint, "attempts_left": session.attempts_left})

    return render(request, "game.html", {"attempts_left": session.attempts_left})
