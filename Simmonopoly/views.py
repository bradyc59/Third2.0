from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from Simmonopoly.forms import ProfileForm, CASignupForm
from Simmonopoly.models import Profile, Session
from Simmonopoly.forms import User



def index(request):
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect('/')

def lobby(request):
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        return redirect(
            '/join/%s'
            %(room_code)
        )
    return render(request, "lobby.html")

class LoginView(View):
    initial = {'active_page': 'register'}
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "active_page": "login",
            "error": None
        })

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/lobby")

            else:
                res = {'active_page': 'login',
                       "error": "Inactive user."}
                return render(request, self.template_name, res)
        else:
            res = {'active_page': 'login',
                   "error": "Invalid username or password."}
            return render(request, self.template_name, res)


class ProfileView(View):
    initial = {'key': 'value'}
    template_name = 'profile_view.html'

    def get(self, request, *args, **kwargs):
        try:
            self.profile_user = User.objects.get(username=kwargs.get("profile_user"))
        except Exception:
            self.error = "User {id} not existed.".format(id=kwargs.get("profile_user"))
            self.profile_user = None
            return render(request, "404.html", {})


        try:
            self.profile_info = Profile.objects.get(user=self.profile_user)
        except Exception:
            self.profile_info = None

        res = {
            "user": self.profile_user,
            "profile": self.profile_info
        }
        return render(request, self.template_name, res)

    def post(self, request, *args, **kwargs):
        # Unauthorized modification
        try:
            self.profile_user = User.objects.get(username=kwargs.get("profile_user"))
        except Exception:
            self.error = "User {id} not existed.".format(id=kwargs.get("profile_user"))
            self.profile_user = None
            raise render(request, "404.html", {})

        try:
            self.profile_info = Profile.objects.get(user=self.profile_user)
        except Exception:
            self.profile_info = None

        if self.profile_user != request.user:
            raise PermissionDenied

        bio = request.POST.get("bio", None)
        avatar = request.FILES.get("avatar", None)

        if self.profile_info:
            self.profile_info.bio = bio
            if avatar:
                self.profile_info.avatar = avatar
            self.profile_info.save()
        else:
            self.profile_info = Profile(user=request.user, bio=bio, avatar=avatar)
            form = ProfileForm(request.POST, request.FILES, instance=self.profile_info)

            if form.is_valid():
                print ("valid")
                self.profile_info.save()
            else:
                print (form.errors)

        res = {
            "user": self.profile_user,
            "profile": self.profile_info
        }
        return render(request, self.template_name, res)

class JoinView(View):
    template_name = 'join_view.html'

    def get(self, request, *args, **kwargs):
        print(request.path)
        user = request.user
        host_name = kwargs.get('host_name', user.username)
        room_code = kwargs.get('room_code')

        try:
            profile = Profile.objects.get(user=user)
        except Exception:
            profile = None

        return render(request, self.template_name, {
            "user": {
                "name": user.username,
                "avatar": profile.avatar.url if profile else ""
            },
            "host_name": host_name if len(host_name) else user.username,
            "room_code": room_code
        })
class CaUserSignupView(CreateView):
    model = User
    form_class = CASignupForm
    template_name = 'causer_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/join/' + user.username)


