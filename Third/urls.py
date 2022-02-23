"""Third URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf import  settings
from django.conf.urls.static import static

from Simmonopoly import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('join/<host_name>', login_required(views.JoinView.as_view()), name="join"),
    path('login/', views.LoginView.as_view(), name="index"), # /app
    path('', views.LoginView.as_view(), name="index"), # /app
    path('profile/<profile_user>', login_required(views.ProfileView.as_view()), name="profile"),
    path('register/', views.CaUserSignupView.as_view(), name='confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)