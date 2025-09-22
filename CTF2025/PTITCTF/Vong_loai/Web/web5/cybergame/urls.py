from django.urls import path
from .views import GameView, UserListView, LevelListView, ScoreboardView, ReleaseListView

urlpatterns = [
    path('games/', GameView.as_view(), name='game-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('levels/', LevelListView.as_view(), name='level-list'),
    path('scoreboard/', ScoreboardView.as_view(), name='scoreboard'),
    path('releases/', ReleaseListView.as_view(), name='release-list'),
]
