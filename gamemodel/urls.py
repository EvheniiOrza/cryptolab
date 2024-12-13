from django.urls import path
from .views import start_game, play_game

urlpatterns = [
    path('start/', start_game, name='start_game'),
    path('play/<int:session_id>/', play_game, name='play_game'),
]
