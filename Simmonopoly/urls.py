
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Simmonopoly import views

urlpatterns = [
    path('join/<room_code>', login_required(views.JoinView.as_view()), name="join"),
    path('login/', views.LoginView.as_view(), name="index"), # /app
    path('', views.LoginView.as_view(), name="index"), # /app
    path('profile/<profile_user>', login_required(views.ProfileView.as_view()), name="profile"),
    path('register/', views.CaUserSignupView.as_view(), name='confirm'),
    path('lobby/', views.lobby),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

