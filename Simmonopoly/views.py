from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from Simmonopoly.forms import CASignupForm
from Simmonopoly.models import CaUser


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'registration.html')

class CaUserSignupView(CreateView):
    model = CaUser
    form_class = CASignupForm
    template_name = 'causer_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')


class GameView(View):
    template_name = 'game_view.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "username": request.user.username,
            "hostname": kwargs.get("host_name")
        })
