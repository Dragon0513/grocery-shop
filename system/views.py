from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from system.forms import LoginForm, SignUpForm

User = get_user_model()


# Create your views here.
def sign_in(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        form = LoginForm()
        return render(request, "pages/authentication/login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Erfolgreich angemeldet!")
                return redirect("home")

        messages.error(request, "Benutzername oder Passwort ist falsch.")
        return render(request, "pages/authentication/login.html", {"form": form})


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "pages/authentication/signup.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def custom_logout(request):
    logout(request)
    return redirect("home")


class HomeView(generic.ListView):
    model = User
    template_name = "pages/root/home.html"
