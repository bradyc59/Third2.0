from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"), # /app
    path('registration/', views.register, name="register"),
    path('signup/', views.CaUserSignupView.as_view(), name="signup"),
    path('game/', views.GameView.as_view(), name="game")
]
